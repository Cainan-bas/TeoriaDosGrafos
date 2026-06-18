# Relatorio: Algoritmo de Boyer-Myrvold

O algoritmo de Boyer-Myrvold realiza o teste de planaridade em tempo linear. A ideia central e construir uma busca em profundidade, analisar as arestas de retorno e tentar montar uma embedding combinatorial do grafo, isto e, a ordem circular das arestas ao redor de cada vertice. Se todas as partes do grafo conseguem ser encaixadas sem cruzamentos, o algoritmo devolve uma embedding planar valida.

Quando o encaixe nao e possivel, o algoritmo consegue produzir um certificado de nao planaridade. Pelo teorema de Kuratowski, esse certificado contem uma subdivisao de `K5` ou de `K3,3`. Assim, vertices de grau 2 podem ser apenas subdivisoes de arestas; ao contrair esses vertices, aparece o nucleo homeomorfo a `K5` ou `K3,3`.

Neste trabalho, o programa usa `nx.check_planarity(G, True)`, que executa o teste baseado no algoritmo de Boyer-Myrvold e obrigatoriamente retorna um certificado:

- se o grafo e planar, o certificado e um objeto `PlanarEmbedding`;
- se o grafo nao e planar, o certificado e um subgrafo testemunha de nao planaridade.

Para grafos planares, o codigo imprime a ordem circular dos vizinhos em cada vertice do `PlanarEmbedding` e desenha o grafo usando `nx.combinatorial_embedding_to_pos(embedding)`. Assim, a imagem final respeita a embedding retornada pelo algoritmo, sem uso de layouts automaticos como `spring_layout`.

Para grafos nao planares, o codigo manipula o subgrafo testemunha retornado, contrai vertices de grau 2 e classifica o nucleo obtido. Se o nucleo possui 5 vertices todos de grau 4 e 10 arestas, ele e identificado como `K5`. Se possui 6 vertices todos de grau 3, 9 arestas e biparticao `3 + 3`, ele e identificado como `K3,3`. O programa exibe os vertices envolvidos no certificado, os vertices do nucleo e, no caso de `K3,3`, as duas particoes.
