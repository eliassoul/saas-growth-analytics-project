import plotly.express as px
import pandas as pd

def mrr_chart(df):
    """
    mrr_chart(df)
    ----------------------

    Generates a Plotly line chart visualizing the Monthly Recurring Revenue (MRR) trend 
    for a given DataFrame and highlights the point where MRR growth begins to decelerate.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (preferably in YYYY-MM format)
        - "mrr": monthly recurring revenue values as numeric data

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly line chart with:
        - MRR trend over time
        - Annotation marking the slowdown point in MRR growth
        - Customized line width and layout for readability

    Details
    -------
    1. Calculates the month-over-month MRR growth rate.
    2. Identifies the month with the lowest growth rate (slowdown point).
    3. Constructs a line chart of MRR across time using Plotly Express.
    4. Updates line width and layout (white template, unified hover mode, axis labels).
    5. Adds an annotation pointing to the slowdown month, highlighting when growth begins 
    to decelerate.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "mrr": [1000, 1200, 1250]
    ... })
    >>> fig = mrr_chart(df)
    >>> fig.show()
    """

    df = df.copy()

    df["mrr_growth_rate"] = df["mrr"].pct_change()

    slowdown_index = df["mrr_growth_rate"].idxmin()

    slowdown_date = df.loc[slowdown_index, "year_month"]
    slowdown_mrr = df.loc[slowdown_index, "mrr"]

    fig = px.line(
        df,
        x="year_month",
        y="mrr",
        title="Monthly Recurring Revenue Trend"
    )

    fig.update_traces(
        line=dict(width=3)
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="",
        yaxis_title="MRR ($)",
        hovermode="x unified"
    )

    fig.add_annotation(
        x=slowdown_date,
        y=slowdown_mrr,
        text="Growth begins to decelerate",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-60
    )

    return fig

def churn_chart(df):
    """
    churn_chart(df)
    ----------------------

    Generates a Plotly line chart visualizing the Customer Churn Rate trend over time, 
    highlighting key metrics such as peak churn, best retention, average churn, and 
    risk threshold.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (preferably in YYYY-MM format)
        - "churn_rate": customer churn rates as numeric values between 0 and 1

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly line chart with:
        - Churn rate trend over time
        - Markers for peak and best retention points
        - Horizontal lines for risk threshold (5%) and average churn
        - Custom hover template and percentage formatting on the y-axis

    Details
    -------
    1. Identifies the month with maximum churn (peak) and minimum churn (best retention).
    2. Calculates the average churn rate across the dataset.
    3. Constructs a line chart with markers using Plotly Express.
    4. Adds horizontal reference lines for the risk threshold (5%) and average churn.
    5. Annotates peak churn and best retention months with arrows for clarity.
    6. Configures layout, line style, hover mode, and y-axis tick formatting.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "churn_rate": [0.04, 0.06, 0.05]
    ... })
    >>> fig = churn_chart(df)
    >>> fig.show()
    """
    df = df.copy()

    max_churn_idx = df["churn_rate"].idxmax()
    min_churn_idx = df["churn_rate"].idxmin()

    churn_date = df.loc[max_churn_idx, "year_month"]
    churn_value = df.loc[max_churn_idx, "churn_rate"]

    best_date = df.loc[min_churn_idx, "year_month"]
    best_value = df.loc[min_churn_idx, "churn_rate"]

    avg_churn = df["churn_rate"].mean()

    fig = px.line(
        df,
        x="year_month",
        y="churn_rate",
        title="Customer Churn Rate Trend"
    )

    fig.update_traces(
        line=dict(width=3),
        mode="lines+markers",
        hovertemplate="Month: %{x}<br>Churn Rate: %{y:.2%}"
    )

    fig.update_layout(
        template="plotly_white",
        height=350,
        xaxis_title="",
        yaxis_title="Churn Rate (%)",
        hovermode="x unified"
    )

    fig.add_hline(
        y=0.05,
        line_dash="dash",
        line_color="red",
        annotation_text="Risk threshold (5%)",
        annotation_position="top left"
    )

    fig.add_hline(
        y=avg_churn,
        line_dash="dot",
        annotation_text=f"Average churn: {avg_churn:.1%}",
        annotation_position="bottom left"
    )

    fig.add_annotation(
        x=churn_date,
        y=churn_value,
        text=f"Peak churn: {churn_value:.1%}",
        showarrow=True,
        arrowhead=2,
        ay=-50
    )

    fig.add_annotation(
        x=best_date,
        y=best_value,
        text=f"Best retention: {best_value:.1%}",
        showarrow=True,
        arrowhead=2,
        ay=40
    )

    fig.update_yaxes(tickformat=".0%")

    return fig

