class Tree:
    def __init__(self, simulator):
        self.sim = simulator
        self.nodes = {}
        self.edges = []     #  arete (parent_id, child_id)

    def add_node(self, node):
        # ajoute le node dans la structure arbre
        self.nodes[node.node_id] = node
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

    def rebuild_tree_after_crash(self, crashed_node_id):
        if crashed_node_id not in self.nodes:
            return
            
        crashed = self.nodes[crashed_node_id]
        orphan_children = crashed.children
        crashed_parent = crashed.parent

        print(f"--- Réparation de l'arbre après crash du Node {crashed_node_id} ---")

        if crashed_parent is not None:
            # détache le nœud crashé de son parent
            if crashed in crashed_parent.children:
                crashed_parent.children.remove(crashed)
                
            for child in orphan_children:
                self.connect_parent_child(crashed_parent.id, child.id)
                #le fils doit pointer vers son nouveau parent pour le jeton
                child.holder = crashed_parent.id
                print(f"Node {child.id} est maintenant rattaché à son grand-parent {crashed_parent.id}")
        else:
            # si c'etait la racine, on choisit le premier enfant comme nouvelle racine
            if len(orphan_children) > 0:
                new_root = orphan_children[0]
                new_root.parent = None
                new_root.holder = new_root.node_id # la racine pointe sur elle-même
                
                for child in orphan_children[1:]:
                    self.connect_parent_child(new_root.node_id, child.node_id)
                    child.holder = new_root.node_id
                print(f"Node {new_root.node_id} devient la nouvelle racine")

    def toString(self, ids):
        # affiche l etat de certain nodes
        for nid in ids:
            self.nodes[nid].toString()