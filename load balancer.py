class nodeAVL:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1

class AVL_Router_Tree:
    def __init__(self):
        self.raiz = None

class nodeRN:
    def __init__(self, valor):
        self.valor = valor
        self.cor = "Vermelho"
        self.esquerda = None
        self.direita = None
        self.pai = None