def customer_base_chart(df):
    """
    customer_base_chart(df)
    ----------------------

    Generates a Plotly area chart visualizing the growth and fluctuations of the active 
    customer base over time, highlighting the month with the highest number of active customers.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (preferably in YYYY-MM format)
        - "active_customers": count of active customers as numeric values

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly area chart with:
        - Active customer trend over time
        - Annotation marking the peak month with total active customers
        - Clean layout with unified hover mode

    Details
    -------
    1. Identifies the month with the maximum active customer count.
    2. Constructs an area chart using Plotly Express to visualize customer base trends.
    3. Adds an annotation pointing to the peak customer month.
    4. Configures layout with white template, axis titles, chart height, and hover mode.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "active_customers": [1200, 1350, 1500]
    ... })
    >>> fig = customer_base_chart(df)
    >>> fig.show()
    """

    df = df.copy()

    max_idx = df["active_customers"].idxmax()

    max_date = df.loc[max_idx, "year_month"]
    max_value = df.loc[max_idx, "active_customers"]

    fig = px.area(
        df,
        x="year_month",
        y="active_customers",
        title="Active Customer Base"
    )

    fig.update_layout(
        template="plotly_white",
        height=350,
        xaxis_title="",
        yaxis_title="Active Customers",
        hovermode="x unified"
    )

    fig.add_annotation(
        x=max_date,
        y=max_value,
        text=f"{int(max_value):,} customers",
        showarrow=True,
        arrowhead=2,
        ay=-40
    )

    return fig

def customer_growth_chart(df):
    """
    customer_growth_chart(df)
    ----------------------

    Generates a Plotly bar chart visualizing the month-over-month growth rate of active 
    customers, highlighting the period with the highest growth.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (preferably in YYYY-MM format)
        - "active_customers": number of active customers in the current month
        - "active_prev_month": number of active customers in the previous month

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly bar chart with:
        - Monthly customer growth rate
        - Annotation marking the month with peak growth
        - Custom layout for readability

    Details
    -------
    1. Calculates the month-over-month customer growth rate as a percentage.
    2. Identifies the month with the maximum growth rate.
    3. Constructs a bar chart of customer growth rates using Plotly Express.
    4. Adds an annotation to highlight the peak growth month.
    5. Configures layout with a white template, axis titles, chart height, and clean formatting.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "active_customers": [1000, 1200, 1500],
    ...     "active_prev_month": [900, 1000, 1200]
    ... })
    >>> fig = customer_growth_chart(df)
    >>> fig.show()
    """

    df = df.copy()

    df["customer_growth_rate"] = (
        (df["active_customers"] - df["active_prev_month"]) /
        df["active_prev_month"]
    )

    max_idx = df["customer_growth_rate"].idxmax()

    max_date = df.loc[max_idx, "year_month"]
    max_growth = df.loc[max_idx, "customer_growth_rate"]

    fig = px.bar(
        df,
        x="year_month",
        y="customer_growth_rate",
        title="Customer Growth Rate"
    )

    fig.update_layout(
        template="plotly_white",
        height=350,
        xaxis_title="",
        yaxis_title="Growth Rate"
    )

    fig.add_annotation(
        x=max_date,
        y=max_growth,
        text=f"Peak growth: {max_growth:.1%}",
        showarrow=True,
        arrowhead=2,
        ay=-40
    )

    return fig

def expansion_revenue_chart(df):
    """
    expansion_revenue_chart(df)
    ----------------------

    Generates a Plotly bar chart visualizing the company's monthly expansion revenue, 
    highlighting the month with the highest revenue from existing customer upgrades or 
    add-ons.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (preferably in YYYY-MM format)
        - "expansion_revenue": numeric values representing revenue generated from customer expansions

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly bar chart with:
        - Expansion revenue trend over time
        - Annotation marking the month with peak expansion revenue
        - Clean and readable layout

    Details
    -------
    1. Identifies the month with the maximum expansion revenue.
    2. Constructs a bar chart using Plotly Express to visualize revenue trends.
    3. Adds an annotation pointing to the peak month with formatted revenue.
    4. Configures layout with white template, axis titles, and chart height.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "expansion_revenue": [5000, 7000, 6500]
    ... })
    >>> fig = expansion_revenue_chart(df)
    >>> fig.show()
    """

    df = df.copy()

    max_idx = df["expansion_revenue"].idxmax()

    max_date = df.loc[max_idx, "year_month"]
    max_value = df.loc[max_idx, "expansion_revenue"]

    fig = px.bar(
        df,
        x="year_month",
        y="expansion_revenue",
        title="Expansion Revenue"
    )

    fig.update_layout(
        template="plotly_white",
        height=350,
        xaxis_title="",
        yaxis_title="Expansion Revenue ($)"
    )

    fig.add_annotation(
        x=max_date,
        y=max_value,
        text=f"${max_value:,.0f} expansion",
        showarrow=True,
        arrowhead=2,
        ay=-40
    )

    return fig

