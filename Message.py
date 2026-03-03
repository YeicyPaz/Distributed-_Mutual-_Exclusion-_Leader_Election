from enum import Enum


class MessageType(Enum):
    REQUEST = "REQUEST"
    TOKEN = "TOKEN"
    RELEASE = "RELEASE"


class Message:
    def __init__(self, msg_type, sender_id, receiver_id, requester=None):
        self.type = msg_type
        self.sender = sender_id
        self.receiver = receiver_id
        self.requester = sender_id if requester is None else requester

    def __repr__(self):
        t = self.type.value if hasattr(self.type, "value") else str(self.type)
        return f"{t}({self.sender} -> {self.receiver}, req={self.requester})"
