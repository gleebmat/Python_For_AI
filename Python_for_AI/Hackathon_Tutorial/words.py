INTENT_KEYWORDS = {
    "technical_issue": [
        "no internet",
        "no connection",
        "disconnected",
        "slow",
        "lag",
        "latency",
        "router",
        "modem",
        "wifi",
        "wi-fi",
    ],
    "billing": ["bill", "invoice", "charged", "payment", "refund", "price", "fee"],
    "order_status": ["order", "delivery", "shipping", "package", "tracking"],
}


ACCOUNT_RULES = {
    "Customer Support": ["Google Workspace", "Zendesk", "Slack", "VPN"],
    "Engineering": ["Google Workspace", "GitHub", "Jira", "Slack", "VPN"],
    "Sales": ["Google Workspace", "CRM", "Slack"],
}

GROUP_RULES = {
    "Customer Support": ["support-agents", "kb-readonly", "call-queue-level1"],
    "Engineering": ["devs", "staging-access"],
    "Sales": ["sales-reps", "crm-users"],
}

HARDWARE_RULES = {
    "Support Engineer": "Standard laptop 16GB RAM + USB headset",
    "Software Engineer": "Developer laptop 32GB RAM + external monitor",
    "Sales Representative": "Lightweight laptop 16GB RAM + USB headset",
}

DEFAULT_ACCOUNTS = ["Google Workspace"]
DEFAULT_GROUPS = []
DEFAULT_HARDWARE = "Standard laptop 16GB RAM"


{
    "name": "Alex Johnson",
    "email": "alex.johnson@example.com",
    "role": "Support Engineer",
    "department": "Customer Support",
    "seniority": "junior",
    "location": "Vienna",
    "start_date": "2026-06-10",
}
