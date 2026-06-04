import pandas as pd
import numpy as np
import os
from io import BytesIO
from typing import Dict, Any
from functools import lru_cache


@lru_cache(maxsize=16)
def _cached_load(file_path: str, mtime: float) -> pd.DataFrame:
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and XLSX are allowed.")


def load_dataset_file(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    mtime = os.path.getmtime(file_path)
    return _cached_load(file_path, mtime)


def load_dataset_bytes(filename: str, file_data: bytes) -> pd.DataFrame:
    buffer = BytesIO(file_data)
    if filename.endswith('.csv'):
        return pd.read_csv(buffer)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(buffer)
    else:
        raise ValueError("Unsupported file format. Only CSV and XLSX are allowed.")


def load_dataset_record(dataset) -> pd.DataFrame:
    if getattr(dataset, "file_data", None):
        return load_dataset_bytes(dataset.filename, dataset.file_data)
    if getattr(dataset, "file_path", None):
        return load_dataset_file(dataset.file_path)
    raise ValueError("Dataset file content is missing.")


def detect_column_type(series: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(series):
        if set(series.dropna().unique()) <= {0, 1}:
            return "boolean"
        return "numeric"
    elif pd.api.types.is_bool_dtype(series):
        return "boolean"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
        unique_count = series.nunique()
        total_count = len(series)
        if unique_count > 0 and (unique_count / total_count < 0.05 or unique_count < 20):
            return "categorical"
        return "text"
    return "unknown"

def analyze_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    row_count, col_count = df.shape

    if row_count == 0:
        return {
            "dataset_shape": {"row_count": 0, "column_count": col_count},
            "missing_summary": {"total_missing_cells": 0, "missing_by_column": {}},
            "duplicates_summary": {"duplicate_row_count": 0},
            "column_types": {},
            "numeric_summary": {},
            "categorical_summary": {},
            "text_summary": {},
            "datetime_summary": {},
            "column_metadata_rows": []
        }

    missing_by_col = df.isnull().sum().to_dict()
    total_missing = int(df.isnull().sum().sum())
    duplicates_count = int(df.duplicated().sum())

    column_types = {}
    numeric_summary = {}
    categorical_summary = {}
    text_summary = {}
    datetime_summary = {}
    metadata_rows = []

    for col in df.columns:
        col_type = detect_column_type(df[col])
        column_types[col] = col_type

        missing_count = int(missing_by_col[col])
        missing_ratio = float(missing_count / row_count) if row_count > 0 else 0.0
        unique_count = int(df[col].nunique(dropna=True))

        metadata_rows.append({
            "column_name": col,
            "data_type": col_type,
            "missing_count": missing_count,
            "missing_ratio": missing_ratio,
            "unique_count": unique_count,
            "is_nullable": missing_count > 0
        })

        if col_type == "numeric":
            s = df[col].dropna()
            if len(s) > 0:
                q1 = s.quantile(0.25)
                q3 = s.quantile(0.75)
                iqr = q3 - q1
                outliers = int(((s < (q1 - 1.5 * iqr)) | (s > (q3 + 1.5 * iqr))).sum())

                numeric_summary[col] = {
                    "mean": float(s.mean()),
                    "median": float(s.median()),
                    "std": float(s.std()) if len(s) > 1 else 0.0,
                    "min": float(s.min()),
                    "max": float(s.max()),
                    "skewness": float(s.skew()) if len(s) > 2 else 0.0,
                    "outlier_count": outliers
                }
        elif col_type == "categorical":
            s = df[col].dropna()
            if len(s) > 0:
                top_vals = s.value_counts().head(5).to_dict()
                categorical_summary[col] = {
                    "unique_count": unique_count,
                    "top_values": {str(k): int(v) for k, v in top_vals.items()}
                }
        elif col_type == "text":
            s = df[col].dropna().astype(str)
            if len(s) > 0:
                lengths = s.str.len()
                empty_count = int((s.str.strip() == "").sum())
                text_summary[col] = {
                    "avg_length": float(lengths.mean()),
                    "max_length": int(lengths.max()),
                    "empty_string_count": empty_count
                }
        elif col_type == "datetime":
            s = pd.to_datetime(df[col], errors='coerce').dropna()
            if len(s) > 0:
                datetime_summary[col] = {
                    "min_date": s.min().isoformat(),
                    "max_date": s.max().isoformat()
                }

    def clean_dict(d):
        if isinstance(d, dict):
            return {k: clean_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [clean_dict(v) for v in d]
        elif isinstance(d, float) and (np.isnan(d) or np.isinf(d)):
            return None
        return d

    result = {
        "dataset_shape": {"row_count": row_count, "column_count": col_count},
        "missing_summary": {"total_missing_cells": total_missing, "missing_by_column": {str(k): int(v) for k, v in missing_by_col.items()}},
        "duplicates_summary": {"duplicate_row_count": duplicates_count},
        "column_types": column_types,
        "numeric_summary": clean_dict(numeric_summary),
        "categorical_summary": clean_dict(categorical_summary),
        "text_summary": clean_dict(text_summary),
        "datetime_summary": clean_dict(datetime_summary),
        "column_metadata_rows": metadata_rows
    }
    return result
