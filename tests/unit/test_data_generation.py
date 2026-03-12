import pytest
import numpy as np
import pandas as pd

from config import settings
from src.data_generation import (
    sample_from_distribution,
    generate_customer_ids,
    generate_customers,
    save_customers,
    simulate_acquisition,
    simulate_churn,
    simulate_expansion,
    generate_subscription_history
    )


class TestSampleFromDistribution:
    """Unit tests for the sample_from_distribution utility."""

    def test_returns_correct_sample_size(self):
        """Should return a list with the requested number of samples."""
        distribution = {"Basic": 0.5, "Pro": 0.3, "Enterprise": 0.2}

        result = sample_from_distribution(distribution, size=100)

        assert isinstance(result, list)
        assert len(result) == 100

    def test_returns_only_valid_categories(self):
        """All sampled values must belong to the distribution categories."""
        distribution = {"Basic": 0.5, "Pro": 0.3, "Enterprise": 0.2}

        result = sample_from_distribution(distribution, size=200)

        assert set(result).issubset(distribution.keys())

    def test_sampling_respects_probability_distribution(self):
        """
        With a large enough sample, the observed proportions
        should roughly match the input probability distribution.
        """
        np.random.seed(42)

        distribution = {"Basic": 0.6, "Pro": 0.3, "Enterprise": 0.1}
        size = 10000

        result = sample_from_distribution(distribution, size=size)

        counts = {k: result.count(k) / size for k in distribution.keys()}

        for category, expected_prob in distribution.items():
            assert pytest.approx(counts[category], rel=0.1) == expected_prob

    def test_empty_distribution_raises_error(self):
        """An empty distribution should raise an error."""
        with pytest.raises(ValueError):
            sample_from_distribution({}, size=10)

    def test_invalid_probability_sum(self):
        """
        If probabilities do not sum to 1, numpy should raise an error.
        """
        invalid_distribution = {"Basic": 0.5, "Pro": 0.5, "Enterprise": 0.5}

        with pytest.raises(ValueError):
            sample_from_distribution(invalid_distribution, size=10)

class TestGenerateCustomerIds:
    """Unit tests for the generate_customer_ids function."""

    def test_returns_correct_number_of_ids(self):
        """Should generate the requested number of customer IDs."""
        result = generate_customer_ids(10)

        assert isinstance(result, list)
        assert len(result) == 10

    def test_ids_are_unique(self):
        """All generated IDs must be unique."""
        result = generate_customer_ids(100)

        assert len(result) == len(set(result))

    def test_ids_follow_expected_format(self):
        """IDs should follow the CUST-000001 format."""
        result = generate_customer_ids(3)

        assert result == [
            "CUST-000001",
            "CUST-000002",
            "CUST-000003",
        ]

    def test_last_id_matches_expected_sequence(self):
        """The final ID should match the expected sequential number."""
        n = 50
        result = generate_customer_ids(n)

        assert result[-1] == "CUST-000050"

    def test_zero_customers_returns_empty_list(self):
        """Requesting zero customers should return an empty list."""
        result = generate_customer_ids(0)

        assert result == []

    @pytest.mark.parametrize(
        "n,expected_first",
        [
            (1, "CUST-000001"),
            (5, "CUST-000001"),
            (10, "CUST-000001"),
        ],
    )
    def test_first_id_is_always_correct(self, n, expected_first):
        """The first generated ID should always be CUST-000001."""
        result = generate_customer_ids(n)

        assert result[0] == expected_first

