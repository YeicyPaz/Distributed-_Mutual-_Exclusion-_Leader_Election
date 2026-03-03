## il control le temps et l'ordre d'execution

import heapq
import random
from Node import Node
from Message import Message, MessageType

class Simulator:
    def __init__(self):
        self.event_queue = [] # queue d'attend de priorité used with heapq
        self.current_time = 0
        self.nodes = {}
        self.last_arrival_per_link = {} #dictionnaire pour garantir l'ordre FIFO par canal
        self.event_seq = 0

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

            #avance le global time au temps de l'evenment actuel
            self.current_time = arrival_time

            #donation du message au node destine
            target_node =self.nodes[message.receiver]
            target_node.receive_message(message)

            processed_steps += 1


        print("______Simulation finalisé______")

    

# ## ____TEST____
# if __name__=="__main__":
#     sim = Simulator()

#     #creation de node de test
#     n1= Node(1, sim)
#     n2= Node(2, sim)
#     n3= Node(3, sim)

    

#     sim.add_node(n1)
#     sim.add_node(n2)
#     sim.add_node(n3)

#     n1.has_token = True
#     n1.holder = 1

#     n2.has_token = False
#     n2.holder = 1

#     n3.has_token = False
#     n3.holder = 1
                
#     #simulation d'envoi de message pour tester l'ordre FIFO et les retards des system
#     print("Programando mensajes...")
#     n1.send_message(MessageType.REQUEST, 3)
#     n1.send_message(MessageType.REQUEST, 2)
            
#     # Ejecutar
#     sim.run()