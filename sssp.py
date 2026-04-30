import networkx as nx

#------------------------------------
# SSSP - Single Source Shortest Path 
#------------------------------------

#-------------------------------------------------------
# Algoritmo de dijkstra para encontrar caminhos mínimos
#-------------------------------------------------------

def dijkstra(G, inicio, end):

    visitados = set()
    pai = {v: None for v in G.nodes()}; # Cria um dicionario com os vertices como chave e none como valor - {A: None}
    dist = {v: float('inf') for v in G.nodes()}; # Cria um dicionario com os vertices como chave e infinito como valor - {A: inf}
    
    dist[inicio] = 0

    while len(visitados) < len(G.nodes()):
        # Ordena pelo valor e não pela key
        dist_ordenado = dict(sorted(dist.items(), key=lambda x: x[1])) 

        vertice_atual = [v[0] for v in dist_ordenado.items() if v[0] not in visitados][0]
        print(f"Vertice atual - {vertice_atual}")
        
        if vertice_atual == end:
            return dist, pai

        visitados.add(vertice_atual)

        for vizinho in G.neighbors(vertice_atual):
            peso = G[vertice_atual][vizinho].get('weight', 1)
            if vizinho not in visitados and dist[vizinho] > dist[vertice_atual] + peso:
                dist[vizinho] = dist[vertice_atual] + peso
                pai[vizinho] = vertice_atual
    
    return dist, pai

#----------------------------------------------------------
# Algoritmo de Bellman-Ford para encontrar caminhos mínimos
#-----------------------------------------------------------

def bellman_ford(G, inicio):
    pai = {v: None for v in G.nodes()}
    dist = {v: float('inf') for v in G.nodes()}
    
    dist[inicio] = 0
    
    for i in range (len(G.nodes)-1):
        for u, v in G.edges():
            peso = G[u][v].get('weight',1)
            if dist[v] > dist[u] + peso:
                dist[v] = dist[u] + peso
                pai[v] = u
    
    for i in range (len(G.nodes)-1):
        for u, v in G.edges():
            peso = G[u][v].get('weight',1)
            if dist[v] > dist[u] + peso:
                print("Existe caminho negativo")
                return None ,None
    
    return dist, pai


#----------------------------------------------------------
# Print de melhor caminho e distancias dos algoritmos SSSP
#-----------------------------------------------------------         

def print_sssp_caminho(pai, destino):
    caminho = []

    if pai[destino] is None:
        print(f"Não há caminho para '{destino}'.")
        return caminho
    
    while destino is not None:
        caminho.insert(0, destino)
        destino = pai[destino]
    
    print(" -> ".join(caminho))


def print_sssp_distancias(dist):
    print(f"\nDistâncias a partir do vértice {list(dist.keys())[0]}:")
    for vertice, distancia in dist.items():
        print(f"Distância até '{vertice}': {distancia}")   