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
        self.is_alive = True
        self.current_leader = None

    def fail(self): #crash du node
        print("t=", self.simulator.current_time,", Node", self.node_id, "crash")
        self.is_alive = False

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

        if len(self.request_queue) > 0 and (not self.asked) and (self.holder is not None):
            self.asked = True
            self.send_message(MessageType.REQUEST, self.holder, requester=self.request_queue[0], delay=1)

    def leave_cs(self):
        if self.in_cs:
            self.in_cs = False
            print("t=", self.simulator.current_time,", Node", self.node_id, "quitte la section critique")
        self.give_token_if_possible()

    def receive_message(self, message):
        if not self.is_alive:
            print("t=", self.simulator.current_time,", Node", self.node_id, "ignore le message car le node a crash", message)
            return
        print("t=", self.simulator.current_time,", Node", self.node_id, "reçoit le message", message)

        if message.type == MessageType.REQUEST:
            origin = message.requester         
            neighbor = message.sender

            if neighbor not in self.request_queue:
                self.request_queue.append(neighbor)

            if (not self.has_token) and (self.holder is not None) and (len(self.request_queue) == 1):
                self.asked = True
                self.send_message(MessageType.REQUEST, self.holder, requester=origin, delay=1)

            if self.has_token and (not self.in_cs):
                self.give_token_if_possible()

        elif message.type == MessageType.TOKEN:
            self.has_token = True
            self.holder = self.node_id
            self.asked = False
            # CONDITION D'ÉLECTION : 
            # Si je reçois le jeton et que je sais qu'une élection est en cours 
            # (ou que le leader précédent est mort)
            if self.simulator.nodes.get(self.current_leader) is None or not hasattr(self.simulator.nodes[self.current_leader], 'is_alive') or not self.simulator.nodes[self.current_leader].is_alive:
                self.become_leader()
            self.give_token_if_possible()

        elif message.type == MessageType.RELEASE:
            self.leave_cs()
        
        elif message.type == MessageType.COORDINATOR:
            self.current_leader = message.requester
            # le token est dans la direction de celui qui m'envoie l'info
            self.holder = message.sender 
            
            print(f"---->Node {self.node_id} confirme : le nouveau COORDINATEUR est Node {self.current_leader} (connu via Node {message.sender})")
            # annonce du nouveau coordinateur aux voisins
            for neighbor_id in self.neighbors:
                if neighbor_id != message.sender:
                    self.send_message(MessageType.COORDINATOR, neighbor_id, requester=message.requester, delay=1)

            # si il y a des requetes en attente, je les renvoie vers le nouveau holder
            if self.request_queue and not self.has_token:
                self.asked = True
                self.send_message(MessageType.REQUEST, self.holder, requester=self.request_queue[0], delay=1)
                
    def become_leader(self):
        self.current_leader = self.node_id
        for neighbor_id in self.neighbors:
            self.send_message(MessageType.COORDINATOR, neighbor_id, requester=self.node_id, delay=1)

    def toString(self):
        print("Etat de Node ", self.node_id, "holder=", self.holder, ",queue=", self.request_queue, ", token=", self.has_token, ", cs=", self.in_cs, ", asked=", self.asked)