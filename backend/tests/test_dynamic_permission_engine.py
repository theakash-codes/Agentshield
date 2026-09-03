from app.services.dynamic_permission_engine import DynamicPermissionEngine


engine = DynamicPermissionEngine()


original_permissions = {
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
        "max_amount": 100000,
        "requires_approval": False
    }
}


trust_scores = [90, 65, 40, 15]


for trust in trust_scores:

    print("\n==============================")
    print(f"TRUST SCORE: {trust}")
    print("==============================")

    effective_permissions = engine.get_effective_permissions(
        original_permissions,
        trust
    )

    for action, permission in effective_permissions.items():

        print(f"\n{action}")
        print(f"  Enabled: {permission['enabled']}")
        print(
            f"  Max Amount: ₹{permission['max_amount']:,.2f}"
        )
        print(
            f"  Requires Approval: "
            f"{permission['requires_approval']}"
        )


print("\n==============================")
print("ORIGINAL PERMISSIONS")
print("==============================")

print(original_permissions)