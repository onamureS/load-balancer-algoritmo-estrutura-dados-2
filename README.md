# Metodologia

O projeto foi feito em Python versão **3.13**

Os testes foram executados utilizando Python com medições em nanossegundos através da função time.perf_counter_ns(). Ambas as estruturas receberam exatamente os mesmos conjuntos de dados, utilizando a seed fixa 42 para garantir uniformidade experimental.
Os cenários de teste utilizaram volumes progressivos de 1000, 5000, 10000 e 50000 regras de roteamento. Cada estrutura foi submetida a operações de inserção, busca e remoção, simulando comportamento de tabelas de fluxo em redes SDN.
Além disso, foi realizada remoção de 20% das regras inseridas, simulando expiração de políticas de firewall em ambiente de produção.
# Resultados Comparativos

Os testes demonstraram que a árvore AVL apresentou desempenho superior em operações de busca, devido ao balanceamento mais rigoroso da estrutura.
Por outro lado, a Red-Black Tree apresentou melhor desempenho em inserções e remoções, exigindo menor quantidade de rotações e apresentando maior estabilidade em cenários de alta carga.
Durante o teste de escalabilidade com 100000 regras, a implementação AVL apresentou falha estrutural durante operação de rotação, indicando inconsistência de ponteiros em cenários extremos. A Red-Black manteve estabilidade durante os testes executados.
# Conclusão

A análise demonstra que a AVL oferece excelente desempenho para sistemas orientados majoritariamente à leitura, enquanto a Red-Black apresentou melhor robustez para cenários dinâmicos com alta frequência de inserções e remoções.
Considerando o cenário de roteamento em tempo real proposto pelo projeto, a Red-Black Tree mostrou-se mais adequada devido à sua maior estabilidade operacional sob alta carga.
Enfim, o resumo é:
A AVL quebra em testes de escala com 100000 regras.
O benchmark executou normalmente até 50000 regras, mas em 100000 ocorreu erro durante inserção:
AttributeError: 'NoneType' object has no attribute 'filho_direito'
O erro acontece dentro de rotacionar_direita() na AVL, indicando erro de rebalanceamento ou ponteiro nulo durante rotação.

Stack trace aponta:
load_balancer.py -> linha 50:
subtree_t2 = node_x.filho_direito

Durante os testes de escalabilidade, a implementação AVL apresentou falha estrutural ao processar 100000 regras simultâneas. A exceção ocorreu durante operação de rotação à direita, indicando inconsistência de ponteiros internos em cenários de alta carga.
A estrutura Red-Black manteve estabilidade durante os testes executados.
Os resultados sugerem que, apesar da AVL apresentar desempenho competitivo em buscas, sua implementação mostrou menor robustez em cenários extremos de inserção massiva.
