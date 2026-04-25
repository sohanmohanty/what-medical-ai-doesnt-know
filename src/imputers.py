"""Reusable imputer builders for the final project layout."""

from copy import deepcopy

from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer


DEFAULT_IMPUTER_SPECS = {
    "simple": {
        "method": "simple",
        "default_params": {
            "strategy_numeric": "median",
            "strategy_binary": "most_frequent",
            "strategy_categorical": "most_frequent",
            "add_missing_indicators": False,
        },
        "param_grid": {},
    },
    "simple_plus_indicators": {
        "method": "simple",
        "default_params": {
            "strategy_numeric": "median",
            "strategy_binary": "most_frequent",
            "strategy_categorical": "most_frequent",
            "add_missing_indicators": True,
        },
        "param_grid": {},
    },
    "knn": {
        "method": "knn",
        "default_params": {
            "n_neighbors": 5,
            "weights": "uniform",
            "strategy_binary": "most_frequent",
            "strategy_categorical": "most_frequent",
            "add_missing_indicators": False,
        },
        "param_grid": {
            "n_neighbors": [3, 5, 7],
            "weights": ["uniform"],
        },
    },
    "iterative": {
        "method": "iterative",
        "default_params": {
            "max_iter": 10,
            "random_state": 42,
            "strategy_binary": "most_frequent",
            "strategy_categorical": "most_frequent",
            "add_missing_indicators": False,
        },
        "param_grid": {},
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


def normalize_imputer_spec(name: str, spec: dict | None = None) -> dict:
    if name not in DEFAULT_IMPUTER_SPECS and spec is None:
        raise ValueError(f"Unknown imputer: {name}")

    base = DEFAULT_IMPUTER_SPECS.get(
        name,
        {
            "method": name,
            "default_params": {},
            "param_grid": {},
        },
    )
    merged = _merge_spec(base, spec)
    merged.setdefault("method", name)
    merged.setdefault("default_params", {})
    merged.setdefault("param_grid", {})
    return merged


def build_simple_imputer(strategy: str = "median", add_indicator: bool = False):
    return SimpleImputer(strategy=strategy, add_indicator=add_indicator)


def build_knn_imputer(
    n_neighbors: int = 5,
    weights: str = "uniform",
    add_indicator: bool = False,
):
    return KNNImputer(
        n_neighbors=n_neighbors,
        weights=weights,
        add_indicator=add_indicator,
    )


def build_iterative_imputer(
    max_iter: int = 10,
    random_state: int = 42,
    add_indicator: bool = False,
):
    return IterativeImputer(
        max_iter=max_iter,
        random_state=random_state,
        add_indicator=add_indicator,
    )


def build_numeric_imputer(name: str, spec: dict | None = None):
    config = normalize_imputer_spec(name, spec)
    params = config.get("default_params", {})
    method = config["method"]
    add_indicator = bool(params.get("add_missing_indicators", False))

    if method == "simple":
        return build_simple_imputer(
            strategy=params.get("strategy_numeric", "median"),
            add_indicator=add_indicator,
        )
    if method == "knn":
        return build_knn_imputer(
            n_neighbors=int(params.get("n_neighbors", 5)),
            weights=params.get("weights", "uniform"),
            add_indicator=add_indicator,
        )
    if method == "iterative":
        return build_iterative_imputer(
            max_iter=int(params.get("max_iter", 10)),
            random_state=int(params.get("random_state", 42)),
            add_indicator=add_indicator,
        )

    raise ValueError(f"Unknown imputer method: {method}")


def build_binary_imputer(name: str, spec: dict | None = None):
    config = normalize_imputer_spec(name, spec)
    params = config.get("default_params", {})
    return build_simple_imputer(
        strategy=params.get("strategy_binary", "most_frequent"),
        add_indicator=bool(params.get("add_missing_indicators", False)),
    )


def build_categorical_imputer(name: str, spec: dict | None = None):
    config = normalize_imputer_spec(name, spec)
    params = config.get("default_params", {})
    return build_simple_imputer(
        strategy=params.get("strategy_categorical", "most_frequent"),
        add_indicator=False,
    )


def get_numeric_imputer_param_grid(name: str, spec: dict | None = None) -> dict:
    config = normalize_imputer_spec(name, spec)
    method = config["method"]

    if method == "simple":
        return {}

    return {
        f"preprocessor__num__imputer__{param_name}": values
        for param_name, values in config.get("param_grid", {}).items()
    }


def build_imputer(name: str, spec: dict | None = None):
    """Backward-compatible alias for numeric imputers."""

    return build_numeric_imputer(name, spec)
