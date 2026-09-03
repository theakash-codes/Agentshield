from typing import Dict, Any


class PermissionEngine:
    def evaluate(
        self,
        agent_permissions: Dict[str, Dict[str, Any]],
        action_type: str,
        amount: float
    ) -> Dict[str, Any]:

        # Check whether the action exists in the agent's permissions
        if action_type not in agent_permissions:
            return {
                "allowed": False,
                "decision": "BLOCK",
                "reason": f"Agent does not have permission for {action_type}"
            }

        permission = agent_permissions[action_type]

        # Check whether the permission is enabled
        if not permission.get("enabled", False):
            return {
                "allowed": False,
                "decision": "BLOCK",
                "reason": f"{action_type} permission is disabled"
            }

        # Check maximum transaction amount
        max_amount = permission.get("max_amount")

        if max_amount is not None and amount > max_amount:
            return {
                "allowed": False,
                "decision": "REVIEW",
                "reason": (
                    f"Amount ₹{amount:,.2f} exceeds "
                    f"agent limit of ₹{max_amount:,.2f}"
                )
            }

        # Check whether human approval is required
        if permission.get("requires_approval", False):
            return {
                "allowed": False,
                "decision": "REVIEW",
                "reason": f"{action_type} requires human approval"
            }

        # Permission passed all checks
        return {
            "allowed": True,
            "decision": "ALLOW",
            "reason": f"Agent is authorized to perform {action_type}"
        }