import json
from datetime import datetime


class ConversationContext:
    def __init__(self):
        self.state = "GREETING"
        self.intent = None
        self.customer_name = None
        self.details = {}
        self.conversation = []  # list of {"from": "user"/"assistant", "text": "..."}
        self.ticket_id_counter = 1

    def log_user(self, text: str):
        self.conversation.append({"from": "user", "text": text})

    def log_assistant(self, text: str):
        self.conversation.append({"from": "assistant", "text": text})
        print(text)
