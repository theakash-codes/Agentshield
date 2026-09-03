from fastapi import APIRouter, HTTPException

from app.database.connection import SessionLocal
from app.models.agent import Agent
from app.schemas.agent import AgentCreate


router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


@router.get("/")
def get_agents():
    db = SessionLocal()

    try:
        agents = db.query(Agent).all()

        return [
            {
                "id": agent.id,
                "name": agent.name,
                "agent_type": agent.agent_type,
                "status": agent.status,
                "trust_score": agent.trust_score
            }
            for agent in agents
        ]

    finally:
        db.close()
@router.get("/{agent_id}")
def get_agent(agent_id: int):
    db = SessionLocal()

    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()

        if agent is None:
            raise HTTPException(
                status_code=404,
                detail="Agent not found"
            )

        return {
            "id": agent.id,
            "name": agent.name,
            "agent_type": agent.agent_type,
            "status": agent.status,
            "trust_score": agent.trust_score
        }

    finally:
        db.close()
@router.post("/")
def create_agent(agent_data: AgentCreate):
    db = SessionLocal()

    try:
        agent = Agent(
            name=agent_data.name,
            agent_type=agent_data.agent_type,
            status="ACTIVE",
            trust_score=100.0
        )

        db.add(agent)
        db.commit()
        db.refresh(agent)

        return {
            "id": agent.id,
            "name": agent.name,
            "agent_type": agent.agent_type,
            "status": agent.status,
            "trust_score": agent.trust_score
        }

    finally:
        db.close()