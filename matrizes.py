import networkx as nx

def gerar_matriz_adjacencia(G):
    matriz = []
    for u in G.nodes():
        row = []
        for v in G.nodes():
            if G.has_edge(u, v):
                row.append(G[u][v]['weight'] if 'weight' in G[u][v] else 1)
            else:
                row.append(0)
        matriz.append(row)
    return matriz

def gerar_matriz_incidencia(G):
    matriz = []
    for u in G.nodes():
        row = []
        for v in G.edges():
            if u in v:
                row.append(G[v[0]][v[1]]['weight'] if 'weight' in G[v[0]][v[1]] else 1)
            else:
                row.append(0)
        matriz.append(row)
    return matriz

def gerar_lista_adjacencia(G):
    lista = {}
    for u in G.nodes():
        lista[u] = []
        for v in G.neighbors(u):
            peso = G[u][v]['weight'] if 'weight' in G[u][v] else 1
            lista[u].append((v, peso))
    return lista