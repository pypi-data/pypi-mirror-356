import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from prophet import Prophet
import warnings

class LagFeatureGenerator:
    def __init__(self, lags=[1, 3, 7]):
        self.lags = lags

    def transform(self, df, target_col):
        df = df.copy()
        for lag in self.lags:
            df[f"{target_col}_lag{lag}"] = df[target_col].shift(lag)
        df.dropna(inplace=True)
        return df

class RollingFeatureGenerator:
    def __init__(self, windows=[3, 7]):
        self.windows = windows

    def transform(self, df, target_col):
        df = df.copy()
        for w in self.windows:
            df[f"{target_col}_roll{w}_mean"] = df[target_col].rolling(w).mean()
            df[f"{target_col}_roll{w}_std"] = df[target_col].rolling(w).std()
        df.dropna(inplace=True)
        return df

class TimeSplit:
    def __init__(self, n_splits=5):
        self.splitter = TimeSeriesSplit(n_splits=n_splits)

    def split(self, X, y):
        return self.splitter.split(X, y)

class ClassicalTimeSeriesModel:
    def __init__(self, model=None):
        self.model = model or GradientBoostingRegressor()
        self.metrics = []

    def train_evaluate(self, X, y, n_splits=5):
        tscv = TimeSeriesSplit(n_splits=n_splits)
        for train_idx, test_idx in tscv.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            self.model.fit(X_train, y_train)
            preds = self.model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            self.metrics.append(rmse)
        return np.mean(self.metrics), np.std(self.metrics)

class ProphetWrapper:
    def __init__(self, config=None):
        self.model = Prophet(**(config or {}))

    def train(self, df, date_col, target_col):
        df = df.rename(columns={date_col: "ds", target_col: "y"})
        self.model.fit(df)

    def predict(self, periods, freq='D'):
        future = self.model.make_future_dataframe(periods=periods, freq=freq)
        forecast = self.model.predict(future)
        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
