class Channel:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self.queue = []

    def send(self, message):
        self.queue.append(message)

    def pop(self):
        if self.queue:
            return self.queue.pop(0)
        return None
