from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

class FeatureExpander:
    def __init__(self, degree=2, interaction_only=False, include_bias=False):
        self.poly = PolynomialFeatures(degree=degree, interaction_only=interaction_only, include_bias=include_bias)
        self.columns_ = None

    def fit_transform(self, X):
        X_poly = self.poly.fit_transform(X)
        self.columns_ = self.poly.get_feature_names_out(X.columns)
        return pd.DataFrame(X_poly, columns=self.columns_, index=X.index)

    def transform(self, X):
        X_poly = self.poly.transform(X)
        return pd.DataFrame(X_poly, columns=self.columns_, index=X.index)
