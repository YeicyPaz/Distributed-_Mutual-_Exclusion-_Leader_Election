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

    def toString(self, ids):
        # affiche l etat de certain nodes
        for nid in ids:
            self.nodes[nid].toString()