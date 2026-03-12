import pandas as pd
import tempfile
from pathlib import Path

import config.settings as settings
from src.metrics import generate_executive_metrics


def test_generate_executive_metrics_pipeline(monkeypatch):
    """Integration test for executive metrics pipeline."""

    # ----------------------------------
    # Create temporary directories
    # ----------------------------------

    with tempfile.TemporaryDirectory() as tmpdir:

        raw_dir = Path(tmpdir) / "raw"
        processed_dir = Path(tmpdir) / "processed"

        raw_dir.mkdir()
        processed_dir.mkdir()

        # ----------------------------------
        # Fake subscription dataset
        # ----------------------------------

        df = pd.DataFrame(
            {
                "customer_id": ["C1", "C2", "C1", "C2"],
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-02-01",
                    "2024-02-01",
                ],
                "monthly_revenue": [29, 79, 29, 79],
                "active": [True, True, True, False],
                "churn_flag": [False, False, False, True],
                "expansion_flag": [False, False, False, False],
            }
        )

        file_path = raw_dir / "subscriptions_monthly.csv"

        df.to_csv(file_path, index=False)

        # ----------------------------------
        # Patch settings directories
        # ----------------------------------

        monkeypatch.setattr(settings, "RAW_DIR", raw_dir)
        monkeypatch.setattr(settings, "PROCESSED_DIR", processed_dir)

        # ----------------------------------
        # Run pipeline
        # ----------------------------------

        result = generate_executive_metrics()

        # ----------------------------------
        # Assertions
        # ----------------------------------

        assert isinstance(result, pd.DataFrame)

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

        assert expected_columns.issubset(result.columns)

        # File should be saved
        output_file = processed_dir / "executive_metrics.csv"

        assert output_file.exists()