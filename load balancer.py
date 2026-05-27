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

    def inserir(self, node, valor):
        if not node:
            return node(valor)

        if valor < node.valor:
            node.filho_esquerdo = self.inserir(node.filho_esquerdo, valor)
        else:
            node.filho_direito = self.inserir(node.filho_direito, valor)

        self.recalcular_altura(node)

        fator_balanceamento = self.balanceamento(node)

        #Esquerda-Esquerda
        if fator_balanceamento > 1 and valor < node.filho_esquerdo.valor:
            return self.rotacionar_direita(node)

        #Direita-Direita
        if fator_balanceamento < -1 and valor > node.filho_direito.valor:
            return self.rotacionar_esquerda(node)

        #Esquerda-Direita
        if fator_balanceamento > 1 and valor > node.filho_esquerdo.valor:
            node.filho_esquerdo = self.rotacionar_esquerda(node.filho_esquerdo)
            return self.rotacionar_direita(node)

        #Direita-Esquerda
        if fator_balanceamento < -1 and valor < node.filho_direito.valor:
            node.filho_direito = self.rotacionar_direita(node.filho_direito)
            return self.rotacionar_esquerda(node)

        return node

class nodeRN:
    def __init__(self, valor):
        self.valor = valor
        self.cor = "Vermelho"
        self.esquerda = None
        self.direita = None
        self.pai = None
