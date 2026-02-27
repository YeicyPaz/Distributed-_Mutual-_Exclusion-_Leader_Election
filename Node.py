from Message import Message, MessageType

class Node:
    def __init__(self, node_id, simulator):
        self.node_id = node_id
        self.simulator = simulator
        self.neighbors = {}
        self.parent = None
        self.children = []
        self.holder = None
        self.request_queue = []
        self.has_token = False
        self.asked = False
        self.in_cs = False

    def add_neighbor(self, neighbor_id, channel=None):
        self.neighbors[neighbor_id] = channel

    def send_message(self, msg_type, receiver_id, requester=None, delay=None):
        m = Message(msg_type, self.node_id, receiver_id, requester=requester)
        self.simulator.schedule_event(self.node_id, receiver_id, m, delay=delay)

    def request_cs(self):
        print("t=", self.simulator.current_time,", Node", self.node_id, "demande la section critique")
        if self.node_id not in self.request_queue:
            self.request_queue.append(self.node_id)

        if (not self.has_token) and (not self.asked):
            self.asked = True
            self.send_message(MessageType.REQUEST, self.holder, requester=self.node_id, delay=1)

        if self.has_token and (not self.in_cs):
            self.give_token_if_possible()

    def give_token_if_possible(self):
        if (not self.has_token) or self.in_cs:
            return
        if len(self.request_queue) == 0:
            return

        nxt = self.request_queue.pop(0)
        self.asked = False

        if nxt == self.node_id:
            self.in_cs = True
            print("t=", self.simulator.current_time,", Node", self.node_id, "entre en section critique")
            self.send_message(MessageType.RELEASE, self.node_id, delay=2)
            return

        self.has_token = False
        self.holder = nxt
        self.send_message(MessageType.TOKEN, nxt, requester=nxt, delay=1)

    def leave_cs(self):
        if self.in_cs:
            self.in_cs = False
            print("t=", self.simulator.current_time,", Node", self.node_id, "quitte la section critique")
        self.give_token_if_possible()

    def receive_message(self, message):
        print("t=", self.simulator.current_time,", Node", self.node_id, "reçoit le message", message)

        if message.type == MessageType.REQUEST:
            req = message.requester
            if req not in self.request_queue:
                self.request_queue.append(req)

            if (not self.has_token) and (not self.asked):
                self.asked = True
                self.send_message(MessageType.REQUEST, self.holder, requester=req, delay=1)

            if self.has_token and (not self.in_cs):
                self.give_token_if_possible()

        elif message.type == MessageType.TOKEN:
            self.has_token = True
            self.holder = self.node_id
            self.asked = False
            self.give_token_if_possible()

        elif message.type == MessageType.RELEASE:
            self.leave_cs()


    def toString(self):
        print("Etat de Node ", self.node_id, "holder=", self.holder, ",queue=", self.request_queue, ", token=", self.has_token, ", cs=", self.in_cs, ", asked=", self.asked)