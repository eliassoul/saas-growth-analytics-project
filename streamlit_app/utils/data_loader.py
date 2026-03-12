import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data
def load_executive_metrics() -> pd.DataFrame:
    """
    load_executive_metrics()
    ----------------------

    Loads the preprocessed executive metrics dataset from the local project directory, 
    caches the result, and returns it as a sorted pandas DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the executive metrics with at least the following columns:
        - "year_month": datetime values representing the month
        - Other relevant metrics used across the dashboard (e.g., "mrr", "active_customers", "churn_rate", "expansion_revenue")

    Details
    -------
    1. Resolves the dataset path relative to the project root (two levels above the current file) 
    under `data/processed/executive_metrics.csv`.
    2. Validates that the dataset exists; raises `FileNotFoundError` if missing.
    3. Loads the CSV into a pandas DataFrame.
    4. Converts "year_month" to datetime and sorts the DataFrame chronologically.
    5. Resets the index to provide a clean integer index.
    6. Decorated with `@st.cache_data` to cache the loaded DataFrame for improved performance 
    across Streamlit reruns.

    Example
    -------
    >>> import pandas as pd
    >>> df = load_executive_metrics()
    >>> df.head()
    """

    # -------------------------------------------------
    # PATH RESOLUTION
    # -------------------------------------------------

    project_root = Path(__file__).resolve().parents[2]

    data_path = project_root / "data" / "processed" / "executive_metrics.csv"

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at expected location: {data_path}"
        )

    # -------------------------------------------------
    # LOAD DATA
    # -------------------------------------------------

    df = pd.read_csv(data_path)

    # -------------------------------------------------
    # DATA PREPARATION
    # -------------------------------------------------

    df["year_month"] = pd.to_datetime(df["year_month"])

    df = df.sort_values("year_month")

    df = df.reset_index(drop=True)

    return df