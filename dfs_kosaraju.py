import networkx as nx
import matrizes as matriz

def enumerar_seguencia(G, seguecia):
    """Retorna um dicionário mapeando nós para seus índices na ordem da sequência."""
    indices = {v: i for i, v in enumerate(G.nodes())}
    return {v: indices[v] for v in seguecia if v in indices}

def dfs_kosaraju_passagem(G):
    visitado = set()
    sequencia = []
    nodes = list(G.nodes())
    
    def dfs(node):
        visitado.add(node)
        for neighbor in G.neighbors(node):
            if neighbor not in visitado:
                dfs(neighbor)
        sequencia.append(node)  
    
    for node in nodes:
        if node not in visitado:
            dfs(node)
    return sequencia

def dfs_kosaraju(G):

    sequencia = dfs_kosaraju_passagem(G)

    visitado = set()
    componentes = []
    m = []
    m_inversa = []
    nodes = list(G.nodes())

    m = matriz.gerar_matriz_adjacencia(G)
    for i in range(len(m)):
        m_inversa.append([m[j][i] for j in range(len(m))])

    print("\nMatriz de inversa: ")
    for linha in m_inversa:
        print(linha)

    indices = enumerar_seguencia(G, sequencia)

    def dfs(node, componente):
        visitado.add(node)
        componente.append(node)
        i = indices[node]
        for j in range(len(m_inversa[i])):
            if m_inversa[i][j] != 0:
                neighbor = nodes[j]
                if neighbor not in visitado:
                    dfs(neighbor, componente)
    
    for node in reversed(sequencia):
        if node not in visitado:
            componente = []
            dfs(node, componente)
            componentes.append(componente)

    return componentes