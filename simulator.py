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
    
    def crash_simulator(self,tree, node_id): #the node crash and the tree build it self again
        if node_id in self.nodes:
            print(f"[t={self.time}] Node {node_id} has crashed.")
            crashed_node = self.nodes[node_id]
            
            if(crashed_node.has_token):
                print(f"Node {node_id} was in critical section during crash. Releasing token.")
                # If the crashed node was in the critical section, we need to release the token
                # and trigger the election process to find a new token holder
                
                tree.raymond_election(node_id,3)  #------------ CHANGE the initiator of the election ------------
            
                # After the crash, we need to check if the election process has completed and if the new leader is correctly elected
                token_holders = [nid for nid, node in self.nodes.items() if node.has_token]
                print(f"\n--- Token verification ---")
                if len(token_holders) == 1:
                    print(f"✅ Token détenu uniquement par Node {token_holders[0]}")
                elif len(token_holders) == 0:
                    print(f"⚠️  Aucun nœud ne détient le token")
                else:
                    print(f"❌ VIOLATION : {len(token_holders)} nœuds ont le token : {token_holders}")
                


            # remove the node from neighbors to clean up the network
            for neighbor_id in crashed_node.neighbors:
                neighbor = self.nodes[neighbor_id]
                neighbor.neighbors.pop(node_id, None) #in the neighbor list of neighbors remove the crashed node

            del self.nodes[node_id]
            self.tree.rebuild_tree_after_crash(node_id)

