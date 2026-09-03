from typing import Dict, Any


class DynamicPermissionEngine:

    def get_effective_permissions(
        self,
        agent_permissions: Dict[str, Dict[str, Any]],
        trust_score: float
    ) -> Dict[str, Dict[str, Any]]:

        # Make a copy so the original permissions are not modified
        effective_permissions = {
            action: permission.copy()
            for action, permission in agent_permissions.items()
        }

        # QUARANTINED
        # Trust score <= 20
        # Block all financial actions
        if trust_score <= 20:

            for permission in effective_permissions.values():
                permission["enabled"] = False

            return effective_permissions

        # RESTRICTED
        # Trust score 21-50
        # All enabled financial actions require approval
        if trust_score <= 50:

            for permission in effective_permissions.values():

                if permission.get("enabled", False):
                    permission["requires_approval"] = True

            return effective_permissions

        # MONITORED
        # Trust score 51-80
        # Keep normal permissions, but require approval
        # for high-value actions.
        if trust_score <= 80:

            for permission in effective_permissions.values():

                max_amount = permission.get("max_amount")

                if (
                    permission.get("enabled", False)
                    and max_amount is not None
                    and max_amount >= 50000
                ):
                    permission["requires_approval"] = True

            return effective_permissions

        # ACTIVE
        # Trust score > 80
        # Keep original permissions unchanged.
        return effective_permissions