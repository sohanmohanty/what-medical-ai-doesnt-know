from pathlib import Path

import pytest
import yaml

from src.project_config import load_project_configs, override_output_paths, select_named_entries


def test_load_project_configs_has_expected_sections():
    configs = load_project_configs()

    assert set(configs.keys()) == {"datasets", "models", "imputers", "experiment"}
    assert "wdbc" in configs["datasets"]
    assert "statlog_heart" in configs["datasets"]
    assert "logistic_regression" in configs["models"]
    assert "simple" in configs["imputers"]


def test_override_output_paths_namespaces_noncanonical_runs():
    configs = load_project_configs()
    outputs = override_output_paths(configs["experiment"], run_name="paper_preview")

    assert Path(outputs["metrics_path"]).as_posix() == "results/user_runs/paper_preview/metrics.csv"
    assert Path(outputs["summary_path"]).as_posix() == "results/user_runs/paper_preview/summary.csv"
    assert Path(outputs["predictions_path"]).as_posix() == "results/user_runs/paper_preview/predictions.csv"
    assert Path(outputs["manifest_path"]).as_posix() == "results/user_runs/paper_preview/run_manifest.json"
    assert Path(outputs["masks_dir"]).as_posix() == "results/user_runs/paper_preview/masks"
    assert Path(outputs["figures_dir"]).as_posix() == "figures/user_runs/paper_preview"


def test_override_output_paths_can_route_sample_runs():
    configs = load_project_configs()
    outputs = override_output_paths(
        configs["experiment"],
        run_name="smoke_test",
        output_namespace="sample",
    )

    assert Path(outputs["metrics_path"]).as_posix() == "results/samples/smoke_test/metrics.csv"
    assert Path(outputs["summary_path"]).as_posix() == "results/samples/smoke_test/summary.csv"
    assert Path(outputs["predictions_path"]).as_posix() == "results/samples/smoke_test/predictions.csv"
    assert Path(outputs["manifest_path"]).as_posix() == "results/samples/smoke_test/run_manifest.json"
    assert Path(outputs["masks_dir"]).as_posix() == "results/samples/smoke_test/masks"
    assert Path(outputs["figures_dir"]).as_posix() == "figures/samples/smoke_test"


def test_select_named_entries_rejects_unknown_names():
    with pytest.raises(ValueError, match="Unknown models"):
        select_named_entries({"a": 1}, ["a", "b"], "models")


def test_load_project_configs_can_fall_back_to_base_files(tmp_path: Path):
    override_dir = tmp_path / "paper_core"
    override_dir.mkdir()
    (override_dir / "experiments.yaml").write_text(
        yaml.safe_dump(
            {
                "experiment": {
                    "name": "paper_core_test",
                    "datasets": ["wdbc"],
                    "models": ["logistic_regression"],
                    "imputers": ["simple"],
                }
            }
        ),
        encoding="utf-8",
    )

    configs = load_project_configs(override_dir)

    assert configs["experiment"]["name"] == "paper_core_test"
    assert "wdbc" in configs["datasets"]
    assert "simple" in configs["imputers"]
