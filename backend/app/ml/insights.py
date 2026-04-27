from typing import List, Dict, Any

def generate_insights(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    insights = []
    
    shape = analysis.get("dataset_shape", {})
    rows = shape.get("row_count", 0)
    cols = shape.get("column_count", 0)
    
    size_msg = "small"
    if rows > 100000:
        size_msg = "large"
    elif rows > 10000:
        size_msg = "medium"
    insights.append({
        "message": f"Dataset is {size_msg} with {rows} rows and {cols} columns.",
        "severity": "info",
        "category": "distribution"
    })
    
    duplicates = analysis.get("duplicates_summary", {}).get("duplicate_row_count", 0)
    if duplicates > 0:
        insights.append({
            "message": f"Found {duplicates} duplicate rows in the dataset.",
            "severity": "warning",
            "category": "duplicates"
        })
    else:
        insights.append({
            "message": "No duplicate rows found.",
            "severity": "success",
            "category": "duplicates"
        })
        
    metadata_rows = analysis.get("column_metadata_rows", [])
    numeric_summary = analysis.get("numeric_summary", {})
    
    for col_data in metadata_rows:
        col = col_data["column_name"]
        missing_ratio = col_data["missing_ratio"]
        unique_count = col_data["unique_count"]
        
        if missing_ratio > 0.3:
            insights.append({
                "message": f"Column '{col}' has {missing_ratio:.1%} missing values.",
                "severity": "warning",
                "category": "missing_values"
            })
            
        if unique_count == rows and rows > 0:
            insights.append({
                "message": f"Column '{col}' has unique values for every row. It might be an ID column.",
                "severity": "info",
                "category": "distribution"
            })
            
        if missing_ratio == 0 and unique_count > 1 and unique_count < rows:
            insights.append({
                "message": f"Column '{col}' is complete with no missing values.",
                "severity": "success",
                "category": "column_quality"
            })
            
    for col, stats in numeric_summary.items():
        skew = stats.get("skewness", 0.0)
        if skew and abs(skew) > 1.0:
            dir = "positive" if skew > 0 else "negative"
            insights.append({
                "message": f"Column '{col}' has strong {dir} skewness ({skew:.2f}).",
                "severity": "warning",
                "category": "skewness"
            })
            
        outliers = stats.get("outlier_count", 0)
        if outliers > 0 and rows > 0:
            outlier_ratio = outliers / rows
            if outlier_ratio > 0.05:
                insights.append({
                    "message": f"Column '{col}' has a high number of outliers ({outliers} rows, {outlier_ratio:.1%}).",
                    "severity": "warning",
                    "category": "outliers"
                })

    return insights
