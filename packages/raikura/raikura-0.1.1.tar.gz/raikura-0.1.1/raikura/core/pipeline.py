import os
import time
import uuid
import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from transformers import Trainer, TrainingArguments
from .models import ModelFactory
from .utils import set_seed, save_model, load_model
from .metrics import Metrics
from .tuner import HyperparameterTuner
from .preprocess import Preprocessor

class AutoMLPipeline:
    def __init__(self, task_type="classification", model_type="logistic_regression", problem="tabular"):
        self.task_type = task_type
        self.model_type = model_type
        self.problem = problem
        self.model_factory = ModelFactory()
        self.model = None
        self.preprocessor = None
        self.callbacks = {"on_train_start": [], "on_eval_end": []}
        self.metrics = Metrics(task_type)
        self.tuner = None
        self.history = []
        self.seed = 42
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preprocessing_config = {}

    def register_callback(self, event, fn):
        if event in self.callbacks:
            self.callbacks[event].append(fn)

    def _run_callbacks(self, event, context):
        for cb in self.callbacks.get(event, []):
            cb(context)

    def configure(self, **kwargs):
        self.config = kwargs
        self.preprocessing_config = kwargs.get("preprocessing", {})
        set_seed(self.seed)
        if self.problem == "tabular":
            self.model = self.model_factory.create_pipeline(
                model_name=self.model_type,
                scale=kwargs.get("scale", True),
                feature_selection=kwargs.get("feature_selection", None),
                pca=kwargs.get("pca", None),
                svd=kwargs.get("svd", None)
            )
        elif self.problem == "dl":
            input_dim, output_dim = kwargs["input_dim"], kwargs["output_dim"]
            self.model = self.model_factory.create_pytorch_model(input_dim, output_dim)
            self.model.to(self.device)
        elif self.problem == "nlp":
            self.model = self.model_factory.create_transformer_model(self.model_type, kwargs.get("num_labels", 2))

    def train(self, X, y, test_size=0.2, eval=True):
        self._run_callbacks("on_train_start", {"X": X, "y": y})
        if self.problem == "tabular":
            X, y = shuffle(X, y, random_state=self.seed)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            if self.preprocessing_config:
                self.preprocessor = Preprocessor()
                X_train = self.preprocessor.fit_transform(X_train, config=self.preprocessing_config)
                X_test = self.preprocessor.transform(X_test)
            self.model.fit(X_train, y_train)
            if eval:
                preds = self.model.predict(X_test)
                report = self.metrics.evaluate(y_test, preds, proba=self._try_proba(X_test))
                self._run_callbacks("on_eval_end", report)
                self.history.append(report)
                return report
        elif self.problem == "dl":
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(self.device)
            y_train_tensor = torch.tensor(y_train, dtype=torch.long).to(self.device)
            X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(self.device)
            y_test_tensor = torch.tensor(y_test, dtype=torch.long).to(self.device)
            criterion = torch.nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
            for epoch in range(10):
                self.model.train()
                optimizer.zero_grad()
                output = self.model(X_train_tensor)
                loss = criterion(output, y_train_tensor)
                loss.backward()
                optimizer.step()
            with torch.no_grad():
                self.model.eval()
                preds = torch.argmax(self.model(X_test_tensor), axis=1).cpu().numpy()
                report = self.metrics.evaluate(y_test, preds)
                self._run_callbacks("on_eval_end", report)
                self.history.append(report)
                return report
        elif self.problem == "nlp":
            pass

    def _try_proba(self, X_test):
        try:
            return self.model.predict_proba(X_test)
        except:
            return None

    def tune(self, X, y, search_space):
        self.tuner = HyperparameterTuner(model_name=self.model_type, search_space=search_space)
        self.model = self.tuner.search(X, y)
        return self.model

    def cross_validate(self, X, y, folds=5):
        skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=self.seed)
        scores = []
        for train_idx, test_idx in skf.split(X, y):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            model = self.model_factory.create_pipeline(self.model_type)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = accuracy_score(y_test, y_pred)
            scores.append(score)
        return np.mean(scores), np.std(scores)

    def save(self, path):
        save_model(self.model, path)

    def load(self, path):
        self.model = load_model(path)
