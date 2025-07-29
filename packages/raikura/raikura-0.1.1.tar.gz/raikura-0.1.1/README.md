# Raikura

**Raikura** is an advanced, modular Python library for machine learning that extends beyond the traditional capabilities of scikit-learn. It integrates classical ML models, deep learning, transformers, time series forecasting, fairness auditing, AutoML pipelines, and model interpretability — all in a production-ready, extensible architecture.

Raikura is designed for researchers, engineers, and builders who want control, flexibility, and intelligence in one place.

---

## 📚 Philosophy

Raikura is structured around these design principles:

- **Modularity**: You can use only what you need — from preprocessing to full AutoML pipelines.
- **Extensibility**: Add your own models, metrics, or transformations with minimal friction.
- **Explainability-first**: SHAP, LIME, and Captum are built-in for responsible AI development.
- **Multi-modal**: Combine tabular, text, and image data in one pipeline.
- **Reproducibility**: Config-based pipelines, serialization, and audit logging ensure traceable results.

---

## ⚡ Capabilities Overview

### 🔨 Modeling
- Classical: Logistic Regression, Random Forest, SVM, Gradient Boosting, etc.
- Tree Boosting: XGBoost, LightGBM with auto-hyperparameter tuning
- Deep Learning: PyTorch MLPs and CNNs for tabular and image tasks
- NLP: Transformer models from HuggingFace for classification tasks

### 🧱 Preprocessing
- Auto column classification: numeric, categorical, text, datetime
- Feature scaling, one-hot and ordinal encoding
- TF-IDF/Count vectorization for text
- Polynomial and interaction features with custom degrees
- Lag and rolling-window features for time series

### 🎯 Metrics
- Classification: Accuracy, Precision, Recall, F1, ROC-AUC, Log-loss
- Regression: MAE, MSE, RMSE, R2
- Visuals: Confusion Matrix, ROC curves, metric plots

### 🧠 Explainability
- SHAP: global and local explanations for any model
- LIME: instance-level perturbation insights
- Captum: saliency and attribution for PyTorch-based models

### 📈 Time Series
- Lag and rolling features
- Time-based train/test splits and CV
- Prophet forecasting wrapper
- Hybrid classical + DL time series modeling

### 🔬 Fairness & Bias Auditing
- TPR/FPR/precision/recall by group
- Parity ratios for protected attributes
- Disparate impact calculations

### ⚙️ Automation
- Full YAML-configured training pipelines
- CLI and REST API interfaces
- Config tracking, hashing, and versioning
- Model + config + feature saving

---

## 🔧 Installation

```bash
pip install raikura
```

Requires Python 3.8+ and pip. Some components (like Prophet or Torch) require platform-specific setup.

---

## ✨ Quick Start (Python)

```python
from raikura import AutoMLPipeline, DataLoader

# Load data
df_loader = DataLoader()
X, y = df_loader.load_csv("data/train.csv", target="label")

# Train model
pipe = AutoMLPipeline(model_type="random_forest")
pipe.configure(
    preprocessing={
        "expand_polynomial": True,
        "poly_degree": 2
    }
)
pipe.train(X, y)
```

---

## 🧪 CLI Usage

```bash
raikura train --config config.yaml
```

### Example `config.yaml`
```yaml
data:
  path: data/train.csv
  target: label

model:
  type: logistic_regression
  params: {}

task: classification
problem: tabular

preprocessing:
  expand_polynomial: true
  poly_degree: 2
  poly_interaction_only: false

output:
  model_path: outputs/model.pkl
  columns_path: outputs/columns.pkl
```

---

## 🌐 REST API (FastAPI)

```bash
uvicorn raikura.core.api:app --reload
```

### Endpoints
| Method | Endpoint     | Purpose                    |
|--------|--------------|----------------------------|
| POST   | `/predict`   | Run predictions            |
| POST   | `/evaluate`  | Evaluate with ground truth |
| GET    | `/info`      | Model metadata             |

Send JSON payloads with `columns` and `data` keys.

---

## 🔍 Directory Structure

```
raikura/
├── cli.py               # CLI entrypoint
├── core/
│   ├── models.py        # Model factory
│   ├── pipeline.py      # AutoML logic
│   ├── train.py         # DL and transformers
│   ├── tuner.py         # Hyperparameter tuning
│   ├── preprocess.py    # Full preprocessing suite
│   ├── metrics.py       # Metrics & evaluation
│   ├── explain.py       # SHAP, LIME, Captum
│   ├── fusion.py        # Multi-modal models
│   ├── timeseries.py    # Time series tools
│   ├── audit.py         # Fairness auditing
│   ├── data.py          # Loading & splitting
│   ├── utils.py         # Seeding, saving, logging
│   └── api.py           # FastAPI serving
```

---

## 🧰 Advanced Features

### 🧠 FusionModel
- Accepts tabular + image + text data
- Unified forward pass and joint latent space
- Useful for medical ML, fraud detection, etc.

### 🧪 AutoMLPipeline
- Wraps training, preprocessing, evaluation
- Configurable via code or YAML
- Deep learning and classical interchangeable

### 📊 Metric Tracking
- Logs reports per epoch or fold
- Confusion matrix, F1, precision recall
- Visualizations available in `metrics.py`

---

## 📊 Example: Fairness Audit

```python
from raikura import FairnessAudit

audit = FairnessAudit(sensitive_col="gender", privileged_group="male")
results = audit.evaluate(df_with_preds)
impact = audit.disparate_impact(df_with_preds)
```

---

## 🧪 Testing

Run tests using:
```bash
python -m unittest discover tests/
```
---

## 🙌 Contribute
- Fork and PR on GitHub
- Submit feature requests
- Help expand time series and multi-modal examples
