
import random
import time
import matplotlib.pyplot as plt
from load_balancer import *


# CONFIGURAÇÃO DO TESTE

VOLUMES = [1000, 5000, 10000, 50000]
SEED = 42

random.seed(SEED)

avl_insert_resultados = []
rb_insert_resultados = []

avl_search_resultados = []
rb_search_resultados = []

avl_delete_resultados = []
rb_delete_resultados = []


for TOTAL_REGRAS in VOLUMES:

    print(f"\nTESTANDO {TOTAL_REGRAS} REGRAS\n")

    # GERAÇÃO DAS REGRAS

    regras = []

    for i in range(TOTAL_REGRAS):

        prioridade = random.randint(1, 1_000_000)

        regra = Packet_Rule(
            id=i,
            ip_origem=f"192.168.0.{random.randint(1,254)}",
            ip_destino=f"10.0.0.{random.randint(1,254)}",
            prioridade=prioridade
        )

        regras.append(regra)

    # ESTRUTURAS

    avl = AVL_Router_Tree()
    rb = RedBlack_Router_Tree()

    # TESTE DE INSERÇÃO AVL

    inicio_avl_insert = time.perf_counter_ns()

    for regra in regras:
        avl.raiz = avl.inserir(avl.raiz, regra)

    fim_avl_insert = time.perf_counter_ns()

    tempo_avl_insert = fim_avl_insert - inicio_avl_insert
    avl_insert_resultados.append(tempo_avl_insert)

    # TESTE DE INSERÇÃO RED-BLACK

    inicio_rb_insert = time.perf_counter_ns()

    for regra in regras:
        rb.inserir(regra)

    fim_rb_insert = time.perf_counter_ns()

    tempo_rb_insert = fim_rb_insert - inicio_rb_insert
    rb_insert_resultados.append(tempo_rb_insert)

    # REGRAS BUSCA

    regras_busca = random.sample(regras, 1000)

    # TESTE BUSCA AVL

    inicio_avl_search = time.perf_counter_ns()

    for regra in regras_busca:
        avl.buscar_por_prioridade(
            avl.raiz,
            regra.prioridade
        )

    fim_avl_search = time.perf_counter_ns()

    tempo_avl_search = fim_avl_search - inicio_avl_search
    avl_search_resultados.append(tempo_avl_search)

    # TESTE BUSCA RED-BLACK

    inicio_rb_search = time.perf_counter_ns()

    for regra in regras_busca:
        rb.buscar_por_prioridade(
            rb.raiz,
            regra.prioridade
        )

    fim_rb_search = time.perf_counter_ns()

    tempo_rb_search = fim_rb_search - inicio_rb_search
    rb_search_resultados.append(tempo_rb_search)

    # TESTE REMOÇÃO AVL

    quantidade_remocao = int(TOTAL_REGRAS * 0.2)

    regras_remocao = random.sample(
        regras,
        quantidade_remocao
    )

    inicio_avl_delete = time.perf_counter_ns()

    for regra in regras_remocao:
        avl.raiz = avl.remover(
            avl.raiz,
            regra
        )

    fim_avl_delete = time.perf_counter_ns()

    tempo_avl_delete = fim_avl_delete - inicio_avl_delete
    avl_delete_resultados.append(tempo_avl_delete)

    # TESTE REMOÇÃO RED-BLACK

    inicio_rb_delete = time.perf_counter_ns()

    for regra in regras_remocao:
        rb.remover(regra)

    fim_rb_delete = time.perf_counter_ns()

    tempo_rb_delete = fim_rb_delete - inicio_rb_delete
    rb_delete_resultados.append(tempo_rb_delete)

    # RESULTADOS

    print("\n========== RESULTADOS ==========\n")

    print("AVL TREE")
    print(f"Inserção: {tempo_avl_insert} ns")
    print(f"Busca:    {tempo_avl_search} ns")
    print(f"Remoção:  {tempo_avl_delete} ns")

    print("\nRED-BLACK TREE")
    print(f"Inserção: {tempo_rb_insert} ns")
    print(f"Busca:    {tempo_rb_search} ns")
    print(f"Remoção:  {tempo_rb_delete} ns")

    # MÉDIAS

    print("\n========== MÉDIAS ==========\n")

    print("AVL")
    print(f"Busca média:   {tempo_avl_search / 1000:.2f} ns/op")
    print(f"Remoção média: {tempo_avl_delete / 1000:.2f} ns/op")

    print("\nRED-BLACK")
    print(f"Busca média:   {tempo_rb_search / 1000:.2f} ns/op")
    print(f"Remoção média: {tempo_rb_delete / 1000:.2f} ns/op")


# =========================
# GRÁFICO DE INSERÇÃO
# =========================

plt.figure()

plt.plot(VOLUMES, avl_insert_resultados, label="AVL")
plt.plot(VOLUMES, rb_insert_resultados, label="Red-Black")

plt.xlabel("Quantidade de Regras")
plt.ylabel("Tempo (ns)")
plt.title("Inserção AVL vs Red-Black")

plt.legend()

plt.show()


# =========================
# GRÁFICO DE BUSCA
# =========================

plt.figure()

plt.plot(VOLUMES, avl_search_resultados, label="AVL")
plt.plot(VOLUMES, rb_search_resultados, label="Red-Black")

plt.xlabel("Quantidade de Regras")
plt.ylabel("Tempo (ns)")
plt.title("Busca AVL vs Red-Black")

plt.legend()

plt.show()


# =========================
# GRÁFICO DE REMOÇÃO
# =========================

plt.figure()

plt.plot(VOLUMES, avl_delete_resultados, label="AVL")
plt.plot(VOLUMES, rb_delete_resultados, label="Red-Black")

plt.xlabel("Quantidade de Regras")
plt.ylabel("Tempo (ns)")
plt.title("Remoção AVL vs Red-Black")

plt.legend()

plt.show()

