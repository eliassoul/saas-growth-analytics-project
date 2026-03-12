"""
Data generation module for SaaS Growth Analytics simulation.

This module is responsible for generating the foundational datasets
used throughout the analytical pipeline.

The first layer of the simulation creates the customer base with
realistic distributions of:

- Pricing plans
- Countries
- Acquisition channels
- Signup timeline

The generated dataset follows a structure compatible with
subscription lifecycle simulation and executive metric modeling.

Author: Elias Soul
Project: SaaS Growth Analytics
"""

from __future__ import annotations
import logging
import config.settings as settings

import numpy as np
import pandas as pd
from typing import List

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def sample_from_distribution(distribution: dict, size: int) -> List[str]:
    """
    _sample_from_distribution(distribution, size)
    ----------------------

    Generates random samples from a categorical probability distribution.

    Parameters
    ----------
    distribution : dict
        A dictionary mapping category names (str) to probabilities (float). The probabilities
        must sum to 1.
    size : int
        The total number of samples to generate.

    Returns
    -------
    List[str]
        A list of sampled categories according to the specified probability distribution.

    Details
    -------
    1. Extracts categories and their associated probabilities from the input dictionary.
    2. Uses NumPy's `np.random.choice` to draw samples according to the probability weights.
    3. Returns the results as a Python list.
    4. Useful for simulating customer acquisition, churn, or other categorical events in SaaS data.

    Example
    -------
    >>> distribution = {"Basic": 0.5, "Pro": 0.3, "Enterprise": 0.2}
    >>> _sample_from_distribution(distribution, size=5)
    ['Basic', 'Pro', 'Basic', 'Enterprise', 'Pro']
    """

    logger.debug(
        "Sampling from distribution | categories=%s | size=%s",
        list(distribution.keys()),
        size,
    )

    categories = list(distribution.keys())
    probabilities = list(distribution.values())

    samples = np.random.choice(categories, size=size, p=probabilities)

    logger.debug("Sampling completed | samples_generated=%s", len(samples))

    return list(samples)

def generate_customer_ids(n_customers: int) -> List[str]:
    """
    generate_customer_ids(n_customers)
    ----------------------

    Generates a list of unique, formatted customer identifiers.

    Parameters
    ----------
    n_customers : int
        Number of customer IDs to generate.

    Returns
    -------
    List[str]
        A list of customer IDs in the format "CUST-000001", "CUST-000002", ..., up to n_customers.

    Details
    -------
    1. Uses zero-padded integers to ensure consistent ID formatting.
    2. IDs start at "CUST-000001" and increment sequentially.
    3. Useful for simulating or assigning unique identifiers to customers in synthetic datasets.

    Example
    -------
    >>> _generate_customer_ids(3)
    ['CUST-000001', 'CUST-000002', 'CUST-000003']
    """

    logger.debug("Generating customer IDs | total_customers=%s", n_customers)

    customer_ids = [f"CUST-{i:06d}" for i in range(1, n_customers + 1)]

    logger.debug("Customer IDs generated successfully | count=%s", len(customer_ids))

    return customer_ids

# ---------------------------------------------------------
# Core generation function
# ---------------------------------------------------------

