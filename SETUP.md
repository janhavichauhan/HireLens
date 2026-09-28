# Setup Guide - HireLens

## 📋 Prerequisites

- **Windows, Mac, or Linux**
- **8GB RAM minimum** (16GB recommended)
- **10GB disk space** (for LLM models)
- **Python 3.8+**

---

## Step 1: Install Ollama

1. Download: https://ollama.ai
2. Install following on-screen instructions
3. Restart your computer

---

## Step 2: Download LLM Model

Open **PowerShell/Terminal** and run:

```bash
ollama pull mistral
```

This downloads Mistral (~5GB). Takes ~5-10 minutes.

**Alternative models:**
- `ollama pull llama2` - Smaller, faster
- `ollama pull neural-chat` - Good for conversation

---

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs: streamlit, requests, pandas, numpy, etc.

---

## Step 4: Start Ollama Server

Open a **terminal/PowerShell** and run:

```bash
ollama serve
```

You should see: `listening on 127.0.0.1:11434`

**Keep this window open!**

---

## Step 5: Run Application

Open a **new terminal/PowerShell** and run:

```bash
streamlit run app_llm.py
```

This starts the app at: `http://localhost:8501`

---

## ✅ Complete Setup Summary

| Step | Command | Terminal |
|------|---------|----------|
| 1 | Install Ollama | N/A |
| 2 | `ollama pull mistral` | 1 |
| 3 | `pip install -r requirements.txt` | 1 |
| 4 | `ollama serve` | 1 (keep open) |
| 5 | `streamlit run app_llm.py` | 2 |

Then open: `http://localhost:8501`

---

## 🔧 Configuration

### Change Model

Edit `llm_evaluator.py` line 5:

```python
evaluator = LLMEvaluator(model="llama2")  # Change mistral to llama2
```

### Change Strictness

Edit `llm_evaluator.py` in `evaluate_answer()`:

```python
response_text = self.generate_response(prompt, temperature=0.1)
# 0.1 = strict, 0.3 = balanced, 0.5 = lenient
```

### Change Port

If port 11434 is in use, edit `llm_evaluator.py`:

```python
evaluator = LLMEvaluator(ollama_url="http://localhost:9999")
```

---

## 🐛 Troubleshooting

### ❌ "Could not connect to Ollama"

**Solution:**
```bash
ollama serve  # In new terminal
```

### ❌ "Model not found: mistral"

**Solution:**
```bash
ollama pull mistral  # Download model
```

Then refresh browser.

### ⏱️ "Response takes too long"

**Solution:**
```bash
ollama pull llama2  # Smaller model
# Then restart app
```

### 💾 "Out of memory"

**Solution:**
```bash
ollama pull neural-chat  # Smaller model
```

Or close other applications.

### 🔴 "Ollama server crashes"

**Solution:**
Check logs for error. Often memory issue:
```bash
ollama serve --memory=8G  # Limit to 8GB
```

---

## 🎮 First Run

1. Go to `http://localhost:8501`
2. Select topic (e.g., "Machine Learning")
3. Set 3 questions
4. Click "🚀 Start Interview"
5. Answer the question
6. Click "✅ Submit Answer"
7. Review feedback
8. Click "➡️ Next Question"
9. Repeat

After all questions, see interview summary and export as JSON.

---

## 📊 Models Comparison

| Model | Speed | Quality | Size | RAM |
|-------|-------|---------|------|-----|
| mistral | 2-3s | ⭐⭐⭐ | 5GB | 8GB |
| llama2 | 1-2s | ⭐⭐ | 4GB | 8GB |
| neural-chat | 1-2s | ⭐⭐ | 4GB | 8GB |

**Recommended:** mistral (best balance)

---

## 💡 Tips

1. **Faster setup**: Use `llama2` instead of `mistral`
2. **Better quality**: Use `mistral` (default)
3. **Limited RAM**: Use `llama2`
4. **GPU available**: Ollama auto-detects (NVIDIA CUDA)
5. **CPU only**: Works but slower (1-2 minutes per eval)

---

## 🚀 You're Done!

Run these commands:

```bash
# Terminal 1:
ollama serve

# Terminal 2:
streamlit run app_llm.py
```

Visit: `http://localhost:8501`

Enjoy! 🎉
