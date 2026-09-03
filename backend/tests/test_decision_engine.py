from app.services.decision_engine import DecisionEngine


engine = DecisionEngine()


def test_decision(risk, policy, permission):
    risk_result = {
        "decision": risk,
        "reasons": ["Risk engine test"]
    }

    policy_result = {
        "decision": policy,
        "reasons": ["Policy engine test"]
    }

    permission_result = {
        "decision": permission,
        "reason": "Permission engine test"
    }

    result = engine.make_final_decision(
        risk_result,
        policy_result,
        permission_result
    )

    print("\n--------------------------------")
    print(f"Risk       : {risk}")
    print(f"Policy     : {policy}")
    print(f"Permission : {permission}")
    print(f"FINAL      : {result['decision']}")
    print("--------------------------------")


print("\n==============================")
print("TEST 1: ALL ALLOW")
print("==============================")

test_decision(
    "ALLOW",
    "ALLOW",
    "ALLOW"
)


print("\n==============================")
print("TEST 2: ONE REVIEW")
print("==============================")

test_decision(
    "ALLOW",
    "REVIEW",
    "ALLOW"
)


print("\n==============================")
print("TEST 3: ONE BLOCK")
print("==============================")

test_decision(
    "ALLOW",
    "ALLOW",
    "BLOCK"
)


print("\n==============================")
print("TEST 4: REVIEW + BLOCK")
print("==============================")

test_decision(
    "REVIEW",
    "ALLOW",
    "BLOCK"
)


print("\n==============================")
print("TEST 5: RISK BLOCK")
print("==============================")

test_decision(
    "BLOCK",
    "ALLOW",
    "ALLOW"
)