from Channel import Channel
from Node import Node
from tree import Tree
from simulator import Simulator
from Message import MessageType
from visualizer import Visualizer


class Main:
    def __init__(self):
        self.tree = Tree()
        self.channels = Channel()
        self.nodes = Node(self.tree, self.channels)

if __name__ == "__main__":
    sim = Simulator()

    n1 = Node(1, sim)
    n2 = Node(2, sim)

    sim.add_node(n1)
    sim.add_node(n2)

    n1.send_message(MessageType.REQUEST, 2)

    nodes = [Node(1,sim), Node(2, sim), 
                      Node(3, sim), Node(4, sim), 
                      Node(5, sim), Node(6, sim), Node(7, sim), Node(8, sim)]
    tree = Tree()
    tree.addRoot(nodes[0])
    tree.addLevel([nodes[1], nodes[2]])
    tree.addLevel([nodes[3], nodes[4], nodes[5], nodes[6]])
        
    tree.addChannels(nodes[0], nodes[1])
    tree.addChannels(nodes[0], nodes[2])
    tree.addChannels(nodes[1], nodes[3])
    tree.addChannels(nodes[2], nodes[4])
    tree.addChannels(nodes[2], nodes[5])
    tree.addChannels(nodes[2], nodes[6])
    
    tree.toString()

    sim.run()

    # Init
    visualizer = Visualizer()
    visualizer.setNodes(nodes)
    visualizer.setEdges(tree.channels)
    visualizer.setLeader(nodes[0])
    visualizer.moveToken(nodes[0])
    visualizer.capture()

    # Test all features
    visualizer.moveToken(nodes[2])
    visualizer.messageTransit(nodes[0], nodes[1], "coordinator")
    visualizer.messageTransit(nodes[0], nodes[2], "coordinator")
    visualizer.messageTransit(nodes[6], nodes[2], "election")
    visualizer.messageTransit(nodes[4], nodes[2], "request")
    visualizer.messageTransit(nodes[3], nodes[1], "request")
    visualizer.capture()
    visualizer.clearTransit()
    visualizer.capture()
