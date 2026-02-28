from platform import node

from shapely import node
import random


class Tree:
    def __init__(self, simulator):
        self.sim = simulator
        self.nodes = {}
        self.edges = []     #  arete (parent_id, child_id)
        self.election_in_progress = False

    def add_node(self, node):
        # ajoute le node dans la structure arbre
        self.nodes[node.id] = node
        # enregistre aussi le node dans simulateur
        self.sim.add_node(node)

    def connect_parent_child(self, parent_id, child_id):
        # recupere les objets Node
        p = self.nodes[parent_id]
        c = self.nodes[child_id]

        # relation arbre
        p.children.append(c)
        c.parent = p

        # relation reseau (voisins pour envoi de messages)
        p.add_neighbor(child_id)
        c.add_neighbor(parent_id)

        # memorise l arete
        self.edges.append((parent_id, child_id))

    def init_holders_from_token(self, token_id):
        # Breadth-First Search pour orienter tous les holder vers le token initial
        visited = {}
        parent_in_bfs = {}

        # initialisation Breadth-First Search à partir du node qui possede le token
        q = [token_id]
        visited[token_id] = True
        parent_in_bfs[token_id] = None

        # construction de la liste d’adjacence
        adj = {}
        for (a, b) in self.edges:
            if a not in adj: adj[a] = []
            if b not in adj: adj[b] = []
            adj[a].append(b)
            adj[b].append(a)

        # parcours Breadth-First Search pour trouver les parents de chaque node dans le BFS
        while len(q) > 0:
            cur = q.pop(0)
            for nxt in adj.get(cur, []):
                if nxt not in visited:
                    visited[nxt] = True
                    parent_in_bfs[nxt] = cur
                    q.append(nxt)

        # initialisation des variables Raymond pour chaque node
        for nid, node in self.nodes.items():
            node.has_token = False
            node.in_cs = False
            node.asked = False
            node.request_queue = []

            if nid == token_id:
                # le token holder pointe sur lui meme
                node.holder = nid
                node.has_token = True
            else:
                # le holder pointe vers le voisin qui rapproche du token
                node.holder = parent_in_bfs[nid]

    def toString(self, ids):
        # affiche l etat de certain nodes
        for nid in ids:
            self.nodes[nid].toString()

    def rebuild_tree_after_crash(self, crashed_node_id):
        crashed = self.nodes[crashed_node_id]
        orphan_children = crashed.children
        crashed_parent = crashed.parent
        if crashed_parent is not None:
            # if the crashed node is not the root
            for child in orphan_children:
                self.connect_parent_child(crashed_parent.id, child.id)
        else: #if its the root
            if len(orphan_children) > 0:
                new_root = orphan_children[0]
                new_root.parent = None
                
                for child in orphan_children[1:]:
                    if len(orphan_children) > 0:
                        new_root = orphan_children[0]
                        new_root.parent = None
                        print(f"Node {new_root.id} devient nouvelle racine")
                        
                        # the orphan children (except the new root) are reattached to the new root
                        for child in orphan_children[1:]:
                            child.parent = new_root          # lien arbre
                            new_root.children.append(child)  # lien arbre
                            new_root.add_neighbor(child.id)  # lien réseau
                            child.add_neighbor(new_root.id)  # lien réseau
                            self.edges.append((new_root.id, child.id))  # arête
                            print(f"Node {child.id} attached to {new_root.id}")


    def test1_raymond_election(self, crashed_node_id, initiator_id):
        print(f"\n=== ELECTION after crash of Node {crashed_node_id}, initiated by Node {initiator_id} ===")
        self.election_in_progress = True
        nodes_in_election = set(self.nodes.keys()) - {crashed_node_id}  # we take all nodes except the crashed one
        for node_id, node in self.nodes.items():
            if node_id in nodes_in_election:
                print(f"Node {node_id} enters the election process.")
                node.request_cs()
        
        #we give the token to the elected node
        for node_id, node in self.nodes.items():
            if node_id == crashed_node_id:
                
                node.has_token = False  # the crashed node can no longer hold the token

    def raymond_election(self, crashed_node_id, initiator_id):
        print(f"\n=== ELECTION after crash of Node {crashed_node_id}, initiated by Node {initiator_id} ===")
        self.election_in_progress = True
        
        nodes_in_election = set(self.nodes.keys()) - {crashed_node_id}
        
        other_nodes = list(nodes_in_election - {initiator_id})
        random.shuffle(other_nodes)
        ordered_nodes = [initiator_id] + other_nodes 

        #asking to enter the cs with previous order
        for node_id in ordered_nodes:
            node = self.nodes[node_id]
            print(f"Node {node_id} enters the election process.")
            node.request_cs()
    
        #we give the token to the elected node
        for node_id in self.nodes:
            node = self.nodes[node_id]
            if node.has_token:
                print(f"the queue of the crashed node {node_id} is: {node.request_queue}")
                node.give_token_if_possible()  # the elected node takes the token and enters the critical section
        
