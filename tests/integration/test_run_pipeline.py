import tempfile
from pathlib import Path

import pandas as pd

from src.run_pipeline import main
import config.settings as settings

def test_run_pipeline_end_to_end(monkeypatch):
    """End-to-end test for the full SaaS data pipeline."""

    with tempfile.TemporaryDirectory() as tmpdir:

        raw_dir = Path(tmpdir) / "raw"
        processed_dir = Path(tmpdir) / "processed"

        raw_dir.mkdir()
        processed_dir.mkdir()

        # Patch settings paths
        monkeypatch.setattr(settings, "RAW_DIR", raw_dir)
        monkeypatch.setattr(settings, "PROCESSED_DIR", processed_dir)

        # Reduce simulation size for faster tests
        monkeypatch.setattr(settings, "N_INITIAL_CUSTOMERS", 10)
        monkeypatch.setattr(settings, "SIMULATION_MONTHS", 3)

        # Run pipeline
        main()

        # ---------------------------------
        # Validate raw datasets
        # ---------------------------------

        customers_file = raw_dir / "customers.csv"
        subscriptions_file = raw_dir / "subscriptions_monthly.csv"

        assert customers_file.exists()
        assert subscriptions_file.exists()

        customers_df = pd.read_csv(customers_file)
        subscriptions_df = pd.read_csv(subscriptions_file)

        assert not customers_df.empty
        assert not subscriptions_df.empty

        # ---------------------------------
        # Validate processed metrics
        # ---------------------------------

        metrics_file = processed_dir / "executive_metrics.csv"

        assert metrics_file.exists()

        metrics_df = pd.read_csv(metrics_file)

        assert not metrics_df.empty

        expected_columns = {
            "year_month",
            "mrr",
            "active_customers",
            "new_customers",
            "churned_customers",
            "expansion_revenue",
            "active_prev_month",
            "churn_rate",
        }

        assert expected_columns.issubset(metrics_df.columns)