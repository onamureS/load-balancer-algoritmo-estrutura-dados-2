class Node:
    def __init__(self, valor, cor="Vermelho"):
        self.valor = valor
        self.filho_esquerdo = None
        self.filho_direito = None
        self.pai = None
        self.altura = 1
        self.cor = cor

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
        self.recalcular_altura(node_inicial)
        self.recalcular_altura(filho)
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

    def menor_valor(self, node):
        node_atual = node
        while node_atual.filho_esquerdo is not None:
            node_atual = node_atual.filho_esquerdo
        return node_atual

    def remover(self, raiz, valor):
        if not raiz:
            return raiz
        elif valor < raiz.valor:
            raiz.filho_esquerdo = self.remover(raiz.filho_esquerdo, valor)
        elif valor > raiz.valor:
            raiz.filho_direito = self.remover(raiz.filho_direito, valor)
        else:
            if raiz.filho_esquerdo is None:
                temp = raiz.filho_direito
                raiz = None
                return temp
            elif raiz.filho_direito is None:
                temp = raiz.filho_esquerdo
                raiz = None
                return temp

            temp = self.menor_valor(raiz.filho_direito)
            raiz.valor = temp.valor
            raiz.filho_direito = self.remover(raiz.filho_direito, temp.valor)

        if raiz is None:
            return raiz

        raiz.altura = self.recalcular_altura(raiz)
        fator_balanceamento = self.balanceamento(raiz)

        #Esquerda-Esquerda
        if fator_balanceamento > 1 and raiz.valor < raiz.filho_esquerdo.valor:
            return self.rotacionar_direita(raiz)

        #Direita-Direita
        if fator_balanceamento < -1 and valor > raiz.filho_direito.valor:
            return self.rotacionar_esquerda(raiz)

        #Esquerda-Direita
        if fator_balanceamento > 1 and valor > raiz.filho_esquerdo.valor:
            raiz.filho_esquerdo = self.rotacionar_esquerda(raiz.filho_esquerdo)
            return self.rotacionar_direita(raiz)

        #Direita-Esquerda
        if fator_balanceamento < -1 and valor < raiz.filho_direito.valor:
            raiz.filho_direito = self.rotacionar_direita(raiz.filho_direito)
            return self.rotacionar_esquerda(raiz)

        return raiz