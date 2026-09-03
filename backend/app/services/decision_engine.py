from typing import Dict, Any


class DecisionEngine:

    def __init__(self):
        # Higher priority = more restrictive decision
        self.decision_priority = {
            "ALLOW": 1,
            "REVIEW": 2,
            "BLOCK": 3
        }

    def make_final_decision(
        self,
        risk_result: Dict[str, Any],
        policy_result: Dict[str, Any],
        permission_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        decisions = {
            "risk": risk_result["decision"],
            "policy": policy_result["decision"],
            "permission": permission_result["decision"]
        }

        # Most restrictive decision wins
        final_decision = max(
            decisions.values(),
            key=lambda decision: self.decision_priority[decision]
        )

        reasons = []

        if risk_result.get("reasons"):
            reasons.extend(
                [f"Risk: {reason}" for reason in risk_result["reasons"]]
            )

        if policy_result.get("reasons"):
            reasons.extend(
                [f"Policy: {reason}" for reason in policy_result["reasons"]]
            )

        if permission_result.get("reason"):
            reasons.append(
                f"Permission: {permission_result['reason']}"
            )

        return {
            "decision": final_decision,
            "reasons": reasons,
            "engine_decisions": decisions
        }