def mrr_growth_chart(df):
    """
    mrr_growth_chart(df)
    ----------------------

    Generates a Plotly line chart visualizing the month-over-month growth rate of Monthly 
    Recurring Revenue (MRR), highlighting the average growth and the point of growth slowdown.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (string or datetime, preferably YYYY-MM format)
        - "mrr": numeric values representing monthly recurring revenue

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly line chart with:
        - Month-over-month MRR growth rates
        - Markers for each month
        - Horizontal line indicating average growth rate
        - Annotation highlighting the month with the lowest growth (slowdown)
        - Custom hover template with percentage formatting

    Details
    -------
    1. Converts "year_month" to datetime for proper time-series plotting.
    2. Calculates the month-over-month MRR growth rate using percentage change.
    3. Identifies the month with the minimum growth rate as the slowdown point.
    4. Constructs a line chart with markers using Plotly Express.
    5. Adds a dashed horizontal line representing average MRR growth.
    6. Adds an annotation pointing to the growth slowdown month.
    7. Configures hover template and layout for readability.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "mrr": [10000, 12000, 12500]
    ... })
    >>> fig = mrr_growth_chart(df)
    >>> fig.show()
    """

    df = df.copy()

    df["year_month"] = pd.to_datetime(df["year_month"])

    df["mrr_growth_rate"] = df["mrr"].pct_change()

    fig = px.line(
        df,
        x="year_month",
        y="mrr_growth_rate",
        markers=True,
        title="MRR Growth Rate"
    )

    avg_growth = df["mrr_growth_rate"].mean()

    fig.add_hline(
        y=avg_growth,
        line_dash="dash",
        annotation_text=f"Average growth: {avg_growth:.2%}"
    )

    min_growth = df.loc[df["mrr_growth_rate"].idxmin()]

    fig.add_annotation(
        x=min_growth["year_month"],
        y=min_growth["mrr_growth_rate"],
        text="Growth slowdown",
        showarrow=True,
        arrowhead=2
    )

    fig.update_traces(
        hovertemplate="Month: %{x|%Y-%m}<br>Growth: %{y:.2%}"
    )

    fig.update_layout(
        yaxis_title="Growth Rate",
        xaxis_title=""
    )

    return fig

def new_customers_chart(df):
    """
    new_customers_chart(df)
    ----------------------

    Generates a Plotly bar chart visualizing the monthly acquisition of new customers, 
    highlighting the month with the highest number of new customers.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (string or datetime, preferably YYYY-MM format)
        - "new_customers": numeric values representing the number of new customers acquired

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly bar chart with:
        - Monthly new customer counts
        - Annotation marking the peak acquisition month
        - Labels displayed above bars
        - Custom hover template for month and customer count

    Details
    -------
    1. Converts "year_month" to datetime for proper time-series plotting.
    2. Identifies the month with the maximum number of new customers.
    3. Constructs a bar chart using Plotly Express.
    4. Adds an annotation pointing to the peak acquisition month.
    5. Configures text positioning, hover template, and axis titles for clarity.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "new_customers": [50, 80, 70]
    ... })
    >>> fig = new_customers_chart(df)
    >>> fig.show()
    """

    df = df.copy()

    df["year_month"] = pd.to_datetime(df["year_month"])

    fig = px.bar(
        df,
        x="year_month",
        y="new_customers",
        text="new_customers",
        title="Monthly New Customers"
    )

    max_month = df.loc[df["new_customers"].idxmax()]

    fig.add_annotation(
        x=max_month["year_month"],
        y=max_month["new_customers"],
        text="Peak acquisition",
        showarrow=True,
        arrowhead=2
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="Month: %{x|%Y-%m}<br>New Customers: %{y}"
    )

    fig.update_layout(
        yaxis_title="Customers",
        xaxis_title=""
    )

    return fig


