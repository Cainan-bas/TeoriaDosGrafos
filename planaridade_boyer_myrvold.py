import matplotlib.pyplot as plt
import networkx as nx


def planaridade_boyer_myrvold(G):
    """
    Aplica o teste de planaridade de Boyer-Myrvold em um grafo simples.
    Usa nx.check_planarity(G, True), e verifica se o certificado retornado é um embedding planar ou um subgrafo de Kuratowski.
    """
    eh_planar, certificado = nx.check_planarity(G, True)

    if eh_planar:
        print("O grafo e planar.")
        imprimir_embedding(certificado)
        desenhar_embedding_planar(G, certificado)
        return True

    print("O grafo NAO e planar.")
    imprimir_kuratowski(certificado)
    return False


def imprimir_embedding(embedding):
    """Imprime os vizinhos em cada vertice do embedding."""
    print("Embedding planar retornado:")
    for vertice in embedding:
        vizinhos = list(embedding.neighbors_cw_order(vertice))
        print(f"  {vertice}: {vizinhos}")


def desenhar_embedding_planar(G, embedding):
    """
    Desenha o grafo usando apenas posicoes obtidas do PlanarEmbedding.
    """
    pos = nx.combinatorial_embedding_to_pos(embedding)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="black",
        node_size=900,
        font_size=11,
        width=1.5,
    )
    plt.title("Embedding planar - Boyer-Myrvold")
    plt.axis("equal")
    plt.show()


def imprimir_kuratowski(certificado):
    """
    Identifica K5 ou K3,3 a partir do certificado retornado pelo teste.
    """
    kuratowski = nx.Graph(certificado)
    nucleo = contrair_vertices_grau_dois(kuratowski)
    graus = sorted(dict(nucleo.degree()).values())

    if nucleo.number_of_nodes() == 5 and nucleo.number_of_edges() == 10 and graus == [4] * 5:
        print("Subgrafo de Kuratowski identificado: K5")
        print(f"Vertices envolvidos: {sorted(kuratowski.nodes())}")
        print(f"Vertices do K5: {sorted(nucleo.nodes())}")
    elif eh_k33(nucleo, graus):
        parte_a, parte_b = obter_biparticao(nucleo)
        print("Subgrafo de Kuratowski identificado: K3,3")
        print(f"Vertices envolvidos: {sorted(kuratowski.nodes())}")
        print(f"Particao A: {parte_a}")
        print(f"Particao B: {parte_b}")
    else:
        print("Subgrafo de Kuratowski identificado: certificado nao planar")
        print(f"Vertices envolvidos: {sorted(kuratowski.nodes())}")
        print(f"Vertices apos contrair subdivisoes: {sorted(nucleo.nodes())}")

    print(f"Arestas do certificado: {sorted(kuratowski.edges())}")


def contrair_vertices_grau_dois(H):
    """Contrai vertices de grau 2 para remover subdivisoes de arestas."""
    nucleo = nx.Graph(H)

    mudou = True
    while mudou:
        mudou = False
        for vertice in list(nucleo.nodes()):
            if nucleo.degree(vertice) != 2:
                continue

            vizinhos = list(nucleo.neighbors(vertice))
            if len(vizinhos) != 2:
                continue

            u, v = vizinhos
            nucleo.remove_node(vertice)
            if u != v:
                nucleo.add_edge(u, v)
            mudou = True
            break

    return nucleo


def obter_biparticao(G):
    """Calcula uma biparticao por BFS, sem usar detector automatico de K3,3."""
    cor = {}

    for origem in G.nodes():
        if origem in cor:
            continue

        cor[origem] = 0
        fila = [origem]
        indice = 0

        while indice < len(fila):
            u = fila[indice]
            indice += 1
            for v in G.neighbors(u):
                if v not in cor:
                    cor[v] = 1 - cor[u]
                    fila.append(v)
                elif cor[v] == cor[u]:
                    return None

    parte_a = sorted([v for v, cor_v in cor.items() if cor_v == 0])
    parte_b = sorted([v for v, cor_v in cor.items() if cor_v == 1])
    return parte_a, parte_b


def eh_k33(G, graus):
    """Verifica se o nucleo tem a estrutura de K3,3."""
    biparticao = obter_biparticao(G)

    if G.number_of_nodes() != 6 or G.number_of_edges() != 9 or graus != [3] * 6:
        return False

    if biparticao is None:
        return False

    if len(biparticao[0]) != 3 or len(biparticao[1]) != 3:
        return False

    return True
