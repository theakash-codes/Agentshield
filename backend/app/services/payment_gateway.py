from typing import Dict, Any


class PaymentGateway:

    def execute(
        self,
        action_type: str,
        amount: float,
        decision: str
    ) -> Dict[str, Any]:

        if decision == "BLOCK":
            return {
                "status": "BLOCKED",
                "message": "Transaction blocked by AgentShield",
                "executed": False
            }

        if decision == "REVIEW":
            return {
                "status": "PENDING_REVIEW",
                "message": "Transaction requires human approval",
                "executed": False
            }

        return {
            "status": "SUCCESS",
            "message": f"{action_type} of INR {amount:.2f} executed successfully",
            "executed": True
        }