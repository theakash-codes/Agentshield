from app.database.connection import SessionLocal
from app.models.agent import Agent


db = SessionLocal()

try:
    agent = Agent(
        name="FinanceBot",
        agent_type="finance",
        status="ACTIVE",
        trust_score=100.0
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    print("\n==============================")
    print("AGENT INSERT SUCCESS")
    print("==============================")
    print(f"ID:          {agent.id}")
    print(f"Name:        {agent.name}")
    print(f"Type:        {agent.agent_type}")
    print(f"Status:      {agent.status}")
    print(f"Trust Score: {agent.trust_score}")

finally:
    db.close()