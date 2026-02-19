from enum import Enum


class MessageType(Enum):
    REQUEST = "REQUEST"
    TOKEN = "TOKEN"


class Message:
    def __init__(self, msg_type, sender_id, receiver_id):
        self.type = msg_type
        self.sender = sender_id
        self.receiver = receiver_id

    def __repr__(self):
        return f"{self.type.value}({self.sender} -> {self.receiver})"