def generate_customers(
    initial_customers: int = 200,
    start_date: str = settings.START_DATE
) -> pd.DataFrame:
    """
    generate_customers(initial_customers=200, start_date=START_DATE)
    ----------------------

    Generates a synthetic dataset of initial customers with assigned attributes for simulation.

    Parameters
    ----------
    initial_customers : int, optional
        Number of initial customers to generate (default is 200).
    start_date : str or datetime-like, optional
        The start date of the simulation; all initial customers are assigned this signup date 
        (default is `START_DATE` constant).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the following columns:
        - "customer_id": unique customer identifiers (e.g., "CUST-000001")
        - "signup_date": datetime of customer registration
        - "plan_initial": initial subscription plan (sampled from PLAN_DISTRIBUTION)
        - "country": assigned country (sampled from COUNTRY_DISTRIBUTION)
        - "acquisition_channel": channel through which the customer was acquired (sampled from ACQUISITION_CHANNELS)

    Details
    -------
    1. Generates sequential customer IDs using `_generate_customer_ids`.
    2. Assigns all initial customers the same signup date at the start of the simulation.
    3. Samples categorical attributes (plan, country, acquisition channel) according to 
    predefined probability distributions.
    4. Useful for initializing the base customer population in SaaS growth simulations.

    Example
    -------
    >>> df_customers = generate_customers(initial_customers=5, start_date="2024-01-01")
    >>> df_customers.head()
    customer_id signup_date plan_initial country acquisition_channel
    0   CUST-000001 2024-01-01        Basic     US      Organic
    1   CUST-000002 2024-01-01         Pro     DE    Referral
    2   CUST-000003 2024-01-01      Enterprise FR  Paid Ads
    3   CUST-000004 2024-01-01        Basic     US      Organic
    4   CUST-000005 2024-01-01         Pro     UK    Referral
    """

    logger.info(
        "Generating initial customers dataset | customers=%s | start_date=%s",
        initial_customers,
        start_date,
    )

    if initial_customers <= 0:
        logger.warning(
            "generate_customers called with non-positive customer count: %s",
            initial_customers,
        )

    try:

        logger.debug("Generating customer IDs")
        customer_ids = generate_customer_ids(initial_customers)

        logger.debug("Creating signup dates")
        signup_dates = [pd.to_datetime(start_date)] * initial_customers

        logger.debug("Sampling customer attributes from distributions")

        plans = sample_from_distribution(
            settings.PLAN_DISTRIBUTION,
            initial_customers
        )

        countries = sample_from_distribution(
            settings.COUNTRY_DISTRIBUTION,
            initial_customers
        )

        channels = sample_from_distribution(
            settings.ACQUISITION_CHANNELS,
            initial_customers
        )

        customers_df = pd.DataFrame(
            {
                "customer_id": customer_ids,
                "signup_date": signup_dates,
                "plan_initial": plans,
                "country": countries,
                "acquisition_channel": channels,
            }
        )

        logger.info(
            "Customer dataset generated successfully | rows=%s | columns=%s",
            customers_df.shape[0],
            customers_df.shape[1],
        )

        return customers_df

    except Exception:
        logger.exception("Failed to generate customers dataset")
        raise

# ---------------------------------------------------------
# Export helper
# ---------------------------------------------------------

def save_customers(
    df: pd.DataFrame,
    path: str
) -> None:
    """
    save_customers(df, path)
    ----------------------

    Saves a customer DataFrame to a CSV file at the specified path.

    Parameters
    ----------
    df : pandas.DataFrame
        The customer dataset to save. Expected to include columns such as:
        - "customer_id"
        - "signup_date"
        - "plan_initial"
        - "country"
        - "acquisition_channel"
    path : str
        File path (including filename) where the CSV will be written.

    Returns
    -------
    None
        Writes the DataFrame to disk as a CSV file without the index column.

    Details
    -------
    1. Uses `pandas.DataFrame.to_csv` with `index=False` to produce a clean CSV.
    2. Useful for persisting generated or simulated customer datasets for downstream analysis 
    or pipeline stages.
    3. The function does not perform path validation or directory creation; ensure the target 
    path exists.

    Example
    -------
    >>> save_customers(df_customers, "data/raw/customers.csv")
    """   

    logger.info("Saving customers dataset | path=%s", path)
    logger.debug("Customers dataframe shape | rows=%s | columns=%s", df.shape[0], df.shape[1])

    try:
        df.to_csv(path, index=False)

        logger.info(
            "Customers dataset saved successfully | path=%s | rows=%s",
            path,
            df.shape[0],
        )

    except Exception:
        logger.exception("Failed to save customers dataset | path=%s", path)
        raise

