import streamlit as st
from utils.data_loader import load_executive_metrics
from utils.metrics import compute_kpis
from components.kpi_cards import render_kpi_cards
from components.charts import mrr_chart, churn_chart, expansion_revenue_chart

def render_diagnosis():
    """
    render_diagnosis()
    ----------------------

    Renders the Strategic Diagnosis page in a Streamlit app, analyzing company performance 
    to identify growth opportunities, emerging risks, structural concerns, and strategic recommendations.

    Parameters
    ----------
    None
        The function internally loads the required dataset using `load_executive_metrics()` 
        and computes KPIs via `compute_kpis()`.

    Returns
    -------
    None
        Renders interactive Streamlit components directly:
        - Page title and caption
        - KPI cards
        - Sectioned analysis with charts for growth phase, emerging risks, and structural concerns
        - Strategic recommendations as a markdown list

    Details
    -------
    1. Displays the page title ("Strategic Diagnosis") and a descriptive caption.
    2. Loads executive metrics dataset internally.
    3. Computes key KPIs and renders them via `render_kpi_cards`.
    4. Section: Growth Phase
    - Provides an info panel summarizing early growth achievements
    - Plots MRR chart to illustrate revenue expansion
    5. Section: Emerging Risk
    - Highlights increasing customer churn with a warning panel
    - Plots churn trend to visualize retention risks
    6. Section: Structural Concern
    - Highlights critical NRR trends with an error panel
    - Plots expansion revenue to show potential gaps or missed opportunities
    7. Section: Strategic Recommendations
    - Provides actionable steps for retention, product value, upgrades, and acquisition optimization
    8. Uses Streamlit subheaders, dividers, info/warning/error panels, and charts for a structured and clear presentation.

    Example
    -------
    >>> import streamlit as st
    >>> render_diagnosis()
    """
    st.title("Strategic Diagnosis")
    
    st.caption(
        "Analysis of company performance to identify growth opportunities, emerging risks, "
        "and structural concerns impacting overall strategic positioning."
    )
  
    df = load_executive_metrics()
    kpis = compute_kpis(df)
    render_kpi_cards(kpis)

    st.divider()
 
    st.subheader("Growth Phase")
    st.info(
        "The company experienced strong early acquisition, reflected in steady MRR and new customer growth."
    )
    st.plotly_chart(mrr_chart(df), use_container_width=True)

    st.subheader("Emerging Risk")
    st.warning(
        "Customer churn began increasing after the expansion phase. Monitor churn spikes carefully and address retention issues."
    )
    st.plotly_chart(churn_chart(df), use_container_width=True)

    st.subheader("Structural Concern")
    st.error(
        "Net Revenue Retention is trending toward critical levels, signaling potential revenue leakage or underutilization of expansion opportunities."
    )
    st.plotly_chart(expansion_revenue_chart(df), use_container_width=True)

    st.divider()

    st.subheader("Strategic Recommendations")
    st.markdown("""
    - Invest in retention initiatives
    - Improve product value for Basic tier customers
    - Encourage upgrades to Pro and Enterprise plans
    - Optimize acquisition channels
    - Monitor churn and expansion revenue trends closely
    """)