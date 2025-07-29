import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
import lime
import lime.lime_tabular
from sklearn.inspection import permutation_importance
from .utils import log_info

class Explainer:
    def __init__(self, model, X, mode="classification"):
        self.model = model
        self.X = X
        self.mode = mode
        self.explainer = None
        self.framework = self._detect_framework()

    def _detect_framework(self):
        if hasattr(self.model, "predict_proba"):
            return "sklearn"
        elif "transformers" in str(type(self.model)).lower():
            return "transformers"
        elif hasattr(self.model, "forward"):
            return "pytorch"
        return "unknown"

    def shap_summary(self):
        try:
            if self.framework == "sklearn":
                self.explainer = shap.Explainer(self.model, self.X)
            elif self.framework == "pytorch":
                self.explainer = shap.DeepExplainer(self.model, torch.tensor(self.X.values, dtype=torch.float32))
            else:
                log_info("SHAP not supported for this model type", level="WARNING")
                return
            shap_values = self.explainer(self.X)
            shap.plots.beeswarm(shap_values)
        except Exception as e:
            log_info(f"SHAP failed: {e}", level="WARNING")

    def lime_explain(self, instance_idx=0):
        try:
            explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=np.array(self.X),
                mode=self.mode,
                feature_names=self.X.columns.tolist(),
                discretize_continuous=True
            )
            explanation = explainer.explain_instance(
                data_row=self.X.iloc[instance_idx].values,
                predict_fn=self.model.predict_proba if hasattr(self.model, "predict_proba") else self.model.predict
            )
            explanation.show_in_notebook()
        except Exception as e:
            log_info(f"LIME failed: {e}", level="WARNING")

    def permutation_importance_plot(self, y, scoring="accuracy", n_repeats=10):
        try:
            result = permutation_importance(self.model, self.X, y, n_repeats=n_repeats, scoring=scoring)
            importances = pd.Series(result.importances_mean, index=self.X.columns)
            fig, ax = plt.subplots(figsize=(10, 5))
            importances.sort_values().plot.barh(ax=ax)
            ax.set_title("Permutation Importance")
            plt.tight_layout()
            return fig
        except Exception as e:
            log_info(f"Permutation importance failed: {e}", level="WARNING")

    def captum_saliency(self, input_tensor, target_label):
        try:
            from captum.attr import Saliency
            saliency = Saliency(self.model)
            grads = saliency.attribute(input_tensor, target=target_label)
            return grads
        except Exception as e:
            log_info(f"Captum saliency failed: {e}", level="WARNING")

    def captum_integrated_gradients(self, input_tensor, target_label):
        try:
            from captum.attr import IntegratedGradients
            ig = IntegratedGradients(self.model)
            attributions, _ = ig.attribute(input_tensor, target=target_label, return_convergence_delta=True)
            return attributions
        except Exception as e:
            log_info(f"Captum IG failed: {e}", level="WARNING")