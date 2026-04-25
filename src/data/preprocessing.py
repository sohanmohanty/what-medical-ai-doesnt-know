from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.imputers import (
    build_binary_imputer,
    build_categorical_imputer,
    build_numeric_imputer,
)


def build_preprocessor(
    schema,
    scale_numeric=True,
    imputer_name="simple",
    imputer_spec=None,
):
    numeric_columns = schema.get("numeric_columns", schema.get("numeric_features", []))
    binary_columns = schema.get("binary_columns", schema.get("binary_features", []))
    categorical_columns = schema.get("categorical_columns", schema.get("categorical_features", []))

    transformers = []

    if numeric_columns:
        numeric_steps = [
            ("imputer", build_numeric_imputer(imputer_name, imputer_spec)),
        ]
        if scale_numeric:
            numeric_steps.append(("scaler", StandardScaler()))

        numeric_transformer = Pipeline(steps=numeric_steps)
        transformers.append(("num", numeric_transformer, numeric_columns))

    if binary_columns:
        binary_transformer = Pipeline(
            steps=[
                ("imputer", build_binary_imputer(imputer_name, imputer_spec)),
            ]
        )
        transformers.append(("bin", binary_transformer, binary_columns))

    if categorical_columns:
        categorical_transformer = Pipeline(
            steps=[
                ("imputer", build_categorical_imputer(imputer_name, imputer_spec)),
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]
        )
        transformers.append(("cat", categorical_transformer, categorical_columns))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
    )

    return preprocessor