class TestGenerateCustomers:
    """Unit tests for the generate_customers function."""

    def test_returns_dataframe(self):
        """Function should return a pandas DataFrame."""
        df = generate_customers(initial_customers=10)

        assert isinstance(df, pd.DataFrame)

    def test_dataframe_has_expected_columns(self):
        """Generated dataset should contain the expected schema."""
        df = generate_customers(initial_customers=5)

        expected_columns = {
            "customer_id",
            "signup_date",
            "plan_initial",
            "country",
            "acquisition_channel",
        }

        assert set(df.columns) == expected_columns

    def test_generates_correct_number_of_customers(self):
        """The number of rows should match the requested customer count."""
        n = 50
        df = generate_customers(initial_customers=n)

        assert len(df) == n

    def test_customer_ids_are_unique(self):
        """Customer IDs must be unique."""
        df = generate_customers(initial_customers=200)

        assert df["customer_id"].is_unique

    def test_signup_date_is_correct(self):
        """All customers should have the provided signup date."""
        start_date = "2024-01-01"

        df = generate_customers(initial_customers=20, start_date=start_date)

        expected_date = pd.to_datetime(start_date)

        assert (df["signup_date"] == expected_date).all()

    def test_plan_values_within_distribution(self):
        """Plan values must exist in PLAN_DISTRIBUTION."""
        df = generate_customers(initial_customers=100)

        valid_plans = set(settings.PLAN_DISTRIBUTION.keys())

        assert set(df["plan_initial"]).issubset(valid_plans)

    def test_country_values_within_distribution(self):
        """Country values must exist in COUNTRY_DISTRIBUTION."""
        df = generate_customers(initial_customers=100)

        valid_countries = set(settings.COUNTRY_DISTRIBUTION.keys())

        assert set(df["country"]).issubset(valid_countries)

    def test_acquisition_channel_values_within_distribution(self):
        """Channels must exist in ACQUISITION_CHANNELS."""
        df = generate_customers(initial_customers=100)

        valid_channels = set(settings.ACQUISITION_CHANNELS.keys())

        assert set(df["acquisition_channel"]).issubset(valid_channels)

    def test_zero_customers_returns_empty_dataframe(self):
        """Requesting zero customers should return an empty dataframe."""
        df = generate_customers(initial_customers=0)

        assert isinstance(df, pd.DataFrame)
        assert df.empty

class TestSaveCustomers:
    """Unit tests for the save_customers function."""

    def test_creates_csv_file(self, tmp_path):
        """Function should create a CSV file at the specified path."""

        df = pd.DataFrame(
            {
                "customer_id": ["CUST-000001"],
                "signup_date": ["2024-01-01"],
                "plan_initial": ["Basic"],
                "country": ["US"],
                "acquisition_channel": ["Organic"],
            }
        )

        file_path = tmp_path / "customers.csv"

        save_customers(df, file_path)

        assert file_path.exists()

    def test_saved_csv_matches_dataframe(self, tmp_path):
        """Saved CSV content should match the input DataFrame."""

        df = pd.DataFrame(
            {
                "customer_id": ["CUST-000001", "CUST-000002"],
                "signup_date": ["2024-01-01", "2024-01-01"],
                "plan_initial": ["Basic", "Pro"],
                "country": ["US", "DE"],
                "acquisition_channel": ["Organic", "Referral"],
            }
        )

        file_path = tmp_path / "customers.csv"

        save_customers(df, file_path)

        loaded_df = pd.read_csv(file_path)

        pd.testing.assert_frame_equal(df, loaded_df)

    def test_csv_is_saved_without_index(self, tmp_path):
        """CSV file should not contain an index column."""

        df = pd.DataFrame(
            {
                "customer_id": ["CUST-000001"],
                "signup_date": ["2024-01-01"],
                "plan_initial": ["Basic"],
                "country": ["US"],
                "acquisition_channel": ["Organic"],
            }
        )

        file_path = tmp_path / "customers.csv"

        save_customers(df, file_path)

        loaded_df = pd.read_csv(file_path)

        assert "Unnamed: 0" not in loaded_df.columns

class TestSimulateAcquisition:
    """Unit tests for the simulate_acquisition function."""

    def test_returns_dataframe(self):
        """Function should return a pandas DataFrame."""
        df = simulate_acquisition(months=12)

        assert isinstance(df, pd.DataFrame)

    def test_dataframe_has_expected_columns(self):
        """Output should contain the expected schema."""
        df = simulate_acquisition(months=12)

        expected_columns = {"year_month", "new_customers"}

        assert set(df.columns) == expected_columns

    def test_correct_number_of_months(self):
        """DataFrame length should match the requested number of months."""
        months = 24

        df = simulate_acquisition(months=months)

        assert len(df) == months

    def test_year_month_is_datetime(self):
        """year_month column must be datetime."""
        df = simulate_acquisition(months=12)

        assert pd.api.types.is_datetime64_any_dtype(df["year_month"])

    def test_month_sequence_is_continuous(self):
        """Months should follow a continuous monthly sequence."""
        months = 12

        df = simulate_acquisition(months=months)

        expected_dates = pd.date_range(
            start=settings.START_DATE,
            periods=months,
            freq="MS"
        )

        pd.testing.assert_series_equal(
            df["year_month"].reset_index(drop=True),
            pd.Series(expected_dates, name="year_month"),
        )

    def test_new_customers_are_non_negative(self):
        """Acquisition values must never be negative."""
        df = simulate_acquisition(months=36)

        assert (df["new_customers"] >= 0).all()

    def test_new_customers_are_integers(self):
        """Acquisition values should be integers."""
        df = simulate_acquisition(months=36)

        assert pd.api.types.is_integer_dtype(df["new_customers"])

    def test_acquisition_respects_upper_bound(self):
        """
        Acquisition should not significantly exceed the theoretical maximum.
        Allows tolerance due to noise.
        """
        max_acq = 300

        df = simulate_acquisition(
            months=36,
            max_monthly_acquisition=max_acq,
            noise_scale=5
        )

        assert df["new_customers"].max() <= max_acq * 1.5

    def test_reproducibility_with_seed(self):
        """Setting a random seed should produce reproducible results."""
        np.random.seed(42)
        df1 = simulate_acquisition(months=12)

        np.random.seed(42)
        df2 = simulate_acquisition(months=12)

        pd.testing.assert_frame_equal(df1, df2)

