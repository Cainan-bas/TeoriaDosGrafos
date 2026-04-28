import networkx as nx

#------------------------------------
# SSSP - Single Source Shortest Path 
#------------------------------------

#-------------------------------------------------------
# Algoritmo de dijkstra para encontrar caminhos mínimos
#-------------------------------------------------------

def dijkstra(G, inicio):

    visitados = set()
    pai = {v: None for v in G.nodes()}; # Cria um dicionario com os vertices como chave e none como valor - {A: None}
    dist = {v: float('inf') for v in G.nodes()}; # Cria um dicionario com os vertices como chave e infinito como valor - {A: inf}
    
    dist[inicio] = 0

    while len(visitados) < len(G.nodes()):

        vertice_atual = [v[0] for v in dist.items() if v[0] not in visitados and v[1] != float('inf')][0]

        visitados.add(vertice_atual)

        for vizinho in G.neighbors(vertice_atual):
            peso = G[vertice_atual][vizinho].get('weight', 1)
            if vizinho not in visitados and dist[vizinho] > dist[vertice_atual] + peso:
                dist[vizinho] = dist[vertice_atual] + peso
                pai[vizinho] = vertice_atual
    
    return dist, pai

def print_dijkstra_caminho(pai, destino):
    caminho = []

    if pai[destino] is None:
        print(f"Não há caminho para '{destino}'.")
        return caminho
    
    while destino is not None:
        caminho.insert(0, destino)
        destino = pai[destino]
    
    print(" -> ".join(caminho))


def print_dijkstra_distancias(dist):
    print(f"\nDistâncias a partir do vértice {list(dist.keys())[0]}:")
    for vertice, distancia in dist.items():
        print(f"Distância até '{vertice}': {distancia}")

#----------------------------------------------------------
# Algoritmo de Bellman-Ford para encontrar caminhos mínimos
#-----------------------------------------------------------