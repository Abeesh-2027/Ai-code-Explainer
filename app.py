from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import re

app = Flask(__name__)
CORS(app)  # Allow all origins — required so the browser can call /analyze and /health

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"


# ----------------------------------------
# QUERY OLLAMA
# ----------------------------------------
def query_ollama(prompt: str) -> str:

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,        # Lower = more deterministic JSON output
            "top_p": 0.9,
            "num_predict": 2048,
            "stop": [],                # No stop tokens — let it finish the JSON
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180              # Give Qwen 2.5 enough time on slower machines
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Cannot connect to Ollama. Run: ollama serve")

    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out. Try shorter code or increase timeout.")

    except Exception as e:
        raise RuntimeError(f"Ollama error: {str(e)}")


# ----------------------------------------
# CLEAN RAW AI OUTPUT → EXTRACT JSON
# ----------------------------------------
def extract_json(raw: str) -> dict:
    """
    Qwen 2.5 sometimes wraps JSON in markdown fences even when told not to.
    This function strips all wrappers and finds the first valid JSON object.
    """
    # 1. Strip common markdown fences (handles ```json, ```JSON, ``` etc.)
    cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", raw.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())
    cleaned = cleaned.strip()

    # 2. Try direct parse first (happy path)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 3. Find the first { ... } block in the text (handles preamble text)
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # 4. Nothing worked — return a fallback so the UI still renders
    return {
        "_parse_failed": True,
        "raw": raw[:2000]
    }


# ----------------------------------------
# BUILD PROMPT
# ----------------------------------------
def build_prompt(code: str, language: str) -> str:

    lang_hint = (
        f"The code is written in {language}. "
        if language and language != "auto"
        else ""
    )

    # Using explicit JSON key names + short examples reduces parse failures
    return f"""You are an expert code analyst. Analyze the code below.

IMPORTANT: Respond with ONLY a JSON object. No markdown. No backticks. No explanation outside the JSON.

Use exactly this structure:
{{
  "summary": "One or two sentence overview of what this code does.",
  "explanation": "Step-by-step explanation of how the code works, one step per line.",
  "errors": ["List each bug or issue as a separate string. If none, write: No issues found."],
  "optimizations": ["List each suggestion as a separate string. If none, write: No suggestions."],
  "complexity": {{
    "time": "O(...)",
    "space": "O(...)",
    "explanation": "Brief plain-English explanation of why."
  }}
}}

{lang_hint}Code to analyze:

{code}
"""


# ----------------------------------------
# HOME PAGE
# ----------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------------------------
# ANALYZE CODE
# ----------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    code = data.get("code", "").strip()
    language = data.get("language", "auto")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    if len(code) > 20000:
        return jsonify({"error": "Code too long (max 20,000 characters)"}), 400

    try:
        prompt = build_prompt(code, language)
        raw = query_ollama(prompt)

        result = extract_json(raw)

        # If JSON extraction failed, surface the raw text so the user sees something useful
        if result.get("_parse_failed"):
            return jsonify({
                "summary": "AI returned a non-JSON response. Raw output shown below.",
                "explanation": result.get("raw", "No output."),
                "errors": ["Could not parse structured response from AI."],
                "optimizations": ["Try a shorter or simpler code snippet."],
                "complexity": {"time": "N/A", "space": "N/A", "explanation": ""}
            })

        # Fill in any missing keys with safe defaults
        defaults = {
            "summary": "Analysis completed.",
            "explanation": "No explanation provided.",
            "errors": ["No issues found."],
            "optimizations": ["No suggestions."],
            "complexity": {"time": "Unknown", "space": "Unknown", "explanation": ""}
        }
        for key, value in defaults.items():
            if key not in result or not result[key]:
                result[key] = value

        # Ensure errors and optimizations are lists, not strings
        for list_key in ("errors", "optimizations"):
            if isinstance(result[list_key], str):
                result[list_key] = [result[list_key]]

        # Ensure complexity is a dict
        if not isinstance(result.get("complexity"), dict):
            result["complexity"] = defaults["complexity"]

        return jsonify(result)

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


# ----------------------------------------
# HEALTH CHECK
# ----------------------------------------
@app.route("/health")
def health():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = [m["name"] for m in response.json().get("models", [])]
        model_ready = any(MODEL_NAME in m for m in models)
        return jsonify({
            "ollama": "running",
            "model": MODEL_NAME,
            "model_available": model_ready,
            "available_models": models
        })
    except Exception as e:
        return jsonify({"ollama": "unreachable", "error": str(e)}), 503


# ----------------------------------------
# MAIN
# ----------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print(" LogicLens AI — Backend Started")
    print(f" Model  : {MODEL_NAME}")
    print(f" Ollama : {OLLAMA_URL}")
    print(" Open   : http://127.0.0.1:5000")
    print("=" * 50)
    print(" Make sure Ollama is running:")
    print("   ollama serve")
    print("   ollama pull qwen2.5:7b")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)