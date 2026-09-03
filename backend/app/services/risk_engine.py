from typing import Dict, Any


class RiskEngine:

    def calculate_risk(
        self,
        transaction: Dict[str, Any],
        ml_score: float = 0.0
    ) -> Dict[str, Any]:

        risk_score = 0
        reasons = []

        # 1. LARGE AMOUNT
        amount_ratio = transaction.get("amount_ratio", 1.0)

        if amount_ratio >= 20:
            risk_score += 25
            reasons.append(
                "Transaction amount is extremely higher than agent's normal behavior"
            )

        elif amount_ratio >= 10:
            risk_score += 15
            reasons.append(
                "Transaction amount is significantly higher than agent's normal behavior"
            )

        elif amount_ratio >= 4:
            risk_score += 15
            reasons.append(
                "Transaction amount is significantly higher than agent's normal behavior"
            )

        # 2. UNUSUAL TIME
        if transaction.get("is_unusual_hour", 0) == 1:
            risk_score += 20
            reasons.append(
                "Transaction occurred during an unusual hour"
            )

        # 3. NEW BENEFICIARY
        if transaction.get("is_new_beneficiary", 0) == 1:
            risk_score += 20
            reasons.append(
                "Transaction targets a new beneficiary"
            )

        # 4. DEVICE CHANGE
        if transaction.get("is_device_change", 0) == 1:
            risk_score += 15
            reasons.append(
                "Agent is using a different device"
            )

        # 5. IP CHANGE
        if transaction.get("is_ip_change", 0) == 1:
            risk_score += 10
            reasons.append(
                "Agent is operating from a different IP"
            )

        # 6. TRANSACTION BURST
        transaction_count = transaction.get(
            "transaction_count_last_10",
            0
        )

        if transaction_count >= 10:
            risk_score += 20
            reasons.append(
                "Unusual transaction burst detected"
            )

        elif transaction_count >= 5:
            risk_score += 10
            reasons.append(
                "Elevated transaction frequency detected"
            )

        # 7. ML ANOMALY SCORE
        ml_score = max(
            0,
            min(100, float(ml_score))
        )

        risk_score += ml_score * 0.10

        if ml_score >= 70:
            reasons.append(
                "ML model detected unusual behavior"
            )

        # 8. CAP SCORE
        risk_score = min(round(risk_score), 100)

        # 9. DECISION
        if risk_score >= 80:
            decision = "BLOCK"

        elif risk_score >= 50:
            decision = "REVIEW"

        else:
            decision = "ALLOW"

        return {
            "risk_score": risk_score,
            "decision": decision,
            "reasons": reasons,
            "ml_score": round(ml_score, 2)
        }