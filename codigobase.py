import networkx as nx
import matplotlib.pyplot as plt
import os

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


def adicionar_vertice(G, v):
    """Adiciona um vértice ao grafo, se não existir."""
    if v not in G:
        G.add_node(v)
        print(f"Vértice '{v}' adicionado.")
    else:
        print(f"Vértice '{v}' já existe.")


def adicionar_aresta(G, u, v, w=1, ponderado=False):
    """Adiciona uma aresta ao grafo."""
    if ponderado:
        G.add_edge(u, v, weight=float(w))
        print(f"Aresta '{u} - {v}' com peso {w} adicionada.")
    else:
        G.add_edge(u, v)
        print(f"Aresta '{u} - {v}' adicionada.")


def visualizar_grafo(G, ponderado=False):
    """Desenha o grafo (ou dígrafo) com ou sem pesos."""
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='black', node_size=1000, font_size=12,
            arrows=isinstance(G, nx.DiGraph), arrowsize=20)

    # Se for ponderado, mostrar pesos
    if ponderado:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Visualização do Grafo")
    plt.show()

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
        

# -------------------------------
# Exemplo de uso do programa
# -------------------------------
if __name__ == "__main__":
    # Ler grafo a partir de arquivo
    system_dir = "C:\\Users\\Sorar Santos\\Documents\\programação (VSCode)\\TeoriaDosGrafos"
    nome_arquivo = "grafo02.txt"  # Arquivo de entrada
    file = os.path.join(system_dir, nome_arquivo)
    G, ponderado = ler_grafo_arquivo(file)


    print("Matriz de Adjacência:")
    for linha in gerar_matriz_adjacencia(G):
        print(linha)

    print("\nMatriz de Incidência:")
    for linha in gerar_matriz_incidencia(G):
        print(linha)

    print("\nLista de Adjacência:")
    lista_adj = gerar_lista_adjacencia(G)
    for vertice, vizinhos in lista_adj.items():
        print(f"{vertice}: {vizinhos}")


    if(ponderado == False):
        k = 2
        start = 'A'
        end = 'C'

        print(f"\nCaminhos de '{start}' para '{end}' com no máximo {k} arestas:")
        num_caminhos = gerar_dfs_modificada(G, start, end, k)
        print(f"\nNúmero total de caminhos encontrados: {num_caminhos}")

        S = ['A', 'B', 'C', 'D', 'A']  # Exemplo de sequência de vértices
        verificar_sequencia(G, S)

    # Visualizar grafo
    visualizar_grafo(G, ponderado)
