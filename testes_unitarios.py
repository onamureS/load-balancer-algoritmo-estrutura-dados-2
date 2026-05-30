import unittest
import random
import sys

from main import (
    Packet_Rule,
    AVL_Router_Tree,
    RedBlack_Router_Tree
)

sys.setrecursionlimit(1_000_000)

def criar_regra(i, prioridade):
    return Packet_Rule(
        id=i,
        ip_origem=f"192.168.1.{i % 255}",
        ip_destino=f"10.0.0.{i % 255}",
        prioridade=prioridade
    )


def validar_avl(node, tree):

    if node is None:
        return True, 0

    esquerda_ok, altura_esquerda = validar_avl(
        node.filho_esquerdo,
        tree
    )

    direita_ok, altura_direita = validar_avl(
        node.filho_direito,
        tree
    )

    if not esquerda_ok or not direita_ok:
        return False, 0

    fator = altura_esquerda - altura_direita

    if abs(fator) > 1:
        return False, 0

    altura_correta = 1 + max(
        altura_esquerda,
        altura_direita
    )


    if node.altura != altura_correta:
        return False, 0

    return True, altura_correta

def validar_red_black(tree):

    # Propriedade 2:
    # raiz deve ser preta
    if tree.raiz.cor != "PRETO":
        return False

    def dfs(node):

        if node == tree.NIL:
            return 1

        # Propriedade 4:
        # nó vermelho não pode ter filho vermelho
        if node.cor == "VERMELHO":
            if (
                node.filho_esquerdo.cor == "VERMELHO"
                or
                node.filho_direito.cor == "VERMELHO"
            ):
                raise Exception("Violação Red-Red")

        esquerda = dfs(node.filho_esquerdo)
        direita = dfs(node.filho_direito)

        # Propriedade 5:
        # mesma black-height
        if esquerda != direita:
            raise Exception("Black-height inconsistente")

        return esquerda + (1 if node.cor == "PRETO" else 0)

    try:
        dfs(tree.raiz)
        return True

    except Exception:
        return False

class TestAVL(unittest.TestCase):

    def setUp(self):
        self.avl = AVL_Router_Tree()

    def test_insercao_simples(self):

        regras = [
            criar_regra(1, 30),
            criar_regra(2, 20),
            criar_regra(3, 10)
        ]

        for r in regras:
            self.avl.raiz = self.avl.inserir(self.avl.raiz, r)

        valido, _ = validar_avl(self.avl.raiz, self.avl)

        self.assertTrue(valido)

    def test_busca(self):

        regra = criar_regra(1, 50)

        self.avl.raiz = self.avl.inserir(
            self.avl.raiz,
            regra
        )

        resultado = self.avl.buscar_por_prioridade(
            self.avl.raiz,
            50
        )

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.regra.prioridade, 50)

    def test_remocao(self):

        regras = [
            criar_regra(1, 10),
            criar_regra(2, 20),
            criar_regra(3, 30),
            criar_regra(4, 40)
        ]

        for r in regras:
            self.avl.raiz = self.avl.inserir(self.avl.raiz, r)

        self.avl.raiz = self.avl.remover(
            self.avl.raiz,
            regras[2]
        )

        self.assertTrue(validar_avl(self.avl.raiz, self.avl))

    def test_carga_alta_avl(self):

        random.seed(42)

        for i in range(100_000):

            regra = criar_regra(
                i,
                random.randint(1, 1_000_000)
            )

            self.avl.raiz = self.avl.inserir(
                self.avl.raiz,
                regra
            )

        self.assertTrue(validar_avl(self.avl.raiz, self.avl))

class TestRedBlack(unittest.TestCase):

    def setUp(self):
        self.rb = RedBlack_Router_Tree()

    def test_insercao_simples(self):

        regras = [
            criar_regra(1, 10),
            criar_regra(2, 20),
            criar_regra(3, 30)
        ]

        for r in regras:
            self.rb.inserir(r)

        self.assertTrue(validar_red_black(self.rb))

    def test_busca(self):

        regra = criar_regra(1, 100)

        self.rb.inserir(regra)

        resultado = self.rb.buscar_por_prioridade(
            self.rb.raiz,
            100
        )

        self.assertIsNotNone(resultado)

    def test_remocao(self):

        regras = [
            criar_regra(1, 10),
            criar_regra(2, 20),
            criar_regra(3, 30),
            criar_regra(4, 40)
        ]

        for r in regras:
            self.rb.inserir(r)

        self.rb.remover(regras[2])

        self.assertTrue(validar_red_black(self.rb))

    def test_carga_alta_red_black(self):

        random.seed(42)

        for i in range(100_000):

            regra = criar_regra(
                i,
                random.randint(1, 1_000_000)
            )

            self.rb.inserir(regra)

        self.assertTrue(validar_red_black(self.rb))

class TestComparativo(unittest.TestCase):

    def test_mesmos_resultados_busca(self):

        avl = AVL_Router_Tree()
        rb = RedBlack_Router_Tree()

        random.seed(42)

        prioridades = []

        for i in range(10_000):

            prioridade = random.randint(1, 1_000_000)

            prioridades.append(prioridade)

            regra = criar_regra(i, prioridade)

            avl.raiz = avl.inserir(avl.raiz, regra)
            rb.inserir(regra)

        for prioridade in prioridades[:1000]:

            resultado_avl = avl.buscar_por_prioridade(
                avl.raiz,
                prioridade
            )

            resultado_rb = rb.buscar_por_prioridade(
                rb.raiz,
                prioridade
            )

            self.assertIsNotNone(resultado_avl)
            self.assertIsNotNone(resultado_rb)

            self.assertEqual(
                resultado_avl.regra.prioridade,
                resultado_rb.regra.prioridade
            )

if __name__ == "__main__":
    unittest.main(verbosity=2)