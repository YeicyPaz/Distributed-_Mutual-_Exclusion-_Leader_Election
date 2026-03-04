from simulator import Simulator
from Node import Node
from tree import Tree
from Message import MessageType
from visualizer import Visualizer

if __name__ == "__main__":
    visualizer = Visualizer(img_folder="default")   # CHOOSE NAME OF FOLDER TO SAVE SNAPSHOTS (Beware of overwrite!)
    sim = Simulator(visualizer)
    tree = Tree(sim)
    sim.tree = tree

    # CHOOSE THE NUMBER OF NODES HERE
    nodes = {}
    for i in range(1,11):
        node = Node(i, sim)
        nodes[i] = node
        tree.add_node(node)
    visualizer.setNodes(nodes)

    # CREATE TREE STRUCTURE HERE
    edges = [
        [1,2], [1,3],
        [2,4], [2,5], [2,6], [3,7], [3,8],
        [8,9], [8,10]
    ]
    for i,j in edges:
        tree.connect_parent_child(i,j)
    visualizer.setEdges(edges)

    # CHOOSE THE NODE LEADER OF SYSTEM
    leader = 1
    visualizer.setLeader(nodes[leader])
    # init the leader knowledge by nodes to prevent new election at start
    for node in nodes.values():
        node.current_leader = leader

    # CHOOSE NODES THAT WILL CRASH AND WHEN (to simulate new leader election)
    sim.crash_schedule[16] = 1    # node 1 (leader) will crash at timestamp 15

    # CHOOSE THE TOKEN'S HOLDER AT STARTING AND WHEN IT RELEASES
    tk_holder = 1
    tree.init_holders_from_token(token_id=tk_holder)
    nodes[tk_holder].in_cs = True
    print(f"Initial: token at Node {tk_holder} and it is " + "" if nodes[tk_holder].in_cs else "not" + " in CS")
    nodes[tk_holder].send_message(MessageType.RELEASE, tk_holder, delay=3)
    visualizer.moveToken(nodes[tk_holder])

    # CHOOSE NODES THAT REQUEST TOKEN AT STARTING
    nodes[6].request_cs()
    nodes[9].request_cs()
    nodes[7].request_cs()
    nodes[5].request_cs()

    tree.toString(nodes.keys())
    sim.run()
    tree.toString(nodes.keys())

    visualizer.show()
