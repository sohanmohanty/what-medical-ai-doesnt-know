import numpy as np
import pandas as pd

from src.data.loaders import load_statlog_heart, load_wdbc
from src.preprocessing import build_preprocessor


def test_wdbc_schema_is_all_numeric():
    X, y, schema = load_wdbc()

    assert X.shape[1] == 30
    assert len(y) == len(X)
    assert len(schema["numeric_columns"]) == 30
    assert schema["binary_columns"] == []
    assert schema["categorical_columns"] == []


def test_statlog_schema_has_mixed_feature_types():
    X, y, schema = load_statlog_heart()

    assert X.shape[1] == 13
    assert len(y) == len(X)
    assert len(schema["numeric_columns"]) == 6
    assert len(schema["binary_columns"]) == 3
    assert len(schema["categorical_columns"]) == 4
    assert set(schema["numeric_columns"]) | set(schema["binary_columns"]) | set(schema["categorical_columns"]) == set(X.columns)


def test_preprocessor_fit_transform_is_stable_for_mixed_types():
    train = pd.DataFrame(
        {
            "age": [41.0, np.nan, 55.0, 63.0],
            "sex": [1, 0, np.nan, 1],
            "chest": ["typical", "asymptomatic", "typical", "non_anginal"],
        }
    )
    test = pd.DataFrame(
        {
            "age": [47.0, np.nan],
            "sex": [1, 0],
            "chest": ["atypical", "typical"],
        }
    )
    schema = {
        "numeric_columns": ["age"],
        "binary_columns": ["sex"],
        "categorical_columns": ["chest"],
    }

    preprocessor = build_preprocessor(schema, scale_numeric=True, imputer_name="simple")
    train_matrix = preprocessor.fit_transform(train)
    test_matrix = preprocessor.transform(test)

    assert train_matrix.shape[0] == len(train)
    assert test_matrix.shape[0] == len(test)
    assert train_matrix.shape[1] == test_matrix.shape[1]
    assert train_matrix.shape[1] >= 4
