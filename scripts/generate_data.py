import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

NUM_AGENTS = 50
NUM_CUSTOMERS = 5000
NUM_BENEFICIARIES = 500
NUM_TRANSACTIONS = 100000

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ============================================================
# AGENT TYPES
# ============================================================

AGENT_TYPES = [
    "finance",
    "support",
    "commerce",
    "collections",
    "accounting"
]


# ============================================================
# NORMAL BEHAVIOR FOR EACH AGENT TYPE
# ============================================================

AGENT_BEHAVIOR = {

    "finance": {
        "mean_amount": 12000,
        "std_amount": 5000,
        "daily_transactions": 40,
        "start_hour": 9,
        "end_hour": 18,
        "actions": ["PAYOUT", "PAYMENT"]
    },

    "support": {
        "mean_amount": 3000,
        "std_amount": 1500,
        "daily_transactions": 25,
        "start_hour": 9,
        "end_hour": 20,
        "actions": ["REFUND", "PAYMENT"]
    },

    "commerce": {
        "mean_amount": 2500,
        "std_amount": 1200,
        "daily_transactions": 60,
        "start_hour": 8,
        "end_hour": 22,
        "actions": ["PAYMENT", "PAYMENT_LINK"]
    },

    "collections": {
        "mean_amount": 8000,
        "std_amount": 4000,
        "daily_transactions": 35,
        "start_hour": 8,
        "end_hour": 19,
        "actions": ["PAYMENT", "PAYOUT"]
    },

    "accounting": {
        "mean_amount": 15000,
        "std_amount": 7000,
        "daily_transactions": 30,
        "start_hour": 9,
        "end_hour": 18,
        "actions": ["PAYOUT", "REFUND"]
    }
}


# ============================================================
# DATA DIRECTORIES
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "ml" / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. GENERATE AGENTS
# ============================================================

def generate_agents(count):

    agents = []

    for i in range(count):

        agent_type = random.choice(AGENT_TYPES)

        agents.append({
            "agent_id": f"agent_{i + 1:03d}",
            "agent_name": f"{agent_type.title()}Bot-{i + 1:03d}",
            "agent_type": agent_type
        })

    return pd.DataFrame(agents)


# ============================================================
# 2. GENERATE CUSTOMERS
# ============================================================

def generate_customers(count):

    customers = []

    for i in range(count):

        customers.append({
            "customer_id": f"customer_{i + 1:05d}",
            "name": f"Customer-{i + 1:05d}",
            "email": f"customer{i + 1}@example.com"
        })

    return pd.DataFrame(customers)


# ============================================================
# 3. GENERATE BENEFICIARIES
# ============================================================

def generate_beneficiaries(count):

    beneficiaries = []

    for i in range(count):

        beneficiaries.append({
            "beneficiary_id": f"vendor_{i + 1:04d}",
            "name": f"Vendor-{i + 1:04d}"
        })

    return pd.DataFrame(beneficiaries)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_device_id():

    return f"device_{random.randint(1, 200):03d}"


def generate_ip_address():

    return (
        f"192.168."
        f"{random.randint(0, 255)}."
        f"{random.randint(1, 254)}"
    )


def generate_normal_timestamp(start_date, agent_type):

    behavior = AGENT_BEHAVIOR[agent_type]

    start_hour = behavior["start_hour"]
    end_hour = behavior["end_hour"]

    days_offset = random.randint(0, 29)

    date = start_date + timedelta(days=days_offset)

    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return date.replace(
        hour=hour,
        minute=minute,
        second=second
    )


def generate_amount(agent_type):

    behavior = AGENT_BEHAVIOR[agent_type]

    amount = np.random.normal(
        behavior["mean_amount"],
        behavior["std_amount"]
    )

    # Prevent negative or unrealistic amounts
    amount = max(100, amount)

    return round(float(amount), 2)


# ============================================================
# 4. GENERATE NORMAL TRANSACTION
# ============================================================

