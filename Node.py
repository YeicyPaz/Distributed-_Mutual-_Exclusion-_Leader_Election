from Message import Message


class Node:
    def __inti__ (self, node_id, simulator:Simulator, holder:Node = None, token:bool=False ):
        self.simulator=simulator
        self.node_id=node_id
        self.holder=holder
        self.token=token
        self.queue=[]

    def send_message(self, destination:Node, content:str):
        message = Message(self, destination, content)
        self.simulator.schedule_event()
        destination.receive_message(message)

    def receive_message(message:Message):
        if message.content == "REQUEST":
            pass
        if message.content == "TOKEN":
            pass

    def handle_message():      
        pass

        
