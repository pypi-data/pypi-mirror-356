import os
import random
import time
import json
import logging
import hashlib
import joblib
import torch
import numpy as np
import pandas as pd

class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is None:
            return 0
        elapsed = time.time() - self.start_time
        self.start_time = None
        return elapsed

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except:
        pass

def get_hash(obj):
    try:
        return hashlib.md5(json.dumps(obj, sort_keys=True).encode()).hexdigest()
    except:
        return str(hash(obj))

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def load_model(path):
    return joblib.load(path)

def log_info(message, level="INFO", name="raikura"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    getattr(logger, level.lower())(message)

def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def memory_usage():
    import psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1e6

def inspect_tensor(tensor):
    if isinstance(tensor, torch.Tensor):
        return {
            "shape": list(tensor.shape),
            "dtype": str(tensor.dtype),
            "device": str(tensor.device),
            "mean": tensor.float().mean().item(),
            "std": tensor.float().std().item()
        }
    return {}

def explain_model(model, X, method="auto"):
    try:
        import shap
        explainer = shap.Explainer(model, X)
        shap_values = explainer(X)
        shap.plots.beeswarm(shap_values)
    except Exception as e:
        log_info(f"SHAP explanation failed: {e}", level="WARNING")

def save_config(config, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(config, f, indent=4)

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)
