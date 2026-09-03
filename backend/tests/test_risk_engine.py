from app.services.risk_engine import RiskEngine
from app.services.policy_engine import PolicyEngine


# Create engines
risk_engine = RiskEngine()
policy_engine = PolicyEngine()


def evaluate_transaction(name, transaction, ml_score):
    """
    Run a transaction through:

    Transaction
        ↓
    Risk Engine
        ↓
    Policy Engine
        ↓
    Final Decision
    """

    risk_result = risk_engine.calculate_risk(
        transaction,
        ml_score=ml_score
    )

    policy_result = policy_engine.evaluate(
        transaction,
        risk_result
    )

    print("\n==============================")
    print(name)
    print("==============================")

    print("Risk Score :", risk_result["risk_score"])
    print("ML Score   :", risk_result["ml_score"])

    print("Risk Reasons:")

    for reason in policy_result["reasons"]:
        print(" -", reason)

    print("FINAL DECISION:", policy_result["decision"])


# --------------------------------------------------
# TEST 1 — NORMAL TRANSACTION
# --------------------------------------------------

normal_transaction = {
    "amount_ratio": 1.2,
    "is_unusual_hour": 0,
    "is_new_beneficiary": 0,
    "is_device_change": 0,
    "is_ip_change": 0,
    "transaction_count_last_10": 1
}

evaluate_transaction(
    "TEST 1 — NORMAL TRANSACTION",
    normal_transaction,
    10
)


# --------------------------------------------------
# TEST 2 — SUSPICIOUS TRANSACTION
# --------------------------------------------------

suspicious_transaction = {
    "amount_ratio": 8,
    "is_unusual_hour": 0,
    "is_new_beneficiary": 1,
    "is_device_change": 0,
    "is_ip_change": 0,
    "transaction_count_last_10": 4
}

evaluate_transaction(
    "TEST 2 — SUSPICIOUS TRANSACTION",
    suspicious_transaction,
    45
)


# --------------------------------------------------
# TEST 3 — ATTACK TRANSACTION
# --------------------------------------------------

attack_transaction = {
    "amount_ratio": 70,
    "is_unusual_hour": 1,
    "is_new_beneficiary": 1,
    "is_device_change": 1,
    "is_ip_change": 1,
    "transaction_count_last_10": 12
}

evaluate_transaction(
    "TEST 3 — ATTACK TRANSACTION",
    attack_transaction,
    80
)