def generate_normal_transaction(
    transaction_number,
    agents_df,
    customers_df,
    beneficiaries_df,
    start_date
):

    agent = agents_df.sample(1).iloc[0]

    agent_id = agent["agent_id"]
    agent_type = agent["agent_type"]

    behavior = AGENT_BEHAVIOR[agent_type]

    customer = customers_df.sample(1).iloc[0]

    action_type = random.choice(
        behavior["actions"]
    )

    amount = generate_amount(agent_type)

    timestamp = generate_normal_timestamp(
        start_date,
        agent_type
    )

    beneficiary = beneficiaries_df.sample(1).iloc[0]

    return {
        "transaction_id": f"txn_{transaction_number:07d}",

        "agent_id": agent_id,

        "customer_id": customer["customer_id"],

        "beneficiary_id": beneficiary["beneficiary_id"],

        "action_type": action_type,

        "amount": amount,

        "currency": "INR",

        "timestamp": timestamp,

        "device_id": generate_device_id(),

        "ip_address": generate_ip_address(),

        "status": random.choice(
            ["SUCCESS", "SUCCESS", "SUCCESS", "FAILED"]
        ),

        "is_anomaly": 0,

        "anomaly_type": "NONE"
    }


# ============================================================
# 5. GENERATE ANOMALOUS TRANSACTION
# ============================================================

def generate_anomalous_transaction(
    transaction_number,
    agents_df,
    customers_df,
    beneficiaries_df,
    start_date
):

    agent = agents_df.sample(1).iloc[0]

    agent_id = agent["agent_id"]

    agent_type = agent["agent_type"]

    customer = customers_df.sample(1).iloc[0]

    anomaly_type = random.choice([
        "LARGE_AMOUNT",
        "UNUSUAL_TIME",
        "NEW_BENEFICIARY",
        "TRANSACTION_BURST",
        "DEVICE_CHANGE",
        "IP_CHANGE"
    ])

    behavior = AGENT_BEHAVIOR[agent_type]

    # --------------------------------------------
    # LARGE AMOUNT
    # --------------------------------------------

    if anomaly_type == "LARGE_AMOUNT":

        amount = random.uniform(
            300000,
            1000000
        )

        timestamp = generate_normal_timestamp(
            start_date,
            agent_type
        )

        beneficiary = beneficiaries_df.sample(1).iloc[0]

        device_id = generate_device_id()

        ip_address = generate_ip_address()


    # --------------------------------------------
    # UNUSUAL TIME
    # --------------------------------------------

    elif anomaly_type == "UNUSUAL_TIME":

        amount = generate_amount(agent_type)

        days_offset = random.randint(0, 29)

        date = start_date + timedelta(
            days=days_offset
        )

        timestamp = date.replace(
            hour=random.choice([0, 1, 2, 3, 4]),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )

        beneficiary = beneficiaries_df.sample(1).iloc[0]

        device_id = generate_device_id()

        ip_address = generate_ip_address()


    # --------------------------------------------
    # NEW BENEFICIARY
    # --------------------------------------------

    elif anomaly_type == "NEW_BENEFICIARY":

        amount = generate_amount(agent_type)

        timestamp = generate_normal_timestamp(
            start_date,
            agent_type
        )

        beneficiary = beneficiaries_df.sample(1).iloc[0]

        device_id = generate_device_id()

        ip_address = generate_ip_address()


    # --------------------------------------------
    # TRANSACTION BURST
    # --------------------------------------------

    elif anomaly_type == "TRANSACTION_BURST":

        amount = generate_amount(agent_type)

        days_offset = random.randint(0, 29)

        date = start_date + timedelta(
            days=days_offset
        )

        timestamp = date.replace(
            hour=random.randint(9, 17),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )

        beneficiary = beneficiaries_df.sample(1).iloc[0]

        device_id = generate_device_id()

        ip_address = generate_ip_address()


    # --------------------------------------------
    # DEVICE CHANGE
    # --------------------------------------------

    elif anomaly_type == "DEVICE_CHANGE":

        amount = generate_amount(agent_type)

        timestamp = generate_normal_timestamp(
            start_date,
            agent_type
        )

        beneficiary = beneficiaries_df.sample(1).iloc[0]

        device_id = f"unknown_device_{random.randint(1000, 9999)}"

        ip_address = generate_ip_address()


    # --------------------------------------------
    # IP CHANGE
    # --------------------------------------------

    else:

        amount = generate_amount(agent_type)

        timestamp = generate_normal_timestamp(
            start_date,
            agent_type
        )

        beneficiary = beneficiaries_df.sample(1).iloc[0]

        device_id = generate_device_id()

        ip_address = (
            f"10."
            f"{random.randint(1, 255)}."
            f"{random.randint(1, 255)}."
            f"{random.randint(1, 254)}"
        )

    return {
        "transaction_id": f"txn_{transaction_number:07d}",

        "agent_id": agent_id,

        "customer_id": customer["customer_id"],

        "beneficiary_id": beneficiary["beneficiary_id"],

        "action_type": random.choice(
            behavior["actions"]
        ),

        "amount": round(float(amount), 2),

        "currency": "INR",

        "timestamp": timestamp,

        "device_id": device_id,

        "ip_address": ip_address,

        "status": random.choice(
            ["SUCCESS", "SUCCESS", "FAILED"]
        ),

        "is_anomaly": 1,

        "anomaly_type": anomaly_type
    }


