# DataSense Lab

DataSense Lab is a smart data understanding and experimentation platform built for data analysts and ML students. It provides an intuitive interface for uploading datasets, automatically generating insights, performing visual data exploration, and running quick machine learning experiments.

## Features

* **File Upload**: Easily ingest CSV and Excel datasets.
* **Dataset Profiling**: Automatically infer data types, summary statistics, missing values, and outliers.
* **Smart Insights Engine**: A rule-based system that flags dataset issues like extreme skewness, high missing ratios, or potential ID columns.
* **Visual Explorer**: Dynamically generate histograms, boxplots, bar charts, heatmaps, and scatter plots.
* **ML Sandbox**: Build automated machine learning pipelines with preprocessing logic for classification, regression, and clustering tasks using `scikit-learn`.
* **Experiment History**: Save and track your trained models and their metrics.
* **What-If Lab**: Reload a trained model pipeline and provide custom inputs to see real-time predictions based on your saved experiment.

## Architecture & Technology Stack

The project strictly follows a decoupled API-first architecture:
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
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head      # Run database migrations
uvicorn app.main:app --reload
```
The FastAPI server will run at `http://localhost:8000`.

### 3. Frontend Setup
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
The Streamlit app will run at `http://localhost:8501`.

## Usage

1. Open the Streamlit dashboard.
2. Go to the **Upload** page to ingest a dataset.
3. Review the **Overview** and **Insights** to understand your data.
4. Go to the **Visual Explorer** to plot graphs interactively.
5. Enter the **ML Sandbox** to define a task, select features, and train a model.
6. Visit the **Experiment History** to review past models.
7. Open the **What-If Lab** to predict outcomes using hypothetical input values.