def arpu_chart(df):
    """
    arpu_chart(df)
    ----------------------

    Generates a Plotly line chart visualizing the Average Revenue per User (ARPU) over 
    time, highlighting the highest ARPU month and indicating the average ARPU.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (string or datetime, preferably YYYY-MM format)
        - "mrr": monthly recurring revenue as numeric values
        - "active_customers": number of active customers as numeric values

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly line chart with:
        - Month-over-month ARPU values
        - Markers for each month
        - Horizontal line representing average ARPU
        - Annotation highlighting the month with highest ARPU
        - Custom hover template with currency formatting

    Details
    -------
    1. Converts "year_month" to datetime for proper time-series plotting.
    2. Calculates ARPU by dividing MRR by active customers.
    3. Identifies the month with maximum ARPU.
    4. Constructs a line chart with markers using Plotly Express.
    5. Adds a dashed horizontal line representing average ARPU.
    6. Adds an annotation pointing to the month with the highest ARPU.
    7. Configures hover template and layout for readability.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "mrr": [10000, 12000, 12500],
    ...     "active_customers": [100, 120, 125]
    ... })
    >>> fig = arpu_chart(df)
    >>> fig.show()
    """

    df = df.copy()

    df["year_month"] = pd.to_datetime(df["year_month"])

    df["arpu"] = df["mrr"] / df["active_customers"]

    fig = px.line(
        df,
        x="year_month",
        y="arpu",
        markers=True,
        title="Average Revenue per User (ARPU)"
    )

    avg_arpu = df["arpu"].mean()

    fig.add_hline(
        y=avg_arpu,
        line_dash="dash",
        annotation_text=f"Average ARPU: ${avg_arpu:.0f}"
    )

    max_arpu = df.loc[df["arpu"].idxmax()]

    fig.add_annotation(
        x=max_arpu["year_month"],
        y=max_arpu["arpu"],
        text="Highest ARPU",
        showarrow=True,
        arrowhead=2
    )

    fig.update_traces(
        hovertemplate="Month: %{x|%Y-%m}<br>ARPU: $%{y:.2f}"
    )

    fig.update_layout(
        yaxis_title="Revenue ($)",
        xaxis_title=""
    )

    return fig

def customer_churn_chart(df):
    """
    customer_churn_chart(df)
    ----------------------

    Generates a Plotly line chart visualizing the customer churn rate trend over time, 
    highlighting peak churn, best retention, average churn, and risk threshold.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "year_month": time periods (string or datetime, preferably YYYY-MM format)
        - "churn_rate": customer churn rates as numeric values between 0 and 1

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly line chart with:
        - Month-over-month churn rate trend
        - Markers for each month
        - Horizontal lines indicating risk threshold (5%) and average churn
        - Annotations for peak churn and best retention
        - Percentage formatting on the y-axis
        - Unified hover template

    Details
    -------
    1. Converts "year_month" to datetime for proper time-series plotting.
    2. Calculates maximum, minimum, and average churn rates.
    3. Constructs a line chart with markers using Plotly Express.
    4. Adds dashed and dotted horizontal lines for risk threshold and average churn.
    5. Annotates peak churn and best retention months with arrows.
    6. Configures hover template, axis formatting, chart height, and layout.

    Example
    -------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> df = pd.DataFrame({
    ...     "year_month": ["2024-01", "2024-02", "2024-03"],
    ...     "churn_rate": [0.04, 0.06, 0.05]
    ... })
    >>> fig = customer_churn_chart(df)
    >>> fig.show()
    """

    df = df.copy()
    df["year_month"] = pd.to_datetime(df["year_month"])
   
    max_churn_idx = df["churn_rate"].idxmax()
    min_churn_idx = df["churn_rate"].idxmin()
    avg_churn = df["churn_rate"].mean()

    peak_date = df.loc[max_churn_idx, "year_month"]
    peak_value = df.loc[max_churn_idx, "churn_rate"]

    best_date = df.loc[min_churn_idx, "year_month"]
    best_value = df.loc[min_churn_idx, "churn_rate"]

    fig = px.line(
        df,
        x="year_month",
        y="churn_rate",
        title="Customer Churn Rate Trend",
        markers=True
    )

    fig.update_traces(
        line=dict(width=3),
        hovertemplate="Month: %{x|%Y-%m}<br>Churn Rate: %{y:.2%}"
    )

    fig.update_layout(
        template="plotly_white",
        height=350,
        xaxis_title="",
        yaxis_title="Churn Rate (%)",
        hovermode="x unified"
    )
   
    fig.add_hline(
        y=0.05,
        line_dash="dash",
        line_color="red",
        annotation_text="Risk threshold (5%)",
        annotation_position="top left"
    )
   
    fig.add_hline(
        y=avg_churn,
        line_dash="dot",
        annotation_text=f"Average churn: {avg_churn:.1%}",
        annotation_position="bottom left"
    )
    
    fig.add_annotation(
        x=peak_date,
        y=peak_value,
        text=f"Peak churn: {peak_value:.1%}",
        showarrow=True,
        arrowhead=2,
        ay=-50
    )
   
    fig.add_annotation(
        x=best_date,
        y=best_value,
        text=f"Best retention: {best_value:.1%}",
        showarrow=True,
        arrowhead=2,
        ay=40
    )
    
    fig.update_yaxes(tickformat=".0%")

    return fig