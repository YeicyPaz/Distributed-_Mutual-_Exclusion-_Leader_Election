import heapq
import random
from Event import Event

class Simulator:
    def __init__(self):
        self.time = 0
        self.event_queue = []
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.id] = node

    def schedule_message(self, message, delay=None):
        if delay is None:
            delay = random.randint(1, 5)

        event_time = self.time + delay
        event = Event(event_time, message)
        heapq.heappush(self.event_queue, event)

        print(f"[t={self.time}] Scheduled {message} at t={event_time}")

    def run(self):
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            self.time = event.timestamp

            receiver = self.nodes[event.message.receiver]
            receiver.receive_message(event.message)