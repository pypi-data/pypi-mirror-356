import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier, Perceptron, PassiveAggressiveClassifier
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier,
    ExtraTreesClassifier, HistGradientBoostingClassifier, VotingClassifier, StackingClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.base import clone
from transformers import AutoModelForSequenceClassification, AutoConfig
from joblib import dump, load
import warnings

class BasicNN(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dims=[256, 128, 64], dropout=0.3, activation='relu'):
        super().__init__()
        activations = {
            "relu": nn.ReLU(),
            "leaky_relu": nn.LeakyReLU(),
            "gelu": nn.GELU(),
            "tanh": nn.Tanh()
        }
        act_fn = activations.get(activation.lower(), nn.ReLU())
        layers = []
        dims = [input_dim] + hidden_dims
        for i in range(len(dims) - 1):
            layers.extend([nn.Linear(dims[i], dims[i+1]), act_fn, nn.Dropout(dropout)])
        layers.append(nn.Linear(dims[-1], output_dim))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

class ModelFactory:
    def __init__(self):
        self.registry = {
            "logistic_regression": lambda: LogisticRegression(max_iter=1000),
            "ridge": lambda: RidgeClassifier(),
            "sgd": lambda: SGDClassifier(),
            "perceptron": lambda: Perceptron(),
            "passive_aggressive": lambda: PassiveAggressiveClassifier(),
            "svm": lambda: SVC(probability=True),
            "linear_svc": lambda: CalibratedClassifierCV(LinearSVC()),
            "random_forest": lambda: RandomForestClassifier(),
            "extra_trees": lambda: ExtraTreesClassifier(),
            "gradient_boosting": lambda: GradientBoostingClassifier(),
            "hist_gradient_boosting": lambda: HistGradientBoostingClassifier(),
            "decision_tree": lambda: DecisionTreeClassifier(),
            "knn": lambda: KNeighborsClassifier(),
            "naive_bayes_gaussian": lambda: GaussianNB(),
            "naive_bayes_bernoulli": lambda: BernoulliNB(),
            "naive_bayes_multinomial": lambda: MultinomialNB(),
            "mlp": lambda: MLPClassifier(max_iter=500),
            "lda": lambda: LinearDiscriminantAnalysis(),
            "qda": lambda: QuadraticDiscriminantAnalysis(),
            "adaboost": lambda: AdaBoostClassifier(),
            "xgboost": lambda: XGBClassifier(use_label_encoder=False, eval_metric="mlogloss"),
            "lightgbm": lambda: LGBMClassifier(),
            "catboost": lambda: CatBoostClassifier(verbose=0)
        }

    def create_pipeline(self, model_name, scale=True, feature_selection=None, pca=None, svd=None):
        if model_name not in self.registry:
            raise ValueError(f"{model_name} is not supported.")
        steps = []
        if scale:
            steps.append(('scaler', StandardScaler()))
        if feature_selection is not None:
            selector = SelectKBest(score_func=mutual_info_classif if feature_selection == 'mutual_info' else f_classif, k=10)
            steps.append(('feature_selection', selector))
        if pca is not None:
            steps.append(('pca', PCA(n_components=pca)))
        if svd is not None:
            steps.append(('svd', TruncatedSVD(n_components=svd)))
        steps.append(('model', self.registry[model_name]()))
        return Pipeline(steps)

    def create_pytorch_model(self, input_dim, output_dim, hidden_dims=None, dropout=0.3, activation='relu'):
        hidden_dims = hidden_dims or [256, 128, 64]
        return BasicNN(input_dim, output_dim, hidden_dims, dropout, activation)

    def create_transformer_model(self, model_name, num_labels=2):
        config = AutoConfig.from_pretrained(model_name, num_labels=num_labels)
        return AutoModelForSequenceClassification.from_pretrained(model_name, config=config)

    def create_voting_ensemble(self, model_names, voting='soft', weights=None):
        models = []
        for name in model_names:
            if name in self.registry:
                models.append((name, self.registry[name]()))
            else:
                warnings.warn(f"Model {name} not found in registry.")
        return VotingClassifier(estimators=models, voting=voting, weights=weights)

    def create_stacking_ensemble(self, base_models, final_model='logistic_regression', passthrough=True):
        estimators = [(name, self.registry[name]()) for name in base_models if name in self.registry]
        final_estimator = self.registry[final_model]() if final_model in self.registry else LogisticRegression()
        return StackingClassifier(estimators=estimators, final_estimator=final_estimator, passthrough=passthrough)

    def clone_model(self, model):
        return clone(model)

    def save_model(self, model, path):
        dump(model, path)

    def load_model(self, path):
        return load(path)
