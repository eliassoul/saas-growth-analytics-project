import streamlit as st

def render_kpi_cards(kpis):
    """
    render_kpi_cards(kpis)
    ----------------------

    Renders a set of six KPI cards in a Streamlit app, displaying key SaaS metrics with 
    values and optional deltas.

    Parameters
    ----------
    kpis : dict
        A dictionary containing the following keys and their corresponding numeric values:
        - "mrr": Monthly Recurring Revenue
        - "mrr_delta": change in MRR since previous period
        - "growth_rate": overall growth rate (0-1)
        - "growth_delta": change in growth rate since previous period
        - "churn_rate": customer churn rate (0-1)
        - "nrr": Net Revenue Retention rate (0-1)
        - "ltv": Lifetime Value in dollars
        - "customers": number of active customers

    Returns
    -------
    None
        Renders KPI metrics directly in Streamlit columns.

    Details
    -------
    1. Creates six equally spaced columns in a single row using Streamlit.
    2. Displays the following KPIs in each column:
    - Column 1: MRR with delta
    - Column 2: Growth Rate with delta
    - Column 3: Churn Rate
    - Column 4: Net Revenue Retention (NRR)
    - Column 5: Lifetime Value (LTV)
    - Column 6: Active Customers
    3. Formats numeric values for currency, percentage, or integer display as appropriate.
    4. Designed to provide an at-a-glance summary of key SaaS performance metrics.

    Example
    -------
    >>> kpis = {
    ...     "mrr": 12000,
    ...     "mrr_delta": 1500,
    ...     "growth_rate": 0.12,
    ...     "growth_delta": 0.03,
    ...     "churn_rate": 0.05,
    ...     "nrr": 0.98,
    ...     "ltv": 450,
    ...     "customers": 1250
    ... }
    >>> render_kpi_cards(kpis)
    """
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        "MRR",
        f"${kpis['mrr']:,.0f}",
        delta=f"${kpis['mrr_delta']:,.0f}"
    )

    col2.metric(
        "Growth Rate",
        f"{kpis['growth_rate']:.2%}",
        delta=f"{kpis['growth_delta']:.2%}"
    )

    col3.metric(
        "Churn Rate",
        f"{kpis['churn_rate']:.2%}"
    )

    col4.metric(
        "NRR",
        f"{kpis['nrr']:.2%}"
    )

    col5.metric(
        "LTV",
        f"${kpis['ltv']:,.0f}"
    )

    col6.metric(
        "Active Customers",
        f"{kpis['customers']:,.0f}"
    )