import networkx as nx

#-----------------------------
# mst - Minimum Spanning Tree
#-----------------------------


def kruskal(G):
    """Implementação do algoritmo de Kruskal para encontrar a árvore geradora mínima."""
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

            if lista_vertices[v] == 0:
                lista_vertices[v] = lista_vertices[u]
            elif lista_vertices[u] == 0:
                lista_vertices[u] = lista_vertices[v]
            else:
                lista_vertices = normalizar_grupos(lista_vertices, lista_vertices[v], lista_vertices[u])

    return arvore_geradora_minima

def normalizar_grupos(lista_vertices, grupo1, grupo2):
    """Unifica os grupos de vértices para evitar ciclos."""
    grupo_normalizado = min(grupo1, grupo2)

    for v in lista_vertices:
        if lista_vertices[v] == grupo1 or lista_vertices[v] == grupo2:
            lista_vertices[v] = grupo_normalizado
    return lista_vertices

    # fazer funcao de plot do grafo destacando as arestas da arvore geradora minima

def visualizar_grafo_arvore(G, arvore=None, ponderado=False): # NOSONAR
    """Desenha o grafo destacando a árvore geradora mínima (se fornecida)."""
    pos = nx.spring_layout(G, seed=42) 
    
    cores_arestas = []
    espessura_arestas = []
    
    if arvore is not None:
        for u, v in G.edges():
            if arvore.has_edge(u, v):
                cores_arestas.append('blue')
                espessura_arestas.append(2.5) # Deixa a aresta da árvore mais grossa
            else:
                cores_arestas.append('lightgray')
                espessura_arestas.append(1.0) # Arestas ignoradas ficam finas e cinzas
    else:
        cores_arestas = 'black'
        espessura_arestas = 1.0

    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color=cores_arestas, width=espessura_arestas, 
            node_size=1000, font_size=12,
            arrows=isinstance(G, nx.DiGraph), arrowsize=20)

    if ponderado:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        