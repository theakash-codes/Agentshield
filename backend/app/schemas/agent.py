from pydantic import BaseModel


class AgentCreate(BaseModel):
    name: str
    agent_type: str