from typing import Dict, Any


class AgentProfiles:

    PROFILES = {

        "finance": {
            "PAYMENT": {
                "enabled": True,
                "max_amount": 50000,
                "requires_approval": False
            },
            "PAYOUT": {
                "enabled": True,
                "max_amount": 100000,
                "requires_approval": False
            },
            "REFUND": {
                "enabled": True,
                "max_amount": 10000,
                "requires_approval": False
            },
            "PAYMENT_LINK": {
                "enabled": False,
                "max_amount": 0,
                "requires_approval": False
            }
        },

        "support": {
            "PAYMENT": {
                "enabled": True,
                "max_amount": 10000,
                "requires_approval": False
            },
            "REFUND": {
                "enabled": True,
                "max_amount": 10000,
                "requires_approval": False
            },
            "PAYOUT": {
                "enabled": False,
                "max_amount": 0,
                "requires_approval": False
            },
            "PAYMENT_LINK": {
                "enabled": False,
                "max_amount": 0,
                "requires_approval": False
            }
        },

        "commerce": {
            "PAYMENT": {
                "enabled": True,
                "max_amount": 25000,
                "requires_approval": False
            },
            "PAYMENT_LINK": {
                "enabled": True,
                "max_amount": 25000,
                "requires_approval": False
            },
            "REFUND": {
                "enabled": False,
                "max_amount": 0,
                "requires_approval": False
            },
            "PAYOUT": {
                "enabled": False,
                "max_amount": 0,
                "requires_approval": False
            }
        },

        "collections": {
            "PAYMENT": {
                "enabled": True,
                "max_amount": 50000,
                "requires_approval": False
            },
            "PAYOUT": {
                "enabled": True,
                "max_amount": 50000,
                "requires_approval": True
            },
            "REFUND": {
                "enabled": False,
                "max_amount": 0,
                "requires_approval": False
            },
            "PAYMENT_LINK": {
                "enabled": True,
                "max_amount": 25000,
                "requires_approval": False
            }
        },

        "accounting": {
            "PAYMENT": {
                "enabled": True,
                "max_amount": 50000,
                "requires_approval": False
            },
            "PAYOUT": {
                "enabled": True,
                "max_amount": 100000,
                "requires_approval": True
            },
            "REFUND": {
                "enabled": True,
                "max_amount": 10000,
                "requires_approval": True
            },
            "PAYMENT_LINK": {
                "enabled": False,
                "max_amount": 0,
                "requires_approval": False
            }
        }
    }

    @classmethod
    def get_profile(cls, agent_type: str) -> Dict[str, Dict[str, Any]]:
        agent_type = agent_type.lower()

        if agent_type not in cls.PROFILES:
            raise ValueError(
                f"Unknown agent type: {agent_type}"
            )

        # Return a copy so the original profile cannot be modified
        return {
            action: permission.copy()
            for action, permission in cls.PROFILES[agent_type].items()
        }