def simulate_acquisition(
    months: int = 36,
    initial_customers: int = 200,
    max_monthly_acquisition: int = 320,
    growth_rate: float = 0.18,
    noise_scale: float = 12,
) -> pd.DataFrame:
    """
    simulate_acquisition(months=36, initial_customers=200, max_monthly_acquisition=320, growth_rate=0.18, noise_scale=12)
    ----------------------

    Simulates monthly customer acquisition over a defined period using a logistic growth model with added noise.

    Parameters
    ----------
    months : int, optional
        Total number of months to simulate (default is 36).
    initial_customers : int, optional
        Number of customers at simulation start (default is 200). Currently used as a reference; not directly added to monthly counts.
    max_monthly_acquisition : int, optional
        Maximum potential monthly new customers, defining the logistic curve's asymptote (default is 320).
    growth_rate : float, optional
        Growth rate of the logistic curve controlling the speed of acquisition increase (default is 0.18).
    noise_scale : float, optional
        Standard deviation of Gaussian noise added to each month's acquisition to simulate variability (default is 12).

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns:
        - "year_month": datetime for each month in the simulation
        - "new_customers": simulated number of newly acquired customers for that month

    Details
    -------
    1. Constructs a timeline of monthly periods starting from the global `START_DATE`.
    2. Applies a logistic growth function to model realistic acquisition saturation over time.
    3. Adds Gaussian noise to introduce variability in monthly acquisitions.
    4. Ensures acquisition values are non-negative and rounded to integers.
    5. Useful for generating synthetic acquisition data for SaaS growth simulations.

    Example
    -------
    >>> df_acq = simulate_acquisition(months=12, max_monthly_acquisition=200)
    >>> df_acq.head()
    year_month  new_customers
    0 2024-01-01            15
    1 2024-02-01            23
    2 2024-03-01            36
    3 2024-04-01            45
    4 2024-05-01            58
    """

    logger.info(
        "Starting acquisition simulation | months=%s | max_monthly_acquisition=%s | growth_rate=%s | noise_scale=%s",
        months,
        max_monthly_acquisition,
        growth_rate,
        noise_scale,
    )

    if months <= 0:
        logger.warning("simulate_acquisition called with non-positive months: %s", months)

    try:

        months_index = pd.date_range(
            start=settings.START_DATE,
            periods=months,
            freq="MS"
        )

        acquisition_values = []

        midpoint = months / 2

        logger.debug("Calculated logistic midpoint for acquisition curve | midpoint=%s", midpoint)

        for t in range(months):

            base_growth = max_monthly_acquisition / (
                1 + np.exp(-growth_rate * (t - midpoint))
            )

            noise = np.random.normal(0, noise_scale)

            monthly_acquisition = base_growth + noise

            acquisition_values.append(max(0, int(round(monthly_acquisition))))

        acquisition_df = pd.DataFrame(
            {
                "year_month": months_index,
                "new_customers": acquisition_values,
            }
        )

        logger.info(
            "Acquisition simulation completed | months=%s | total_new_customers=%s | avg_monthly_acquisition=%.2f",
            months,
            acquisition_df["new_customers"].sum(),
            acquisition_df["new_customers"].mean(),
        )

        logger.debug(
            "Acquisition dataframe generated | rows=%s | columns=%s",
            acquisition_df.shape[0],
            acquisition_df.shape[1],
        )

        return acquisition_df

    except Exception:
        logger.exception("Failed during acquisition simulation")
        raise

def simulate_churn(
    plan: str,
    month_index: int,
    random_state: np.random.Generator,
) -> bool:
    """
    simulate_churn(plan, month_index, random_state)
    ----------------------

    Simulates whether a customer churns in a given month based on subscription plan and lifecycle phase.

    Parameters
    ----------
    plan : str
        Customer subscription plan. Expected values: "Basic", "Pro", "Enterprise".
    month_index : int
        Zero-based index of the month in the simulation. Determines the lifecycle phase:
        - 0–11: "hypergrowth"
        - 12–23: "expansion"
        - 24+: "competitive"
    random_state : numpy.random.Generator
        NumPy random number generator instance for reproducible stochastic simulation.

    Returns
    -------
    bool
        True if the customer churns in the given month; False otherwise.

    Details
    -------
    1. Determines the customer's lifecycle phase based on `month_index`.
    2. Uses a predefined churn probability matrix for each combination of phase and plan.
    3. Draws a Bernoulli trial using the `random_state` generator to decide churn.
    4. Useful for modeling retention dynamics in SaaS simulations with plan- and phase-specific behavior.

    Example
    -------
    >>> rng = np.random.default_rng(42)
    >>> simulate_churn("Basic", 5, rng)
    False
    >>> simulate_churn("Pro", 15, rng)
    True
    """

    # --------------------------------------------------
    # Define lifecycle phase
    # --------------------------------------------------

    if month_index < 12:
        phase = "hypergrowth"

    elif month_index < 24:
        phase = "expansion"

    else:
        phase = "competitive"

    logger.debug(
        "Simulating churn | plan=%s | month_index=%s | phase=%s",
        plan,
        month_index,
        phase,
    )

    # --------------------------------------------------
    # Churn probabilities by phase and plan
    # --------------------------------------------------

    churn_matrix = {

        "hypergrowth": {
            "Basic": 0.03,
            "Pro": 0.02,
            "Enterprise": 0.01,
        },

        "expansion": {
            "Basic": 0.04,
            "Pro": 0.03,
            "Enterprise": 0.015,
        },

        "competitive": {
            "Basic": 0.06,
            "Pro": 0.04,
            "Enterprise": 0.02,
        },
    }

    try:

        churn_probability = churn_matrix[phase][plan]

        churn_event = random_state.random() < churn_probability

        return churn_event

    except KeyError:
        logger.exception(
            "Invalid plan or phase in churn simulation | plan=%s | phase=%s",
            plan,
            phase,
        )
        raise

