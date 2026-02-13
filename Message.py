from Node import Node

class Message:
    def __init__(self, sender:Node, receiver:Node, content, timestamp=None):
        self.sender=sender
        self.receiver=receiver
        self.content=content
        self.timestamp= timestamp
