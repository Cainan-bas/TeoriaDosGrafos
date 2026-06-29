import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.optimize import linear_sum_assignment


def obter_biparticao(G):
    """Retorna os dois conjuntos da biparticao, ordenados para saida estavel."""
    if not nx.is_bipartite(G):
        raise ValueError("O grafo informado nao e bipartido.")

    
    if "lado_esquerdo" in G.graph and "lado_direito" in G.graph:
        return G.graph["lado_esquerdo"], G.graph["lado_direito"]
    
    cores = nx.bipartite.color(G)
    lado_0 = sorted([vertice for vertice, cor in cores.items() if cor == 0])
    lado_1 = sorted([vertice for vertice, cor in cores.items() if cor == 1])

    if len(lado_0) <= len(lado_1):
        return lado_0, lado_1

    return lado_1, lado_0


def gerar_matriz_custo(G, lado_esquerdo=None, lado_direito=None):
    """Constroi a matriz de custos usada pelo Algoritmo Hungaro."""
    if lado_esquerdo is None or lado_direito is None:
        lado_esquerdo, lado_direito = obter_biparticao(G)

    pesos = [
        dados.get("weight", 1)
        for _, _, dados in G.edges(data=True)
    ]
    maior_peso_abs = max(abs(peso) for peso in pesos)
    penalidade = (sum(abs(peso) for peso in pesos) + maior_peso_abs + 1)

    matriz = np.full((len(lado_esquerdo), len(lado_direito)), penalidade)

    for indice_u, u in enumerate(lado_esquerdo):
        for indice_v, v in enumerate(lado_direito):
            if G.has_edge(u, v):
                matriz[indice_u][indice_v] = G[u][v]["weight"]

    return matriz, lado_esquerdo, lado_direito, penalidade


def algoritmo_hungaro(G):
    """Encontra o emparelhamento bipartido de menor custo total."""
    matriz, lado_esquerdo, lado_direito, penalidade = gerar_matriz_custo(G)
    linhas, colunas = linear_sum_assignment(matriz)

    emparelhamento = []
    custo_total = 0

    for linha, coluna in zip(linhas, colunas):
        custo = matriz[linha][coluna]

        if custo >= penalidade:
            raise ValueError(
                "Nao existe emparelhamento que cubra todo o menor lado da biparticao."
            )

        u = lado_esquerdo[linha]
        v = lado_direito[coluna]
        emparelhamento.append((u, v, custo))
        custo_total += custo

    return emparelhamento, custo_total, matriz, lado_esquerdo, lado_direito

#---------------------------
# Funções de print colorido
#---------------------------  

def formatar_peso(peso):
    """Evita imprimir casas decimais desnecessarias."""
    if float(peso).is_integer():
        return str(int(peso))

    return str(peso)


def visualizar_emparelhamento(
    G,
    emparelhamento,
    caminho_saida=os.path.join("imagens", "emparelhamento_otimo.png"),
    exibir=True
):
    """Desenha o grafo destacando o emparelhamento em azul e salva a figura."""
    os.makedirs(os.path.dirname(caminho_saida) or ".", exist_ok=True)

    arestas_emparelhamento = {
        frozenset((u, v))
        for u, v, _ in emparelhamento
    }
    cores_arestas = []
    espessuras = []

    for u, v in G.edges():
        if frozenset((u, v)) in arestas_emparelhamento:
            cores_arestas.append("blue")
            espessuras.append(3)
        else:
            cores_arestas.append("lightgray")
            espessuras.append(1.5)

    lado_esquerdo, lado_direito = obter_biparticao(G)
    pos = nx.bipartite_layout(G, lado_esquerdo)

    plt.figure(figsize=(9, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color=cores_arestas,
        width=espessuras,
        node_size=1000,
        font_size=11
    )

    labels = {
        (u, v): formatar_peso(dados.get("weight", 1))
        for u, v, dados in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

    plt.title("Emparelhamento Otimo de Custo Minimo")
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    plt.savefig(caminho_saida, dpi=150)

    if exibir:
        plt.show()

    plt.close()
    return caminho_saida


def imprimir_resultado(emparelhamento, custo_total, matriz, lado_esquerdo, lado_direito):
    """Exibe a matriz de custos, o emparelhamento e seu custo total."""
    print("Vertices do lado esquerdo:", lado_esquerdo)
    print("Vertices do lado direito:", lado_direito)
    print("\nMatriz de custos:")
    print(matriz)

    print("\nEmparelhamento otimo:")
    for u, v, custo in emparelhamento:
        print(f"{u} - {v} | custo = {formatar_peso(custo)}")

    print(f"\nCusto total: {formatar_peso(custo_total)}")
