# 🛡️ AgentShield

### AI Trust, Risk & Security Layer for Autonomous Financial Agents

AgentShield is a security layer that monitors AI agents performing financial transactions. It evaluates an agent's behavior, risk, policies, and permissions before allowing a transaction to execute.

## 🎯 Problem

AI agents can perform financial actions autonomously. Traditional authorization only checks whether an agent is allowed to perform an action, but does not determine whether its current behavior is trustworthy.

## 💡 Solution

AgentShield evaluates every transaction using:

- 🧠 Behavioral analysis
- 🤖 ML anomaly detection
- ⚠️ Risk scoring
- 📜 Policy enforcement
- 🔐 Role-based permissions
- 🛡️ Agent trust scoring
- 🚦 ALLOW / REVIEW / BLOCK decisions

## 🏗️ Architecture

```text
AI Agent
   ↓
AgentShield API
   ↓
Behavior Analysis
   ↓
Risk Engine + ML
   ↓
Policy Engine
   ↓
Permission Engine
   ↓
Decision Engine
   ↓
ALLOW / REVIEW / BLOCK
   ↓
Mock Financial Gateway
   ↓
PostgreSQL
   ↓
Dashboard


##🤖 ML Approach

AgentShield uses Isolation Forest for unsupervised anomaly detection.
The model analyzes features such as transaction amount, amount deviation, transaction frequency, unusual hours, new beneficiaries, device changes, and IP changes.
The ML model is used as an advisory signal, while deterministic security rules enforce the final decision.
Initial evaluation on the synthetic dataset achieved approximately 2% anomaly recall, so the current ML model is treated as a prototype component rather than a production fraud detector.
