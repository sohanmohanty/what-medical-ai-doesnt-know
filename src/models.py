"""Reusable model builders for the final project layout."""

from copy import deepcopy

from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression


DEFAULT_MODEL_SPECS = {
    "logistic_regression": {
        "use_scaling": True,
        "default_params": {
            "C": 1.0,
            "solver": "liblinear",
            "max_iter": 1000,
        },
        "param_grid": {
            "C": [0.01, 0.1, 1.0, 10.0],
            "solver": ["liblinear"],
        },
    },
    "random_forest": {
        "use_scaling": False,
        "default_params": {
            "n_estimators": 200,
            "max_depth": None,
            "min_samples_leaf": 1,
            "max_features": "sqrt",
            "random_state": 42,
        },
        "param_grid": {
            "n_estimators": [200, 500],
            "max_depth": [None, 4, 8],
            "min_samples_leaf": [1, 3, 5],
            "max_features": ["sqrt", "log2"],
        },
    },
    "gradient_boosting": {
        "use_scaling": False,
        "default_params": {
            "learning_rate": 0.05,
            "max_depth": None,
            "max_iter": 200,
            "random_state": 42,
        },
        "param_grid": {
            "learning_rate": [0.03, 0.05, 0.1],
            "max_depth": [None, 3, 5],
            "max_iter": [100, 200],
        },
    },
}


def _merge_spec(base: dict, updates: dict | None) -> dict:
    merged = deepcopy(base)

    for key, value in (updates or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key].update(value)
        else:
            merged[key] = deepcopy(value)

    return merged


def normalize_model_spec(name: str, spec: dict | None = None) -> dict:
    if name not in DEFAULT_MODEL_SPECS and spec is None:
        raise ValueError(f"Unknown model: {name}")

    base = DEFAULT_MODEL_SPECS.get(name, {"use_scaling": True, "default_params": {}, "param_grid": {}})
    merged = _merge_spec(base, spec)
    merged.setdefault("use_scaling", True)
    merged.setdefault("default_params", {})
    merged.setdefault("param_grid", {})
    return merged


def build_logistic_regression(**params):
    return LogisticRegression(**params)


def build_random_forest(**params):
    return RandomForestClassifier(**params)


def build_gradient_boosting(**params):
    return HistGradientBoostingClassifier(**params)


def build_model(name: str, params: dict | None = None, model_spec: dict | None = None):
    config = normalize_model_spec(name, model_spec)
    merged_params = dict(config.get("default_params", {}))
    merged_params.update(params or {})

    if name == "logistic_regression":
        return build_logistic_regression(**merged_params)
    if name == "random_forest":
        return build_random_forest(**merged_params)
    if name == "gradient_boosting":
        return build_gradient_boosting(**merged_params)
    raise ValueError(f"Unknown model: {name}")


def get_model_param_grid(name: str, model_spec: dict | None = None) -> dict:
    config = normalize_model_spec(name, model_spec)
    return {
        f"model__{param_name}": values
        for param_name, values in config.get("param_grid", {}).items()
    }


def model_uses_scaling(name: str, model_spec: dict | None = None) -> bool:
    config = normalize_model_spec(name, model_spec)
    return bool(config.get("use_scaling", True))
