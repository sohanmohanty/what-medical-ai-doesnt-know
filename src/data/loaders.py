from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer
from ucimlrepo import fetch_ucirepo


WDBC_NUMERIC_COLUMNS = [
    "mean radius",
    "mean texture",
    "mean perimeter",
    "mean area",
    "mean smoothness",
    "mean compactness",
    "mean concavity",
    "mean concave points",
    "mean symmetry",
    "mean fractal dimension",
    "radius error",
    "texture error",
    "perimeter error",
    "area error",
    "smoothness error",
    "compactness error",
    "concavity error",
    "concave points error",
    "symmetry error",
    "fractal dimension error",
    "worst radius",
    "worst texture",
    "worst perimeter",
    "worst area",
    "worst smoothness",
    "worst compactness",
    "worst concavity",
    "worst concave points",
    "worst symmetry",
    "worst fractal dimension",
]

STATLOG_NUMERIC_COLUMNS = [
    "age",
    "resting_blood_pressure",
    "serum_cholestoral",
    "maximum_heart_rate_achieved",
    "oldpeak",
    "number_of_major_vessels",
]

STATLOG_BINARY_COLUMNS = [
    "sex",
    "fasting_blood_sugar",
    "exercise_induced_angina",
]

STATLOG_CATEGORICAL_COLUMNS = [
    "chest",
    "resting_electrocardiographic_results",
    "slope",
    "thal",
]


def _build_schema(
    X: pd.DataFrame,
    numeric_columns=None,
    binary_columns=None,
    categorical_columns=None,
) -> dict:
    numeric_columns = list(numeric_columns or [])
    binary_columns = list(binary_columns or [])
    categorical_columns = list(categorical_columns or [])

    assigned = set(numeric_columns) | set(binary_columns) | set(categorical_columns)
    remainder = [column for column in X.columns if column not in assigned]
    if remainder:
        numeric_columns.extend(remainder)

    return {
        "numeric_columns": numeric_columns,
        "binary_columns": binary_columns,
        "categorical_columns": categorical_columns,
        "numeric_features": numeric_columns,
        "binary_features": binary_columns,
        "categorical_features": categorical_columns,
    }


def load_wdbc():
    cache_dir = Path("data/raw")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "wdbc.csv"

    if cache_path.exists():
        df = pd.read_csv(cache_path)
    else:
        data = load_breast_cancer(as_frame=True)
        df = data.data.copy()
        df["target"] = data.target.copy()
        df.to_csv(cache_path, index=False)

    X = df.drop(columns=["target"]).copy()
    y = df["target"].astype(int).copy()
    schema = _build_schema(X, numeric_columns=WDBC_NUMERIC_COLUMNS)

    return X, y, schema


def load_statlog_heart():
    cache_dir = Path("data/raw")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "statlog_heart_cached.csv"

    if cache_path.exists():
        df = pd.read_csv(cache_path)
    else:
        dataset = fetch_ucirepo(id=145)
        X = dataset.data.features.copy()
        y = dataset.data.targets.copy()

        if isinstance(y, pd.DataFrame):
            y = y.iloc[:, 0]

        df = X.copy()
        df["target"] = y
        df.to_csv(cache_path, index=False)

    X = df.drop(columns=["target"]).copy()
    y = df["target"].copy()

    if not pd.api.types.is_numeric_dtype(y):
        y = (
            y.astype(str)
            .str.strip()
            .str.lower()
            .map({"absent": 0, "present": 1})
        )

    if y.isna().any():
        raise ValueError(f"Unexpected target values: {df['target'].drop_duplicates().tolist()}")

    y = y.astype(int)
    schema = _build_schema(
        X,
        numeric_columns=STATLOG_NUMERIC_COLUMNS,
        binary_columns=STATLOG_BINARY_COLUMNS,
        categorical_columns=STATLOG_CATEGORICAL_COLUMNS,
    )

    return X, y, schema
