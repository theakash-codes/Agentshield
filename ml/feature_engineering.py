import pandas as pd
import numpy as np
from pathlib import Path


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "ml" / "data"

TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"
OUTPUT_FILE = DATA_DIR / "transaction_features.csv"


# --------------------------------------------------
# 2. LOAD TRANSACTION DATA
# --------------------------------------------------

print("Loading transaction data...")

df = pd.read_csv(TRANSACTIONS_FILE)

print(f"Loaded {len(df)} transactions")


# --------------------------------------------------
# 3. CONVERT TIMESTAMP
# --------------------------------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["hour"] = df["timestamp"].dt.hour

df["day_of_week"] = df["timestamp"].dt.dayofweek


# --------------------------------------------------
# 4. TIME-BASED FEATURES
# --------------------------------------------------

# Normal working hours
df["is_unusual_hour"] = (
    (df["hour"] < 7) |
    (df["hour"] > 22)
).astype(int)


# Weekend indicator
df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)


# --------------------------------------------------
# 5. AMOUNT FEATURES
# --------------------------------------------------

df["amount"] = df["amount"].astype(float)

# Log transformation helps reduce the effect
# of extremely large transaction values.
df["log_amount"] = np.log1p(df["amount"])


# --------------------------------------------------
# 6. AGENT BEHAVIOR FEATURES
# --------------------------------------------------

print("Calculating agent behavior...")

agent_stats = df.groupby("agent_id").agg(
    agent_avg_amount=("amount", "mean"),
    agent_median_amount=("amount", "median"),
    agent_std_amount=("amount", "std"),
    agent_max_amount=("amount", "max"),
    agent_transaction_count=("amount", "count")
).reset_index()


df = df.merge(
    agent_stats,
    on="agent_id",
    how="left"
)


# --------------------------------------------------
# 7. AMOUNT DEVIATION
# --------------------------------------------------

df["amount_ratio"] = (
    df["amount"] /
    (df["agent_avg_amount"] + 1)
)


df["amount_zscore"] = (
    (df["amount"] - df["agent_avg_amount"]) /
    (df["agent_std_amount"] + 1)
)


# --------------------------------------------------
# 8. ACTION FEATURES
# --------------------------------------------------

df["is_refund"] = (
    df["action_type"] == "REFUND"
).astype(int)

df["is_payout"] = (
    df["action_type"] == "PAYOUT"
).astype(int)

df["is_payment"] = (
    df["action_type"] == "PAYMENT"
).astype(int)


# --------------------------------------------------
# 9. NEW BENEFICIARY FEATURE
# --------------------------------------------------

print("Calculating beneficiary behavior...")

# Sort transactions chronologically
df = df.sort_values(
    ["agent_id", "timestamp"]
).reset_index(drop=True)


# Track whether this agent has previously
# interacted with this beneficiary.

df["previous_beneficiary_count"] = (
    df.groupby(
        ["agent_id", "beneficiary_id"]
    ).cumcount()
)


df["is_new_beneficiary"] = (
    df["previous_beneficiary_count"] == 0
).astype(int)


# --------------------------------------------------
# 10. DEVICE CHANGE FEATURE
# --------------------------------------------------

df["previous_device"] = (
    df.groupby("agent_id")["device_id"]
    .shift(1)
)


df["is_device_change"] = (
    (
        df["device_id"] != df["previous_device"]
    ) &
    df["previous_device"].notna()
).astype(int)


# --------------------------------------------------
# 11. IP CHANGE FEATURE
# --------------------------------------------------

df["previous_ip"] = (
    df.groupby("agent_id")["ip_address"]
    .shift(1)
)


df["is_ip_change"] = (
    (
        df["ip_address"] != df["previous_ip"]
    ) &
    df["previous_ip"].notna()
).astype(int)


# --------------------------------------------------
# 12. TRANSACTION FREQUENCY
# --------------------------------------------------

print("Calculating transaction frequency...")

# Make sure transactions are sorted by agent and time
df = df.sort_values(
    ["agent_id", "timestamp"]
).reset_index(drop=True)


def calculate_transaction_frequency(group):
    """
    Calculate how many previous transactions
    the agent performed during the previous 10 minutes.
    """

    timestamps = group["timestamp"]

    counts = []

    for i, current_time in enumerate(timestamps):

        window_start = current_time - pd.Timedelta(minutes=10)

        previous_transactions = (
            (timestamps.iloc[:i] >= window_start) &
            (timestamps.iloc[:i] < current_time)
        ).sum()

        counts.append(previous_transactions)

    group = group.copy()

    group["transaction_count_last_10"] = counts

    return group


df = (
    df.groupby("agent_id", group_keys=False)
    .apply(calculate_transaction_frequency)
    .reset_index(drop=True)
)


# --------------------------------------------------
# 13. FAILED ACTION FEATURE
# --------------------------------------------------

df["is_failed"] = (
    df["status"] != "SUCCESS"
).astype(int)


# Calculate the historical failure rate for each agent.
#
# IMPORTANT:
# We shift by one transaction so that the current
# transaction does not influence its own risk score.

df["previous_failed_count"] = (
    df.groupby("agent_id")["is_failed"]
    .cumsum()
    .shift(1)
    .fillna(0)
)


df["previous_transaction_count"] = (
    df.groupby("agent_id")
    .cumcount()
)


df["agent_failure_rate"] = (
    df["previous_failed_count"] /
    (df["previous_transaction_count"] + 1)
)

# --------------------------------------------------
# 14. SELECT ML FEATURES
# --------------------------------------------------

feature_columns = [
    "amount",
    "log_amount",
    "hour",
    "day_of_week",
    "is_unusual_hour",
    "is_weekend",

    "agent_avg_amount",
    "agent_median_amount",
    "agent_std_amount",
    "agent_max_amount",
    "agent_transaction_count",

    "amount_ratio",
    "amount_zscore",

    "is_refund",
    "is_payout",
    "is_payment",

    "is_new_beneficiary",
    "is_device_change",
    "is_ip_change",

    "transaction_count_last_10",
    "is_failed",
    "agent_failure_rate"
]


# --------------------------------------------------
# 15. CLEAN DATA
# --------------------------------------------------

features = df[
    feature_columns
].copy()


features = features.replace(
    [np.inf, -np.inf],
    np.nan
)


features = features.fillna(0)


# --------------------------------------------------
# 16. SAVE FEATURE DATASET
# --------------------------------------------------

features.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nFeature engineering completed!")

print(f"Output file: {OUTPUT_FILE}")

print(f"Rows: {len(features)}")

print(f"Features: {len(features.columns)}")

print("\nFeature columns:")

for column in features.columns:
    print(f" - {column}")