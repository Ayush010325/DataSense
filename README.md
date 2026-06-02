# DataSense Lab

DataSense Lab helps you get oriented in a dataset quickly. Upload a CSV or Excel file, review the profile, explore patterns with charts, and run lightweight machine learning experiments from a Streamlit workspace backed by FastAPI.

## Features

* **File upload**: Bring in CSV and Excel datasets.
* **Dataset profile**: Review inferred data types, summary statistics, missing values, duplicates, and outliers.
* **Insights**: Surface practical issues such as skewed columns, high missingness, and likely ID fields.
* **Visual explorer**: Create histograms, boxplots, bar charts, heatmaps, scatter plots, pie charts, and line charts.
* **ML sandbox**: Train quick classification, regression, and clustering experiments with `scikit-learn`.
* **Experiment history**: Revisit saved models and compare their metrics.
* **What-if lab**: Load a saved experiment and try custom inputs to see predictions.

## Architecture & Technology Stack

The app is split into a FastAPI backend and a Streamlit frontend:
* **Backend**: FastAPI
* **Database**: PostgreSQL with SQLAlchemy 2.0 ORM
* **Data Processing**: Pandas, NumPy
* **Machine Learning**: Scikit-Learn
* **Frontend**: Streamlit
* **Visualizations**: Plotly

## Local Setup

### 1. Database
Ensure you have PostgreSQL running locally and create a database named `datasense_db`.
Update your `backend/.env` file with the correct `DATABASE_URL`.

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ../scripts/initialize_db.py
uvicorn app.main:app --reload
```
The FastAPI server will run at `http://localhost:8000`.

### 3. Frontend Setup
```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
The Streamlit app will run at `http://localhost:8501`.

## Usage

1. Open the Streamlit app.
2. Upload a dataset or select one you already added.
3. Review the overview and insights to understand what is in the file.
4. Build charts in the Visual Explorer.
5. Train a quick model in the ML Sandbox.
6. Check past runs in Experiment History.
7. Use the What-If Lab to test new input values against a saved model.
