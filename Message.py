

class Message:
    def __init__(self, sender, receiver, content, timestamp=None):
        self.sender=sender
        self.receiver=receiver
        self.content=content #request ou token, ou coordinator
        self.timestamp= timestamp

    def __repr__(self):
        return f"[{self.content}] de {self.sender} a {self.receiver}"