import networkx as nx

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
