# 🔍 LogicLens AI

> AI-powered code analysis running **100% locally** via Ollama + Qwen 2.5. No API keys. No cloud. No data leaving your machine.

# 📸 Preview

![img alt](https://github.com/Abeesh-2027/Ai-notes-generator/blob/fef35ec55133c31919b287f350ac8e80e3d2757a/Screenshot%20(108).png)

---

## ✨ Features

- 🧠 **AI Code Analysis** — Deep semantic understanding of any code snippet
- 🐛 **Bug Detection** — Identifies syntax errors, logic flaws, and runtime risks
- ⚡ **Optimization Suggestions** — Actionable tips to improve speed and memory usage
- 📊 **Complexity Analysis** — Time & space complexity with Big-O notation
- 📝 **Line-by-Line Explanation** — Step-by-step breakdown of what the code does
- 🌐 **25+ Languages** — Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
- 🔒 **100% Private** — Everything runs locally, nothing leaves your machine
- 📁 **File Upload** — Upload code files directly from your filesystem

---

## 🖥️ Demo

```
Paste your code → Click "Analyze with AI" → Get instant insights
```

The app provides a clean, modern web UI with:
- Collapsible result sections
- Copy-to-clipboard
- Ollama live status indicator
- Mobile responsive layout

---

## 🚀 Quick Start

### 1. Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.8+ |
| Ollama | Latest |
| Qwen 2.5 model | 7B |

### 2. Install Ollama

Download from [ollama.com](https://ollama.com) and then pull the model:

```bash
ollama pull qwen2.5:7b
```

### 3. Clone the Repository

```bash
git clone https://github.com/your-username/logiclens-ai.git
cd logiclens-ai
```

### 4. Install Python Dependencies

```bash
pip install flask flask-cors requests
```

### 5. Run the App

Open **two terminals**:

**Terminal 1 — Start Ollama:**
```bash
ollama serve
```

**Terminal 2 — Start Flask:**
```bash
python app.py
```

### 6. Open in Browser

```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
logiclens-ai/
│
├── app.py                  # Flask backend — API routes + Ollama integration
├── templates/
│   └── index.html          # Frontend — full single-page UI
├── README.md

```

---

## 🔌 API Endpoints

### `POST /analyze`
Analyzes a code snippet using Qwen 2.5.

**Request body:**
```json
{
  "code": "def hello():\n    print('Hello World')",
  "language": "python"
}
```

**Response:**
```json
{
  "summary": "A simple function that prints Hello World.",
  "explanation": "Line 1: Defines a function named hello...",
  "errors": ["No issues found."],
  "optimizations": ["Consider adding a docstring."],
  "complexity": {
    "time": "O(1)",
    "space": "O(1)",
    "explanation": "Single print statement, constant time."
  }
}
```

---

### `GET /health`
Returns Ollama and model status.

**Response:**
```json
{
  "ollama": "running",
  "model": "qwen2.5:7b",
  "model_available": true,
  "available_models": ["qwen2.5:7b"]
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, Vanilla JS |
| Backend | Python, Flask, Flask-CORS |
| AI Model | Qwen 2.5:7B |
| AI Runtime | Ollama |
| Fonts | Inter, JetBrains Mono |
| Icons | Font Awesome 6 |

---

## ⚙️ Configuration

You can change the model or Ollama URL in `app.py`:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"   # swap to qwen2.5:14b for better results
```

**Supported alternative models:**
- `qwen2.5:3b` — Faster, lighter
- `qwen2.5:14b` — More accurate, needs more RAM
- `codellama:7b` — Code-focused alternative
- `deepseek-coder:6.7b` — Another code-focused option

---

## 🧯 Troubleshooting

| Problem | Fix |
|---------|-----|
| `Flask not reachable` | Run `python app.py` |
| `Ollama offline` | Run `ollama serve` |
| `Model not found` | Run `ollama pull qwen2.5:7b` |
| `Request timed out` | Try a shorter code snippet |
| `expText.split is not a function` | Already fixed in latest version |
| CORS error in browser | Make sure `flask-cors` is installed |

---

## 📋 Requirements

Create a `requirements.txt`:

```
flask
flask-cors
requests
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request


---

## 👤 Author

**Abeesh**
- Email: abeesh2027@gmail.com

---

<p align="center">Built with ❤️ using Qwen 2.5 + Ollama + Flask</p>
