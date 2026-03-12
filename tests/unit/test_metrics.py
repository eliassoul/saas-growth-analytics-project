import pandas as pd
import numpy as np
import tempfile
from pathlib import Path

import config.settings as settings
from src.metrics import (
    calculate_mrr,
    calculate_active_customers,
    calculate_new_customers,
    calculate_churned_customers,
    calculate_expansion_revenue,
    calculate_churn_rate,
    generate_executive_metrics,

    )


class TestCalculateMRR:
    """Unit tests for the calculate_mrr function."""

    def test_returns_dataframe(self):
        """Function should return a pandas DataFrame."""
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01", "2024-01-01"],
                "monthly_revenue": [29, 79],
            }
        )

        result = calculate_mrr(df)

        assert isinstance(result, pd.DataFrame)

    def test_expected_columns(self):
        """Output must contain the correct schema."""
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "monthly_revenue": [29],
            }
        )

        result = calculate_mrr(df)

        assert set(result.columns) == {"year_month", "mrr"}

    def test_correct_mrr_aggregation(self):
        """MRR should equal the sum of monthly_revenue per month."""
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-02-01",
                ],
                "monthly_revenue": [
                    29,
                    79,
                    199,
                ],
            }
        )

        result = calculate_mrr(df)

        jan_mrr = result[result["year_month"] == "2024-01-01"]["mrr"].iloc[0]
        feb_mrr = result[result["year_month"] == "2024-02-01"]["mrr"].iloc[0]

        assert jan_mrr == 108
        assert feb_mrr == 199

    def test_output_row_count_equals_unique_months(self):
        """Number of rows should match number of unique months."""
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-02-01",
                ],
                "monthly_revenue": [10, 20, 30],
            }
        )

        result = calculate_mrr(df)

        assert len(result) == df["year_month"].nunique()

    def test_no_negative_mrr(self):
        """MRR values should not be negative."""
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                ],
                "monthly_revenue": [50, 20],
            }
        )

        result = calculate_mrr(df)

        assert (result["mrr"] >= 0).all()

    def test_empty_dataframe(self):
        """Empty input should return empty output."""
        df = pd.DataFrame(columns=["year_month", "monthly_revenue"])

        result = calculate_mrr(df)

        assert result.empty

class TestCalculateActiveCustomers:
    """Unit tests for calculate_active_customers."""

    def test_returns_dataframe(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "customer_id": ["CUST-1"],
                "active": [True],
            }
        )

        result = calculate_active_customers(df)

        assert isinstance(result, pd.DataFrame)

    def test_expected_columns(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "customer_id": ["CUST-1"],
                "active": [True],
            }
        )

        result = calculate_active_customers(df)

        assert set(result.columns) == {"year_month", "active_customers"}

    def test_counts_unique_active_customers(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-01",
                ],
                "customer_id": [
                    "C1",
                    "C2",
                    "C3",
                ],
                "active": [
                    True,
                    True,
                    True,
                ],
            }
        )

        result = calculate_active_customers(df)

        assert result["active_customers"].iloc[0] == 3

    def test_ignores_inactive_customers(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                ],
                "customer_id": [
                    "C1",
                    "C2",
                ],
                "active": [
                    True,
                    False,
                ],
            }
        )

        result = calculate_active_customers(df)

        assert result["active_customers"].iloc[0] == 1

    def test_counts_unique_ids_only(self):
        """Duplicate rows should not inflate counts."""
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-01",
                ],
                "customer_id": [
                    "C1",
                    "C1",
                    "C2",
                ],
                "active": [
                    True,
                    True,
                    True,
                ],
            }
        )

        result = calculate_active_customers(df)

        assert result["active_customers"].iloc[0] == 2

    def test_multiple_months(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-02-01",
                ],
                "customer_id": [
                    "C1",
                    "C2",
                    "C1",
                ],
                "active": [
                    True,
                    True,
                    True,
                ],
            }
        )

        result = calculate_active_customers(df)

        jan = result[result["year_month"] == "2024-01-01"]["active_customers"].iloc[0]
        feb = result[result["year_month"] == "2024-02-01"]["active_customers"].iloc[0]

        assert jan == 2
        assert feb == 1

    def test_empty_dataframe(self):
        df = pd.DataFrame(
            columns=["year_month", "customer_id", "active"]
        )

        result = calculate_active_customers(df)

        assert result.empty

