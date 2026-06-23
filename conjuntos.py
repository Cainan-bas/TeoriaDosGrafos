import os

import matplotlib.pyplot as plt
import networkx as nx


def conjunto_estavel_guloso(G):
    """Gera um conjunto estavel maximal."""
    grafo_trabalho = G.copy()
    conjunto_estavel = []

    while len(grafo_trabalho.nodes()) > 0:
        vertice_escolhido = min(
            grafo_trabalho.nodes(),
            key=lambda vertice: grafo_trabalho.degree(vertice)
        )

        conjunto_estavel.append(vertice_escolhido)

        vertices_remover = list(grafo_trabalho.neighbors(vertice_escolhido))
        vertices_remover.append(vertice_escolhido)
        grafo_trabalho.remove_nodes_from(vertices_remover)

    return conjunto_estavel


def cobertura_vertices(G, conjunto_estavel):
    """Retorna a cobertura com a subtração dos vertices menos o conjunto estavel."""
    cobertura = []

    for vertice in G.nodes():
        if vertice not in conjunto_estavel:
            cobertura.append(vertice)

    return cobertura


def clique_maximal(G):
    """Gera o clique reutilizando a função do conjunto estavel e o grafo complementar."""
    grafo_complementar = gerar_grafo_complementar(G)
    return conjunto_estavel_guloso(grafo_complementar)


def gerar_grafo_complementar(G):
    """Cria o grafo complementar para usar no clique"""
    grafo_complementar = nx.Graph()
    vertices = list(G.nodes())

    grafo_complementar.add_nodes_from(vertices)

    for indice_u in range(len(vertices)):
        for indice_v in range(indice_u + 1, len(vertices)):
            u = vertices[indice_u]
            v = vertices[indice_v]

            if not G.has_edge(u, v):
                grafo_complementar.add_edge(u, v)

    return grafo_complementar

#---------------------------
# Funções de print colorido
#---------------------------   

def visualizar_conjunto_estavel(G, conjunto_estavel, pos):
    """Salva a imagem do conjunto estavel em verde."""
    cores_vertices = []

    for vertice in G.nodes():
        if vertice in conjunto_estavel:
            cores_vertices.append("green")
        else:
            cores_vertices.append("lightgray")

    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=cores_vertices,
        edge_color="lightgray",
        node_size=900,
        font_size=11
    )
    plt.title("Conjunto Estavel Maximal")
    os.makedirs("imagens", exist_ok=True)
    plt.savefig(os.path.join("imagens", "conjunto_estavel.png"), dpi=150)
    plt.close()


def visualizar_clique(G, clique, pos):
    """Salva a imagem da clique em vermelho, incluindo as arestas internas."""
    cores_vertices = []
    cores_arestas = []

    for vertice in G.nodes():
        if vertice in clique:
            cores_vertices.append("red")
        else:
            cores_vertices.append("lightgray")

    for u, v in G.edges():
        if u in clique and v in clique:
            cores_arestas.append("red")
        else:
            cores_arestas.append("lightgray")

    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=cores_vertices,
        edge_color=cores_arestas,
        width=2,
        node_size=900,
        font_size=11
    )
    plt.title("Clique Maximal")
    os.makedirs("imagens", exist_ok=True)
    plt.savefig(os.path.join("imagens", "clique.png"), dpi=150)
    plt.close()


def visualizar_cobertura(G, cobertura, pos):
    """Salva a imagem da cobertura de vertices em azul."""
    cores_vertices = []

    for vertice in G.nodes():
        if vertice in cobertura:
            cores_vertices.append("lightblue")
        else:
            cores_vertices.append("lightgray")

    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=cores_vertices,
        edge_color="lightgray",
        node_size=900,
        font_size=11
    )
    plt.title("Cobertura de Vertices")
    os.makedirs("imagens", exist_ok=True)
    plt.savefig(os.path.join("imagens", "cobertura.png"), dpi=150)
    plt.close()
