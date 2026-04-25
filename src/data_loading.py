"""Top-level dataset loading entry points for the final project layout."""

from src.data.loaders import load_statlog_heart, load_wdbc

__all__ = [
    "load_wdbc",
    "load_statlog_heart",
]
