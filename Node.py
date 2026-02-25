from Message import Message



class Node:
    def __init__ (self, node_id, simulator, holder:Node = None, token:bool=False ):
        self.simulator=simulator
        self.node_id=node_id
        self.holder= None
        self.queue=[] #pour la 2eme partie

    def send_message(self, destination_id:Node, content:str):
        message = Message(self.node_id, destination_id, content)
        #on le pass au simulateur
        # Nota: schedule_event espera (sender, receiver, message)
        self.simulator.schedule_event(self.node_id, destination_id, message)
        

    def handle_message(self,message:Message):
        if message.content == "REQUEST":
            pass
        if message.content == "TOKEN":
            pass
        
        print(f"Time={self.simulator.current_time} | Node {self.node_id} received {message}")
    

        
