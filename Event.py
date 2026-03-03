class Event:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message

    def __lt__(self, other):
        return self.timestamp < other.timestamp
