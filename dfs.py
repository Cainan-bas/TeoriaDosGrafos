import networkx as nx
import matrizes as matriz

#------------------------------------------------------------------
# Algoritmo de DFS modificado para caminhos de no maximo k arestas
#------------------------------------------------------------------

def gerar_dfs_modificada(G, start, end, k):
    path = [] 
    def dfs(atual, destino, visitado, caminho):
        if len(caminho) - 1 > k:
            return
        if atual == destino:
            path.append(caminho.copy())
            print(caminho)
            return
        for vizinho in G.neighbors(atual):
            if vizinho not in visitado:
                visitado.add(vizinho)
                caminho.append(vizinho)
                dfs(vizinho, destino, visitado, caminho)
                caminho.pop()
                visitado.remove(vizinho)
    visitado = set([start])
    dfs(start, end, visitado, [start])
    return len(path)

def verificar_sequencia(G, S):
    passeio_valido = True
    arestas = []
    for i in range(len(S) - 1):
        u, v = S[i], S[i + 1]
        if G.has_edge(u, v):
            arestas.append((u, v))
        else:
            passeio_valido = False
            break
    print("Passeio válido:", passeio_valido)
    if not passeio_valido:
        print("A sequência não é válida no grafo.")
        return
    # -----------------------------
    caminho = len(set(S)) == len(S)
    print("É caminho:", caminho)
    # -----------------------------
    arestas_normalizadas = [
        tuple(sorted((u, v))) for (u, v) in arestas
    ]
    trilha = len(set(arestas_normalizadas)) == len(arestas_normalizadas)
    print("É trilha:", trilha)
    # -----------------------------
    circuito = trilha and (S[0] == S[-1])
    print("É circuito:", circuito)
    
def print_verificar_sequencia(G):
    k = 2
    start = 'A'
    end = 'C'

    print(f"\nCaminhos de '{start}' para '{end}' com no máximo {k} arestas:")
    num_caminhos = gerar_dfs_modificada(G, start, end, k)
    print(f"\nNúmero total de caminhos encontrados: {num_caminhos}")

    S = ['A', 'B', 'C', 'D', 'A']  # Exemplo de sequência de vértices
    verificar_sequencia(G, S)

#---------------------------------------------------------------------
# Algoritmo de kosaraju para encontrar componentes fortemente conexas
#---------------------------------------------------------------------

def enumerar_seguencia(G, seguecia):
    """Pega a seguencia gerada pela primeira passagem e retorna um dicionário mapeando nós para seus índices na ordem da sequência."""
    indices = {v: i for i, v in enumerate(G.nodes())}
    return {v: indices[v] for v in seguecia if v in indices}


def kosaraju_primeira_passagem(G):
    """Realiza a primeira passagem do algoritmo de Kosaraju, retornando a sequência de nós na ordem de término."""
    visitado = set()
    sequencia = []
    nodes = list(G.nodes())
    
    """DFS para procurar os vertices de termino"""
    def dfs(node):
        visitado.add(node)
        for neighbor in G.neighbors(node):
            if neighbor not in visitado:
                dfs(neighbor)
        sequencia.append(node)  
    
    for node in nodes:
        if node not in visitado:
            dfs(node)

    """Retorna a sequência de nós na ordem de término (do último para o primeiro)."""
    return sequencia


def kosaraju(G):
    """Realiza o algoritmo de Kosaraju para encontrar as componentes fortemente conexas do grafo."""
    sequencia = kosaraju_primeira_passagem(G)

    visitado = set()
    componentes = []
    m = []
    m_inversa = []
    nodes = list(G.nodes())

    """Gerar a matriz de adjacência e sua inversa para o grafo."""
    m = matriz.gerar_matriz_adjacencia(G)
    for i in range(len(m)):
        m_inversa.append([m[j][i] for j in range(len(m))])

    print("\nMatriz de inversa: ")
    for linha in m_inversa:
        print(linha)

    """Gerar um dicionário mapeando nós para seus índices na ordem da sequência."""
    indices = enumerar_seguencia(G, sequencia)

    """DFS para encontrar as componentes fortemente conexas usando a matriz inversa."""
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

    """Retorna a lista de componentes fortemente conexas."""
    return componentes


#----------------------------------------------------------------------------------
# Algoritmo de Tarjan como outro metodo de encontrar componentes fortemente conexas
#----------------------------------------------------------------------------------