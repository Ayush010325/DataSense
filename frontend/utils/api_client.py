import requests
import streamlit as st

BASE_URL = "https://datasense-backend-wr78.onrender.com"

def get_health() -> bool:
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200 and response.json().get("status") == "ok"
    except Exception:
        return False

def upload_dataset(file, name: str) -> dict:
    url = f"{BASE_URL}/api/v1/datasets/upload"
    files = {"file": (file.name, file.getvalue(), "application/octet-stream")}
    data = {"name": name}
    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error uploading file: {e}")
        return {}

def get_datasets():
    url = f"{BASE_URL}/api/v1/datasets"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching datasets: {e}")
        return []

def get_dataset_analysis(dataset_id: int) -> dict:
    url = f"{BASE_URL}/api/v1/datasets/{dataset_id}/analysis"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching analysis: {e}")
        return {}

def get_dataset_insights(dataset_id: int) -> list:
    url = f"{BASE_URL}/api/v1/datasets/{dataset_id}/insights"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching insights: {e}")
        return []

def get_plottable_columns(dataset_id: int) -> dict:
    url = f"{BASE_URL}/api/v1/charts/plottable_columns/{dataset_id}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching columns: {e}")
        return {}

def get_chart_histogram(dataset_id: int, column: str) -> dict:
    url = f"{BASE_URL}/api/v1/charts/histogram"
    try:
        res = requests.post(url, json={"dataset_id": dataset_id, "column": column})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching histogram: {e}")
        return {}

def get_chart_boxplot(dataset_id: int, column: str) -> dict:
    url = f"{BASE_URL}/api/v1/charts/boxplot"
    try:
        res = requests.post(url, json={"dataset_id": dataset_id, "column": column})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching boxplot: {e}")
        return {}

def get_chart_barplot(dataset_id: int, column_x: str, column_y: str) -> dict:
    url = f"{BASE_URL}/api/v1/charts/barplot"
    try:
        res = requests.post(url, json={"dataset_id": dataset_id, "column_x": column_x, "column_y": column_y})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching barplot: {e}")
        return {}

def get_chart_heatmap(dataset_id: int, columns: list) -> dict:
    url = f"{BASE_URL}/api/v1/charts/heatmap"
    try:
        res = requests.post(url, json={"dataset_id": dataset_id, "columns": columns})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching heatmap: {e}")
        return {}

def get_chart_scatter(dataset_id: int, column_x: str, column_y: str) -> dict:
    url = f"{BASE_URL}/api/v1/charts/scatter"
    try:
        res = requests.post(url, json={"dataset_id": dataset_id, "column_x": column_x, "column_y": column_y})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching scatter: {e}")
        return {}

def get_chart_pie(dataset_id: int, column: str) -> dict:
    url = f"{BASE_URL}/api/v1/charts/pie"
    try:
        res = requests.post(url, json={"dataset_id": dataset_id, "column": column})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching pie chart: {e}")
        return {}

def get_chart_line(dataset_id: int, column_x: str, column_y: str) -> dict:
    url = f"{BASE_URL}/api/v1/charts/line"
    try:
        res = requests.post(url, json={"dataset_id": dataset_id, "column_x": column_x, "column_y": column_y})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching line chart: {e}")
        return {}

def train_experiment(payload: dict) -> dict:
    url = f"{BASE_URL}/api/v1/experiments/train"
    try:
        res = requests.post(url, json=payload)
        if res.status_code != 200:
            st.error(f"Error: {res.json().get('detail', 'Unknown error')}")
            return {}
        return res.json()
    except Exception as e:
        st.error(f"Error training experiment: {e}")
        return {}

def get_experiment(experiment_id: int) -> dict:
    url = f"{BASE_URL}/api/v1/experiments/{experiment_id}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching experiment: {e}")
        return {}

def get_dataset_experiments(dataset_id: int) -> list:
    url = f"{BASE_URL}/api/v1/experiments/dataset/{dataset_id}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching experiments: {e}")
        return []

def predict_experiment(experiment_id: int, payload: dict) -> dict:
    url = f"{BASE_URL}/api/v1/experiments/{experiment_id}/predict"
    try:
        res = requests.post(url, json=payload)
        if res.status_code != 200:
            st.error(f"Prediction Error: {res.json().get('detail', 'Unknown error')}")
            return {}
        return res.json()
    except Exception as e:
        st.error(f"Error running prediction: {e}")
        return {}
