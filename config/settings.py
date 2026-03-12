"""
Project configuration module.

This file centralizes all global settings used across the project,
including paths, simulation parameters, and business constants.

Keeping configuration isolated improves maintainability and
prevents hardcoding values throughout the codebase.
"""

from pathlib import Path
import numpy as np

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

STREAMLIT_DIR = PROJECT_ROOT / "streamlit_app"
REPORTS_DIR = PROJECT_ROOT / "reports"


# ---------------------------------------------------------
# Random seed configuration
# ---------------------------------------------------------

RANDOM_SEED = 42


# ---------------------------------------------------------
# Simulation parameters
# ---------------------------------------------------------

N_INITIAL_CUSTOMERS = 1000
SIMULATION_MONTHS = 36
START_DATE = "2022-01-01"


# ---------------------------------------------------------
# SaaS business configuration
# ---------------------------------------------------------

PLAN_DISTRIBUTION = {
    "Basic": 0.60,
    "Pro": 0.30,
    "Enterprise": 0.10,
}

COUNTRY_DISTRIBUTION = {
    "US": 0.60,
    "UK": 0.20,
    "Germany": 0.20,
}

ACQUISITION_CHANNELS = {
    "Organic": 0.40,
    "Paid Ads": 0.30,
    "Referral": 0.20,
    "Sales Team": 0.10,
}


# ---------------------------------------------------------
# Plan pricing configuration
# ---------------------------------------------------------

PLAN_PRICING = {
    "Basic": 29,
    "Pro": 79,
    "Enterprise": 199,
}


# ---------------------------------------------------------
# SaaS behavioral parameters
# ---------------------------------------------------------

MONTHLY_CHURN_RATE = 0.035

UPGRADE_PROBABILITIES = {
    "Basic": 0.05,
    "Pro": 0.03,
    "Enterprise": 0.00,
}


UPGRADE_PATHS = {
    "Basic": "Pro",
    "Pro": "Enterprise",
    "Enterprise": "Enterprise",
}