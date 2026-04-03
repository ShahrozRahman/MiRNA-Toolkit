def explain_with_shap(model, x):
    """Generate SHAP values for supported tree and linear models."""
    try:
        import shap
    except ImportError as exc:
        raise ImportError("shap is required for explainability. Install with: pip install mirna-toolkit[full]") from exc

    explainer = shap.Explainer(model, x)
    shap_values = explainer(x)
    return shap_values


def explain_with_lime(model, x_train, x_instance, class_names=None):
    """Generate a local explanation for one sample using LIME."""
    try:
        from lime.lime_tabular import LimeTabularExplainer
    except ImportError as exc:
        raise ImportError("lime is required for explainability. Install with: pip install mirna-toolkit[full]") from exc

    explainer = LimeTabularExplainer(
        training_data=x_train.values,
        feature_names=list(x_train.columns),
        class_names=class_names,
        mode="classification",
    )
    return explainer.explain_instance(x_instance.values, model.predict_proba)
