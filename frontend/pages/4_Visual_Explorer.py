import math
import streamlit as st
import pandas as pd
import altair as alt
from utils.api_client import (
    get_plottable_columns, get_chart_histogram, get_chart_boxplot,
    get_chart_barplot, get_chart_heatmap, get_chart_scatter,
    get_chart_pie, get_chart_line
)

st.set_page_config(page_title="Visual Explorer", layout="wide")
st.title("Visual Explorer")

# ── Guard ───────────────────────────────────────────────────────────────────
if "dataset_id" not in st.session_state:
    st.warning("Upload or select a dataset first.")
    st.stop()

dataset_id = st.session_state["dataset_id"]

plottable = get_plottable_columns(dataset_id)
if not plottable:
    st.error("Could not load columns for plotting. Open Overview first, then try again.")
    st.stop()

num_cols  = plottable.get("numeric", [])
cat_cols  = plottable.get("categorical", [])
dt_cols   = plottable.get("datetime", [])
x_axis_cols = num_cols + cat_cols + dt_cols

# ── Available chart types ───────────────────────────────────────────────────
chart_options = []
if num_cols or cat_cols:
    chart_options.append("Distribution (Histogram)")
if num_cols:
    chart_options.extend(["Boxplot", "Violin Plot"])
if cat_cols and num_cols:
    chart_options.append("Barplot")
if cat_cols:
    chart_options.append("Pie Chart")
if x_axis_cols and num_cols:
    chart_options.append("Line Chart")
if len(num_cols) > 1:
    chart_options.extend(["Heatmap (Correlation)", "Scatter Plot"])

if not chart_options:
    st.warning("This dataset does not have columns that can be plotted yet.")
    st.stop()

chart_type = st.selectbox("Chart type", chart_options)
st.divider()

# ── Helpers ─────────────────────────────────────────────────────────────────
def clean_numeric(lst):
    return [v for v in lst
            if v is not None
            and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))]


# ── Charts ──────────────────────────────────────────────────────────────────

if chart_type == "Distribution (Histogram)":
    all_cols = num_cols + cat_cols
    col = st.selectbox("Column", all_cols)
    if col:
        with st.spinner("Loading data..."):
            data = get_chart_histogram(dataset_id, col)

        if not data:
            st.warning("No data returned from API.")
        elif data.get("type") == "numeric":
            # ── Numeric: use Streamlit native histogram via Altair
            values = clean_numeric(data.get("values", []))
            if not values:
                st.warning("No usable numeric values in this column.")
            else:
                df_v = pd.DataFrame({col: values})
                unique_count = df_v[col].nunique()
                if unique_count <= 20:
                    # Few unique integers → count bar chart
                    df_cnt = df_v[col].value_counts().sort_index().reset_index()
                    df_cnt.columns = ["value", "count"]
                    df_cnt["value"] = df_cnt["value"].astype(str)
                    chart = (
                        alt.Chart(df_cnt)
                        .mark_bar(color="#4C9BE8")
                        .encode(
                            x=alt.X("value:N", title=col, sort=None),
                            y=alt.Y("count:Q", title="Count"),
                            tooltip=["value", "count"],
                        )
                        .properties(title=f"Distribution of {col}", height=400)
                    )
                else:
                    chart = (
                        alt.Chart(df_v)
                        .mark_bar(color="#4C9BE8")
                        .encode(
                            x=alt.X(f"{col}:Q", bin=alt.Bin(maxbins=40), title=col),
                            y=alt.Y("count():Q", title="Count"),
                            tooltip=[alt.Tooltip(f"{col}:Q", bin=True), "count()"],
                        )
                        .properties(title=f"Distribution of {col}", height=400)
                    )
                st.altair_chart(chart, use_container_width=True)

        else:
            # ── Categorical: backend already aggregated — just plot labels/counts
            labels = data.get("labels", [])
            counts = data.get("counts", [])
            if not labels:
                st.warning("No usable values found in this column.")
            else:
                df_cnt = pd.DataFrame({"category": labels, "count": counts})
                chart = (
                    alt.Chart(df_cnt)
                    .mark_bar(color="#4C9BE8")
                    .encode(
                        x=alt.X("category:N", title=col,
                                sort=alt.SortField("count", order="descending")),
                        y=alt.Y("count:Q", title="Count"),
                        tooltip=["category", "count"],
                    )
                    .properties(title=f"Distribution of {col}", height=400)
                )
                st.altair_chart(chart, use_container_width=True)

