# 🧠 NeuralScan — AI Text Detector (v2)

> High-precision AI text detector using **TF-IDF + Logistic Regression** trained on 212 curated samples. Achieves **100% 5-fold cross-validated accuracy** on in-distribution data.

---

## 🚀 Quick Start

```bash
cd ai-detector
pip install flask flask-cors scikit-learn numpy
python app.py
# Open http://localhost:5000
```

---

## 📁 Project Structure

```
ai-detector/
├── app.py                  ← Flask server + ML model
├── requirements.txt        ← Dependencies
├── model.pkl               ← Auto-generated on first run
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/
        ├── particles.js
        └── app.js
```

---

## 🎨 Theme & Design

**Aesthetic:** Dark cyberpunk / neural network terminal

| Element | Choice |
|---|---|
| Primary font | Orbitron |
| Background | Deep navy `#030712` |
| Accent | Neon green `#00ff88` |
| AI color | Neon red `#ff3366` |
| Human color | Neon green `#00ff88` |

---

## 🤖 How Detection Works (v2)

### 1. TF-IDF + Logistic Regression (75% weight)
- Text converted to TF-IDF feature vectors with **1–3 word n-grams**
- Up to **15,000 features** with sublinear TF scaling
- **Logistic Regression** with balanced class weights
- Trained on **212 samples** (106 AI / 106 Human) across 10+ topic domains

### 2. Heuristic Engine (25% weight)

| Signal | AI indicator | Human indicator |
|---|---|---|
| Avg sentence length | > 22 words | Short sentences |
| Sentence length variance | Low < 10 | High > 60 |
| AI buzzwords | "furthermore", "leverage", "paradigm", "robust", "holistic"… | — |
| Human slang | "lol", "ngl", "kinda", "honestly"… | — |
| Contractions | Absent | 3+ present |
| Exclamation / ? marks | Rare | Frequent |
| ALL CAPS words | Rare | Present |
| Ellipsis / dashes | Rare | Frequent |
| First-person pronouns | Low | High |
| Passive voice | Heavy | Light |

### 3. Fusion
```
final_score = 0.75 × TF-IDF_LR_probability + 0.25 × heuristic_score
label       = "ai"    if final_score > 0.5
confidence  = final_score       if AI
            = 1 - final_score   if Human
```

---

## 📊 Dataset (v2)

**212 samples** balanced evenly (106 AI / 106 Human) across domains:

| Domain | AI samples | Human samples |
|---|---|---|
| Technology & AI | 20 | — |
| Health & Science | 10 | — |
| Education | 10 | — |
| Business & Economics | 10 | — |
| Environment | 10 | — |
| Politics & Society | 10 | — |
| Culture & Arts | 10 | — |
| Personal development | 10 | — |
| General | 6 | — |
| Casual / Personal | — | 22 |
| Tech / Work | — | 10 |
| Food & Cooking | — | 10 |
| Relationships | — | 10 |
| Health & Fitness | — | 10 |
| Travel | — | 10 |
| Emotions | — | 10 |
| Opinions | — | 10 |
| Other | — | 14 |

**5-fold cross-validation accuracy: ~100%** on in-distribution text.

---

## 🔌 API Endpoints

### `POST /api/detect`

```json
{ "text": "Your text here..." }
```

Response:
```json
{
  "label":      "ai",
  "confidence": 87.3,
  "score":      0.873,
  "ml_score":   0.891,
  "heuristic":  0.820,
  "word_count": 42,
  "char_count": 268,
  "model_type": "TF-IDF + Logistic Regression"
}
```

### `GET /api/dataset/stats`

```json
{
  "total":       212,
  "ai":          106,
  "human":       106,
  "vocab":       8432,
  "model":       "TF-IDF + Logistic Regression",
  "cv_accuracy": 100.0,
  "ngrams":      "1-3",
  "features":    "15000"
}
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web server |
| `flask-cors` | Cross-origin requests |
| `scikit-learn` | TF-IDF vectorizer + Logistic Regression |
| `numpy` | Numerical ops |

> Falls back to enhanced Naive Bayes if scikit-learn is unavailable.

---

## 📄 License

MIT
