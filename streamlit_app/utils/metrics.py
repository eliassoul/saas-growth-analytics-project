import logging

logger = logging.getLogger(__name__)

def calculate_growth_rate(current_mrr, previous_mrr):
    """
    calculate_growth_rate(current_mrr, previous_mrr)
    ----------------------

    Calculates the month-over-month growth rate of Monthly Recurring Revenue (MRR).

    Parameters
    ----------
    current_mrr : float
        The MRR value for the current period.
    previous_mrr : float
        The MRR value for the previous period.

    Returns
    -------
    float
        The growth rate as a decimal (e.g., 0.05 for 5%). Returns 0 if the previous MRR is zero 
        to avoid division by zero.

    Details
    -------
    1. Computes the relative change in MRR between the current and previous periods.
    2. Handles the edge case where the previous period MRR is zero to prevent division errors.
    3. Commonly used in KPI computations for SaaS dashboards to monitor revenue growth trends.

    Example
    -------
    >>> calculate_growth_rate(12000, 10000)
    0.2
    >>> calculate_growth_rate(5000, 0)
    0
    """
    logger.debug(
        "Calculating MRR growth rate | current_mrr=%s | previous_mrr=%s",
        current_mrr,
        previous_mrr,
    )

    if previous_mrr == 0:
        logger.warning(
            "Previous MRR is zero; returning growth rate 0 to avoid division by zero"
        )
        return 0

    growth_rate = current_mrr / previous_mrr - 1

    logger.debug("MRR growth rate calculated | growth_rate=%.4f", growth_rate)

    return growth_rate

def calculate_nrr(latest, previous):
    """
    calculate_nrr(latest, previous)
    ----------------------

    Calculates the Net Revenue Retention (NRR) rate for a given period, accounting for 
    expansion revenue and churned customer revenue.

    Parameters
    ----------
    latest : dict
        Dictionary representing the latest period metrics, expected keys:
        - "mrr": Monthly Recurring Revenue for the latest period
        - "active_customers": number of active customers in the latest period
        - "churned_customers": number of customers lost since previous period
        - "expansion_revenue": optional, revenue gained from upsells/cross-sells (default 0)
    previous : dict
        Dictionary representing the previous period metrics, expected key:
        - "mrr": Monthly Recurring Revenue for the previous period

    Returns
    -------
    float
        The NRR as a decimal (e.g., 1.05 for 105%). Returns 0 if previous MRR is zero 
        to avoid division by zero.

    Details
    -------
    1. Computes revenue lost from churned customers based on average revenue per customer:
    churned_revenue = churned_customers * (latest MRR / latest active customers)
    2. Adds expansion revenue to the latest MRR.
    3. Divides net revenue (latest MRR + expansion - churned) by previous MRR to calculate NRR.
    4. Handles edge cases where previous MRR is zero to avoid division errors.
    5. Useful for SaaS financial analysis to assess whether existing customers’ revenue 
    offsets churn and drives net growth.

    Example
    -------
    >>> latest = {"mrr": 12000, "active_customers": 100, "churned_customers": 5, "expansion_revenue": 500}
    >>> previous = {"mrr": 11000}
    >>> calculate_nrr(latest, previous)
    1.0454545454545454
    """
    logger.debug(
        "Calculating NRR | latest_mrr=%s | previous_mrr=%s",
        latest.get("mrr"),
        previous.get("mrr"),
    )

    expansion = latest.get("expansion_revenue", 0)

    active_customers = latest.get("active_customers", 0)

    if active_customers == 0:
        logger.warning(
            "Active customers is zero; churned revenue assumed as 0"
        )
        churned_revenue = 0
    else:
        churned_revenue = latest["churned_customers"] * (
            latest["mrr"] / active_customers
        )

    previous_mrr = previous.get("mrr", 0)

    if previous_mrr == 0:
        logger.warning(
            "Previous MRR is zero; returning NRR=0 to avoid division by zero"
        )
        return 0

    nrr = (latest["mrr"] + expansion - churned_revenue) / previous_mrr

    logger.debug(
        "NRR calculated | expansion=%s | churned_revenue=%s | nrr=%.4f",
        expansion,
        churned_revenue,
        nrr,
    )

    return nrr

def calculate_ltv(mrr, churn_rate):
    """
    calculate_ltv(mrr, churn_rate)
    ----------------------

    Calculates the Customer Lifetime Value (LTV) based on Monthly Recurring Revenue (MRR) 
    and churn rate.

    Parameters
    ----------
    mrr : float
        Monthly Recurring Revenue per customer.
    churn_rate : float
        Customer churn rate as a decimal (e.g., 0.05 for 5%).

    Returns
    -------
    float
        The LTV value in monetary units. Returns 0 if churn rate is zero to prevent division by zero.

    Details
    -------
    1. Uses the standard formula for LTV in a subscription-based business:
    LTV = MRR / churn_rate
    2. Assumes constant MRR and stable churn rate over time.
    3. Handles the edge case where churn rate is zero to avoid infinite LTV.

    Example
    -------
    >>> calculate_ltv(100, 0.05)
    2000.0
    >>> calculate_ltv(100, 0)
    0
    """

    logger.debug(
        "Calculating LTV | mrr=%s | churn_rate=%s",
        mrr,
        churn_rate
    )

    if churn_rate == 0:
        logger.warning(
            "Churn rate is zero; returning LTV=0 to avoid division by zero"
        )
        return 0

    ltv = mrr / churn_rate

    logger.debug("LTV calculated | ltv=%.2f", ltv)

    return ltv

