from typing import Dict, Any


class PolicyEngine:
    """
    AgentShield Policy Engine.

    Converts risk and transaction context
    into an authorization decision.
    """

    def evaluate(
        self,
        transaction: Dict[str, Any],
        risk_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        risk_score = risk_result["risk_score"]

        reasons = list(
            risk_result.get("reasons", [])
        )

        # --------------------------------------------------
        # 1. HIGH RISK
        # --------------------------------------------------

        if risk_score >= 80:

            return {
                "decision": "BLOCK",
                "risk_score": risk_score,
                "reasons": reasons
            }

        # --------------------------------------------------
        # 2. NEW BENEFICIARY
        # --------------------------------------------------

        if transaction.get(
            "is_new_beneficiary",
            0
        ) == 1:

            if transaction.get(
                "amount_ratio",
                1
            ) >= 5:

                reasons.append(
                    "High-value transaction to "
                    "new beneficiary requires review"
                )

                return {
                    "decision": "REVIEW",
                    "risk_score": risk_score,
                    "reasons": reasons
                }

        # --------------------------------------------------
        # 3. HIGH AMOUNT
        # --------------------------------------------------

        if transaction.get(
            "amount_ratio",
            1
        ) >= 10:

            reasons.append(
                "Transaction exceeds permitted "
                "behavioral amount threshold"
            )

            return {
                "decision": "REVIEW",
                "risk_score": risk_score,
                "reasons": reasons
            }

        # --------------------------------------------------
        # 4. UNUSUAL TIME + NEW BENEFICIARY
        # --------------------------------------------------

        if (
            transaction.get(
                "is_unusual_hour",
                0
            ) == 1
            and
            transaction.get(
                "is_new_beneficiary",
                0
            ) == 1
        ):

            reasons.append(
                "Unusual-hour transaction to "
                "new beneficiary requires review"
            )

            return {
                "decision": "REVIEW",
                "risk_score": risk_score,
                "reasons": reasons
            }

        # --------------------------------------------------
        # 5. MEDIUM RISK
        # --------------------------------------------------

        if risk_score >= 50:

            reasons.append(
                "Transaction exceeds medium-risk "
                "threshold"
            )

            return {
                "decision": "REVIEW",
                "risk_score": risk_score,
                "reasons": reasons
            }

        # --------------------------------------------------
        # 6. NORMAL
        # --------------------------------------------------

        return {
            "decision": "ALLOW",
            "risk_score": risk_score,
            "reasons": reasons
        }