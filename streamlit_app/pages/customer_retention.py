import streamlit as st
from components.charts import churn_chart

def render_customer_retention(df):
    """
    render_customer_retention(df)
    ----------------------

    Renders a comprehensive Customer Retention page in a Streamlit app, including churn 
    trend visualization, key retention metrics, and strategic insights.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (datetime or string)
        - "churn_rate": numeric values representing customer churn rate (0-1)

    Returns
    -------
    None
        Renders interactive Streamlit components directly:
        - Page title and caption
        - Churn trend line chart
        - Retention KPI metrics
        - Strategic insights section

    Details
    -------
    1. Displays a page title ("Customer Retention") and a brief caption describing the analysis.
    2. Plots the customer churn trend using the `churn_chart` function in an interactive Plotly chart.
    3. Calculates retention metrics:
    - Average churn rate
    - Best retention month (lowest churn)
    - Highest churn month (peak churn)
    These metrics are displayed as Streamlit metric cards in a three-column layout.
    4. Provides a strategic interpretation section with key insights on retention importance, 
    churn patterns, and actionable strategies to reduce churn and maximize LTV.
    5. Uses Streamlit dividers and subheaders for clear visual separation of sections.

    Example
    -------
    >>> import pandas as pd
    >>> import streamlit as st
    >>> df = pd.DataFrame({
    ...     "year_month": pd.to_datetime(["2024-01", "2024-02", "2024-03"]),
    ...     "churn_rate": [0.04, 0.06, 0.05]
    ... })
    >>> render_customer_retention(df)
    """
    
    df = df.copy()

    st.title("Customer Retention")

    st.caption(
        "Analysis of customer retention performance and churn dynamics over time."
    )

    st.divider()

    st.subheader("Customer Churn Trend")

    st.plotly_chart(
        churn_chart(df),
        use_container_width=True
    )

    st.divider()

    avg_churn = df["churn_rate"].mean()

    best_month = df.loc[df["churn_rate"].idxmin()]
    worst_month = df.loc[df["churn_rate"].idxmax()]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Average Churn",
            value=f"{avg_churn:.2%}"
        )

    with col2:
        st.metric(
            label="Best Retention Month",
            value=best_month["year_month"].strftime("%b %Y"),
            delta=f"{best_month['churn_rate']:.2%}"
        )

    with col3:
        st.metric(
            label="Highest Churn Month",
            value=worst_month["year_month"].strftime("%b %Y"),
            delta=f"{worst_month['churn_rate']:.2%}"
        )

    st.divider()

    st.subheader("Retention Insight")

    st.info(
        """
        Customer retention remains one of the most critical drivers of sustainable SaaS growth.

        The churn trend indicates periods where customer loss increases, potentially reflecting
        product adoption challenges, onboarding friction, or pricing sensitivity.

        Maintaining churn below the typical SaaS risk threshold (around 5%) is essential to
        ensure healthy long-term growth and maximize customer lifetime value.

        Improving retention strategies — such as better onboarding, stronger product engagement,
        and expansion opportunities within the existing customer base — can significantly
        enhance revenue stability and growth efficiency.
        """
    )