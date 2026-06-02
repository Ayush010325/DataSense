import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.crud.dataset import get_dataset
from app.crud.column_metadata import get_columns_for_dataset
from app.ml.analyzer import load_dataset_file

def _load_df(db: Session, dataset_id: int) -> pd.DataFrame:
    dataset = get_dataset(db, dataset_id)
    if not dataset:
        raise ValueError("Dataset not found")
    return load_dataset_file(dataset.file_path)

def _sample_df(df: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if len(df) > max_rows:
        return df.sample(n=max_rows, random_state=42)
    return df

def get_plottable_columns(db: Session, dataset_id: int) -> dict:
    columns = get_columns_for_dataset(db, dataset_id)
    res = {"numeric": [], "categorical": [], "datetime": []}
    for col in columns:
        if col.data_type == "numeric":
            res["numeric"].append(col.column_name)
        elif col.data_type in ["categorical", "boolean"]:
            res["categorical"].append(col.column_name)
        elif col.data_type == "text" and col.unique_count < 50:
            res["categorical"].append(col.column_name)
        elif col.data_type == "datetime":
            res["datetime"].append(col.column_name)
    return res

def get_chart_data_for_distribution(dataset_id: int, db: Session, column: str, max_rows: int = 10000) -> dict:
    df = _load_df(db, dataset_id)
    if column not in df.columns:
        raise ValueError(f"Column {column} not found")

    col_type = "numeric" if pd.api.types.is_numeric_dtype(df[column]) else "categorical"
    df_sample = _sample_df(df, max_rows).dropna(subset=[column])

    values = df_sample[column].tolist()
    if col_type == "numeric":
        values = [float(x) for x in values]
    else:
        values = [str(x) for x in values]

    return {"column_name": column, "values": values, "type": col_type}

def get_chart_data_for_boxplot(dataset_id: int, db: Session, column: str, max_rows: int = 10000) -> dict:
    df = _load_df(db, dataset_id)
    if column not in df.columns:
        raise ValueError(f"Column {column} not found")

    df[column] = pd.to_numeric(df[column], errors='coerce')
    df_sample = _sample_df(df, max_rows).dropna(subset=[column])
    values = [float(x) for x in df_sample[column].tolist()]
    return {"column_name": column, "values": values}

def get_chart_data_for_barplot(dataset_id: int, db: Session, column_x: str, column_y: str, max_rows: int = 10000) -> dict:
    df = _load_df(db, dataset_id)
    if column_x not in df.columns or column_y not in df.columns:
        raise ValueError("Column not found")

    df[column_y] = pd.to_numeric(df[column_y], errors='coerce')
    df_clean = df.dropna(subset=[column_x, column_y])
    grouped = df_clean.groupby(column_x)[column_y].mean().reset_index()
    grouped = grouped.sort_values(by=column_y, ascending=False).head(50)

    x_labels = [str(x) for x in grouped[column_x].tolist()]
    values = [float(x) for x in grouped[column_y].tolist()]
    return {"x_labels": x_labels, "values": values}

def get_chart_data_for_heatmap(dataset_id: int, db: Session, columns: list[str], max_rows: int = 10000) -> dict:
    df = _load_df(db, dataset_id)
    valid_cols = [c for c in columns if c in df.columns]
    if len(valid_cols) < 2:
        return {"column_names": valid_cols, "data": []}

    for c in valid_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df_sample = _sample_df(df, max_rows)[valid_cols].dropna()
    corr = df_sample.corr().replace({np.nan: 0})

    return {
        "column_names": corr.columns.tolist(),
        "data": corr.values.tolist()
    }

def get_chart_data_for_scatter(dataset_id: int, db: Session, column_x: str, column_y: str, max_rows: int = 10000) -> dict:
    df = _load_df(db, dataset_id)
    if column_x not in df.columns or column_y not in df.columns:
        raise ValueError("Column not found")

    df[column_x] = pd.to_numeric(df[column_x], errors='coerce')
    df[column_y] = pd.to_numeric(df[column_y], errors='coerce')
    df_sample = _sample_df(df, max_rows).dropna(subset=[column_x, column_y])

    x_vals = [float(x) for x in df_sample[column_x].tolist()]
    y_vals = [float(y) for y in df_sample[column_y].tolist()]

    return {
        "x": x_vals,
        "y": y_vals,
        "column_x": column_x,
        "column_y": column_y
    }

def get_chart_data_for_pie(dataset_id: int, db: Session, column: str, max_rows: int = 10000) -> dict:
    df = _load_df(db, dataset_id)
    if column not in df.columns:
        raise ValueError(f"Column {column} not found")

    df_sample = _sample_df(df, max_rows).dropna(subset=[column])
    counts = df_sample[column].value_counts().head(20)

    labels = [str(k) for k in counts.index.tolist()]
    values = [int(v) for v in counts.values.tolist()]

    return {"labels": labels, "values": values}

def get_chart_data_for_line(dataset_id: int, db: Session, column_x: str, column_y: str, max_rows: int = 10000) -> dict:
    df = _load_df(db, dataset_id)
    if column_x not in df.columns or column_y not in df.columns:
        raise ValueError("Column not found")

    df[column_y] = pd.to_numeric(df[column_y], errors='coerce')
    df_clean = df.dropna(subset=[column_x, column_y])
    grouped = df_clean.groupby(column_x)[column_y].mean().reset_index()
    grouped = grouped.sort_values(by=column_x).head(1000)

    x_labels = [str(x) for x in grouped[column_x].tolist()]
    values = [float(x) for x in grouped[column_y].tolist()]

    return {
        "x_labels": x_labels,
        "values": values,
        "column_x": column_x,
        "column_y": column_y
    }
