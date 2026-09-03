import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "ml" / "data"

FEATURE_FILE = DATA_DIR / "transaction_features.csv"

MODEL_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_FILE = MODEL_DIR / "isolation_forest.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"


# --------------------------------------------------
# 2. LOAD FEATURES
# --------------------------------------------------

print("Loading feature dataset...")

df = pd.read_csv(FEATURE_FILE)

print(f"Loaded {len(df)} transactions")


# --------------------------------------------------
# 3. SELECT FEATURES
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

    "amount_ratio",
    "amount_zscore",

    "is_refund",
    "is_payout",
    "is_payment",

    "is_new_beneficiary",
    "is_device_change",
    "is_ip_change",

    "transaction_count_last_10",

    "agent_failure_rate"
]


X = df[feature_columns].copy()
# --------------------------------------------------
# 3.1 TRAIN ONLY ON NORMAL BEHAVIOR
# --------------------------------------------------

# The original synthetic dataset contains a known
# anomaly label. We use it ONLY to exclude anomalies
# from training.
#
# In a real production system, this label would come
# from historical trusted/clean data.

original_transactions = pd.read_csv(
    DATA_DIR / "transactions.csv"
)

normal_mask = (
    original_transactions["is_anomaly"] == 0
)

X_normal = X[normal_mask].copy()

print(
    f"Normal transactions used for training: "
    f"{len(X_normal)}"
)

# --------------------------------------------------
# 4. SCALE FEATURES
# --------------------------------------------------

print("Scaling features...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X_normal)


# --------------------------------------------------
# 5. TRAIN ISOLATION FOREST
# --------------------------------------------------

print("Training Isolation Forest...")

model = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42,
    n_jobs=-1
)

model.fit(X_scaled)


# --------------------------------------------------
# 6. GENERATE ANOMALY PREDICTIONS
# --------------------------------------------------

print("Detecting anomalies...")

# --------------------------------------------------
# 6. PREDICT ALL TRANSACTIONS
# --------------------------------------------------

X_all = df[feature_columns].copy()

X_all_scaled = scaler.transform(X_all)

predictions = model.predict(X_all_scaled)

df["anomaly_prediction"] = predictions


# --------------------------------------------------
# 7. GENERATE ANOMALY SCORE
# --------------------------------------------------

raw_scores = model.decision_function(
    X_all_scaled
)

# Lower Isolation Forest score means more anomalous.
# We invert it so higher = more suspicious.

df["anomaly_score"] = -raw_scores


# Normalize approximately to 0-100.

min_score = df["anomaly_score"].min()
max_score = df["anomaly_score"].max()

df["anomaly_score"] = (
    (df["anomaly_score"] - min_score)
    /
    (max_score - min_score + 1e-8)
) * 100

# --------------------------------------------------
# 8. SAVE MODEL
# --------------------------------------------------

print("Saving model...")

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    scaler,
    SCALER_FILE
)


# --------------------------------------------------
# 9. SAVE PREDICTIONS
# --------------------------------------------------

PREDICTION_FILE = (
    DATA_DIR /
    "transaction_predictions.csv"
)

df.to_csv(
    PREDICTION_FILE,
    index=False
)


# --------------------------------------------------
# 10. SUMMARY
# --------------------------------------------------

anomaly_count = (
    df["anomaly_prediction"] == -1
).sum()

normal_count = (
    df["anomaly_prediction"] == 1
).sum()


print("\n--------------------------------")
print("MODEL TRAINING COMPLETE")
print("--------------------------------")

print(f"Total transactions : {len(df)}")
print(f"Normal transactions: {normal_count}")
print(f"Anomalies detected  : {anomaly_count}")

print(
    f"Anomaly percentage  : "
    f"{anomaly_count / len(df) * 100:.2f}%"
)

print("\nModel saved to:")
print(MODEL_FILE)

print("\nScaler saved to:")
print(SCALER_FILE)

print("\nPredictions saved to:")
print(PREDICTION_FILE)