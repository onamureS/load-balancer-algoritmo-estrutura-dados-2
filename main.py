class Packet_Rule:
    def __init__(self, id, ip_origem, ip_destino, prioridade):
        self.id = id
        self.ip_origem = ip_origem
        self.ip_destino = ip_destino
        self.prioridade = prioridade

    def __lt__(self, other):
        return self.prioridade < other.prioridade

    def __gt__(self, other):
        return self.prioridade > other.prioridade

    def __eq__(self, other):
        return (self.prioridade == other.prioridade) and (self.id == other.id)

    def __str__(self):
        return f"[ID={self.id}, Prioridade={self.prioridade}]"


class Node:
    def __init__(self, regra:Packet_Rule, cor="VERMELHO"):
        self.regra = regra
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

    def rotacionar_direita(self, y:Node):
        if y is None:
            return y

        x = y.filho_esquerdo

        if x is None:
            return y

        subtree_t2 = x.filho_direito

        x.filho_direito = y
        y.filho_esquerdo = subtree_t2
        x.pai = y.pai
        y.pai = x

        if subtree_t2 is not None:
            subtree_t2.pai = y

        self.recalcular_altura(y)
        self.recalcular_altura(x)

        return x

    def rotacionar_esquerda(self, x:Node):
        if x is None:
            return x

        y = x.filho_direito

        if x is None:
            return y

        subtree_t2 = y.filho_esquerdo

        y.filho_esquerdo = x
        x.filho_direito = subtree_t2
        y.pai = x.pai
        x.pai = y

        if subtree_t2 is not None:
            subtree_t2.pai = x

        self.recalcular_altura(x)
        self.recalcular_altura(y)

        return y

    def inserir(self, node, regra):
        if not node:
            return Node(regra)

        if regra < node.regra:
            node.filho_esquerdo = self.inserir(node.filho_esquerdo, regra)
            node.filho_esquerdo.pai = node
        else:
            node.filho_direito = self.inserir(node.filho_direito, regra)
            node.filho_direito.pai = node

        self.recalcular_altura(node)

        fator_balanceamento = self.balanceamento(node)

        #Esquerda-Esquerda
        if fator_balanceamento > 1 and regra < node.filho_esquerdo.regra:
            return self.rotacionar_direita(node)

        #Direita-Direita
        if fator_balanceamento < -1 and regra > node.filho_direito.regra:
            return self.rotacionar_esquerda(node)

        #Esquerda-Direita
        if fator_balanceamento > 1 and regra > node.filho_esquerdo.regra:
            node.filho_esquerdo = self.rotacionar_esquerda(node.filho_esquerdo)
            return self.rotacionar_direita(node)

        #Direita-Esquerda
        if fator_balanceamento < -1 and regra < node.filho_direito.regra:
            node.filho_direito = self.rotacionar_direita(node.filho_direito)
            return self.rotacionar_esquerda(node)

        return node

    def menor_regra(self, node):
        node_atual = node

        while node_atual.filho_esquerdo is not None:
            node_atual = node_atual.filho_esquerdo
        return node_atual

    def remover(self, raiz, regra):
        if not raiz:
            return raiz
        elif regra < raiz.regra:
            raiz.filho_esquerdo = self.remover(raiz.filho_esquerdo, regra)
        elif regra > raiz.regra:
            raiz.filho_direito = self.remover(raiz.filho_direito, regra)
        else:
            if raiz.filho_esquerdo is None:
                temp = raiz.filho_direito
                raiz = None
                return temp
            elif raiz.filho_direito is None:
                temp = raiz.filho_esquerdo
                raiz = None
                return temp

            temp = self.menor_regra(raiz.filho_direito)
            raiz.regra = temp.regra
            raiz.filho_direito = self.remover(raiz.filho_direito, temp.regra)

        if raiz is None:
            return raiz

        self.recalcular_altura(raiz)
        fator_balanceamento = self.balanceamento(raiz)

        #Esquerda-Esquerda
        if fator_balanceamento > 1 and raiz.filho_esquerdo is not None and self.balanceamento(raiz.filho_esquerdo) >= 0:
            return self.rotacionar_direita(raiz)

        #Direita-Direita
        if fator_balanceamento < -1 and raiz.filho_esquerdo is not None and self.balanceamento(raiz.filho_direito) <= 0:
            return self.rotacionar_esquerda(raiz)

        #Esquerda-Direita
        if fator_balanceamento > 1 and raiz.filho_esquerdo is not None and self.balanceamento(raiz.filho_esquerdo) < 0:
            raiz.filho_esquerdo = self.rotacionar_esquerda(raiz.filho_esquerdo)
            return self.rotacionar_direita(raiz)

        #Direita-Esquerda
        if fator_balanceamento < -1 and raiz.filho_esquerdo is not None and self.balanceamento(raiz.filho_direito) > 0:
            raiz.filho_direito = self.rotacionar_direita(raiz.filho_direito)
            return self.rotacionar_esquerda(raiz)

        return raiz

    def buscar_por_prioridade(self, node, prioridade):
        while node and node is not None:
            if prioridade == node.regra.prioridade:
                return node
            elif prioridade < node.regra.prioridade:
                node = node.filho_esquerdo
            else:
                node = node.filho_direito
        return None


