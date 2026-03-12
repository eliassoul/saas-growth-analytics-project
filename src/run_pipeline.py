"""
SaaS Growth Analytics - Data Generation Pipeline

This script orchestrates the synthetic data generation pipeline for the
Startup SaaS Growth Analytics project.

Pipeline Steps
--------------
1. Generate synthetic customers
2. Simulate customer acquisition
3. Generate subscription lifecycle history
4. Save raw datasets
5. Compute SaaS executive metrics

Outputs
-------
data/raw/customers.csv
data/raw/subscriptions_monthly.csv
data/processed/executive_metrics.csv

Usage
-----
python src/run_pipeline.py
"""

import logging

from config.logging_config import setup_logging
import config.settings as settings

from src.data_generation import (
    generate_customers,
    simulate_acquisition,
    generate_subscription_history
)

from src.metrics import generate_executive_metrics

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------

def main() -> None:
    """
    main()
    ------

    Executes the complete synthetic SaaS data generation and metric computation pipeline.

    Description
    -----------
    This function orchestrates all steps required to produce synthetic datasets simulating
    customer acquisition, subscription lifecycle, revenue, and retention for a SaaS platform.
    It also computes executive-level metrics suitable for dashboards and KPI tracking.

    Pipeline Steps
    --------------
    1. Directory Preparation:
    - Ensures RAW_DIR exists for storing raw datasets.
    2. Initial Customer Generation:
    - Generates a set of initial customers with assigned plans, countries, and acquisition channels.
    3. Acquisition Simulation:
    - Simulates monthly new customer acquisition over a defined number of months.
    4. Subscription Lifecycle Simulation:
    - Generates month-by-month subscription history including active status, churn, expansion, and revenue.
    5. Dataset Saving:
    - Saves generated customer and subscription datasets to CSV files within RAW_DIR.
    6. Executive Metrics Computation:
    - Aggregates subscription data to compute metrics such as MRR, active customers, churn, expansion revenue, and churn rate.
    - Saves the metrics to PROCESSED_DIR.

    Returns
    -------
    None

    Side Effects
    ------------
    - Creates directories RAW_DIR and PROCESSED_DIR if they do not exist.
    - Writes CSV files:
    - RAW_DIR/customers.csv
    - RAW_DIR/subscriptions_monthly.csv
    - PROCESSED_DIR/executive_metrics.csv
    - Prints progress and completion messages to the console.

    Example
    -------
    >>> main()
    Starting SaaS data generation pipeline...
    Generating initial customers...
    Simulating acquisition...
    Generating subscription history...
    Datasets saved successfully.
    Customers dataset: /path/to/raw/customers.csv
    Subscriptions dataset: /path/to/raw/subscriptions_monthly.csv
    Pipeline finished.
    Executive metrics generated.
    """
    try:
        # -----------------------------------------------------
        # Ensure directories exist
        # -----------------------------------------------------

        logger.info("Ensuring raw data directory exists")
        settings.RAW_DIR.mkdir(parents=True, exist_ok=True)

        # -----------------------------------------------------
        # Step 1 - Generate initial customers
        # -----------------------------------------------------

        logger.info("Generating initial customers")

        customers_df = generate_customers(
            initial_customers=settings.N_INITIAL_CUSTOMERS,
        )

        logger.info(f"Initial customers generated: {len(customers_df)}")

        # -----------------------------------------------------
        # Step 2 - Simulate acquisition
        # -----------------------------------------------------

        logger.info("Simulating customer acquisition")

        acquisition_df = simulate_acquisition(
            months=settings.SIMULATION_MONTHS,
        )

        logger.info(f"Acquisition records generated: {len(acquisition_df)}")

        # -----------------------------------------------------
        # Step 3 - Generate subscription lifecycle
        # -----------------------------------------------------

        logger.info("Generating subscription lifecycle history")

        subscriptions_df = generate_subscription_history(
            customers_df=customers_df,
            acquisition_df=acquisition_df,
            months=settings.SIMULATION_MONTHS,
        )

        logger.info(
            f"Subscription history generated: {len(subscriptions_df)} records"
        )

        # -----------------------------------------------------
        # Step 4 - Save datasets
        # -----------------------------------------------------

        customers_path = settings.RAW_DIR / "customers.csv"
        subscriptions_path = settings.RAW_DIR / "subscriptions_monthly.csv"

        logger.info("Saving raw datasets")

        customers_df.to_csv(customers_path, index=False)
        subscriptions_df.to_csv(subscriptions_path, index=False)

        logger.info(f"Customers dataset saved to: {customers_path}")
        logger.info(f"Subscriptions dataset saved to: {subscriptions_path}")

        # -----------------------------------------------------
        # Step 5 - Generate executive metrics
        # -----------------------------------------------------

        logger.info("Generating executive metrics")

        executive_metrics = generate_executive_metrics()
        
        logger.info(
            f"Executive metrics generated with {len(executive_metrics)} rows"
        )
        
        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.exception("Pipeline execution failed")
        raise


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    setup_logging()
    main()