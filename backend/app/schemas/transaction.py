from pydantic import BaseModel, Field


class TransactionCheck(BaseModel):
    agent_id: int
    action_type: str
    amount: float = Field(gt=0)
    beneficiary_id: int
    device_id: str
    ip_address: str
    