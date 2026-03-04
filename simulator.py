## il control le temps et l'ordre d'execution

import heapq
import random
from Node import Node
from Message import Message, MessageType

class Simulator:
    def __init__(self, visualizer=None):
        self.event_queue = [] # queue d'attend de priorité used with heapq
        self.current_time = 0
        self.nodes = {}
        self.last_arrival_per_link = {} #dictionnaire pour garantir l'ordre FIFO par canal
        self.event_seq = 0
        self.visualizer = visualizer
        self.crash_schedule = {}    # format: {timestamp:nodeID}
        self.tree = None

    def crash_simulator(self, tree, node_id):
        if node_id in self.nodes:
            crashed_node = self.nodes[node_id]
            crashed_node.fail()
            if self.visualizer: self.visualizer.nodes_crashed.append(crashed_node)
            
            for neighbor_id in list(crashed_node.neighbors.keys()):
                neighbor = self.nodes[neighbor_id]
                neighbor.neighbors.pop(node_id, None)

            #reparation de l'arbre avant de supprimer le nœud
            node_promoted = tree.rebuild_tree_after_crash(node_id)

            del self.nodes[node_id]

            # remove crashed node in requests queues
            for node in self.nodes.values():
                node.request_queue = list(filter(lambda x: x!=node_id, node.request_queue))
            crashed_node.request_queue = []
            # and retry the failed requests
            while crashed_node.request_queue:
                self.nodes[crashed_node.request_queue.pop(0)].request_cs()
            

            # Node promoted start election for a new leader if crashed node was leader
            # if node promoted has token, it will become directly leader (no election transmission)
            if node_promoted.has_token: node_promoted.become_leader()
            elif node_id == node_promoted.current_leader: node_promoted.start_election()

            if self.visualizer:
                self.visualizer.setNodes(self.tree.nodes)
                self.visualizer.setEdges(self.tree.edges)
                self.visualizer.capture()

    def add_node(self, node): #registre de nodes dans le system
        print(f"Adding node {node} to the simulator.")
        self.nodes[node.node_id] = node
        print(f"Current nodes in the simulator: {list(self.nodes.keys())}")

    #calcul de retard et ajoute des messages dans la file en respectant FIFO
    def schedule_event(self, sender, receiver, message, delay=None):
        if delay is None:
            delay = random.randint(1, 5)
        
        link = (message.sender, message.receiver) #(link = fil)
        last_arrival = self.last_arrival_per_link.get(link, 0)

        #logique FIFO
        arrival_time = max(self.current_time, last_arrival) + delay
        self.last_arrival_per_link[link] = arrival_time

        self.event_seq += 1
        heapq.heappush(self.event_queue, (arrival_time, self.event_seq, message)) #garde dans la file de priorité et orden pour le premier element(arrival_time)

      

    def run(self, steps=None): #execute la simulation en processant event par event
        print("_______beginning of the simulation______")
        processed_steps = 0

        while self.event_queue:
            if steps and processed_steps >= steps or self.event_queue == []:
                break

            arrival_time, _, message = heapq.heappop(self.event_queue)

            # capture another instant system state 
            if self.visualizer and arrival_time != self.current_time:
                self.visualizer.capture()
                self.visualizer.clearTransit()

            #avance le global time au temps de l'evenment actuel
            self.current_time = arrival_time

            # check if crash must happen
            crashed_node_id = self.crash_schedule.get(self.current_time)
            if crashed_node_id:
                self.crash_simulator(self.tree, crashed_node_id)
                self.crash_schedule.pop(self.current_time)

            #donation du message au node destine
            if message.receiver in self.nodes: #ajout du if pour eviter les messages fantomes
                target_node =self.nodes[message.receiver]
                target_node.receive_message(message)

                # draw message transit in visualizer
                if self.visualizer:
                    self.visualizer.messageTransit(self.nodes[message.sender], self.nodes[message.receiver], message.type.value)
                    # view one instant in 2 frames for token moving
                    if message.type.value == "TOKEN":
                        self.visualizer.moveToken(None) # token is moving
                        self.visualizer.capture()
                        self.visualizer.clearTransit()
                        self.visualizer.moveToken(self.nodes[message.receiver])

            else:
                print(f"t={self.current_time}: Message {message} ignoré. Node {message.receiver} n'existe pas/plus.")

            processed_steps += 1


        print("______Simulation finalisé______")
