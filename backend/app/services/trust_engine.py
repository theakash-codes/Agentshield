from typing import Dict, Any


class TrustEngine:
    """
    AgentShield Trust Engine.

    Maintains a dynamic trust score for an AI agent.

    Higher score = more trusted
    Lower score = less trusted
    """

    def __init__(self):
        self.default_trust_score = 100.0

    # --------------------------------------------------
    # GET INITIAL TRUST
    # --------------------------------------------------

    def get_initial_trust(self) -> float:
        """
        Return the default trust score for a new agent.
        """

        return self.default_trust_score

    # --------------------------------------------------
    # UPDATE TRUST
    # --------------------------------------------------

    def update_trust(
        self,
        current_trust: float,
        risk_score: float,
        decision: str
    ) -> Dict[str, Any]:
        """
        Update an agent's trust score based on
        the risk and final security decision.
        """

        trust_change = 0
        reasons = []

        # --------------------------------------------------
        # BLOCKED TRANSACTION
        # --------------------------------------------------

        if decision == "BLOCK":

            trust_change = -20

            reasons.append(
                "Trust reduced because the transaction "
                "was blocked"
            )

        # --------------------------------------------------
        # REVIEWED TRANSACTION
        # --------------------------------------------------

        elif decision == "REVIEW":

            trust_change = -8

            reasons.append(
                "Trust reduced because the transaction "
                "requires human review"
            )

        # --------------------------------------------------
        # ALLOWED TRANSACTION
        # --------------------------------------------------

        elif decision == "ALLOW":

            # Safe behavior slowly restores trust.
            trust_change = 1

            reasons.append(
                "Trust slightly increased after "
                "successful normal behavior"
            )

        # --------------------------------------------------
        # ADDITIONAL HIGH-RISK PENALTY
        # --------------------------------------------------

        if risk_score >= 90:

            trust_change -= 10

            reasons.append(
                "Additional trust penalty applied "
                "for extremely high risk"
            )

        elif risk_score >= 70:

            trust_change -= 5

            reasons.append(
                "Additional trust penalty applied "
                "for high risk"
            )

        # --------------------------------------------------
        # CALCULATE NEW TRUST
        # --------------------------------------------------

        new_trust = current_trust + trust_change

        # Keep trust between 0 and 100.

        new_trust = max(
            0,
            min(100, new_trust)
        )

        # --------------------------------------------------
        # DETERMINE AGENT STATUS
        # --------------------------------------------------

        if new_trust <= 20:

            status = "QUARANTINED"

        elif new_trust <= 50:

            status = "RESTRICTED"

        elif new_trust <= 80:

            status = "MONITORED"

        else:

            status = "ACTIVE"

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "previous_trust": round(
                current_trust,
                2
            ),
            "trust_change": trust_change,
            "new_trust": round(
                new_trust,
                2
            ),
            "status": status,
            "reasons": reasons
        }