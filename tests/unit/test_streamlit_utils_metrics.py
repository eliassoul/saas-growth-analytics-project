import pytest
import pandas as pd

from streamlit_app.utils.metrics import (
    calculate_growth_rate,
    calculate_nrr,
    calculate_ltv,
    compute_kpis
    )

class CalculateGrowthRate:
    """Unit tests for the calculate_growth_rate function."""

    def test_growth_rate_positive():
        """Should compute positive growth correctly."""
        result = calculate_growth_rate(12000, 10000)

        assert result == pytest.approx(0.2)

    def test_growth_rate_negative():
        """Should compute negative growth correctly."""
        result = calculate_growth_rate(8000, 10000)

        assert result == pytest.approx(-0.2)

    def test_growth_rate_zero_growth():
        """Should return zero when MRR does not change."""
        result = calculate_growth_rate(10000, 10000)

        assert result == 0

    def test_growth_rate_previous_zero():
        """Should return zero when previous MRR is zero."""
        result = calculate_growth_rate(5000, 0)

        assert result == 0

class CalculateNrr:
    """Unit tests for the calculate_nrr function."""

    def test_calculate_nrr_standard_case():
        """Should compute NRR correctly with churn and expansion."""

        latest = {
            "mrr": 12000,
            "active_customers": 100,
            "churned_customers": 5,
            "expansion_revenue": 500,
        }

        previous = {"mrr": 11000}

        result = calculate_nrr(latest, previous)

        # churned revenue = 5 * (12000 / 100) = 600
        # (12000 + 500 - 600) / 11000 = 11900 / 11000
        expected = 11900 / 11000

        assert result == pytest.approx(expected)


    def test_calculate_nrr_without_expansion():
        """Should assume expansion revenue = 0 if not provided."""

        latest = {
            "mrr": 12000,
            "active_customers": 100,
            "churned_customers": 5,
        }

        previous = {"mrr": 11000}

        result = calculate_nrr(latest, previous)

        expected = (12000 - 600) / 11000

        assert result == pytest.approx(expected)


    def test_calculate_nrr_previous_zero():
        """Should return 0 when previous MRR is zero."""

        latest = {
            "mrr": 12000,
            "active_customers": 100,
            "churned_customers": 5,
            "expansion_revenue": 500,
        }

        previous = {"mrr": 0}

        result = calculate_nrr(latest, previous)

        assert result == 0


    def test_calculate_nrr_high_expansion():
        """NRR should exceed 1 when expansion outweighs churn."""

        latest = {
            "mrr": 12000,
            "active_customers": 100,
            "churned_customers": 2,
            "expansion_revenue": 2000,
        }

        previous = {"mrr": 11000}

        result = calculate_nrr(latest, previous)

        assert result > 1


    def test_calculate_nrr_high_churn():
        """NRR should drop below 1 when churn dominates."""

        latest = {
            "mrr": 12000,
            "active_customers": 100,
            "churned_customers": 20,
            "expansion_revenue": 0,
        }

        previous = {"mrr": 12000}

        result = calculate_nrr(latest, previous)

        assert result < 1

class CalculateLtv:
    """Unit tests for the calculate_ltv function."""

    def test_calculate_ltv_standard():
        """Should compute LTV correctly."""
        result = calculate_ltv(100, 0.05)

        assert result == pytest.approx(2000)


    def test_calculate_ltv_zero_churn():
        """Should return 0 when churn rate is zero."""
        result = calculate_ltv(100, 0)

        assert result == 0


    def test_calculate_ltv_high_churn():
        """High churn should produce lower LTV."""
        result = calculate_ltv(100, 0.5)

        assert result == pytest.approx(200)


    def test_calculate_ltv_small_churn():
        """Small churn should produce very high LTV."""
        result = calculate_ltv(100, 0.01)

        assert result == pytest.approx(10000)


    def test_calculate_ltv_zero_mrr():
        """Zero MRR should result in zero LTV."""
        result = calculate_ltv(0, 0.05)

        assert result == 0

class ComputeKips:
    """Unit tests for the compute_kpis function."""

    def test_compute_kpis_standard():
        """Should compute all KPIs correctly."""

        df = pd.DataFrame({
            "mrr": [10000, 11000, 12000],
            "churn_rate": [0.05, 0.04, 0.03],
            "active_customers": [100, 110, 120],
            "churned_customers": [5, 4, 3],
            "expansion_revenue": [500, 600, 700]
        })

        result = compute_kpis(df)

        assert result["mrr"] == 12000
        assert result["mrr_delta"] == 1000
        assert result["customers"] == 120

        assert result["growth_rate"] == pytest.approx(12000 / 11000 - 1)

        assert "nrr" in result
        assert "ltv" in result


    def test_compute_kpis_keys():
        """Should return all expected KPI keys."""

        df = pd.DataFrame({
            "mrr": [100, 200, 300],
            "churn_rate": [0.1, 0.1, 0.1],
            "active_customers": [10, 20, 30],
            "churned_customers": [1, 1, 1],
            "expansion_revenue": [0, 0, 0]
        })

        result = compute_kpis(df)

        expected_keys = {
            "mrr",
            "mrr_delta",
            "growth_rate",
            "growth_delta",
            "churn_rate",
            "nrr",
            "ltv",
            "customers",
        }

        assert expected_keys.issubset(result.keys())


    def test_compute_kpis_previous_mrr_zero():
        """Growth and NRR should handle previous MRR = 0."""

        df = pd.DataFrame({
            "mrr": [0, 100, 200],
            "churn_rate": [0.05, 0.05, 0.05],
            "active_customers": [10, 20, 30],
            "churned_customers": [1, 1, 1],
            "expansion_revenue": [0, 0, 0]
        })

        result = compute_kpis(df)

        assert result["growth_rate"] >= 0
        assert result["nrr"] >= 0


    def test_compute_kpis_zero_churn():
        """LTV should be zero if churn rate is zero."""

        df = pd.DataFrame({
            "mrr": [10000, 11000, 12000],
            "churn_rate": [0, 0, 0],
            "active_customers": [100, 110, 120],
            "churned_customers": [0, 0, 0],
            "expansion_revenue": [0, 0, 0]
        })

        result = compute_kpis(df)

        assert result["ltv"] == 0