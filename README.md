# 🤖 HireLens

> **An intelligent, adaptive interview system powered by local LLM (Ollama)**  
> Take realistic multi-turn interviews with AI-generated questions, get personalized feedback, and track your progress—all running locally, completely free.

---

## ✨ How HireLens Works

HireLens uses **Local LLM (Ollama)** to conduct intelligent, adaptive interviews:

```
Your Answer → LLM Analysis → Intelligent Evaluation → Personalized Feedback
```

The system understands concepts and context, not just keywords. It adapts follow-up questions based on your answers to test deeper knowledge.

---

## 🎯 Key Features

| Feature | Benefit |
|---------|---------|
| **🧠 AI-Powered Evaluation** | LLM understands concepts, not just keywords |
| **🔄 Multi-turn Interviews** | Adaptive follow-up questions based on your answers |
| **💬 Intelligent Feedback** | Get personalized, actionable recommendations |
| **📊 Performance Reports** | Track your score, trends, and improvement areas |
| **💾 Export Results** | Save interviews as JSON for tracking progress |
| **🆓 100% FREE** | Runs locally with no API costs |
| **🔌 Offline Ready** | Works without internet after initial setup |
| **⚡ Fast** | 2-3 seconds per evaluation (on modern hardware) |

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Windows/Mac/Linux
- 8GB RAM (16GB recommended)
- Python 3.8+

### Step 1: Download & Install Ollama
1. Go to **https://ollama.ai**
2. Download for your OS
3. Install and **restart your computer**

### Step 2: Get a Model
```bash
ollama pull mistral
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the App

**Windows:** Double-click `start_llm.bat`

**Or manually** (all platforms):
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start app
streamlit run app_llm.py
```

**Open:** http://localhost:8501 ✅

---

## 📖 How to Use

### Starting an Interview

1. **Select a Topic**
   - Machine Learning
   - Python Programming
   - Data Science
   - Web Development
   - Or enter custom topic

2. **Add Keywords** (optional)
   - Concepts you want evaluated
   - Helps LLM focus on specific areas

3. **Set Question Count**
   - 1-5 questions for your interview

4. **Click "🚀 Start Interview"**
   - AI generates first question

### During Interview

1. **Read AI-Generated Question**
2. **Type Your Answer**
3. **Click "✅ Submit Answer"**
4. **Review Feedback:**
   - ⭐ Score (1-10)
   - 💪 Strengths (what you did well)
   - 📈 Improvements (areas to focus on)
5. **Click "➡️ Next Question"** or generate follow-ups

### After Interview

- **View Summary** - Average score, trends
- **See Full Transcript** - All Q&A history
- **Export as JSON** - Download for records
- **Start New Interview** - Take another test

---

## 💡 Example Interview

```
Q: "What is Machine Learning?" [AI-Generated]

Your Answer: 
"ML is when systems learn patterns from data without explicit programming"

📊 Evaluation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 8/10

💪 Strengths:
  ✓ Clear, concise definition
  ✓ Mentions learning mechanism
  ✓ Correctly explains automation

📈 Areas to Improve:
  → Explain role of algorithms
  → Add example of supervised learning
  → Discuss practical applications

🎯 Follow-up Question:
"How do supervised and unsupervised learning differ?"
```

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────┐
│      Streamlit UI                   │
│   (Interactive Web Interface)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Interview Conversation Manager   │
│  (Multi-turn flow, question gen)    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      LLM Evaluator                  │
│  (Ollama integration, scoring)      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Local Ollama Server              │
│  (Mistral / Llama2 / Neural-Chat)   │
└─────────────────────────────────────┘
```

**How it works:**
1. User inputs answer
2. Interview manager processes it
3. LLM evaluator scores & analyzes
4. Results displayed in UI
5. Next question generated (if needed)

---

## ⚙️ Configuration

### Change LLM Model

Edit `llm_evaluator.py` (line 5):

```python
evaluator = LLMEvaluator(model="mistral")  # Change to:
```

Available models:
- `mistral` (recommended) - Best balance of speed & quality
- `llama2` - Faster, smaller, good quality
- `neural-chat` - Optimized for conversation
- `dolphin-mixtral` - Best quality, slower

### Adjust Evaluation Strictness

Edit `llm_evaluator.py` in `evaluate_answer()`:

```python
# Stricter (penalizes vagueness, more consistent)
temperature=0.1

# Balanced (default, recommended)
temperature=0.3