elif chart_type == "Boxplot":
    col = st.selectbox("Numeric column", num_cols)
    if col:
        with st.spinner("Loading data..."):
            data = get_chart_boxplot(dataset_id, col)
        values = clean_numeric(data.get("values", [])) if data else []
        if not values:
            st.warning("No usable numeric values in this column.")
        else:
            df_v = pd.DataFrame({col: values})
            chart = (
                alt.Chart(df_v)
                .mark_boxplot(color="#4C9BE8", size=60)
                .encode(y=alt.Y(f"{col}:Q", title=col))
                .properties(title=f"Boxplot of {col}", height=400)
            )
            st.altair_chart(chart, use_container_width=True)

elif chart_type == "Violin Plot":
    col = st.selectbox("Numeric column", num_cols)
    if col:
        with st.spinner("Loading data..."):
            data = get_chart_boxplot(dataset_id, col)
        values = clean_numeric(data.get("values", [])) if data else []
        if not values:
            st.warning("No usable numeric values in this column.")
        else:
            # Altair doesn't have native violin — use density + area
            df_v = pd.DataFrame({col: values})
            chart = (
                alt.Chart(df_v)
                .transform_density(col, as_=[col, "density"])
                .mark_area(orient="horizontal", opacity=0.6, color="#4C9BE8")
                .encode(
                    y=alt.Y(f"{col}:Q", title=col),
                    x=alt.X("density:Q", title="Density", stack="center",
                            impute=None, axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True)),
                )
                .properties(title=f"Violin Plot of {col}", height=400)
            )
            st.altair_chart(chart, use_container_width=True)

