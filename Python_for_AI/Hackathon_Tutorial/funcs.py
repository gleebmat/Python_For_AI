from datetime import datetime
import json

from words import INTENT_KEYWORDS
from classes import ConversationContext


def detect_intent(message: str) -> str:
    text = message.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return intent
    return "other"


def run_conversation():
    ctx = ConversationContext()
    # GREETING
    greeting = "Hi, I’m your support assistant. How can I help you today?"
    ctx.log_assistant(greeting)
    ctx.state = "COLLECT_ISSUE"

    while ctx.state != "END":
        user_input = input("> ").strip()
        if not user_input:
            continue
        ctx.log_user(user_input)

        if ctx.state == "COLLECT_ISSUE":
            handle_collect_issue(ctx, user_input)
        elif ctx.state == "CLARIFY_TECHNICAL":
            handle_clarify_technical(ctx, user_input)
        elif ctx.state == "CLARIFY_BILLING":
            handle_clarify_billing(ctx, user_input)
        elif ctx.state == "CLARIFY_ORDER":
            handle_clarify_order(ctx, user_input)
        elif ctx.state == "CLARIFY_OTHER":
            handle_clarify_other(ctx, user_input)
        elif ctx.state == "SUMMARY":
            handle_summary(ctx, user_input)
        else:
            ctx.log_assistant("Something went wrong, ending conversation.")
            ctx.state = "END"


def handle_collect_issue(ctx: ConversationContext, user_input: str):
    intent = detect_intent(user_input)
    ctx.intent = intent

    if intent == "technical_issue":
        ctx.details["issue_description"] = user_input
        ctx.log_assistant(
            "I understand you're having a technical issue with your connection."
        )
        ctx.log_assistant("Is the router's power light currently on?")
        ctx.state = "CLARIFY_TECHNICAL"

    elif intent == "billing":
        ctx.details["issue_description"] = user_input
        ctx.log_assistant("It sounds like you have a question about your bill.")
        ctx.log_assistant("Which month or invoice are you asking about?")
        ctx.state = "CLARIFY_BILLING"

    elif intent == "order_status":
        ctx.details["issue_description"] = user_input
        ctx.log_assistant("You want to know the status of an order, got it.")
        ctx.log_assistant("Can you give me your order number if you have it?")
        ctx.state = "CLARIFY_ORDER"

    else:
        ctx.details["issue_description"] = user_input
        ctx.log_assistant("Thanks for explaining. I'll collect a bit more information.")
        ctx.log_assistant(
            "Can you briefly describe what you need help with in one sentence?"
        )
        ctx.state = "CLARIFY_OTHER"


def handle_clarify_technical(ctx: ConversationContext, user_input: str):
    # Decide which follow-up we’re answering based on what’s already stored
    if "router_power" not in ctx.details:
        ctx.details["router_power"] = user_input
        ctx.log_assistant("Thanks. Are you connected via Wi-Fi or cable?")
        return

    if "connection_type" not in ctx.details:
        ctx.details["connection_type"] = user_input
        ctx.log_assistant("Since when have you been experiencing this issue?")
        return

    if "issue_since" not in ctx.details:
        ctx.details["issue_since"] = user_input
        ctx.log_assistant("Got it. I'll create a support ticket for you.")
        ctx.log_assistant("Can I have your name?")
        ctx.state = "SUMMARY"
        return


def handle_clarify_billing(ctx: ConversationContext, user_input: str):
    if "invoice_period" not in ctx.details:
        ctx.details["invoice_period"] = user_input
        ctx.log_assistant("What seems to be wrong with the amount or charges?")
        return

    if "billing_issue_detail" not in ctx.details:
        ctx.details["billing_issue_detail"] = user_input
        ctx.log_assistant(
            "Understood. I’ll create a ticket so our billing team can review it."
        )
        ctx.log_assistant("Can I have your name?")
        ctx.state = "SUMMARY"
        return


def handle_clarify_order(ctx: ConversationContext, user_input: str):
    if "order_number" not in ctx.details:
        ctx.details["order_number"] = user_input
        ctx.log_assistant("Thanks. When did you place the order?")
        return

    if "order_date" not in ctx.details:
        ctx.details["order_date"] = user_input
        ctx.log_assistant("Okay, I will check this for you by creating a ticket.")
        ctx.log_assistant("Can I have your name?")
        ctx.state = "SUMMARY"
        return


def handle_clarify_other(ctx: ConversationContext, user_input: str):
    if "additional_description" not in ctx.details:
        ctx.details["additional_description"] = user_input
        ctx.log_assistant(
            "Thanks for the clarification. I’ll create a ticket so a human agent can follow up."
        )
        ctx.log_assistant("Can I have your name?")
        ctx.state = "SUMMARY"
        return


def handle_summary(ctx: ConversationContext, user_input: str):
    if ctx.customer_name is None:
        ctx.customer_name = user_input
        ticket = create_ticket(ctx)
        ctx.log_assistant(
            "Thank you. I’ve created a ticket with the following details:"
        )
        print(json.dumps(ticket, indent=2))
        ctx.log_assistant("A human agent will follow up as soon as possible.")
        ctx.state = "END"
    else:
        ctx.state = "END"


def create_ticket(ctx: ConversationContext) -> dict:
    # Simple ticket ID using timestamp
    ticket_id = f"TCK-{int(datetime.utcnow().timestamp())}"

    # Determine priority: technical + severe phrase => high
    issue_text = ctx.details.get("issue_description", "").lower()
    if ctx.intent == "technical_issue" and (
        "no internet" in issue_text or "not working" in issue_text
    ):
        priority = "high"
    else:
        priority = "medium"

    ticket = {
        "id": ticket_id,
        "customer_name": ctx.customer_name,
        "intent": ctx.intent,
        "details": ctx.details,
        "conversation": ctx.conversation,
        "priority": priority,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    return ticket


if __name__ == "__main__":
    run_conversation()
