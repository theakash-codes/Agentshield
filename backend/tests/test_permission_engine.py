from app.services.permission_engine import PermissionEngine


engine = PermissionEngine()

agent_permissions = {
    "PAYMENT": {
        "enabled": True,
        "max_amount": 50000,
        "requires_approval": False
    },
    "REFUND": {
        "enabled": True,
        "max_amount": 10000,
        "requires_approval": False
    },
    "PAYOUT": {
        "enabled": True,
        "max_amount": 50000,
        "requires_approval": True
    }
}


print("\n==============================")
print("TEST 1: NORMAL PAYMENT")
print("==============================")

result = engine.evaluate(
    agent_permissions,
    "PAYMENT",
    5000
)

print(result)


print("\n==============================")
print("TEST 2: HIGH VALUE PAYMENT")
print("==============================")

result = engine.evaluate(
    agent_permissions,
    "PAYMENT",
    100000
)

print(result)


print("\n==============================")
print("TEST 3: PAYOUT REQUIRES APPROVAL")
print("==============================")

result = engine.evaluate(
    agent_permissions,
    "PAYOUT",
    20000
)

print(result)


print("\n==============================")
print("TEST 4: UNAUTHORIZED ACTION")
print("==============================")

result = engine.evaluate(
    agent_permissions,
    "DELETE_ACCOUNT",
    1000
)

print(result)


print("\n==============================")
print("TEST 5: DISABLED PERMISSION")
print("==============================")

agent_permissions["REFUND"]["enabled"] = False

result = engine.evaluate(
    agent_permissions,
    "REFUND",
    5000
)

print(result)