def simulate_expansion(
    current_plan: str,
    random_state: np.random.Generator,
) -> tuple[str, bool]:
    """
    simulate_expansion(current_plan, random_state)
    ----------------------

    Simulates whether a customer upgrades their subscription plan in a given month.

    Parameters
    ----------
    current_plan : str
        Current subscription plan of the customer. Expected values: "Basic", "Pro", "Enterprise".
    random_state : numpy.random.Generator
        NumPy random number generator instance for reproducible stochastic simulation.

    Returns
    -------
    tuple[str, bool]
        - New plan after potential upgrade (may remain the same if no upgrade occurs)
        - Boolean flag indicating whether an upgrade occurred (True) or not (False)

    Details
    -------
    1. Uses predefined monthly upgrade probabilities per plan:
        - Basic → Pro: 5%
        - Pro → Enterprise: 3%
        - Enterprise → Enterprise: 0%
    2. Determines the next plan based on `upgrade_paths` if an upgrade event occurs.
    3. Draws a Bernoulli trial using the `random_state` generator to simulate stochastic upgrades.
    4. Useful for modeling expansion revenue and plan migration in SaaS simulations.

    Example
    -------
    >>> rng = np.random.default_rng(42)
    >>> simulate_expansion("Basic", rng)
    ('Basic', False)
    >>> simulate_expansion("Pro", rng)
    ('Enterprise', True)
    """    
    # --------------------------------------------------
    # Define expansion probabilities
    # --------------------------------------------------

    expansion_probabilities = {
        "Basic": 0.05,
        "Pro": 0.03,
        "Enterprise": 0.0,
    }

    upgrade_paths = {
        "Basic": "Pro",
        "Pro": "Enterprise",
        "Enterprise": "Enterprise",
    }

    try:

        probability = expansion_probabilities[current_plan]

        # --------------------------------------------------
        # Draw expansion event
        # --------------------------------------------------

        upgrade_event = random_state.random() < probability

        if upgrade_event:
            new_plan = upgrade_paths[current_plan]

            logger.debug(
                "Plan upgraded | previous_plan=%s | new_plan=%s",
                current_plan,
                new_plan,
            )

            return new_plan, True

        return current_plan, False

    except KeyError:
        logger.exception(
            "Invalid plan received in expansion simulation | plan=%s",
            current_plan,
        )
        raise