class TestCalculateNewCustomers:
    """Unit tests for calculate_new_customers."""

    def test_returns_dataframe(self):
        df = pd.DataFrame(
            {
                "customer_id": ["C1"],
                "year_month": ["2024-01-01"],
            }
        )

        result = calculate_new_customers(df)

        assert isinstance(result, pd.DataFrame)

    def test_expected_columns(self):
        df = pd.DataFrame(
            {
                "customer_id": ["C1"],
                "year_month": ["2024-01-01"],
            }
        )

        result = calculate_new_customers(df)

        assert set(result.columns) == {"year_month", "new_customers"}

    def test_single_customer(self):
        df = pd.DataFrame(
            {
                "customer_id": ["C1"],
                "year_month": ["2024-01-01"],
            }
        )

        result = calculate_new_customers(df)

        assert result["new_customers"].iloc[0] == 1

    def test_multiple_customers_same_month(self):
        df = pd.DataFrame(
            {
                "customer_id": ["C1", "C2", "C3"],
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-01",
                ],
            }
        )

        result = calculate_new_customers(df)

        assert result["new_customers"].iloc[0] == 3

    def test_customer_appearing_multiple_months(self):
        """Customer should count only in first month."""
        df = pd.DataFrame(
            {
                "customer_id": [
                    "C1",
                    "C1",
                    "C1",
                ],
                "year_month": [
                    "2024-01-01",
                    "2024-02-01",
                    "2024-03-01",
                ],
            }
        )

        result = calculate_new_customers(df)

        assert result["new_customers"].iloc[0] == 1
        assert len(result) == 1

    def test_multiple_months_acquisition(self):
        df = pd.DataFrame(
            {
                "customer_id": [
                    "C1",
                    "C2",
                    "C3",
                    "C4",
                ],
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-02-01",
                    "2024-03-01",
                ],
            }
        )

        result = calculate_new_customers(df)

        jan = result[result["year_month"] == "2024-01-01"]["new_customers"].iloc[0]
        feb = result[result["year_month"] == "2024-02-01"]["new_customers"].iloc[0]
        mar = result[result["year_month"] == "2024-03-01"]["new_customers"].iloc[0]

        assert jan == 2
        assert feb == 1
        assert mar == 1

    def test_duplicate_rows(self):
        """Duplicate records should not create extra customers."""
        df = pd.DataFrame(
            {
                "customer_id": [
                    "C1",
                    "C1",
                    "C2",
                ],
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-01",
                ],
            }
        )

        result = calculate_new_customers(df)

        assert result["new_customers"].iloc[0] == 2

    def test_empty_dataframe(self):
        df = pd.DataFrame(
            columns=["customer_id", "year_month"]
        )

        result = calculate_new_customers(df)

        assert result.empty

class TestCalculateChurnedCustomers:
    """Unit tests for calculate_churned_customers."""

    def test_returns_dataframe(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "customer_id": ["C1"],
                "churn_flag": [True],
            }
        )

        result = calculate_churned_customers(df)

        assert isinstance(result, pd.DataFrame)

    def test_expected_columns(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "customer_id": ["C1"],
                "churn_flag": [True],
            }
        )

        result = calculate_churned_customers(df)

        assert set(result.columns) == {"year_month", "churned_customers"}

    def test_single_churn(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "customer_id": ["C1"],
                "churn_flag": [True],
            }
        )

        result = calculate_churned_customers(df)

        assert result["churned_customers"].iloc[0] == 1

    def test_multiple_churn_same_month(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-01",
                ],
                "customer_id": [
                    "C1",
                    "C2",
                    "C3",
                ],
                "churn_flag": [
                    True,
                    True,
                    True,
                ],
            }
        )

        result = calculate_churned_customers(df)

        assert result["churned_customers"].iloc[0] == 3

    def test_ignores_non_churn_rows(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                ],
                "customer_id": [
                    "C1",
                    "C2",
                ],
                "churn_flag": [
                    True,
                    False,
                ],
            }
        )

        result = calculate_churned_customers(df)

        assert result["churned_customers"].iloc[0] == 1

    def test_multiple_months(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-02-01",
                    "2024-02-01",
                ],
                "customer_id": [
                    "C1",
                    "C2",
                    "C3",
                ],
                "churn_flag": [
                    True,
                    True,
                    True,
                ],
            }
        )

        result = calculate_churned_customers(df)

        jan = result[result["year_month"] == "2024-01-01"]["churned_customers"].iloc[0]
        feb = result[result["year_month"] == "2024-02-01"]["churned_customers"].iloc[0]

        assert jan == 1
        assert feb == 2

    def test_no_churn_returns_empty(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                ],
                "customer_id": [
                    "C1",
                    "C2",
                ],
                "churn_flag": [
                    False,
                    False,
                ],
            }
        )

        result = calculate_churned_customers(df)

        assert result.empty

    def test_empty_dataframe(self):
        df = pd.DataFrame(
            columns=["year_month", "customer_id", "churn_flag"]
        )

        result = calculate_churned_customers(df)

        assert result.empty