class RedBlack_Router_Tree:
    def __init__(self):
        self.NIL = Node(None)
        self.NIL.cor = "PRETO"
        self.NIL.filho_esquerdo = self.NIL
        self.NIL.filho_direito = self.NIL
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

    def inserir(self, regra):
        novo_node = Node(regra)
        novo_node.filho_esquerdo = self.NIL
        novo_node.filho_direito = self.NIL
        pai = None
        atual = self.raiz

        while atual != self.NIL:
            pai = atual
            if novo_node.regra < atual.regra:
                atual = atual.filho_esquerdo
            else:
                atual = atual.filho_direito

        novo_node.pai = pai

        if pai is None:
            self.raiz = novo_node
        elif novo_node.regra < pai.regra:
            pai.filho_esquerdo = novo_node
        else:
            pai.filho_direito = novo_node

        if novo_node.pai is None:
            novo_node.cor = "PRETO"
            return

        if novo_node.pai.pai is None:
            return

        self.corrigir_inserir(novo_node)

    def transplantar(self, u:Node, v:Node):
        if u.pai is None:
            self.raiz = v
        elif u == u.pai.filho_esquerdo:
            u.pai.filho_esquerdo = v
        else:
            u.pai.filho_direito = v
        v.pai = u.pai

    def menor_regra(self, node):
        while node.filho_esquerdo != self.NIL:
            node = node.filho_esquerdo
        return node

    def buscar(self, node, regra):
        if node == self.NIL or regra == node.regra:
            return node

        if regra < node.regra:
            return self.buscar(node.filho_esquerdo, regra)

        return self.buscar(node.filho_direito, regra)

    def corrigir_remover(self, x:Node):
        while x != self.raiz and x.cor == "PRETO":
            if x == x.pai.filho_esquerdo:
                w = x.pai.filho_direito

                if w.cor == "VERMELHO":
                    w.cor = "PRETO"
                    x.pai.cor = "VERMELHO"
                    self.rotacionar_esquerda(x.pai)
                    w = x.pai.filho_direito

                if w.filho_esquerdo.cor == "PRETO" and w.filho_direito.cor == "PRETO":
                    w.cor = "VERMELHO"
                    x = x.pai

                else:
                    if w.filho_direito.cor == "PRETO":
                        w.filho_esquerdo.cor = "PRETO"
                        w.cor = "VERMELHO"
                        self.rotacionar_direita(w)
                        w = x.pai.filho_direito

                    w.cor = x.pai.cor
                    x.pai.cor = "PRETO"
                    w.filho_direito.cor = "PRETO"
                    self.rotacionar_esquerda(x.pai)
                    x = self.raiz

            else:
                w = x.pai.filho_esquerdo
                if w.cor == "VERMELHO":
                    w.cor = "PRETO"
                    x.pai.cor = "VERMELHO"
                    self.rotacionar_direita(x.pai)
                    w = x.pai.filho_esquerdo

                if w.filho_direito.cor == "PRETO" and w.filho_esquerdo.cor == "PRETO":
                    w.cor = "VERMELHO"
                    x = x.pai

                else:
                    if w.filho_esquerdo.cor == "PRETO":
                        w.filho_direito.cor = "PRETO"
                        w.cor = "VERMELHO"
                        self.rotacionar_esquerda(w)
                        w = x.pai.filho_esquerdo

                    w.cor = x.pai.cor
                    x.pai.cor = "PRETO"
                    w.filho_esquerdo.cor = "PRETO"
                    self.rotacionar_direita(x.pai)
                    x = self.raiz

        x.cor = "PRETO"

    def remover(self, regra):
        node_z = self.buscar(self.raiz, regra)

        if node_z == self.NIL:
            return

        node_y = node_z
        node_y_cor_original = node_y.cor

        if node_z.filho_esquerdo == self.NIL:
            node_x = node_z.filho_direito
            self.transplantar(node_z, node_z.filho_direito)

        elif node_z.filho_direito == self.NIL:
            node_x = node_z.filho_esquerdo
            self.transplantar(node_z, node_z.filho_esquerdo)

        else:
            node_y = self.menor_regra(node_z.filho_direito)
            node_y_cor_original = node_y.cor
            node_x = node_y.filho_direito

            if node_y.pai == node_z:
                node_x.pai = node_y
            else:
                self.transplantar(node_y, node_y.filho_direito)
                node_y.filho_direito = node_z.filho_direito
                node_y.filho_direito.pai = node_y

            self.transplantar(node_z, node_y)

            node_y.filho_esquerdo = node_z.filho_esquerdo
            node_y.filho_esquerdo.pai = node_y
            node_y.cor = node_z.cor

        if node_y_cor_original == "PRETO":
            self.corrigir_remover(node_x)

    def buscar_por_prioridade(self, node, prioridade):
        while node and node != self.NIL:
            if prioridade == node.regra.prioridade:
                return node
            elif prioridade < node.regra.prioridade:
                node = node.filho_esquerdo
            else:
                node = node.filho_direito
        return None