from fastapi import APIRouter, HTTPException

from app.database.connection import SessionLocal
from app.models.transaction import Transaction
from app.models.agent import Agent
from app.schemas.transaction import TransactionCheck
from app.services.risk_engine import RiskEngine
from app.services.policy_engine import PolicyEngine
from app.services.permission_engine import PermissionEngine
from app.services.agent_profiles import AgentProfiles
from app.services.behavior_service import BehaviorService
from app.services.decision_engine import DecisionEngine
from app.services.trust_engine import TrustEngine
from app.services.payment_gateway import PaymentGateway


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/check")
def check_transaction(transaction_data: TransactionCheck):
    db = SessionLocal()

    try:
        transaction = Transaction(
            agent_id=transaction_data.agent_id,
            action_type=transaction_data.action_type,
            amount=transaction_data.amount,
            currency="INR",
            beneficiary_id=transaction_data.beneficiary_id,
            status="PENDING",
            device_id=transaction_data.device_id,
            ip_address=transaction_data.ip_address
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        # Get actual agent
        agent = db.query(Agent).filter(
            Agent.id == transaction.agent_id
        ).first()

        if agent is None:
            raise HTTPException(
                status_code=404,
                detail="Agent not found"
            )

        # Behavioral analysis
        behavior_service = BehaviorService()

        behavior_features = behavior_service.get_features(
            db,
            transaction
        )

        # Risk analysis
        risk_engine = RiskEngine()

        risk_result = risk_engine.calculate_risk(
            {
                "amount": transaction.amount,
                **behavior_features
            },
            ml_score=0.0
        )

        # Policy analysis
        policy_engine = PolicyEngine()

        policy_result = policy_engine.evaluate(
            {
                "amount": transaction.amount,
                "amount_ratio": behavior_features["amount_ratio"],
                "is_unusual_hour": behavior_features["is_unusual_hour"],
                "is_new_beneficiary": behavior_features["is_new_beneficiary"]
            },
            risk_result
        )

        # Permission analysis
        agent_profile = AgentProfiles.get_profile(
            agent.agent_type
        )

        permission_engine = PermissionEngine()

        permission_result = permission_engine.evaluate(
            agent_profile,
            transaction.action_type,
            transaction.amount
        )

        # Final security decision
        decision_engine = DecisionEngine()

        final_result = decision_engine.make_final_decision(
            risk_result,
            policy_result,
            permission_result
        )

        # Update agent trust
        trust_engine = TrustEngine()

        trust_result = trust_engine.update_trust(
            agent.trust_score,
            risk_result["risk_score"],
            final_result["decision"]
        )

        agent.trust_score = trust_result["new_trust"]
        agent.status = trust_result["status"]

        db.commit()

        # Execute through mock financial gateway
        payment_gateway = PaymentGateway()

        gateway_result = payment_gateway.execute(
            transaction.action_type,
            transaction.amount,
            final_result["decision"]
        )

        return {
            "transaction_id": transaction.id,
            "agent_id": transaction.agent_id,
            "agent_type": agent.agent_type,
            "action_type": transaction.action_type,
            "amount": transaction.amount,
            "status": transaction.status,

            "risk_score": risk_result["risk_score"],
            "risk_decision": risk_result["decision"],
            "policy_decision": policy_result["decision"],
            "permission_decision": permission_result["decision"],

            "final_decision": final_result["decision"],

            "risk_reasons": risk_result["reasons"],
            "policy_reasons": policy_result["reasons"],
            "permission_reason": permission_result["reason"],
            "final_reasons": final_result["reasons"],

            "previous_trust": trust_result["previous_trust"],
            "trust_change": trust_result["trust_change"],
            "trust_score": trust_result["new_trust"],
            "agent_status": trust_result["status"],

            "behavior_features": behavior_features,

            "gateway_status": gateway_result["status"],
            "gateway_message": gateway_result["message"],
            "transaction_executed": gateway_result["executed"]
        }

    finally:
        db.close()