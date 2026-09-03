from app.services.trust_engine import TrustEngine


# Create Trust Engine
trust_engine = TrustEngine()


# --------------------------------------------------
# STARTING TRUST
# --------------------------------------------------

trust = trust_engine.get_initial_trust()

print("\n==============================")
print("INITIAL AGENT")
print("==============================")

print("Trust Score:", trust)
print("Status: ACTIVE")


# --------------------------------------------------
# EVENT 1 — BLOCKED TRANSACTION
# --------------------------------------------------

result = trust_engine.update_trust(
    current_trust=trust,
    risk_score=85,
    decision="BLOCK"
)

trust = result["new_trust"]

print("\n==============================")
print("AFTER BLOCKED TRANSACTION #1")
print("==============================")

print("Previous Trust:", result["previous_trust"])
print("Trust Change:", result["trust_change"])
print("New Trust:", result["new_trust"])
print("Status:", result["status"])

for reason in result["reasons"]:
    print("-", reason)


# --------------------------------------------------
# EVENT 2 — BLOCKED TRANSACTION
# --------------------------------------------------

result = trust_engine.update_trust(
    current_trust=trust,
    risk_score=92,
    decision="BLOCK"
)

trust = result["new_trust"]

print("\n==============================")
print("AFTER BLOCKED TRANSACTION #2")
print("==============================")

print("Previous Trust:", result["previous_trust"])
print("Trust Change:", result["trust_change"])
print("New Trust:", result["new_trust"])
print("Status:", result["status"])

for reason in result["reasons"]:
    print("-", reason)


# --------------------------------------------------
# EVENT 3 — BLOCKED TRANSACTION
# --------------------------------------------------

result = trust_engine.update_trust(
    current_trust=trust,
    risk_score=95,
    decision="BLOCK"
)

trust = result["new_trust"]

print("\n==============================")
print("AFTER BLOCKED TRANSACTION #3")
print("==============================")

print("Previous Trust:", result["previous_trust"])
print("Trust Change:", result["trust_change"])
print("New Trust:", result["new_trust"])
print("Status:", result["status"])

for reason in result["reasons"]:
    print("-", reason)


# --------------------------------------------------
# EVENT 4 — BLOCKED TRANSACTION
# --------------------------------------------------

result = trust_engine.update_trust(
    current_trust=trust,
    risk_score=98,
    decision="BLOCK"
)

trust = result["new_trust"]

print("\n==============================")
print("AFTER BLOCKED TRANSACTION #4")
print("==============================")

print("Previous Trust:", result["previous_trust"])
print("Trust Change:", result["trust_change"])
print("New Trust:", result["new_trust"])
print("Status:", result["status"])

for reason in result["reasons"]:
    print("-", reason)