def generate_subscription_history(
    customers_df: pd.DataFrame,
    acquisition_df: pd.DataFrame,
    months: int = 36,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    generate_subscription_history(customers_df, acquisition_df, months=36, random_seed=42)
    ----------------------

    Simulates month-by-month subscription history for a customer base, including acquisition, churn, expansion, and revenue.

    Parameters
    ----------
    customers_df : pandas.DataFrame
        Initial customer dataset containing columns:
        - "customer_id"
        - "plan_initial"
        - "signup_date"
        - "country"
        - "acquisition_channel"
    acquisition_df : pandas.DataFrame
        Monthly new customer acquisition data with columns:
        - "year_month": datetime of each month
        - "new_customers": number of new customers acquired
    months : int, optional
        Number of months to simulate (default is 36)
    random_seed : int, optional
        Seed for reproducible random number generation (default is 42)

    Returns
    -------
    pandas.DataFrame
        Simulated subscription history with the following columns:
        - "customer_id": unique identifier for the customer
        - "year_month": month of the record
        - "plan_current": customer's plan in that month
        - "active": boolean flag indicating if the customer is active
        - "monthly_revenue": revenue generated by the customer for the month
        - "expansion_flag": True if the customer upgraded their plan that month
        - "churn_flag": True if the customer churned that month

    Details
    -------
    1. Initializes the simulation state for existing customers.
    2. Generates new customers each month according to `acquisition_df`.
    3. Iterates over all customers each month to:
    - Apply potential plan upgrades via `simulate_expansion`
    - Determine churn events via `simulate_churn`
    - Calculate monthly revenue based on plan pricing
    4. Records the state of each customer per month for downstream analysis.
    5. Returns a comprehensive DataFrame suitable for SaaS metrics calculation and visualization.

    Example
    -------
    >>> subscription_history = generate_subscription_history(df_customers, df_acquisition, months=12, random_seed=123)
    >>> subscription_history.head()
    customer_id year_month plan_current  active  monthly_revenue  expansion_flag  churn_flag
    0   CUST-000001 2024-01-01        Basic    True               29           False       False
    1   CUST-000002 2024-01-01          Pro    True               79           False       False
    2   CUST-000003 2024-01-01      Enterprise True              199           False       False
    3   CUST-000004 2024-01-01        Basic    True               29           False       False
    4   CUST-000005 2024-01-01          Pro    True               79           False       False
    """

    logger.info(
        "Starting subscription lifecycle simulation | months=%s | random_seed=%s",
        months,
        random_seed,
    )

    logger.debug(
        "Initial dataset sizes | customers=%s | acquisition_months=%s",
        len(customers_df),
        len(acquisition_df),
    )

    try:

        rng = np.random.default_rng(random_seed)

        # --------------------------------------------------
        # Pricing table
        # --------------------------------------------------

        plan_prices = {
            "Basic": 29,
            "Pro": 79,
            "Enterprise": 199,
        }

        # --------------------------------------------------
        # Simulation state
        # --------------------------------------------------

        customers = customers_df.copy()

        customer_state = {
            row.customer_id: {
                "plan": row.plan_initial,
                "active": True,
            }
            for row in customers.itertuples()
        }

        records = []

        months_index = acquisition_df["year_month"].values

        next_customer_id = len(customer_state) + 1

        # --------------------------------------------------
        # Month-by-month simulation
        # --------------------------------------------------

        for month_idx, current_month in enumerate(months_index):

            new_customers = int(acquisition_df.iloc[month_idx]["new_customers"])

            expansions_this_month = 0
            churns_this_month = 0

            # ----------------------------------------------
            # New acquisition
            # ----------------------------------------------

            for _ in range(new_customers):

                cid = f"CUST-{next_customer_id:06d}"
                next_customer_id += 1

                plan = rng.choice(
                    ["Basic", "Pro", "Enterprise"],
                    p=[0.60, 0.30, 0.10],
                )

                customer_state[cid] = {
                    "plan": plan,
                    "active": True,
                }

            # ----------------------------------------------
            # Iterate over customers
            # ----------------------------------------------

            for cid, state in customer_state.items():

                plan = state["plan"]
                active = state["active"]

                expansion_flag = False
                churn_flag = False
                revenue = 0

                if active:

                    new_plan, expansion_flag = simulate_expansion(plan, rng)

                    if expansion_flag:
                        expansions_this_month += 1

                    state["plan"] = new_plan
                    plan = new_plan

                    churn_flag = simulate_churn(plan, month_idx, rng)

                    if churn_flag:
                        churns_this_month += 1
                        state["active"] = False
                        active = False

                    if active:
                        revenue = plan_prices[plan]

                records.append(
                    {
                        "customer_id": cid,
                        "year_month": current_month,
                        "plan_current": plan,
                        "active": active,
                        "monthly_revenue": revenue,
                        "expansion_flag": expansion_flag,
                        "churn_flag": churn_flag,
                    }
                )

            logger.info(
                "Month simulated | month=%s | new_customers=%s | expansions=%s | churns=%s | total_customers=%s",
                current_month,
                new_customers,
                expansions_this_month,
                churns_this_month,
                len(customer_state),
            )

        subscription_df = pd.DataFrame(records)

        logger.info(
            "Subscription history generated successfully | rows=%s | columns=%s",
            subscription_df.shape[0],
            subscription_df.shape[1],
        )

        return subscription_df

    except Exception:
        logger.exception("Subscription lifecycle simulation failed")
        raise          