# ============================================================
# 6. GENERATE TRANSACTIONS
# ============================================================

def generate_transactions(
    agents_df,
    customers_df,
    beneficiaries_df,
    count
):

    transactions = []

    start_date = datetime.now() - timedelta(days=30)

    anomaly_count = int(count * 0.05)

    normal_count = count - anomaly_count

    print(
        f"Generating {normal_count} normal transactions..."
    )

    for i in range(normal_count):

        transaction = generate_normal_transaction(
            i + 1,
            agents_df,
            customers_df,
            beneficiaries_df,
            start_date
        )

        transactions.append(transaction)

    print(
        f"Generating {anomaly_count} anomalous transactions..."
    )

    for i in range(anomaly_count):

        transaction_number = normal_count + i + 1

        transaction = generate_anomalous_transaction(
            transaction_number,
            agents_df,
            customers_df,
            beneficiaries_df,
            start_date
        )

        transactions.append(transaction)

    random.shuffle(transactions)

    return pd.DataFrame(transactions)


# ============================================================
# 7. MAIN PROGRAM
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("        AGENTSHIELD SYNTHETIC DATA GENERATOR")
    print("=" * 60)
    print("\n")

    # Generate agents
    print("Generating agents...")

    agents_df = generate_agents(
        NUM_AGENTS
    )

    print(
        f"✓ Generated {len(agents_df)} agents"
    )

    # Generate customers
    print("Generating customers...")

    customers_df = generate_customers(
        NUM_CUSTOMERS
    )

    print(
        f"✓ Generated {len(customers_df)} customers"
    )

    # Generate beneficiaries
    print("Generating beneficiaries...")

    beneficiaries_df = generate_beneficiaries(
        NUM_BENEFICIARIES
    )

    print(
        f"✓ Generated {len(beneficiaries_df)} beneficiaries"
    )

    # Generate transactions
    print("Generating transactions...")

    transactions_df = generate_transactions(
        agents_df,
        customers_df,
        beneficiaries_df,
        NUM_TRANSACTIONS
    )

    print(
        f"✓ Generated {len(transactions_df)} transactions"
    )

    # Save datasets
    print("\nSaving datasets...")

    agents_df.to_csv(
        DATA_DIR / "agents.csv",
        index=False
    )

    customers_df.to_csv(
        DATA_DIR / "customers.csv",
        index=False
    )

    beneficiaries_df.to_csv(
        DATA_DIR / "beneficiaries.csv",
        index=False
    )

    transactions_df.to_csv(
        DATA_DIR / "transactions.csv",
        index=False
    )

    print("\n")
    print("=" * 60)
    print("              DATA GENERATION COMPLETE")
    print("=" * 60)

    print("\nFiles created:")

    print(
        f"✓ {DATA_DIR / 'agents.csv'}"
    )

    print(
        f"✓ {DATA_DIR / 'customers.csv'}"
    )

    print(
        f"✓ {DATA_DIR / 'beneficiaries.csv'}"
    )

    print(
        f"✓ {DATA_DIR / 'transactions.csv'}"
    )

    print("\nTransaction summary:")

    print(
        transactions_df["is_anomaly"]
        .value_counts()
    )

    print("\nAnomaly types:")

    print(
        transactions_df[
            transactions_df["is_anomaly"] == 1
        ]["anomaly_type"].value_counts()
    )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()