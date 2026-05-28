class Node:
    def __init__(self, valor, cor="VERMELHO"):
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

    def rotacionar_direita(self, node_y):
        node_x = node_y.filho_esquerdo
        subtree_t2 = node_x.filho_direito
        #==============================#
        node_x.filho_direito = node_y
        node_y.filho_esquerdo = subtree_t2
        self.recalcular_altura(node_y)
        self.recalcular_altura(node_x)
        return node_x

    def rotacionar_esquerda(self, node_x):
        node_y = node_x.filho_direito
        subtree_t2 = node_y.filho_esquerdo
        #===============================#
        node_y.filho_esquerdo = node_x
        node_x.filho_direito = subtree_t2
        self.recalcular_altura(node_x)
        self.recalcular_altura(node_y)
        return node_y

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

        self.recalcular_altura(raiz)
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


class RedBlack_Router_Tree:
    def __init__(self):
        self.NIL = Node(0)
        self.NIL.cor = "PRETO"
        self.NIL.filho_esquerdo = None
        self.NIL.filho_direito = None
        self.raiz = self.NIL

    def rotacionar_esquerda(self, node_x):
        node_y = node_x.filho_direito
        node_x.filho_direito = node_y.filho_esquerdo
        if node_y.filho_esquerdo != self.NIL:
            node_y.filho_esquerdo.pai = node_x

        node_y.pai = node_x.pai

        if node_x.pai is None:
            self.raiz = node_y
        elif node_x == node_x.pai.filho_esquerdo:
            node_x.pai.filho_esquerdo = node_y
        else:
            node_x.pai.filho_direito = node_y

        node_y.filho_esquerdo = node_x
        node_x.pai = node_y

    def rotacionar_direita(self, node_y):
        node_x = node_y.filho_esquerdo
        node_y.filho_esquerdo = node_x.filho_direito

        if node_x.filho_direito != self.NIL:
            node_x.filho_direito.pai = node_y

        node_x.pai = node_y.pai

        if node_y.pai is None:
            self.raiz = node_x
        elif node_y == node_y.pai.filho_direito:
            node_y.pai.filho_direito = node_x
        else:
            node_y.pai.filho_esquerdo = node_x

        node_x.filho_direito = node_y
        node_y.pai = node_x

    def corrigir_inserir(self, k:Node):
        while k.pai.cor == "VERMELHO":

            if k.pai == k.pai.pai.filho_direito:
                tio = k.pai.pai.filho_esquerdo

                if tio.cor == "VERMELHO":
                    tio.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:
                    if k == k.pai.filho_esquerdo:
                        k = k.pai
                        self.rotacionar_direita(k)

                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self.rotacionar_esquerda(k.pai.pai)

            else:
                tio = k.pai.pai.filho_direito

                if tio.cor == "VERMELHO":
                    tio.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:
                    if k == k.pai.filho_direito:
                        k = k.pai
                        self.rotacionar_esquerda(k)

                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self.rotacionar_direita(k.pai.pai)

            if k == self.raiz:
                break

        self.raiz.cor = "PRETO"

    def inserir(self, valor):
        novo_node = Node(valor)
        novo_node.filho_esquerdo = self.NIL
        novo_node.filho_direito = self.NIL
        pai = None
        atual = self.raiz

        while atual != self.NIL:
            pai = atual.filho_esquerdo
            if novo_node.valor < atual.valor:
                atual = atual.filho_esquerdo
            else:
                atual = atual.filho_direito

        novo_node.pai = pai

        if pai is None:
            self.raiz = novo_node
        elif novo_node.valor < pai.valor:
            pai.filho_esquerdo = novo_node
        else:
            pai.filho_direito = novo_node

        if novo_node.pai is None:
            novo_node.cor = "PRETO"
            return

        if novo_node.pai.pai is None:
            return

        self.corrigir_inserir(novo_node)