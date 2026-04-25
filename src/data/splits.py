from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold


def make_outer_cv_splits(X, y, n_splits=5, random_state=42):
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    return list(cv.split(X, y))


def make_repeated_outer_cv_splits(
    X,
    y,
    n_splits=5,
    n_repeats=5,
    random_state=42,
):
    cv = RepeatedStratifiedKFold(
        n_splits=n_splits,
        n_repeats=n_repeats,
        random_state=random_state,
    )

    splits = []
    for split_idx, (train_idx, test_idx) in enumerate(cv.split(X, y)):
        repeat_idx = split_idx // n_splits
        fold_idx = split_idx % n_splits
        splits.append(
            {
                "repeat": repeat_idx,
                "fold": fold_idx,
                "train_idx": train_idx,
                "test_idx": test_idx,
            }
        )

    return splits


def make_inner_cv(n_splits=3, random_state=42):
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
