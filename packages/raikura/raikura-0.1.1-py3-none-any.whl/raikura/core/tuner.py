import numpy as np
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.metrics import make_scorer, accuracy_score
import optuna
import warnings

class HyperparameterTuner:
    def __init__(self, model_name, search_space, scoring="accuracy", strategy="optuna", trials=25, cv=5):
        self.model_name = model_name
        self.search_space = search_space
        self.strategy = strategy
        self.cv = cv
        self.trials = trials
        self.scoring = scoring
        self.best_model = None
        self.best_params = None
        self.best_score = None

    def search(self, X, y):
        if self.strategy == "grid":
            return self._grid_search(X, y)
        elif self.strategy == "random":
            return self._random_search(X, y)
        elif self.strategy == "optuna":
            return self._optuna_search(X, y)
        else:
            raise ValueError("Unsupported strategy. Choose from: grid, random, optuna.")

    def _grid_search(self, X, y):
        from sklearn.pipeline import Pipeline
        model = self._get_base_model()
        grid = GridSearchCV(model, self.search_space, scoring=self.scoring, cv=self.cv)
        grid.fit(X, y)
        self.best_model = grid.best_estimator_
        self.best_params = grid.best_params_
        self.best_score = grid.best_score_
        return self.best_model

    def _random_search(self, X, y):
        model = self._get_base_model()
        rand = RandomizedSearchCV(model, self.search_space, scoring=self.scoring, cv=self.cv, n_iter=self.trials)
        rand.fit(X, y)
        self.best_model = rand.best_estimator_
        self.best_params = rand.best_params_
        self.best_score = rand.best_score_
        return self.best_model

    def _optuna_search(self, X, y):
        def objective(trial):
            params = {key: trial.suggest_categorical(key, val) if isinstance(val, list) else val for key, val in self.search_space.items()}
            model = self._get_base_model(**params)
            try:
                score = cross_val_score(model, X, y, cv=self.cv, scoring=self.scoring).mean()
            except Exception as e:
                warnings.warn(str(e))
                return 0.0
            return score

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=self.trials)
        self.best_params = study.best_params
        self.best_score = study.best_value
        self.best_model = self._get_base_model(**self.best_params)
        self.best_model.fit(X, y)
        return self.best_model

    def _get_base_model(self, **kwargs):
        from .models import ModelFactory
        mf = ModelFactory()
        return mf.create_pipeline(model_name=self.model_name, **kwargs)
