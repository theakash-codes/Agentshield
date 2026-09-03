from app.services.dynamic_permission_engine import DynamicPermissionEngine
from app.services.permission_engine import PermissionEngine


dynamic_engine = DynamicPermissionEngine()
permission_engine = PermissionEngine()


base_permissions = {
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

    effective_permissions = dynamic_engine.get_effective_permissions(
        base_permissions,
        trust
    )

    result = permission_engine.evaluate(
        effective_permissions,
        "PAYOUT",
        20000
    )

    print(f"Effective Permission:")
    print(effective_permissions["PAYOUT"])

    print(f"\nPermission Decision:")
    print(result["decision"])

    print(f"Reason:")
    print(result["reason"])