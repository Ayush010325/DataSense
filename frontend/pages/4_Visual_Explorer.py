import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import (
    get_plottable_columns, get_chart_histogram, get_chart_boxplot,
    get_chart_barplot, get_chart_heatmap, get_chart_scatter,
    get_chart_pie, get_chart_line
)

st.set_page_config(page_title="Visual Explorer", layout="wide")
st.title("Visual Explorer")

if "dataset_id" not in st.session_state:
    st.warning("Upload or select a dataset first.")
    st.stop()

dataset_id = st.session_state["dataset_id"]

plottable = get_plottable_columns(dataset_id)
if not plottable:
    st.error("I could not load columns for plotting. Open Overview first, then try again.")
    st.stop()

num_cols = plottable.get("numeric", [])
cat_cols = plottable.get("categorical", [])
dt_cols = plottable.get("datetime", [])

chart_type = st.selectbox(
    "Chart type",
    ["Distribution (Histogram)", "Boxplot", "Violin Plot", "Barplot", "Pie Chart", "Line Chart", "Heatmap (Correlation)", "Scatter Plot"]
)

st.divider()

if chart_type == "Distribution (Histogram)":
    all_cols = num_cols + cat_cols
    col = st.selectbox("Column", all_cols)
    if st.button("Build chart") and col:
        with st.spinner("Building chart..."):
            data = get_chart_histogram(dataset_id, col)
            if data and data.get("values"):
                if data["type"] == "numeric":
                    fig = px.histogram(x=data["values"], labels={'x': col}, title=f"Distribution of {col}")
                else:
                    fig = px.histogram(x=data["values"], labels={'x': col}, title=f"Distribution of {col}").update_xaxes(categoryorder="total descending")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("This column does not have enough usable values.")

elif chart_type == "Boxplot":
    col = st.selectbox("Numeric column", num_cols)
    if st.button("Build chart") and col:
        with st.spinner("Building chart..."):
            data = get_chart_boxplot(dataset_id, col)
            if data and data.get("values"):
                df_plot = pd.DataFrame({col: data["values"]})
                fig = px.box(df_plot, y=col, title=f"Boxplot of {col}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("This column does not have enough numeric values.")

elif chart_type == "Violin Plot":
    col = st.selectbox("Numeric column", num_cols)
    if st.button("Build chart") and col:
        with st.spinner("Building chart..."):
            data = get_chart_boxplot(dataset_id, col)
            if data and data.get("values"):
                df_plot = pd.DataFrame({col: data["values"]})
                fig = px.violin(df_plot, y=col, box=True, points="all", title=f"Violin Plot of {col}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("This column does not have enough numeric values.")

elif chart_type == "Barplot":
    col1, col2 = st.columns(2)
    with col1:
        cat_col = st.selectbox("X axis category", cat_cols)
    with col2:
        num_col = st.selectbox("Y axis value", num_cols)

    if st.button("Build chart") and cat_col and num_col:
        with st.spinner("Building chart..."):
            data = get_chart_barplot(dataset_id, cat_col, num_col)
            if data and data.get("x_labels"):
                df_plot = pd.DataFrame({cat_col: data["x_labels"], num_col: data["values"]})
                fig = px.bar(df_plot, x=cat_col, y=num_col, title=f"Barplot: Mean of {num_col} by {cat_col}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("There is not enough usable data to plot this.")

elif chart_type == "Pie Chart":
    col = st.selectbox("Category column", cat_cols)
    if st.button("Build chart") and col:
        with st.spinner("Building chart..."):
            data = get_chart_pie(dataset_id, col)
            if data and data.get("labels"):
                fig = px.pie(names=data["labels"], values=data["values"], title=f"Composition of {col}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("There is not enough usable data to plot this.")

elif chart_type == "Line Chart":
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("X axis", num_cols + cat_cols + dt_cols)
    with col2:
        y_col = st.selectbox("Y axis value", num_cols)

    if st.button("Build chart") and x_col and y_col:
        with st.spinner("Building chart..."):
            data = get_chart_line(dataset_id, x_col, y_col)
            if data and data.get("x_labels"):
                df_plot = pd.DataFrame({x_col: data["x_labels"], y_col: data["values"]})
                fig = px.line(df_plot, x=x_col, y=y_col, markers=True, title=f"Line Chart: Mean of {y_col} over {x_col}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("There is not enough usable data to plot this.")

elif chart_type == "Heatmap (Correlation)":
    selected_cols = st.multiselect("Columns to compare", num_cols, default=num_cols[:5] if len(num_cols) > 5 else num_cols)
    if st.button("Build chart") and len(selected_cols) > 1:
        with st.spinner("Building chart..."):
            data = get_chart_heatmap(dataset_id, selected_cols)
            if data and data.get("data"):
                fig = px.imshow(data["data"], x=data["column_names"], y=data["column_names"], title="Correlation Matrix")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Choose at least two numeric columns with usable values.")

elif chart_type == "Scatter Plot":
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("X axis", num_cols)
    with col2:
        y_col = st.selectbox("Y axis", [c for c in num_cols if c != x_col] if num_cols else [])

    if st.button("Build chart") and x_col and y_col:
        with st.spinner("Building chart..."):
            data = get_chart_scatter(dataset_id, x_col, y_col)
            if data and data.get("x"):
                df_plot = pd.DataFrame({x_col: data["x"], y_col: data["y"]})
                fig = px.scatter(df_plot, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("There is not enough usable data to plot this.")