class TestSimulateChurn:
    """Unit tests for the simulate_churn function."""

    def test_returns_boolean(self):
        """Function should always return a boolean."""
        rng = np.random.default_rng(42)

        result = simulate_churn("Basic", 5, rng)

        assert isinstance(result, bool)

    def test_reproducibility_with_seed(self):
        """Using the same RNG seed should produce reproducible results."""
        rng1 = np.random.default_rng(42)
        rng2 = np.random.default_rng(42)

        result1 = simulate_churn("Pro", 10, rng1)
        result2 = simulate_churn("Pro", 10, rng2)

        assert result1 == result2

    def test_hypergrowth_phase_probability_behavior(self):
        """
        In hypergrowth phase Basic churn probability should be
        roughly around the defined value.
        """
        rng = np.random.default_rng(42)

        trials = 10000
        churns = sum(
            simulate_churn("Basic", 5, rng) for _ in range(trials)
        )

        observed_rate = churns / trials

        assert pytest.approx(observed_rate, rel=0.2) == 0.03

    def test_expansion_phase_probability_behavior(self):
        """Test approximate churn probability during expansion phase."""
        rng = np.random.default_rng(42)

        trials = 10000
        churns = sum(
            simulate_churn("Pro", 15, rng) for _ in range(trials)
        )

        observed_rate = churns / trials

        assert pytest.approx(observed_rate, rel=0.2) == 0.03

    def test_competitive_phase_probability_behavior(self):
        """Test approximate churn probability during competitive phase."""
        rng = np.random.default_rng(42)

        trials = 10000
        churns = sum(
            simulate_churn("Enterprise", 30, rng) for _ in range(trials)
        )

        observed_rate = churns / trials

        assert pytest.approx(observed_rate, rel=0.25) == 0.02

    @pytest.mark.parametrize(
        "month_index,expected_phase_prob",
        [
            (5, 0.03),   # hypergrowth
            (15, 0.04),  # expansion
            (30, 0.06),  # competitive
        ],
    )
    def test_churn_probability_increases_for_basic_plan(
        self, month_index, expected_phase_prob
    ):
        """
        Basic plan churn probability should increase across lifecycle phases.
        """
        rng = np.random.default_rng(123)

        trials = 8000
        churns = sum(
            simulate_churn("Basic", month_index, rng) for _ in range(trials)
        )

        observed_rate = churns / trials

        assert pytest.approx(observed_rate, rel=0.25) == expected_phase_prob

    def test_invalid_plan_raises_key_error(self):
        """Invalid plan should raise a KeyError."""
        rng = np.random.default_rng(42)

        with pytest.raises(KeyError):
            simulate_churn("InvalidPlan", 5, rng)

