import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.utils import shuffle

class DataLoader:
    def __init__(self, seed=42):
        self.seed = seed

    def load_csv(self, path, target):
        df = pd.read_csv(path)
        X = df.drop(columns=[target])
        y = df[target]
        return X, y

    def load_json(self, path, target):
        df = pd.read_json(path)
        X = df.drop(columns=[target])
        y = df[target]
        return X, y

    def split(self, X, y, test_size=0.2, stratify=True, shuffle_data=True):
        if stratify:
            return train_test_split(X, y, test_size=test_size, stratify=y, random_state=self.seed)
        else:
            return train_test_split(X, y, test_size=test_size, random_state=self.seed, shuffle=shuffle_data)

    def kfold(self, X, y, n_splits=5, stratify=True):
        if stratify:
            return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=self.seed).split(X, y)
        else:
            return KFold(n_splits=n_splits, shuffle=True, random_state=self.seed).split(X)

    def summarize(self, X, y=None):
        summary = {
            "rows": X.shape[0],
            "columns": X.shape[1],
            "null_counts": X.isnull().sum().to_dict(),
            "dtypes": X.dtypes.astype(str).to_dict(),
            "unique_counts": {col: X[col].nunique() for col in X.columns},
        }
        if y is not None:
            summary["target_distribution"] = y.value_counts(normalize=True).to_dict()
        return summary
