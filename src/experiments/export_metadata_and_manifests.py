"""Export guide-aligned dataset schemas and repeated-CV manifests."""

import json
from pathlib import Path

from src.data.schemas import save_schema
from src.data.splits import make_repeated_outer_cv_splits
from src.data_loading import load_statlog_heart, load_wdbc
from src.project_config import load_project_configs, merge_schema_with_feature_types


LOADER_REGISTRY = {
    "load_wdbc": load_wdbc,
    "load_statlog_heart": load_statlog_heart,
}


def save_fold_manifest(dataset_name, X, y, out_path, cv_config):
    splits = make_repeated_outer_cv_splits(
        X,
        y,
        n_splits=int(cv_config.get("outer_folds", 5)),
        n_repeats=int(cv_config.get("repeats", 1)),
        random_state=42,
    )

    manifest = {
        "dataset": dataset_name,
        "protocol": cv_config.get("protocol", "repeated_stratified_k_fold"),
        "outer_folds": int(cv_config.get("outer_folds", 5)),
        "repeats": int(cv_config.get("repeats", 1)),
        "inner_folds": int(cv_config.get("inner_folds", 3)),
        "hyperparameter_tuning": bool(cv_config.get("hyperparameter_tuning", False)),
        "tuning_metric": cv_config.get("tuning_metric", "roc_auc"),
        "splits": [
            {
                "repeat": int(split["repeat"]),
                "fold": int(split["fold"]),
                "train_size": int(len(split["train_idx"])),
                "test_size": int(len(split["test_idx"])),
            }
            for split in splits
        ],
    }

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)


def main():
    configs = load_project_configs()
    datasets = configs["datasets"]
    cv_config = configs["experiment"]["cv"]

    for dataset_name, dataset_spec in datasets.items():
        loader_name = dataset_spec["loader_name"]
        X, y, raw_schema = LOADER_REGISTRY[loader_name]()
        schema = merge_schema_with_feature_types(raw_schema, dataset_spec.get("feature_types"), all_columns=X.columns)

        schema_payload = {
            "dataset": dataset_name,
            "n_rows": int(X.shape[0]),
            "n_features": int(X.shape[1]),
            "feature_names": list(X.columns),
            "target_dtype": str(y.dtype),
            "task_type": dataset_spec.get("task_type", "binary_classification"),
            **schema,
        }
        save_schema(schema_payload, dataset_spec["schema_output"])

        save_fold_manifest(
            dataset_name=dataset_name,
            X=X,
            y=y,
            out_path=f"results/manifests/folds_{dataset_name}.json",
            cv_config=cv_config,
        )

    protocol_path = Path("results/manifests/repeated_cv_protocol.json")
    protocol_path.parent.mkdir(parents=True, exist_ok=True)
    with open(protocol_path, "w", encoding="utf-8") as handle:
        json.dump(cv_config, handle, indent=2)

    print("Saved guide-aligned dataset schemas and repeated-CV manifests.")


if __name__ == "__main__":
    main()
