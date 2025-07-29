import unittest
import pandas as pd
import numpy as np
from raikura.core.models import ModelFactory
from raikura.core.pipeline import AutoMLPipeline
from raikura.core.preprocess import Preprocessor, FeatureExpander
from raikura.core.metrics import Metrics
from raikura.core.utils import save_config, load_config

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "a": [1, 2, 3],
            "b": [4, 5, 6],
            "c": ["x", "y", "z"]
        })

    def test_feature_expander(self):
        expander = FeatureExpander(degree=2)
        result = expander.fit_transform(self.df[["a", "b"]])
        self.assertEqual(result.shape[1], 5)  # x1, x2, x1^2, x1*x2, x2^2

    def test_preprocessor_numeric(self):
        pre = Preprocessor()
        pre.auto_detect_columns(self.df)
        pre.build_pipeline(config={"expand_polynomial": True, "poly_degree": 2})
        X = pre.pipeline.transform(self.df)
        self.assertIsNotNone(X)

class TestModelFactory(unittest.TestCase):
    def test_model_creation(self):
        factory = ModelFactory()
        model = factory.create_pipeline("random_forest")
        self.assertTrue(hasattr(model, "fit"))
        self.assertTrue(hasattr(model, "predict"))

class TestAutoMLPipeline(unittest.TestCase):
    def test_pipeline_train(self):
        df = pd.DataFrame({
            "x1": [1, 2, 3, 4],
            "x2": [5, 6, 7, 8],
            "y": [0, 1, 0, 1]
        })
        X = df.drop("y", axis=1)
        y = df["y"]
        pipe = AutoMLPipeline(model_type="logistic_regression")
        pipe.configure()
        result = pipe.train(X, y, test_size=0.25)
        self.assertIn("accuracy", result)

class TestMetrics(unittest.TestCase):
    def test_accuracy(self):
        m = Metrics("classification")
        y_true = [1, 0, 1, 0]
        y_pred = [1, 0, 0, 0]
        results = m.evaluate(y_true, y_pred)
        self.assertIn("accuracy", results)
        self.assertGreaterEqual(results["accuracy"], 0.5)

class TestUtils(unittest.TestCase):
    def test_config_save_load(self):
        cfg = {"a": 1, "b": 2}
        path = "test_config.json"
        save_config(cfg, path)
        loaded = load_config(path)
        self.assertEqual(cfg, loaded)

if __name__ == '__main__':
    unittest.main()
