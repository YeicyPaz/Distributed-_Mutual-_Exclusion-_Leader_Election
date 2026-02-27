import os
import graphviz
from Node import Node

class Visualizer:

    msg_colors = {"request":"orange", "token":"maroon", "election":"blue", "coordinator":"purple"}


    def __init__(self, img_folder="default", autocapture=False):
        # autocapture permits to capture tree when system state change (token move, leader election, ...)
        # but it's not good for showing events that are happening at the same time
        self.img_folder = 'tree_img/'+img_folder
        self.clear_img_folder()
        self.nb_img = 0
        self.autocapture = autocapture
        self.nodes = []
        self.edges = []         # format: [(node1, node2)]      -> represents channels betweeen processes
        self.edges_msg = {}     # format: {(sender_node, receiver_node): message_type}
        self.nodeWithToken = None
        self.nodeLeader = None
    
    def setNodes(self, nodes:[Node]):
        self.nodes = nodes


    def setEdges(self, edges:[[Node, Node]]):
        self.edges = []
        self.edges_msg = {}
        for node1,node2 in edges:
            self.edges.append((node1, node2))


    def moveToken(self, node:Node):
        self.nodeWithToken = node
        if self.autocapture: self.capture()
    

    def setLeader(self, node:Node):
        self.nodeLeader = node
        if self.autocapture: self.capture()
    

    def messageTransit(self, sender:Node, receiver:Node, msg_type:str):
        self.edges_msg[(sender, receiver)] = msg_type
    
    
    def clearTransit(self):
        self.edges_msg = {}
    

    def capture(self):
        # Build tree processes system and save as SVG
        tree = graphviz.Digraph(filename=str(self.nb_img), format='svg')
        
        for node in self.nodes:
            border_color = "red" if node == self.nodeWithToken else "black"
            if node == self.nodeLeader:
                tree.node(str(node.id), color=border_color, style='filled', fillcolor='yellow')
            else:
                tree.node(str(node.id), color=border_color, style='solid')
        
        for node1, node2 in self.edges:
            if (node1,node2) in self.edges_msg:
                # message transits from father to son -> display directed link to the son
                msg_type = self.edges_msg[(node1,node2)]
                color = Visualizer.msg_colors[msg_type] if msg_type in Visualizer.msg_colors else "black"
                tree.edge(str(node1.id), str(node2.id), color=color, dir='forward')
            
            elif (node2,node1) in self.edges_msg:
                # message transits from son to father -> display directed link to the father
                msg_type = self.edges_msg[(node2,node1)]
                color = Visualizer.msg_colors[msg_type] if msg_type in Visualizer.msg_colors else "black"
                tree.edge(str(node1.id), str(node2.id), color=color, dir='back')    # trick to keep same tree structure with edge from father to son but inversed arrow
            
            else:
                # no message transits -> display simple link to represent channel between processes
                tree.edge(str(node1.id), str(node2.id), color="black", dir='none')

        self.nb_img += 1
        return tree.render(directory=self.img_folder)


    def clear_img_folder(self):
        for file in os.listdir(self.img_folder):
            try: os.remove(self.img_folder+'/'+file)
            except: continue
