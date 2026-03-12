import streamlit as st

from components.charts import (
    mrr_chart,
    expansion_revenue_chart,
    new_customers_chart,
    arpu_chart,
    mrr_growth_chart
)

def render_revenue_dynamics(df):
    """
    render_revenue_dynamics(df)
    ----------------------

    Renders the Revenue Dynamics page in a Streamlit app, analyzing revenue growth drivers 
    such as customer acquisition, expansion revenue, ARPU, and overall revenue trajectory.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing the necessary columns for revenue analysis, typically including:
        - "year_month": time periods (datetime or string)
        - "mrr": monthly recurring revenue
        - "active_customers": number of active customers
        - "expansion_revenue": revenue generated from customer expansions
        - "new_customers": monthly new customer counts
        - Additional columns required by chart functions

    Returns
    -------
    None
        Renders interactive Streamlit components directly:
        - Page title and caption
        - Main revenue trend chart
        - Revenue driver charts (MRR growth, expansion revenue, new customers, ARPU)
        - Strategic insight panel

    Details
    -------
    1. Displays the page title ("Revenue Dynamics") and a descriptive caption.
    2. Plots the main revenue trend using `mrr_chart`.
    3. Constructs a grid of revenue driver charts:
    - MRR Growth Rate
    - Expansion Revenue
    - New Customers per Month
    - ARPU Trend
    Arranged in two-column layouts for side-by-side comparison.
    4. Provides a strategic insight section explaining the dynamics of revenue growth, 
    the impact of acquisition stabilization, and the role of expansion revenue.
    5. Highlights the importance of retention strategies and expansion within the existing 
    customer base for sustaining long-term revenue growth.
    6. Uses Streamlit dividers and subheaders for clear visual separation.

    Example
    -------
    >>> import pandas as pd
    >>> import streamlit as st
    >>> df = pd.DataFrame({
    ...     "year_month": pd.to_datetime(["2024-01", "2024-02", "2024-03"]),
    ...     "mrr": [10000, 12000, 12500],
    ...     "active_customers": [100, 120, 125],
    ...     "expansion_revenue": [500, 700, 650],
    ...     "new_customers": [50, 80, 70]
    ... })
    >>> render_revenue_dynamics(df)
    """
    
    st.title("Revenue Dynamics")

    st.caption(
        "Analysis of revenue growth drivers, including customer acquisition, "
        "expansion revenue and overall revenue trajectory."
    )

    st.divider()

    st.subheader("Revenue Trend")

    st.plotly_chart(
        mrr_chart(df),
        use_container_width=True
    )

    st.divider()

    st.subheader("Revenue Drivers")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            mrr_growth_chart(df),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            expansion_revenue_chart(df),
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            new_customers_chart(df),
            use_container_width=True
        )

    with col4:
        st.plotly_chart(
            arpu_chart(df),
            use_container_width=True
        )

    st.divider()

    st.subheader("Revenue Insight")

    st.info(
        """
        Revenue growth was initially driven by strong customer acquisition
        and rapid expansion of the customer base.

        Over time, the rate of new customer acquisition begins to stabilize,
        resulting in a gradual slowdown in overall revenue growth.

        Expansion revenue plays an important role in sustaining revenue
        momentum by increasing the average revenue per customer (ARPU),
        partially offsetting the deceleration in acquisition.

        This dynamic suggests that long-term growth will increasingly
        depend on effective retention strategies and expansion within
        the existing customer base.
        """
    )