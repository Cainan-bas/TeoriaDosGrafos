from platform import node

import networkx as nx
import matplotlib.pyplot as plt
import os

from numpy import indices

import matrizes as matriz
import dfs as dfs
import sssp as sssp

def ler_grafo_arquivo(nome_arquivo):
    """
    Lê um arquivo de texto e cria um grafo/dígrafo (ponderado ou não).
    
    Formato esperado:
    1ª linha: [G|D] [N|W]
        G = Grafo não direcionado
        D = Dígrafo
        N = Não ponderado
        W = Ponderado
    Demais linhas:
        Se não ponderado: u v
        Se ponderado:     u v w
    """
    try:
        with open(nome_arquivo, "r") as f:
            linhas = [linha.strip() for linha in f if linha.strip()]

        if not linhas:
            print("Arquivo vazio!")
            return None, False

        # Definição do tipo de grafo
        tipo, peso = linhas[0].split()
        if tipo == "G":
            G = nx.Graph()
        elif tipo == "D":
            G = nx.DiGraph()
        else:
            raise ValueError("Primeiro caractere deve ser 'G' ou 'D'.")

        ponderado = (peso == "W")

        # Leitura das arestas
        for linha in linhas[1:]:
            partes = linha.split()
            if ponderado:
                if len(partes) != 3:
                    raise ValueError("Esperado formato 'u v w' para grafos ponderados.")
                u, v, w = partes
                adicionar_aresta(G, u, v, w, ponderado)
            else:
                if len(partes) != 2:
                    raise ValueError("Esperado formato 'u v' para grafos não ponderados.")
                u, v = partes
                adicionar_aresta(G, u, v, ponderado)  # peso padrão 1

        print(f"Grafo criado ({'dígrafo' if tipo=='D' else 'grafo'}, "
              f"{'ponderado' if ponderado else 'não ponderado'}) com "
              f"{G.number_of_nodes()} vértices e {G.number_of_edges()} arestas.")
        return G, ponderado

    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None, False


def adicionar_vertice(G, v): # NOSONAR
    """Adiciona um vértice ao grafo, se não existir."""
    if v not in G:
        G.add_node(v)
        print(f"Vértice '{v}' adicionado.")
    else:
        print(f"Vértice '{v}' já existe.")


def adicionar_aresta(G, u, v, w=1, ponderado=False): # NOSONAR
    """Adiciona uma aresta ao grafo."""
    if ponderado:
        G.add_edge(u, v, weight=float(w))
        print(f"Aresta '{u} - {v}' com peso {w} adicionada.")
    else:
        G.add_edge(u, v)
        print(f"Aresta '{u} - {v}' adicionada.")

  
def visualizar_grafo(G, ponderado=False): # NOSONAR
    """Desenha o grafo (ou dígrafo) com ou sem pesos."""
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='black', node_size=1000, font_size=12,
            arrows=isinstance(G, nx.DiGraph), arrowsize=20)

    # Se for ponderado, mostrar pesos
    if ponderado:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)



# -------------------------------
# Exemplo de uso do programa
# -------------------------------
if __name__ == "__main__":
    # Ler grafo a partir de arquivo
    system_dir = os.path.dirname(__file__)
    
    nome_arquivo = "arquivos/grafo05.txt"  # Arquivo de entrada
    file = os.path.join(system_dir, nome_arquivo)
    G, ponderado = ler_grafo_arquivo(file)
        
    
    #Print do resultado do Dijkstra e bellman ford
    #txt de dijkstra grafo05
    if ponderado:
        saida = 'A'
        destino = 'C'
        print(f"\nDistâncias a partir do vértice {saida} usando Dijkstra:")
        distancias, pais = sssp.dijkstra(G, saida, destino)
        sssp.print_sssp_distancias(distancias)
        print(f"\nCaminho mais curto de {saida} para {destino}:")
        sssp.print_sssp_caminho(pais, destino)
        
        
        print(f"\nDistancias a partir do vertice {saida} usando bellman ford:")
        dist, dad = sssp.bellman_ford(G, saida)
        if dad is not None:
            sssp.print_sssp_distancias(dist)
            print(f"\nCaminho mais curto de {saida} para {destino}:")
            sssp.print_sssp_caminho(dad, destino)
        


    # Visualizar o grafo
    visualizar_grafo(G, ponderado)
    plt.show()
    
    


