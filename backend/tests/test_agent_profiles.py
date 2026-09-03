from app.services.agent_profiles import AgentProfiles


agent_types = [
    "finance",
    "support",
    "commerce",
    "collections",
    "accounting"
]


for agent_type in agent_types:

    print("\n==============================")
    print(f"AGENT TYPE: {agent_type.upper()}")
    print("==============================")

    permissions = AgentProfiles.get_profile(agent_type)

    for action, permission in permissions.items():

        status = "ENABLED" if permission["enabled"] else "DISABLED"

        print(f"\n{action}")
        print(f"  Status: {status}")
        print(f"  Max Amount: ₹{permission['max_amount']:,.2f}")
        print(
            f"  Requires Approval: "
            f"{permission['requires_approval']}"
        )