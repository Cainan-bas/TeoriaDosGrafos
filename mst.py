import networkx as nx

#-----------------------------
# mst - Minimum Spanning Tree
#-----------------------------


def kruskal(G):
    lista_arestas = {v: G[v[0]][v[1]].get('weight', 1) for v in G.edges()}
    lista_vertices = {v: 0 for v in G.nodes()}
    lista_ordenada = dict(sorted(lista_arestas.items(), key=lambda x: x[1]))
    
    arvore_geradora_minima = nx.Graph()
    
    cont = 1
    for v, u in lista_ordenada.keys():
        if len(arvore_geradora_minima.edges()) == len(G.nodes()) - 1:
            break
        elif  lista_vertices[v] == 0 and lista_vertices[u] == 0:
            arvore_geradora_minima.add_edge(v, u, weight=G[v][u].get('weight', 1))
            lista_vertices[u] = cont
            lista_vertices[v] = cont
            cont += 1
        elif lista_vertices[v] != lista_vertices[u]:
            arvore_geradora_minima.add_edge(v, u, weight=G[v][u].get('weight', 1))
            lista_vertices[v] = min(lista_vertices[v], lista_vertices[u])
            lista_vertices[u] = min(lista_vertices[v], lista_vertices[u])

    return arvore_geradora_minima

    