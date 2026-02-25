from Simulator import Simulator
from Node import Node
from tree import Tree
from Message import MessageType

if __name__ == "__main__":
    sim = Simulator()
    tree = Tree(sim)

    nodes = {}
    for i in range(1, 9):
        n = Node(i, sim)
        nodes[i] = n
        tree.add_node(n)

    tree.connect_parent_child(1, 2)
    tree.connect_parent_child(1, 3)
    tree.connect_parent_child(2, 4)
    tree.connect_parent_child(3, 5)
    tree.connect_parent_child(3, 6)
    tree.connect_parent_child(3, 7)
    tree.connect_parent_child(7, 8)

    tree.init_holders_from_token(token_id=1)

    nodes[1].in_cs = True
    print("Initial: token at Node 1 and it is in CS")

    nodes[1].send_message(MessageType.RELEASE, 1, delay=1)

    nodes[4].request_cs()
    nodes[7].request_cs()
    nodes[5].request_cs()

    tree.toString([1, 2, 3, 4, 5, 7])
    sim.run()
    tree.toString([1, 2, 3, 4, 5, 7])