class TestSimulateExpansion:
    """Unit tests for the simulate_expansion function."""

    def test_returns_expected_types(self):
        """Function should return (plan:str, upgraded:bool)."""
        rng = np.random.default_rng(42)

        new_plan, upgraded = simulate_expansion("Basic", rng)

        assert isinstance(new_plan, str)
        assert isinstance(upgraded, bool)

    def test_reproducibility_with_seed(self):
        """Using the same RNG seed should produce reproducible results."""
        rng1 = np.random.default_rng(42)
        rng2 = np.random.default_rng(42)

        result1 = simulate_expansion("Basic", rng1)
        result2 = simulate_expansion("Basic", rng2)

        assert result1 == result2

    def test_enterprise_never_upgrades(self):
        """Enterprise plan should never upgrade."""
        rng = np.random.default_rng(42)

        trials = 1000
        upgrades = [
            simulate_expansion("Enterprise", rng) for _ in range(trials)
        ]

        for plan, upgraded in upgrades:
            assert plan == "Enterprise"
            assert upgraded is False

    def test_basic_upgrades_to_pro_only(self):
        """Basic plan upgrades should only go to Pro."""
        rng = np.random.default_rng(42)

        trials = 5000

        for _ in range(trials):
            plan, upgraded = simulate_expansion("Basic", rng)

            if upgraded:
                assert plan == "Pro"

    def test_pro_upgrades_to_enterprise_only(self):
        """Pro plan upgrades should only go to Enterprise."""
        rng = np.random.default_rng(42)

        trials = 5000

        for _ in range(trials):
            plan, upgraded = simulate_expansion("Pro", rng)

            if upgraded:
                assert plan == "Enterprise"

    def test_upgrade_probability_basic(self):
        """Basic upgrade probability should be around 5%."""
        rng = np.random.default_rng(42)

        trials = 10000
        upgrades = sum(
            simulate_expansion("Basic", rng)[1] for _ in range(trials)
        )

        observed_rate = upgrades / trials

        assert pytest.approx(observed_rate, rel=0.25) == 0.05

    def test_upgrade_probability_pro(self):
        """Pro upgrade probability should be around 3%."""
        rng = np.random.default_rng(42)

        trials = 10000
        upgrades = sum(
            simulate_expansion("Pro", rng)[1] for _ in range(trials)
        )

        observed_rate = upgrades / trials

        assert pytest.approx(observed_rate, rel=0.25) == 0.03

    def test_invalid_plan_raises_key_error(self):
        """Invalid plan should raise a KeyError."""
        rng = np.random.default_rng(42)

        with pytest.raises(KeyError):
            simulate_expansion("InvalidPlan", rng)

class TestGenerateSubscriptionHistory:
    """Integration-style tests for the subscription history simulation."""

    def setup_method(self):
        """Prepare small deterministic datasets for testing."""
        self.customers = generate_customers(initial_customers=5)

        self.acquisition = simulate_acquisition(
            months=6,
            max_monthly_acquisition=3,
            noise_scale=0,
        )

    def test_returns_dataframe(self):
        """Function should return a pandas DataFrame."""
        df = generate_subscription_history(
            self.customers,
            self.acquisition,
            months=6,
            random_seed=42,
        )

        assert isinstance(df, pd.DataFrame)

    def test_expected_columns(self):
        """Dataset must contain the expected schema."""
        df = generate_subscription_history(
            self.customers,
            self.acquisition,
            months=6,
        )

        expected_columns = {
            "customer_id",
            "year_month",
            "plan_current",
            "active",
            "monthly_revenue",
            "expansion_flag",
            "churn_flag",
        }

        assert set(df.columns) == expected_columns

    def test_year_month_dtype(self):
        """year_month must be datetime."""
        df = generate_subscription_history(
            self.customers,
            self.acquisition,
            months=6,
        )

        assert pd.api.types.is_datetime64_any_dtype(df["year_month"])

    def test_no_negative_revenue(self):
        """Revenue values must never be negative."""
        df = generate_subscription_history(
            self.customers,
            self.acquisition,
            months=6,
        )

        assert (df["monthly_revenue"] >= 0).all()

    def test_revenue_zero_when_inactive(self):
        """Inactive customers should not generate revenue."""
        df = generate_subscription_history(
            self.customers,
            self.acquisition,
            months=6,
        )

        inactive = df[df["active"] == False]

        assert (inactive["monthly_revenue"] == 0).all()

    def test_plan_values_are_valid(self):
        """Plans should only be valid SaaS plans."""
        df = generate_subscription_history(
            self.customers,
            self.acquisition,
            months=6,
        )

        valid_plans = {"Basic", "Pro", "Enterprise"}

        assert set(df["plan_current"]).issubset(valid_plans)

    def test_reproducibility_with_seed(self):
        """Setting a random seed should produce reproducible results."""

        customers_df = generate_customers(100)
        acquisition_df = simulate_acquisition(months=12)

        df1 = generate_subscription_history(
            customers_df,
            acquisition_df,
            months=12,
            random_seed=42,
        )

        df2 = generate_subscription_history(
            customers_df,
            acquisition_df,
            months=12,
            random_seed=42,
        )

        pd.testing.assert_frame_equal(df1, df2)

    def test_records_exist_for_each_month(self):
        """Each month should appear in the output dataset."""
        df = generate_subscription_history(
            self.customers,
            self.acquisition,
            months=6,
        )

        assert df["year_month"].nunique() == 6

    def test_customer_id_format(self):
        """Customer IDs must follow the expected format."""
        df = generate_subscription_history(
            self.customers,
            self.acquisition,
            months=6,
        )

        assert df["customer_id"].str.startswith("CUST-").all()