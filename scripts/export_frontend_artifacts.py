"""Export richer frontend artifacts from canonical benchmark outputs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_INPUT = ROOT / "results" / "metrics" / "paper_core_summary.csv"
PREDICTIONS_INPUT = ROOT / "results" / "predictions" / "paper_core_predictions.csv"
BASELINE_PREDICTIONS_INPUT = ROOT / "results" / "predictions" / "baseline_predictions.csv"
DEFAULT_OUTPUT = ROOT / "artifacts" / "frontend" / "paper_core_explorer.json"

DATASET_METADATA = {
    "wdbc": {
        "label": "Breast Tumor Classification",
        "shortLabel": "WDBC",
        "audienceSummary": (
            "A cleaner benchmark where models often stay strong overall, which makes calibration drift "
            "especially important to notice."
        ),
        "difficulty": "more separable",
        "exampleFeatures": [
            "mean radius",
            "mean texture",
            "mean perimeter",
            "worst texture",
            "worst perimeter",
        ],
    },
    "statlog_heart": {
        "label": "Heart Disease Classification",
        "shortLabel": "Statlog Heart",
        "audienceSummary": (
            "A smaller, noisier benchmark where missingness exposes fragility more quickly and trust signals "
            "are easier to see."
        ),
        "difficulty": "more fragile",
        "exampleFeatures": [
            "age",
            "resting blood pressure",
            "serum cholestoral",
            "maximum heart rate achieved",
            "exercise induced angina",
        ],
    },
}

MODEL_METADATA = {
    "logistic_regression": {
        "label": "Logistic Regression",
        "audienceSummary": "Often easier to reason about and sometimes gentler on calibration-sensitive metrics.",
    },
    "random_forest": {
        "label": "Random Forest",
        "audienceSummary": "Often the steadiest overall core model in the canonical benchmark.",
    },
    "gradient_boosting": {
        "label": "Gradient Boosting",
        "audienceSummary": "Competitive when conditions are mild, but more brittle in harsher missing-data settings.",
    },
}

MECHANISM_METADATA = {
    "mcar": {
        "label": "MCAR",
        "longLabel": "Missing Completely At Random",
        "audienceSummary": "Values disappear without depending on the patient state in the present simulation.",
    },
    "mar": {
        "label": "MAR",
        "longLabel": "Missing At Random",
        "audienceSummary": "Missingness depends on other observed variables, not purely by chance.",
    },
    "mnar": {
        "label": "MNAR",
        "longLabel": "Missing Not At Random",
        "audienceSummary": "Missingness is tied to the value being hidden in the present construction.",
    },
}

DATASET_ORDER = ["wdbc", "statlog_heart"]
MODEL_ORDER = ["logistic_regression", "random_forest", "gradient_boosting"]
MECHANISM_ORDER = ["mcar", "mar", "mnar"]
RATE_ORDER = [0.1, 0.2, 0.3, 0.5]


def _round(value: float, digits: int = 6) -> float:
    return round(float(value), digits)


def _round_optional(value: float | None, digits: int = 6):
    if value is None or pd.isna(value):
        return None
    return round(float(value), digits)


def _scenario_id(dataset: str, model: str, mechanism: str, rate: float) -> str:
    return f"{dataset}__{model}__{mechanism}__{str(rate).replace('.', 'p')}"


def _severity_label(actual_rate: float) -> str:
    if actual_rate < 0.13:
        return "mild"
    if actual_rate < 0.26:
        return "moderate"
    if actual_rate < 0.41:
        return "heavy"
    return "severe"


def _severity_summary(actual_rate: float) -> str:
    label = _severity_label(actual_rate)

    if label == "mild":
        return "Only a limited share of the input is missing, so the trust question is more about subtle drift than collapse."
    if label == "moderate":
        return "A meaningful share of the input is missing, so visitors should expect probability quality to matter more visibly."
    if label == "heavy":
        return "The model is operating with a substantial information gap, so caution should become part of the story."
    return "Nearly half the relevant input is missing, which is the kind of setting where confident language can become misleading."


def _trust_band(score: int) -> str:
    if score >= 78:
        return "stable"
    if score >= 50:
        return "caution"
    return "fragile"


def _score_breakdown(row: pd.Series) -> dict:
    roc_penalty = min(max(-float(row["mean_roc_auc_change"]), 0.0) / 0.08, 1.0)
    brier_penalty = min(max(float(row["mean_brier_change"]), 0.0) / 0.05, 1.0)
    ece_penalty = min(max(float(row["mean_ece_change"]), 0.0) / 0.06, 1.0)
    missingness_penalty = min(max(float(row["mean_test_actual_rate"]), 0.0) / 0.5, 1.0)

    ranking = int(round((1.0 - roc_penalty) * 100))
    calibration = int(round((1.0 - (0.45 * brier_penalty + 0.55 * ece_penalty)) * 100))
    completeness = int(round((1.0 - 0.75 * missingness_penalty) * 100))
    trust = int(round(0.4 * ranking + 0.4 * calibration + 0.2 * completeness))

    return {
        "trust": max(0, min(100, trust)),
        "ranking": max(0, min(100, ranking)),
        "calibration": max(0, min(100, calibration)),
        "completeness": max(0, min(100, completeness)),
    }


def _status_from_delta(metric: str, delta: float) -> str:
    thresholds = {
        "roc_auc": (-0.005, -0.02),
        "brier": (0.005, 0.02),
        "ece": (0.005, 0.02),
        "accuracy": (-0.01, -0.04),
    }
    soft, hard = thresholds[metric]

    if metric in {"roc_auc", "accuracy"}:
        if delta <= hard:
            return "warning"
        if delta <= soft:
            return "drifting"
        return "holding"

    if delta >= hard:
        return "warning"
    if delta >= soft:
        return "drifting"
    return "holding"


def _metric_cards(row: pd.Series) -> dict:
    return {
        "rocAuc": {
            "value": _round(row["mean_roc_auc"]),
            "cleanValue": _round(row["mean_clean_roc_auc"]),
            "delta": _round(row["mean_roc_auc_change"]),
            "status": _status_from_delta("roc_auc", float(row["mean_roc_auc_change"])),
        },
        "accuracy": {
            "value": _round(row["mean_accuracy"]),
            "cleanValue": _round(row["mean_clean_accuracy"]),
            "delta": _round(row["mean_accuracy_change"]),
            "status": _status_from_delta("accuracy", float(row["mean_accuracy_change"])),
        },
        "brier": {
            "value": _round(row["mean_brier"]),
            "cleanValue": _round(row["mean_clean_brier"]),
            "delta": _round(row["mean_brier_change"]),
            "status": _status_from_delta("brier", float(row["mean_brier_change"])),
        },
        "ece": {
            "value": _round(row["mean_ece"]),
            "cleanValue": _round(row["mean_clean_ece"]),
            "delta": _round(row["mean_ece_change"]),
            "status": _status_from_delta("ece", float(row["mean_ece_change"])),
        },
    }


def _build_reliability_profile(df: pd.DataFrame, n_bins: int = 10) -> dict | None:
    if df.empty:
        return None

    y_true = df["y_true"].to_numpy()
    y_prob = np.clip(df["y_prob"].to_numpy(), 0.0, 1.0)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    total = len(df)

    bins = []
    weighted_gap = 0.0
    max_gap = 0.0

    for index in range(n_bins):
        left = float(edges[index])
        right = float(edges[index + 1])
        if index == n_bins - 1:
            mask = (y_prob >= left) & (y_prob <= right)
        else:
            mask = (y_prob >= left) & (y_prob < right)

        count = int(np.sum(mask))
        if count:
            mean_pred = float(np.mean(y_prob[mask]))
            frac_positive = float(np.mean(y_true[mask]))
            abs_gap = abs(frac_positive - mean_pred)
            weighted_gap += abs_gap * (count / total)
            max_gap = max(max_gap, abs_gap)
        else:
            mean_pred = None
            frac_positive = None
            abs_gap = None

        bins.append(
            {
                "left": _round(left, 3),
                "right": _round(right, 3),
                "midpoint": _round((left + right) / 2.0, 3),
                "count": count,
                "meanPred": _round_optional(mean_pred),
                "fracPositive": _round_optional(frac_positive),
                "absGap": _round_optional(abs_gap),
            }
        )

    return {
        "pooledCount": total,
        "observedPositiveRate": _round(float(np.mean(y_true))),
        "meanPredictedRisk": _round(float(np.mean(y_prob))),
        "meanAbsGap": _round(weighted_gap),
        "maxAbsGap": _round(max_gap),
        "bins": bins,
    }


def _build_reliability_lookup(predictions: pd.DataFrame) -> dict:
    lookup = {}
    group_cols = ["dataset", "model", "mechanism", "rate"]
    for keys, group_df in predictions.groupby(group_cols, sort=False):
        dataset, model, mechanism, rate = keys
        lookup[_scenario_id(dataset, model, mechanism, rate)] = _build_reliability_profile(group_df)
    return lookup


def _build_baseline_reliability_lookup(predictions: pd.DataFrame) -> dict:
    lookup = {}
    if predictions.empty:
        return lookup

    group_cols = ["dataset", "model"]
    for keys, group_df in predictions.groupby(group_cols, sort=False):
        dataset, model = keys
        lookup[f"{dataset}__{model}"] = _build_reliability_profile(group_df)
    return lookup


def _highlight_summary(df: pd.DataFrame) -> dict:
    lowest = df.sort_values(["trustScore", "mean_ece_change", "mean_brier_change"], ascending=[True, False, False]).iloc[0]
    highest = df.sort_values(["trustScore", "mean_roc_auc"], ascending=[False, False]).iloc[0]
    ece_peak = df.sort_values("mean_ece_change", ascending=False).iloc[0]
    roc_drop = df.sort_values("mean_roc_auc_change", ascending=True).iloc[0]

    return {
        "mostFragileScenario": {
            "dataset": lowest["dataset"],
            "model": lowest["model"],
            "mechanism": lowest["mechanism"],
            "rate": _round(lowest["rate"], 2),
            "trustScore": int(lowest["trustScore"]),
        },
        "mostStableScenario": {
            "dataset": highest["dataset"],
            "model": highest["model"],
            "mechanism": highest["mechanism"],
            "rate": _round(highest["rate"], 2),
            "trustScore": int(highest["trustScore"]),
        },
        "largestCalibrationDrift": {
            "dataset": ece_peak["dataset"],
            "model": ece_peak["model"],
            "mechanism": ece_peak["mechanism"],
            "rate": _round(ece_peak["rate"], 2),
            "meanEceChange": _round(ece_peak["mean_ece_change"]),
        },
        "largestRankingDrop": {
            "dataset": roc_drop["dataset"],
            "model": roc_drop["model"],
            "mechanism": roc_drop["mechanism"],
            "rate": _round(roc_drop["rate"], 2),
            "meanRocAucChange": _round(roc_drop["mean_roc_auc_change"]),
        },
    }


def _sort_summary(df: pd.DataFrame) -> pd.DataFrame:
    order_map = {
        **{name: index for index, name in enumerate(DATASET_ORDER)},
        **{name: index for index, name in enumerate(MODEL_ORDER)},
        **{name: index for index, name in enumerate(MECHANISM_ORDER)},
        **{rate: index for index, rate in enumerate(RATE_ORDER)},
    }

    dataset_rank = df["dataset"].map(order_map)
    model_rank = df["model"].map(order_map)
    mechanism_rank = df["mechanism"].map(order_map)
    rate_rank = df["rate"].map(order_map)

    return (
        df.assign(
            _dataset_rank=dataset_rank,
            _model_rank=model_rank,
            _mechanism_rank=mechanism_rank,
            _rate_rank=rate_rank,
        )
        .sort_values(["_dataset_rank", "_model_rank", "_mechanism_rank", "_rate_rank"])
        .drop(columns=["_dataset_rank", "_model_rank", "_mechanism_rank", "_rate_rank"])
    )


def _build_comparison_slices(df: pd.DataFrame) -> list[dict]:
    slices = []
    for keys, group_df in df.groupby(["dataset", "mechanism", "rate"], sort=False):
        dataset, mechanism, rate = keys
        ranked = group_df.sort_values(
            ["trustScore", "mean_roc_auc", "mean_brier", "mean_ece"],
            ascending=[False, False, True, True],
        ).copy()
        ranked["rank"] = range(1, len(ranked) + 1)

        slices.append(
            {
                "id": f"{dataset}__{mechanism}__{str(rate).replace('.', 'p')}",
                "dataset": dataset,
                "mechanism": mechanism,
                "rate": _round(rate, 2),
                "bestModel": ranked.iloc[0]["model"],
                "models": [
                    {
                        "model": row["model"],
                        "rank": int(row["rank"]),
                        "trustScore": int(row["trustScore"]),
                        "trustBand": row["trustBand"],
                        "meanRocAuc": _round(row["mean_roc_auc"]),
                        "meanBrier": _round(row["mean_brier"]),
                        "meanEce": _round(row["mean_ece"]),
                        "meanRocAucChange": _round(row["mean_roc_auc_change"]),
                        "meanBrierChange": _round(row["mean_brier_change"]),
                        "meanEceChange": _round(row["mean_ece_change"]),
                    }
                    for _, row in ranked.iterrows()
                ],
            }
        )

    return slices


def build_payload(
    summary_path: Path = SUMMARY_INPUT,
    predictions_path: Path = PREDICTIONS_INPUT,
    baseline_predictions_path: Path = BASELINE_PREDICTIONS_INPUT,
) -> dict:
    summary_df = pd.read_csv(summary_path)
    predictions_df = pd.read_csv(predictions_path)
    baseline_predictions_df = pd.read_csv(baseline_predictions_path) if baseline_predictions_path.exists() else pd.DataFrame()

    summary_df = summary_df.loc[
        (summary_df["regime"] == "clean_train_corrupt_test")
        & (summary_df["imputer"] == "simple")
        & (summary_df["dataset"].isin(DATASET_ORDER))
        & (summary_df["model"].isin(MODEL_ORDER))
        & (summary_df["mechanism"].isin(MECHANISM_ORDER))
    ].copy()

    if summary_df.empty:
        raise RuntimeError(f"No rows available for frontend export from {summary_path}")

    predictions_df = predictions_df.loc[
        (predictions_df["run_name"] == "paper_core")
        & (predictions_df["regime"] == "clean_train_corrupt_test")
        & (predictions_df["imputer"] == "simple")
    ].copy()

    current_reliability_lookup = _build_reliability_lookup(predictions_df)
    baseline_reliability_lookup = _build_baseline_reliability_lookup(baseline_predictions_df)

    score_breakdowns = summary_df.apply(_score_breakdown, axis=1)
    summary_df["trustScore"] = score_breakdowns.map(lambda item: item["trust"])
    summary_df["trustBand"] = summary_df["trustScore"].map(_trust_band)
    summary_df = _sort_summary(summary_df)

    scenarios = []
    for _, row in summary_df.iterrows():
        scenario_id = _scenario_id(row["dataset"], row["model"], row["mechanism"], row["rate"])
        baseline_key = f"{row['dataset']}__{row['model']}"
        scores = _score_breakdown(row)
        actual_rate = float(row["mean_test_actual_rate"])

        scenarios.append(
            {
                "id": scenario_id,
                "dataset": row["dataset"],
                "model": row["model"],
                "mechanism": row["mechanism"],
                "rate": _round(row["rate"], 2),
                "nRuns": int(row["n_runs"]),
                "trustBand": row["trustBand"],
                "trustScore": int(scores["trust"]),
                "stabilityScore": int(scores["trust"]),
                "scoreBreakdown": scores,
                "severity": {
                    "label": _severity_label(actual_rate),
                    "actualRate": _round(actual_rate),
                    "summary": _severity_summary(actual_rate),
                },
                "meanAccuracy": _round(row["mean_accuracy"]),
                "meanRocAuc": _round(row["mean_roc_auc"]),
                "meanBrier": _round(row["mean_brier"]),
                "meanEce": _round(row["mean_ece"]),
                "meanAccuracyChange": _round(row["mean_accuracy_change"]),
                "meanRocAucChange": _round(row["mean_roc_auc_change"]),
                "meanBrierChange": _round(row["mean_brier_change"]),
                "meanEceChange": _round(row["mean_ece_change"]),
                "meanTrainActualRate": _round(row["mean_train_actual_rate"]),
                "meanTestActualRate": _round(actual_rate),
                "metricCards": _metric_cards(row),
                "baseline": {
                    "meanAccuracy": _round(row["mean_clean_accuracy"]),
                    "meanRocAuc": _round(row["mean_clean_roc_auc"]),
                    "meanBrier": _round(row["mean_clean_brier"]),
                    "meanEce": _round(row["mean_clean_ece"]),
                },
                "reliability": current_reliability_lookup.get(scenario_id),
                "baselineReliability": baseline_reliability_lookup.get(baseline_key),
            }
        )

    payload = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "runName": "paper_core",
            "summaryPath": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
            "predictionsPath": str(predictions_path.relative_to(ROOT)).replace("\\", "/"),
            "baselinePredictionsPath": (
                str(baseline_predictions_path.relative_to(ROOT)).replace("\\", "/")
                if baseline_predictions_path.exists()
                else None
            ),
            "regime": "clean_train_corrupt_test",
            "imputer": "simple",
            "calibrationBins": 10,
            "reliabilityAggregation": "Pooled across saved cross-validation test predictions.",
        },
        "defaultSelection": {
            "dataset": "wdbc",
            "model": "logistic_regression",
            "mechanism": "mcar",
            "rate": 0.2,
        },
        "datasets": [
            {"id": dataset_id, **DATASET_METADATA[dataset_id]}
            for dataset_id in DATASET_ORDER
            if dataset_id in summary_df["dataset"].unique()
        ],
        "models": [
            {"id": model_id, **MODEL_METADATA[model_id]}
            for model_id in MODEL_ORDER
            if model_id in summary_df["model"].unique()
        ],
        "mechanisms": [
            {"id": mechanism_id, **MECHANISM_METADATA[mechanism_id]}
            for mechanism_id in MECHANISM_ORDER
            if mechanism_id in summary_df["mechanism"].unique()
        ],
        "rates": RATE_ORDER,
        "highlights": _highlight_summary(summary_df),
        "comparisonSlices": _build_comparison_slices(summary_df),
        "scenarios": scenarios,
    }
    return payload


def main():
    payload = build_payload()
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved frontend artifact to {DEFAULT_OUTPUT}")


if __name__ == "__main__":
    main()
