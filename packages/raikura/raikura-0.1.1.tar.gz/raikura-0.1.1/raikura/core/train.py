import torch
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
from transformers import Trainer, TrainingArguments
from .metrics import Metrics
from .utils import set_seed, Timer

class DLTrainer:
    def __init__(self, model, optimizer=None, criterion=None, device=None):
        self.model = model
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.optimizer = optimizer or torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = criterion or torch.nn.CrossEntropyLoss()
        self.metrics = Metrics(task_type="classification")
        self.history = {"train_loss": [], "val_loss": [], "metrics": []}
        self.timer = Timer()
        self.early_stopping = None
        self.clip_grad_norm = None
        self.callbacks = {"on_epoch_end": []}

    def register_callback(self, event, fn):
        if event in self.callbacks:
            self.callbacks[event].append(fn)

    def _run_callbacks(self, event, context):
        for cb in self.callbacks.get(event, []):
            cb(context)

    def train(self, X_train, y_train, X_val=None, y_val=None, epochs=10, batch_size=32, shuffle=True):
        set_seed(42)
        X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(self.device)
        y_train_tensor = torch.tensor(y_train, dtype=torch.long).to(self.device)
        train_loader = DataLoader(TensorDataset(X_train_tensor, y_train_tensor), batch_size=batch_size, shuffle=shuffle)
        if X_val is not None:
            X_val_tensor = torch.tensor(X_val, dtype=torch.float32).to(self.device)
            y_val_tensor = torch.tensor(y_val, dtype=torch.long).to(self.device)
            val_loader = DataLoader(TensorDataset(X_val_tensor, y_val_tensor), batch_size=batch_size)
        for epoch in range(epochs):
            self.model.train()
            epoch_loss = 0.0
            self.timer.start()
            for xb, yb in train_loader:
                self.optimizer.zero_grad()
                output = self.model(xb)
                loss = self.criterion(output, yb)
                loss.backward()
                if self.clip_grad_norm:
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.clip_grad_norm)
                self.optimizer.step()
                epoch_loss += loss.item()
            self.history["train_loss"].append(epoch_loss / len(train_loader))
            val_metrics = {}
            if X_val is not None:
                self.model.eval()
                preds = []
                with torch.no_grad():
                    for xb, _ in val_loader:
                        out = self.model(xb)
                        preds.extend(torch.argmax(out, axis=1).cpu().numpy())
                val_metrics = self.metrics.evaluate(y_val, preds)
                self.history["val_loss"].append(val_metrics.get("loss", None))
                self.history["metrics"].append(val_metrics)
            self._run_callbacks("on_epoch_end", {
                "epoch": epoch + 1,
                "train_loss": epoch_loss,
                "val_metrics": val_metrics,
                "elapsed": self.timer.stop()
            })

    def enable_early_stopping(self, patience=3):
        self.early_stopping = {"patience": patience, "counter": 0, "best": float('inf')}

    def enable_gradient_clipping(self, max_norm=1.0):
        self.clip_grad_norm = max_norm

class TransformerTrainer:
    def __init__(self, model, tokenizer, train_dataset, eval_dataset=None, output_dir="./transformer_output", epochs=3):
        self.model = model
        self.tokenizer = tokenizer
        self.train_dataset = train_dataset
        self.eval_dataset = eval_dataset
        self.training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            evaluation_strategy="epoch" if eval_dataset else "no",
            save_strategy="epoch",
            logging_dir=f"{output_dir}/logs",
            load_best_model_at_end=True
        )
        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset if eval_dataset else None
        )

    def train(self):
        self.trainer.train()

    def evaluate(self):
        return self.trainer.evaluate()