elif chart_type == "Barplot":
    c1, c2 = st.columns(2)
    with c1:
        cat_col = st.selectbox("X axis (category)", cat_cols)
    with c2:
        num_col = st.selectbox("Y axis (numeric)", num_cols)

    if cat_col and num_col:
        with st.spinner("Loading data..."):
            data = get_chart_barplot(dataset_id, cat_col, num_col)
        if data and data.get("x_labels"):
            x_labels = data["x_labels"]
            values   = clean_numeric(data["values"])
            n = min(len(x_labels), len(values))
            df_p = pd.DataFrame({cat_col: x_labels[:n], num_col: values[:n]})
            chart = (
                alt.Chart(df_p)
                .mark_bar(color="#4C9BE8")
                .encode(
                    x=alt.X(f"{cat_col}:N", sort="-y", title=cat_col),
                    y=alt.Y(f"{num_col}:Q", title=f"Mean {num_col}"),
                    tooltip=[cat_col, num_col],
                )
                .properties(title=f"Mean of {num_col} by {cat_col}", height=400)
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Not enough usable data to plot.")

elif chart_type == "Pie Chart":
    col = st.selectbox("Category column", cat_cols)
    if col:
        with st.spinner("Loading data..."):
            data = get_chart_pie(dataset_id, col)
        if data and data.get("labels"):
            labels = data["labels"]
            values = clean_numeric(data["values"])
            n = min(len(labels), len(values))
            df_p = pd.DataFrame({"category": labels[:n], "count": values[:n]})
            chart = (
                alt.Chart(df_p)
                .mark_arc()
                .encode(
                    theta=alt.Theta("count:Q"),
                    color=alt.Color("category:N", legend=alt.Legend(title=col)),
                    tooltip=["category", "count"],
                )
                .properties(title=f"Composition of {col}", height=400)
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Not enough usable data to plot.")

elif chart_type == "Line Chart":
    c1, c2 = st.columns(2)
    with c1:
        x_col = st.selectbox("X axis", x_axis_cols)
    with c2:
        y_col = st.selectbox("Y axis (numeric)", num_cols)

    if x_col and y_col:
        with st.spinner("Loading data..."):
            data = get_chart_line(dataset_id, x_col, y_col)
        if data and data.get("x_labels"):
            x_labels = data["x_labels"]
            values   = clean_numeric(data["values"])
            n = min(len(x_labels), len(values))
            df_p = pd.DataFrame({x_col: x_labels[:n], y_col: values[:n]})
            chart = (
                alt.Chart(df_p)
                .mark_line(point=True, color="#4C9BE8")
                .encode(
                    x=alt.X(f"{x_col}:N", title=x_col, sort=None),
                    y=alt.Y(f"{y_col}:Q", title=f"Mean {y_col}"),
                    tooltip=[x_col, y_col],
                )
                .properties(title=f"Mean of {y_col} over {x_col}", height=400)
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Not enough usable data to plot.")

elif chart_type == "Heatmap (Correlation)":
    default_sel = num_cols[:5] if len(num_cols) > 5 else num_cols
    selected_cols = st.multiselect("Columns to compare", num_cols, default=default_sel)
    if len(selected_cols) < 2:
        st.info("Select at least two numeric columns.")
    else:
        with st.spinner("Loading data..."):
            data = get_chart_heatmap(dataset_id, selected_cols)
        if data and data.get("data"):
            col_names = data["column_names"]
            matrix    = data["data"]
            # Flatten to long form for Altair
            rows = []
            for i, r in enumerate(col_names):
                for j, c in enumerate(col_names):
                    rows.append({"row": r, "col": c, "corr": round(matrix[i][j], 3)})
            df_heat = pd.DataFrame(rows)
            chart = (
                alt.Chart(df_heat)
                .mark_rect()
                .encode(
                    x=alt.X("col:N", title=""),
                    y=alt.Y("row:N", title=""),
                    color=alt.Color("corr:Q",
                                    scale=alt.Scale(scheme="redblue", domain=[-1, 1]),
                                    title="r"),
                    tooltip=["row", "col", "corr"],
                )
                .properties(title="Correlation Matrix", height=400)
            )
            text = (
                alt.Chart(df_heat)
                .mark_text(fontSize=11)
                .encode(
                    x="col:N",
                    y="row:N",
                    text=alt.Text("corr:Q", format=".2f"),
                    color=alt.condition(
                        alt.datum.corr > 0.5,
                        alt.value("white"),
                        alt.value("black"),
                    ),
                )
            )
            st.altair_chart(chart + text, use_container_width=True)
        else:
            st.warning("Not enough usable data to plot.")

elif chart_type == "Scatter Plot":
    c1, c2 = st.columns(2)
    with c1:
        x_col = st.selectbox("X axis", num_cols)
    with c2:
        remaining = [c for c in num_cols if c != x_col]
        y_col = st.selectbox("Y axis", remaining if remaining else num_cols)

    if x_col and y_col:
        with st.spinner("Loading data..."):
            data = get_chart_scatter(dataset_id, x_col, y_col)
        if data and data.get("x"):
            x_vals = clean_numeric(data["x"])
            y_vals = clean_numeric(data["y"])
            n = min(len(x_vals), len(y_vals))
            if n == 0:
                st.warning("No usable data points found.")
            else:
                df_p = pd.DataFrame({x_col: x_vals[:n], y_col: y_vals[:n]})
                chart = (
                    alt.Chart(df_p)
                    .mark_circle(opacity=0.5, color="#4C9BE8")
                    .encode(
                        x=alt.X(f"{x_col}:Q", title=x_col),
                        y=alt.Y(f"{y_col}:Q", title=y_col),
                        tooltip=[x_col, y_col],
                    )
                    .properties(title=f"Scatter: {x_col} vs {y_col}", height=400)
                )
                st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Not enough usable data to plot.")
