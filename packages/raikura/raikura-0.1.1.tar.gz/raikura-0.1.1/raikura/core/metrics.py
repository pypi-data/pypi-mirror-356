import numpy as np
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    roc_auc_score, log_loss, confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

class Metrics:
    def __init__(self, task_type="classification"):
        self.task_type = task_type

    def evaluate(self, y_true, y_pred, proba=None):
        if self.task_type == "classification":
            return self._classification_metrics(y_true, y_pred, proba)
        elif self.task_type == "regression":
            return self._regression_metrics(y_true, y_pred)
        else:
            raise ValueError(f"Unsupported task type: {self.task_type}")

    def _classification_metrics(self, y_true, y_pred, proba):
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "f1_macro": f1_score(y_true, y_pred, average='macro'),
            "f1_micro": f1_score(y_true, y_pred, average='micro'),
            "precision": precision_score(y_true, y_pred, average='macro', zero_division=0),
            "recall": recall_score(y_true, y_pred, average='macro', zero_division=0)
        }
        if proba is not None:
            try:
                if len(np.unique(y_true)) == 2:
                    metrics["roc_auc"] = roc_auc_score(y_true, proba[:, 1])
                    metrics["log_loss"] = log_loss(y_true, proba)
                else:
                    y_bin = label_binarize(y_true, classes=np.unique(y_true))
                    metrics["roc_auc_ovr"] = roc_auc_score(y_bin, proba, average="macro", multi_class="ovr")
                    metrics["log_loss"] = log_loss(y_bin, proba)
            except Exception:
                warnings.warn("ROC AUC or log loss could not be computed")
        return metrics

    def _regression_metrics(self, y_true, y_pred):
        return {
            "mae": mean_absolute_error(y_true, y_pred),
            "mse": mean_squared_error(y_true, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "r2": r2_score(y_true, y_pred)
        }

    def confusion_matrix_plot(self, y_true, y_pred, labels=None, title="Confusion Matrix"):
        cm = confusion_matrix(y_true, y_pred, labels=labels)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_title(title)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        if labels is not None:
            ax.set_xticklabels(labels)
            ax.set_yticklabels(labels)
        plt.tight_layout()
        return fig

    def classification_report_text(self, y_true, y_pred):
        return classification_report(y_true, y_pred)

    def plot_metric_curve(self, values, label="Metric", title="Metric Over Time"):
        fig, ax = plt.subplots()
        ax.plot(values, marker='o')
        ax.set_title(title)
        ax.set_xlabel("Epoch")
        ax.set_ylabel(label)
        ax.grid(True)
        return fig
