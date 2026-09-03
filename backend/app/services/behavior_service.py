from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class BehaviorService:

    def get_features(
        self,
        db: Session,
        transaction: Transaction
    ):
        # Get previous transactions from the same agent
        previous_transactions = (
            db.query(Transaction)
            .filter(
                Transaction.agent_id == transaction.agent_id,
                Transaction.id != transaction.id
            )
            .order_by(Transaction.timestamp.desc())
            .all()
        )

        # No previous behavior
        if not previous_transactions:
            return {
                "amount_ratio": 1.0,
                "is_unusual_hour": 0,
                "is_new_beneficiary": 1,
                "is_device_change": 0,
                "is_ip_change": 0,
                "transaction_count_last_10": 1
            }

        # Previous average transaction amount
        previous_amounts = [
            t.amount for t in previous_transactions
            if t.amount is not None
        ]

        average_amount = (
            sum(previous_amounts) / len(previous_amounts)
            if previous_amounts else transaction.amount
        )

        amount_ratio = (
            transaction.amount / average_amount
            if average_amount > 0 else 1.0
        )

        # Check whether beneficiary was used before
        previous_beneficiaries = {
            t.beneficiary_id
            for t in previous_transactions
            if t.beneficiary_id is not None
        }

        is_new_beneficiary = (
            0
            if transaction.beneficiary_id in previous_beneficiaries
            else 1
        )

        # Compare device and IP with most recent transaction
        latest_transaction = previous_transactions[0]

        is_device_change = int(
            transaction.device_id != latest_transaction.device_id
        )

        is_ip_change = int(
            transaction.ip_address != latest_transaction.ip_address
        )

        # Unusual hour
        current_hour = transaction.timestamp.hour

        is_unusual_hour = int(
            current_hour < 8 or current_hour > 22
        )

        # Transactions in the previous 10 minutes
        ten_minutes_ago = transaction.timestamp - timedelta(minutes=10)

        transaction_count_last_10 = sum(
            1
            for t in previous_transactions
            if t.timestamp >= ten_minutes_ago
        ) + 1

        return {
            "amount_ratio": round(amount_ratio, 2),
            "is_unusual_hour": is_unusual_hour,
            "is_new_beneficiary": is_new_beneficiary,
            "is_device_change": is_device_change,
            "is_ip_change": is_ip_change,
            "transaction_count_last_10": transaction_count_last_10
        }
        