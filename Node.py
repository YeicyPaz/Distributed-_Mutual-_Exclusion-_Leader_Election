from Message import Message

class Node:
    def __init__(self, node_id, simulator):
        self.id = node_id
        self.simulator = simulator
        self.neighbors = {}  # neighbor_id -> Channel
        self.holder = None
        self.request_queue = []
        self.has_token = False
        self.asked = False

    def add_neighbor(self, neighbor_id, channel):
        self.neighbors[neighbor_id] = channel

    def send_message(self, msg_type, receiver_id):
        message = Message(msg_type, self.id, receiver_id)
        self.simulator.schedule_message(message)

    def receive_message(self, message):
        print(f"[t={self.simulator.time}] Node {self.id} received {message}")

    def request_cs(self):
        print(f"Node {self.id} requests CS")
        self.request_queue.append(self.id)