class TestCalculateExpansionRevenue:
    """Unit tests for calculate_expansion_revenue."""

    def test_returns_dataframe(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "monthly_revenue": [79],
                "expansion_flag": [True],
            }
        )

        result = calculate_expansion_revenue(df)

        assert isinstance(result, pd.DataFrame)

    def test_expected_columns(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "monthly_revenue": [79],
                "expansion_flag": [True],
            }
        )

        result = calculate_expansion_revenue(df)

        assert set(result.columns) == {"year_month", "expansion_revenue"}

    def test_single_expansion(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "monthly_revenue": [79],
                "expansion_flag": [True],
            }
        )

        result = calculate_expansion_revenue(df)

        assert result["expansion_revenue"].iloc[0] == 79

    def test_multiple_expansions_same_month(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                ],
                "monthly_revenue": [
                    79,
                    199,
                ],
                "expansion_flag": [
                    True,
                    True,
                ],
            }
        )

        result = calculate_expansion_revenue(df)

        assert result["expansion_revenue"].iloc[0] == 278

    def test_ignores_non_expansion_rows(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                ],
                "monthly_revenue": [
                    79,
                    29,
                ],
                "expansion_flag": [
                    True,
                    False,
                ],
            }
        )

        result = calculate_expansion_revenue(df)

        assert result["expansion_revenue"].iloc[0] == 79

    def test_multiple_months(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-02-01",
                    "2024-02-01",
                ],
                "monthly_revenue": [
                    79,
                    199,
                    79,
                ],
                "expansion_flag": [
                    True,
                    True,
                    True,
                ],
            }
        )

        result = calculate_expansion_revenue(df)

        jan = result[result["year_month"] == "2024-01-01"]["expansion_revenue"].iloc[0]
        feb = result[result["year_month"] == "2024-02-01"]["expansion_revenue"].iloc[0]

        assert jan == 79
        assert feb == 278

    def test_no_expansion_returns_empty(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-01-01",
                ],
                "monthly_revenue": [
                    79,
                    29,
                ],
                "expansion_flag": [
                    False,
                    False,
                ],
            }
        )

        result = calculate_expansion_revenue(df)

        assert result.empty

    def test_empty_dataframe(self):
        df = pd.DataFrame(
            columns=["year_month", "monthly_revenue", "expansion_flag"]
        )

        result = calculate_expansion_revenue(df)

        assert result.empty

class TestCalculateChurnRate:
    """Unit tests for calculate_churn_rate."""

    def test_returns_dataframe(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "active_customers": [100],
                "churned_customers": [2],
            }
        )

        result = calculate_churn_rate(df.copy())

        assert isinstance(result, pd.DataFrame)

    def test_creates_expected_columns(self):
        df = pd.DataFrame(
            {
                "year_month": ["2024-01-01"],
                "active_customers": [100],
                "churned_customers": [2],
            }
        )

        result = calculate_churn_rate(df.copy())

        assert "active_prev_month" in result.columns
        assert "churn_rate" in result.columns

    def test_first_month_has_nan_values(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-02-01",
                ],
                "active_customers": [
                    100,
                    110,
                ],
                "churned_customers": [
                    2,
                    3,
                ],
            }
        )

        result = calculate_churn_rate(df.copy())

        assert np.isnan(result["active_prev_month"].iloc[0])
        assert np.isnan(result["churn_rate"].iloc[0])

    def test_correct_previous_month_shift(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-02-01",
                    "2024-03-01",
                ],
                "active_customers": [
                    100,
                    120,
                    130,
                ],
                "churned_customers": [
                    2,
                    4,
                    5,
                ],
            }
        )

        result = calculate_churn_rate(df.copy())

        assert result["active_prev_month"].iloc[1] == 100
        assert result["active_prev_month"].iloc[2] == 120

    def test_correct_churn_rate_calculation(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-02-01",
                ],
                "active_customers": [
                    100,
                    110,
                ],
                "churned_customers": [
                    2,
                    5,
                ],
            }
        )

        result = calculate_churn_rate(df.copy())

        expected = 5 / 100
        actual = result["churn_rate"].iloc[1]

        assert actual == expected

    def test_multiple_months_calculation(self):
        df = pd.DataFrame(
            {
                "year_month": [
                    "2024-01-01",
                    "2024-02-01",
                    "2024-03-01",
                ],
                "active_customers": [
                    200,
                    210,
                    220,
                ],
                "churned_customers": [
                    3,
                    4,
                    5,
                ],
            }
        )

        result = calculate_churn_rate(df.copy())

        feb_rate = result["churn_rate"].iloc[1]
        mar_rate = result["churn_rate"].iloc[2]

        assert feb_rate == 4 / 200
        assert mar_rate == 5 / 210

    def test_empty_dataframe(self):
        df = pd.DataFrame(
            columns=[
                "year_month",
                "active_customers",
                "churned_customers",
            ]
        )

        result = calculate_churn_rate(df.copy())

        assert result.empty