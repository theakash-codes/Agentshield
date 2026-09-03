from datetime import datetime

from app.database.connection import SessionLocal
from app.models.transaction import Transaction


db = SessionLocal()

try:
    transaction = Transaction(
        agent_id=1,
        action_type="PAYOUT",
        amount=5000.0,
        currency="INR",
        beneficiary_id=101,
        status="PENDING",
        device_id="device_001",
        ip_address="192.168.1.10",
        timestamp=datetime.utcnow()
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    print("\n==============================")
    print("TRANSACTION INSERT SUCCESS")
    print("==============================")
    print(f"ID:            {transaction.id}")
    print(f"Agent ID:      {transaction.agent_id}")
    print(f"Action:        {transaction.action_type}")
    print(f"Amount:        ₹{transaction.amount:,.2f}")
    print(f"Beneficiary:   {transaction.beneficiary_id}")
    print(f"Status:        {transaction.status}")

finally:
    db.close()