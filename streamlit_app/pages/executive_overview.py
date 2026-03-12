import streamlit as st
import pandas as pd

from utils.metrics import compute_kpis
from components.kpi_cards import render_kpi_cards
from components.charts import (
    mrr_chart,
    churn_chart,
    customer_base_chart,
    customer_growth_chart,
    expansion_revenue_chart
    
)

def render_overview(df: pd.DataFrame):
    """
    render_overview(df)
    ----------------------

    Renders the Executive Overview page in a Streamlit app, providing a high-level view 
    of revenue performance, customer dynamics, and growth sustainability for a B2B SaaS platform.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing the necessary columns to compute KPIs and generate charts, 
        typically including:
        - "year_month": time periods (datetime or string)
        - "mrr": monthly recurring revenue
        - "active_customers": active customer counts
        - "churn_rate": customer churn rate
        - "expansion_revenue": expansion revenue
        - Additional columns required by `compute_kpis` and related chart functions

    Returns
    -------
    None
        Renders interactive Streamlit components directly:
        - Page title and caption
        - KPI cards for key metrics
        - Revenue performance line chart
        - Analytical grid with growth, retention, churn, and expansion revenue charts
        - Strategic insight panel with high-level observations

    Details
    -------
    1. Displays the page title ("Executive Overview"), a company caption, and a descriptive markdown.
    2. Computes key KPIs using the `compute_kpis` function and renders them via `render_kpi_cards`.
    3. Plots the main revenue trend using `mrr_chart`.
    4. Builds an analytical grid of four charts:
    - Customer growth rate
    - Active customer base
    - Churn rate
    - Expansion revenue
    5. Provides strategic insight with an info panel highlighting revenue trends, churn patterns, 
    and implications for long-term growth sustainability.
    6. Uses Streamlit dividers and subheaders to organize content visually.

    Example
    -------
    >>> import pandas as pd
    >>> import streamlit as st
    >>> df = pd.DataFrame({
    ...     "year_month": pd.to_datetime(["2024-01", "2024-02", "2024-03"]),
    ...     "mrr": [10000, 12000, 12500],
    ...     "active_customers": [100, 120, 125],
    ...     "churn_rate": [0.04, 0.06, 0.05],
    ...     "expansion_revenue": [500, 700, 650]
    ... })
    >>> render_overview(df)
    """

    st.title("Executive Overview")

    st.caption(
        "Nexora Analytics — B2B SaaS platform providing automated financial "
        "reporting solutions for SMEs across the US and Europe."
    )

    st.markdown(
        "This dashboard provides a high-level view of the company's revenue "
        "performance, customer dynamics, and long-term growth sustainability."
    )

    st.divider()

    kpis = compute_kpis(df)

    render_kpi_cards(kpis)

    st.divider()

    st.subheader("Revenue Performance")

    st.plotly_chart(
        mrr_chart(df),
        use_container_width=True
    )

    st.divider()

    st.subheader("Growth and Retention Dynamics")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(customer_growth_chart(df), use_container_width=True)

    with col2:
        st.plotly_chart(customer_base_chart(df), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(churn_chart(df), use_container_width=True)

    with col4:
        st.plotly_chart(expansion_revenue_chart(df), use_container_width=True)

    st.divider()

    st.subheader("Strategic Insight")

    st.info(
    """
    **Revenue growth remains positive but shows signs of deceleration.**

    During the early phase, the company experienced strong expansion driven by
    rapid customer acquisition and low churn levels. However, recent months show
    a noticeable increase in churn and a gradual decline in net revenue retention.

    Although expansion revenue partially offsets customer losses, the current
    trend suggests that long-term growth sustainability may be at risk.

    **Key strategic implication:**  
    Improving customer retention and strengthening product value for higher-tier
    plans may be critical to sustain long-term revenue growth.
    """
    )