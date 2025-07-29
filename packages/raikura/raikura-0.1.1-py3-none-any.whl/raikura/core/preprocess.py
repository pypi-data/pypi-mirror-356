import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, OneHotEncoder, OrdinalEncoder,
    LabelEncoder, FunctionTransformer, PolynomialFeatures
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.base import BaseEstimator, TransformerMixin

class DateFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, drop_original=True):
        self.drop_original = drop_original

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_ = X.copy()
        for col in X_.select_dtypes(include=['datetime64', 'object']).columns:
            try:
                X_[col] = pd.to_datetime(X_[col])
                X_[f"{col}_year"] = X_[col].dt.year
                X_[f"{col}_month"] = X_[col].dt.month
                X_[f"{col}_day"] = X_[col].dt.day
                X_[f"{col}_weekday"] = X_[col].dt.weekday
                if self.drop_original:
                    X_.drop(columns=[col], inplace=True)
            except:
                continue
        return X_

class FeatureGenerator(BaseEstimator, TransformerMixin):
    def __init__(self, functions=None):
        self.functions = functions or []

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_ = X.copy()
        for func in self.functions:
            new_feature = func(X_)
            X_[new_feature.name] = new_feature
        return X_

class FeatureExpander(BaseEstimator, TransformerMixin):
    def __init__(self, degree=2, interaction_only=False, include_bias=False):
        self.poly = PolynomialFeatures(degree=degree, interaction_only=interaction_only, include_bias=include_bias)
        self.columns_ = None

    def fit(self, X, y=None):
        self.poly.fit(X)
        self.columns_ = self.poly.get_feature_names_out(X.columns)
        return self

    def transform(self, X):
        X_poly = self.poly.transform(X)
        return pd.DataFrame(X_poly, columns=self.columns_, index=X.index)

class Preprocessor:
    def __init__(self):
        self.pipeline = None
        self.feature_cols = {
            "numeric": [],
            "categorical": [],
            "text": [],
            "datetime": []
        }
        self.config = {}

    def auto_detect_columns(self, df, text_max_unique=100):
        self.feature_cols["numeric"] = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.feature_cols["categorical"] = [
            col for col in df.select_dtypes(include=['object', 'category']).columns
            if df[col].nunique() < text_max_unique and not self._is_text_column(df[col])
        ]
        self.feature_cols["text"] = [
            col for col in df.select_dtypes(include=['object', 'string']).columns
            if self._is_text_column(df[col])
        ]
        self.feature_cols["datetime"] = df.select_dtypes(include=['datetime64']).columns.tolist()

    def _is_text_column(self, col):
        return col.dtype == 'object' and col.apply(lambda x: isinstance(x, str)).mean() > 0.9

    def build_pipeline(self, strategy="mean", scaler="standard", encoder="onehot", vectorizer="tfidf", config=None):
        self.config = config or {}

        numeric_steps = [
            ('imputer', SimpleImputer(strategy=strategy)),
            ('scaler', StandardScaler() if scaler == "standard" else MinMaxScaler())
        ]
        if self.config.get("expand_polynomial", False):
            numeric_steps.append(('poly', FeatureExpander(
                degree=self.config.get("poly_degree", 2),
                interaction_only=self.config.get("poly_interaction_only", False),
                include_bias=False
            )))
        numeric_transformer = Pipeline(numeric_steps)

        categorical_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy="most_frequent")),
            ('encoder', OneHotEncoder(handle_unknown='ignore') if encoder == "onehot" else OrdinalEncoder())
        ])

        text_transformer = Pipeline([
            ('vectorizer', TfidfVectorizer() if vectorizer == "tfidf" else CountVectorizer())
        ])

        transformers = []
        if self.feature_cols["numeric"]:
            transformers.append(("num", numeric_transformer, self.feature_cols["numeric"]))
        if self.feature_cols["categorical"]:
            transformers.append(("cat", categorical_transformer, self.feature_cols["categorical"]))
        if self.feature_cols["text"]:
            transformers.append(("text", text_transformer, self.feature_cols["text"]))

        self.pipeline = ColumnTransformer(transformers=transformers)

    def transform(self, df):
        return self.pipeline.fit_transform(df)

    def fit_transform(self, df):
        self.auto_detect_columns(df)
        self.build_pipeline()
        return self.transform(df)
