from Node import Node

class Tree:
    def __init__(self, nodes_levels=None):
        self.nodes_levels = nodes_levels if nodes_levels else {}
        self.channels = []

    def addRoot(self, node):
        self.nodes_levels[0] = [node]
        node.token = True

    def addLevel(self, nodes):
        level = len(self.nodes_levels)
        node_to_add = []

        for node in nodes:
            node_to_add.append(node)

        self.nodes_levels[level] = node_to_add

    def addChannels(self, node1, node2):
        level1 = None
        level2 = None
        for level in self.nodes_levels:
            if node1 in self.nodes_levels[level]:
                level1 = level
            if node2 in self.nodes_levels[level]:
                level2 = level
        if level1 != None and level2 != None:
            if level2 == level1 + 1:
                self.channels.append([node1, node2])
            elif level2 == level1:
                print("Error: Nodes are in the same level and can't be connected")
            else:
                print("Error: Nodes are not in adjacent levels")
        else:
            raise IndexError("Error: One or both nodes not found in the tree")

    def findNodeWithToken(self):
        for level in self.nodes_levels:
            for node in self.nodes_levels[level]:
                if node.token:
                    return node
            
        raise ValueError("The token was not given yet")
    
    def _buildParentChildRelationships(self):
        for channel in self.channels :
            channel[0].children.append(channel[1])
            channel[1].father = channel[0]
    
    def get_path_to_root(self, node):
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = current.father
        return path
    
    # def get_common_ancestor(self, node1, node2):
    #     pass
                 
    def raymond(self):
        node_with_token = self.findNodeWithToken()
        
        # ============================================================
        # ÉTAPE 1: Initialisation et préparation
        # ============================================================
        # TODO: Initialiser les variables locales pour tous les nœuds:
        # - token: boolean (qui détient le jeton)
        # - request_queue: liste des demandes en attente
        # - father: le nœud parent dans l'arbre
        # - was_asked: booléen indiquant si ce nœud a été demandé
        
        # TODO: Construire le graphe parent-enfant à partir de self.channels
        self._buildParentChildRelationships()
        
        # ============================================================
        # ÉTAPE 2: Demande de section critique
        # ============================================================
        # TODO: Implémenter une méthode request_critical_section(node)
        # - Si le nœud a déjà le jeton → accès direct
        # - Si le jeton est ailleurs:
        #   * Ajouter à sa request_queue locale
        #   * Envoyer une demande à son père (si pas déjà demandé)
        
        # ============================================================
        # ÉTAPE 3: Transmission du jeton
        # ============================================================
        # TODO: Quand un nœud reçoit une demande:
        # - Si le nœud n'a pas le jeton:
        #   * Ajouter la demande à sa queue
        #   * Marquer was_asked = True
        #   * Transmettre la demande à son père
        # - Si le nœud a le jeton:
        #   * Ajouter à sa queue
        #   * Transmettre le jeton au demandeur via le chemin
        
        # ============================================================
        # ÉTAPE 4: Libération du jeton
        # ============================================================
        # TODO: Implémenter release_critical_section(node)
        # - Quand un nœud sort de la section critique:
        #   * Envoyer le jeton au premier nœud de sa request_queue
        #   * Si was_asked = True: envoyer demande au père après
        
        # ============================================================
        # ÉTAPE 5: Circulation du jeton dans l'arbre
        # ============================================================
        # TODO: Implémenter pass_token(from_node, to_node)
        # - Suivre le chemin dans l'arbre jusqu'au destinataire
        # - Mettre à jour la position du token
        # - Notifier le destinataire
        
        print("Algorithme de Raymond initialisé")


















    def toString(self):
        print("Tree structure:")
        for level in self.nodes_levels:
            node_per_level = [node.id for node in self.nodes_levels[level]]
            print(f"Level {level} : {node_per_level}")

        print("Channels:")
        for channel in self.channels:
            print(f"{channel[0].id} <-> {channel[1].id}")

    