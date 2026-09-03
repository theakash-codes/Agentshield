from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.schema import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    agent_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    action_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
        nullable=False
    )

    beneficiary_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False
    )

    device_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    ip_address: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )