import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from collections import defaultdict

class FairnessAudit:
    def __init__(self, sensitive_col, privileged_group=None):
        self.sensitive_col = sensitive_col
        self.privileged_group = privileged_group
        self.metrics = ["TPR", "FPR", "Accuracy", "Precision", "Recall"]

    def evaluate(self, df, y_true_col="true", y_pred_col="pred"):
        df = df[[self.sensitive_col, y_true_col, y_pred_col]].copy()
        results = defaultdict(dict)
        groups = df[self.sensitive_col].unique()

        for group in groups:
            gdf = df[df[self.sensitive_col] == group]
            y_true = gdf[y_true_col]
            y_pred = gdf[y_pred_col]
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

            results[group]["TPR"] = tp / (tp + fn) if (tp + fn) > 0 else 0
            results[group]["FPR"] = fp / (fp + tn) if (fp + tn) > 0 else 0
            results[group]["Accuracy"] = accuracy_score(y_true, y_pred)
            results[group]["Precision"] = precision_score(y_true, y_pred, zero_division=0)
            results[group]["Recall"] = recall_score(y_true, y_pred, zero_division=0)

        if self.privileged_group and self.privileged_group in results:
            base = results[self.privileged_group]
            for group in results:
                for metric in self.metrics:
                    ratio = results[group][metric] / base[metric] if base[metric] > 0 else 0
                    results[group][f"{metric}_parity_ratio"] = ratio

        return pd.DataFrame(results).T

    def disparate_impact(self, df, y_pred_col="pred"):
        df = df[[self.sensitive_col, y_pred_col]].copy()
        groups = df[self.sensitive_col].unique()
        di = {}
        for group in groups:
            pr = (df[df[self.sensitive_col] == group][y_pred_col] == 1).mean()
            di[group] = pr
        base = di.get(self.privileged_group, None)
        if base:
            return {g: di[g] / base for g in di}
        return di
