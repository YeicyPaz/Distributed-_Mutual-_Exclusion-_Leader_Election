import heapq

class Simulator:
    def __init__(self):
        self.event_queue = [] # used with heapq
        self.current_time = 0
        self.nodes = {}

    def schedule_event(self, sender, receiver, content, delay=1):
        arrival_time = self.current_time + delay
        event = (arrival_time, sender, receiver, content)
        heapq.heappush(self.event_queue, event)

    def run(self):
        while self.event_queue:
            time, src, dest, msg = heapq.heappop(self.event_queue)
            self.current_time = time
            self.nodes[dest].handle_message(msg, src)