# More lenient (more varied, rewards creativity)
temperature=0.5
```

### Change Ollama Port

If port 11434 is in use, edit `llm_evaluator.py`:

```python
evaluator = LLMEvaluator(ollama_url="http://localhost:9999")
```

---

## 📊 Models Comparison

| Model | Speed | Quality | Size | RAM | Best For |
|-------|-------|---------|------|-----|----------|
| **mistral** | 2-3s | ⭐⭐⭐ | 5GB | 8GB | General use (default) |
| **llama2** | 1-2s | ⭐⭐ | 4GB | 8GB | Speed priority |
| **neural-chat** | 1-2s | ⭐⭐ | 4GB | 8GB | Conversational |
| **dolphin-mixtral** | 5-8s | ⭐⭐⭐⭐ | 26GB | 16GB | Maximum accuracy |

---

## 📁 Project Structure

```
HireLens/
├── app_llm.py                    # Main Streamlit application
├── llm_evaluator.py              # LLM integration (Ollama)
├── interview_conversation.py     # Multi-turn interview logic
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── SETUP.md                      # Detailed setup guide
├── start_llm.bat                 # Quick-start script (Windows)
└── CONVERSION_SUMMARY.md         # What was changed from v1
```

---

## 🐛 Troubleshooting

### ❌ "Could not connect to Ollama"

**Solution:**
1. Make sure Ollama is installed: https://ollama.ai
2. Start server in new terminal: `ollama serve`
3. Verify: `ollama --version`

### ❌ "Model not found: mistral"

**Solution:**
```bash
ollama pull mistral
# Or try smaller: ollama pull llama2
```

### ⏱️ "Responses are very slow"

**Solutions:**
1. Use faster model: `ollama pull llama2`
2. Check RAM availability (close other apps)
3. Enable GPU if available (Ollama auto-detects NVIDIA CUDA)

### 💾 "Out of memory"

**Solutions:**
1. Close other applications
2. Use smaller model: `ollama pull neural-chat`
3. Limit memory: `ollama serve --memory=8G`

### 🔴 "Window closes immediately"

**Solution:**
Use manual method instead:
```bash
ollama serve          # Terminal 1
streamlit run app_llm.py  # Terminal 2
```

See **SETUP.md** for comprehensive troubleshooting.

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Setup Time | 5-10 minutes |
| Model Download | ~5GB (Mistral) |
| Response Time | 2-3 seconds |
| Memory Usage | ~8GB (with model) |
| Questions per Interview | 1-5 |
| Cost | $0 (free, local) |
| Internet Required | No (after setup) |

---

## 🎓 Use Cases

- **Job Interview Prep** - Practice technical interviews
- **Self-Study** - Quiz yourself on any topic
- **Teaching** - Create adaptive student assessments
- **Certification Prep** - Practice for exams
- **Skill Tracking** - Monitor progress over time

---

## 📦 What's Included

```
✅ Intelligent answer evaluation (LLM-powered)
✅ Semantic understanding of concepts
✅ AI-generated follow-up questions
✅ Multi-turn adaptive interviews
✅ Detailed performance feedback
✅ Interview transcript export (JSON)
✅ Performance trend tracking
✅ Personalized recommendations
```

---

## 📚 Documentation

| Document | Time | Content |
|----------|------|---------|
| **README.md** | 5 min | Overview & quick start |
| **SETUP.md** | 5 min | Installation & configuration |
| **Code comments** | N/A | Implementation details |

---

## 🚀 Next Steps

1. ✅ Install Ollama from https://ollama.ai
2. ✅ Run `start_llm.bat` (Windows) or manual commands
3. ✅ Take your first interview
4. ✅ Try different models if needed
5. ✅ Export and track your results

---

## 💡 Pro Tips

- **Faster setup**: Use `llama2` instead of `mistral`
- **Better quality**: Use `mistral` (default)
- **Limited RAM**: Use `llama2`
- **GPU available**: Ollama auto-detects and accelerates
- **Improve answers**: Review follow-up questions for weak areas
- **Track progress**: Export results and compare over time

---

## 🤝 Contributing

Have ideas for improvements? Feel free to:
- Modify prompts in `llm_evaluator.py`
- Add new interview topics
- Customize evaluation criteria
- Integrate with other LLMs

---

## 📝 License

Same as original project.

---

## ✨ Built With

- **Streamlit** - Interactive web UI
- **Ollama** - Local LLM runtime (free, open-source)
- **Python** - Core language
- **LLMs** - Mistral, Llama2, and more

---

## 🎉 Ready to Start?

```bash
ollama serve              # Terminal 1
streamlit run app_llm.py  # Terminal 2
```

**Open:** http://localhost:8501

**Questions?** Check **SETUP.md** or review the troubleshooting section above.

---

**Happy interviewing! 🚀**
