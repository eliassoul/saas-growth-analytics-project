import streamlit as st
from utils.data_loader import load_executive_metrics
from utils.metrics import compute_kpis
from components.kpi_cards import render_kpi_cards
from components.charts import (
    customer_growth_chart,
    customer_base_chart,
    customer_churn_chart,
    new_customers_chart,
    arpu_chart,
    expansion_revenue_chart
)

def render_growth():
    """
    render_growth()
    ----------------------

    Renders the Growth Analysis page in a Streamlit app, providing an overview of customer 
    growth, acquisition, ARPU, and expansion revenue trends, along with KPIs and strategic insights.

    Parameters
    ----------
    None
        The function internally loads the required dataset using `load_executive_metrics()` 
        and computes KPIs via `compute_kpis()`.

    Returns
    -------
    None
        Renders interactive Streamlit components directly:
        - Page header and caption
        - KPI cards
        - Primary and secondary charts visualizing customer growth and related metrics
        - Strategic insight panel

    Details
    -------
    1. Displays a page header ("Growth Analysis") and a caption describing the focus of the analysis.
    2. Loads executive metrics dataset internally.
    3. Computes key KPIs and renders them as metric cards using `render_kpi_cards`.
    4. Plots primary chart:
    - Customer Growth Rate Trend
    5. Plots secondary charts in a two-column layout:
    - Column 1: Active Customer Base, Customer Churn Rate Trend
    - Column 2: New Customers per Month, ARPU Trend
    6. Plots Expansion Revenue Trend as a standalone chart.
    7. Provides a strategic insight section highlighting growth trends, churn considerations, 
    ARPU optimization, and expansion revenue opportunities.
    8. Uses Streamlit dividers and subheaders to structure content visually.

    Example
    -------
    >>> import streamlit as st
    >>> render_growth()
    """

    st.title("Growth Analysis")

    st.caption(
        "Analysis of customer growth trends, new customer acquisition, ARPU, and expansion revenue over time."
        )

    df = load_executive_metrics()

    kpis = compute_kpis(df)
    render_kpi_cards(kpis)

    st.divider()

    st.subheader("Customer Growth Rate Trend")
    st.plotly_chart(customer_growth_chart(df), use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Active Customer Base")
        st.plotly_chart(customer_base_chart(df), use_container_width=True)

        st.subheader("Customer Churn Rate Trend")
        st.plotly_chart(customer_churn_chart(df), use_container_width=True)

    with col2:
        st.subheader("New Customers per Month")
        st.plotly_chart(new_customers_chart(df), use_container_width=True)

        st.subheader("ARPU Trend")
        st.plotly_chart(arpu_chart(df), use_container_width=True)

    st.subheader("Expansion Revenue Trend")
    st.plotly_chart(expansion_revenue_chart(df), use_container_width=True)

    st.divider()

    st.subheader("Strategic Insight")
    st.info(
        "While the active customer base continues to grow, the dynamics of growth are " \
        "gradually shifting. Customer acquisition appears to be stabilizing, while periodic " \
        "churn spikes introduce volatility in net customer growth. At the same time, increasing " \
        "ARPU and rising expansion revenue suggest that revenue growth is progressively relying " \
        "more on existing customers rather than purely on new acquisitions. This shift highlights " \
        "the growing importance of retention and account expansion as core levers for sustainable " \
        "SaaS growth."
    )