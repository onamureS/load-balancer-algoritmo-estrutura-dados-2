class NodeAVL:
    def __init__(self, valor):
        self.valor = valor
        self.filho_esquerdo = None
        self.filho_direito = None
        self.altura = 1

class AVL_Router_Tree:
    def __init__(self):
        self.raiz = None

    def get_altura(self, node):
        if not node:
            return 0
        return node.altura

    def recalcular_altura(self, node):
        node.altura = 1 + max(self.get_altura(node.filho_esquerdo), self.get_altura(node.filho_direito))

    def balanceamento(self, node):
        if not node:
            return 0
        return self.get_altura(node.filho_esquerdo) - self.get_altura(node.filho_direito)

    def rotacionar_direita(self, node_inicial):
        filho = node_inicial.filho_esquerdo
        subtree_t2 = filho.filho_direito
        #==============================#
        filho.filho_direito = node_inicial
        node_inicial.filho_esquerdo = subtree_t2
        #node_inicial.altura = 1 + max(self.get_altura(node_inicial.filho_esquerdo), self.get_altura(node_inicial.filho_direito))
        self.recalcular_altura(node_inicial)
        self.recalcular_altura(filho)
        #filho.altura = 1 + max(self.get_altura(filho.filho_esquerdo), self.get_altura(filho.filho_direito))
        return filho

    def rotacionar_esquerda(self, node_inicial):
        filho = node_inicial.filho_direito
        subtree_t2 = filho.filho_esquerdo
        #===============================#
        filho.filho_esquerdo = node_inicial
        node_inicial.filho_direito = subtree_t2
        self.recalcular_altura(node_inicial)
        self.recalcular_altura(filho)
        return filho

class nodeRN:
    def __init__(self, valor):
        self.valor = valor
        self.cor = "Vermelho"
        self.esquerda = None
        self.direita = None
        self.pai = None
