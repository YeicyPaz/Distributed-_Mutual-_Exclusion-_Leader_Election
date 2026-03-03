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


    ## Sample Test made without logical code (just visualizer) -> see SW4

    nodes = {id: Node(id,sim) for id in range(1,11)}
    tree_sw4 = Tree()
    tree_sw4.addRoot(nodes[1])
    tree_sw4.addLevel([nodes[2], nodes[3]])
    tree_sw4.addLevel([nodes[4], nodes[5], nodes[6], nodes[7], nodes[8]])
    tree_sw4.addLevel([nodes[9], nodes[10]])

    tree_sw4.addChannels(nodes[1], nodes[2])
    tree_sw4.addChannels(nodes[1], nodes[3])
    tree_sw4.addChannels(nodes[2], nodes[4])
    tree_sw4.addChannels(nodes[2], nodes[5])
    tree_sw4.addChannels(nodes[2], nodes[6])
    tree_sw4.addChannels(nodes[3], nodes[7])
    tree_sw4.addChannels(nodes[3], nodes[8])
    tree_sw4.addChannels(nodes[8], nodes[9])
    tree_sw4.addChannels(nodes[8], nodes[10])

    visualizer = Visualizer()

    # Capture 0 : initialization
    visualizer.setNodes(list(nodes.values()))
    visualizer.setEdges(tree_sw4.channels)
    visualizer.setLeader(nodes[1])
    visualizer.moveToken(nodes[1])
    nodes[1].request_queue.append(2)
    nodes[2].request_queue.append(6)
    nodes[6].request_queue.append(6)
    visualizer.capture()

    # Capture 1 : node 1 keep token (in the CS) and nodes 9, 7 and 5 request the token
    nodes[9].request_queue.append(9)
    nodes[7].request_queue.append(7)
    nodes[5].request_queue.append(5)
    visualizer.messageTransit(nodes[9], nodes[8], "request")
    visualizer.messageTransit(nodes[7], nodes[3], "request")
    visualizer.messageTransit(nodes[5], nodes[2], "request")
    visualizer.capture()
    visualizer.clearTransit()

    # Capture 2 : update of request queues
    nodes[8].request_queue.append(9)
    nodes[3].request_queue.append(7)
    nodes[2].request_queue.append(5)
    visualizer.capture()

    # Capture 3 : node 1 keep token (in the CS) and propagation of requests
    visualizer.messageTransit(nodes[8], nodes[3], "request")
    visualizer.messageTransit(nodes[3], nodes[1], "request")
    visualizer.messageTransit(nodes[2], nodes[1], "request")
    visualizer.capture()
    visualizer.clearTransit()
    
    # Capture 4 : update of request queues
    nodes[3].request_queue.append(8)
    nodes[1].request_queue.append(3)
    visualizer.capture()

    # Capture 5 : node 1 leaves the CS and give token to first node in request queue (normally node 2)
    receiver_id = nodes[1].request_queue.pop(0)
    visualizer.messageTransit(nodes[1], nodes[receiver_id], "token")
    visualizer.moveToken(None)
    visualizer.capture()
    visualizer.clearTransit()

    # Capture 6 : Token holder changes (normally node 2) and add node which gives the token to request queue
    visualizer.moveToken(nodes[receiver_id])
    nodes[receiver_id].request_queue.append(1)
    visualizer.capture()

    # Continue the algorithm
    while len(nodes[receiver_id].request_queue) > 0:
        sender_id = receiver_id
        receiver_id = nodes[sender_id].request_queue.pop(0)
        #print("sender:",sender_id,nodes[sender_id].request_queue,"receiver",receiver_id,nodes[receiver_id].request_queue)
        if sender_id == receiver_id:
            # node is itself in its request queue -> node needs token to access cs
            # one momentary pause for access to the CS
            visualizer.capture()
            continue
        visualizer.messageTransit(nodes[sender_id], nodes[receiver_id], "token")
        visualizer.moveToken(None)
        visualizer.capture()
        visualizer.clearTransit()
        
        visualizer.moveToken(nodes[receiver_id])
        if len(nodes[sender_id].request_queue) > 0:
            # the node that gives token has others nodes in request queue so needs the token back
            nodes[receiver_id].request_queue.append(sender_id)
        visualizer.capture()

    # Test all features
    # visualizer.moveToken(None)
    # nodes[0].request_queue.pop(0)
    # visualizer.messageTransit(nodes[0], nodes[1], "coordinator")
    # visualizer.messageTransit(nodes[0], nodes[2], "token")
    # visualizer.messageTransit(nodes[6], nodes[2], "election")
    # visualizer.messageTransit(nodes[4], nodes[2], "request")
    # visualizer.messageTransit(nodes[3], nodes[1], "request")
    # visualizer.capture()
    # visualizer.clearTransit()
    # visualizer.moveToken(nodes[2])
    # nodes[1].request_queue.append(4)
    # nodes[2].request_queue.append(5)
    # visualizer.capture()
    
    visualizer.show()