def compute_kpis(df):
    """
    compute_kpis(df)
    ----------------------

    Computes key SaaS metrics (KPIs) from a historical executive metrics DataFrame, 
    including revenue growth, churn, NRR, LTV, and active customers.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - "mrr": Monthly Recurring Revenue
        - "churn_rate": customer churn rate (0-1)
        - "active_customers": number of active customers
        - "churned_customers": number of churned customers
        - "expansion_revenue": optional, revenue gained from upsells/cross-sells

    Returns
    -------
    dict
        A dictionary containing the following KPIs:
        - "mrr": latest MRR value
        - "mrr_delta": change in MRR from the previous period
        - "growth_rate": month-over-month MRR growth rate
        - "growth_delta": change in growth rate from the previous period
        - "churn_rate": latest customer churn rate
        - "nrr": Net Revenue Retention for the period
        - "ltv": Customer Lifetime Value
        - "customers": latest active customer count

    Details
    -------
    1. Uses the last two (or three) rows of the DataFrame to compute deltas and growth rates.
    2. Calculates MRR delta: difference between latest and previous MRR.
    3. Calculates month-over-month growth rate and its delta versus the prior period.
    4. Retrieves the latest churn rate directly from the DataFrame.
    5. Computes Net Revenue Retention (NRR) accounting for expansion revenue and churned customers.
    6. Calculates Customer Lifetime Value (LTV) as MRR divided by churn rate.
    7. Safely handles division by zero for previous MRR and churn rate.
    8. Provides a structured dictionary suitable for rendering KPI cards in dashboards.

    Example
    -------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "mrr": [10000, 11000, 12000],
    ...     "churn_rate": [0.05, 0.04, 0.03],
    ...     "active_customers": [100, 110, 120],
    ...     "churned_customers": [5, 4, 3],
    ...     "expansion_revenue": [500, 600, 700]
    ... })
    >>> compute_kpis(df)
    {
        "mrr": 12000,
        "mrr_delta": 1000,
        "growth_rate": 0.09090909090909091,
        "growth_delta": 0.01694915254237287,
        "churn_rate": 0.03,
        "nrr": 1.0375,
        "ltv": 400000.0,
        "customers": 120
    }
    """

    logger.debug("Computing dashboard KPIs | rows=%s", len(df))

    if len(df) < 2:
        logger.warning("Not enough data to compute KPIs")
        return {}

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    mrr = latest["mrr"]
    previous_mrr = previous["mrr"]

    mrr_delta = mrr - previous_mrr

    # -----------------------------------------------------
    # Growth
    # -----------------------------------------------------

    growth_rate = (mrr / previous_mrr - 1) if previous_mrr != 0 else 0

    previous_growth = 0
    if len(df) >= 3:
        third = df.iloc[-3]["mrr"]
        if third != 0:
            previous_growth = previous_mrr / third - 1
        else:
            logger.warning("Previous-previous MRR is zero; growth delta may be inaccurate")

    growth_delta = growth_rate - previous_growth

    # -----------------------------------------------------
    # Churn
    # -----------------------------------------------------

    churn_rate = latest["churn_rate"]

    # -----------------------------------------------------
    # NRR
    # -----------------------------------------------------

    expansion = latest.get("expansion_revenue", 0)

    if latest["active_customers"] == 0:
        logger.warning("Active customers is zero; churned revenue assumed as 0")
        churned_revenue = 0
    else:
        churned_revenue = latest["churned_customers"] * (
            mrr / latest["active_customers"]
        )

    nrr = (mrr + expansion - churned_revenue) / previous_mrr if previous_mrr != 0 else 0

    # -----------------------------------------------------
    # LTV
    # -----------------------------------------------------

    ltv = mrr / churn_rate if churn_rate != 0 else 0

    logger.debug(
        "KPIs computed | mrr=%s | growth=%.4f | churn=%.4f | nrr=%.4f | ltv=%.2f",
        mrr,
        growth_rate,
        churn_rate,
        nrr,
        ltv,
    )

    return {
        "mrr": mrr,
        "mrr_delta": mrr_delta,
        "growth_rate": growth_rate,
        "growth_delta": growth_delta,
        "churn_rate": churn_rate,
        "nrr": nrr,
        "ltv": ltv,
        "customers": latest["active_customers"],
    }