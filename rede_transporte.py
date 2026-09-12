import heapq
from collections import deque

LINHAS = [
    ("L1 - BRT Almirante Barroso",
        ["Ver-o-Peso", "Nazare", "Sao Bras", "Entroncamento", "Marambaia", "Aguas Lindas"],
        [6, 5, 9, 7, 8], True),
    ("L2 - Augusto Montenegro",
        ["Entroncamento", "Coqueiro", "Icoaraci"],
        [16, 12], True),
    ("L3 - Circular Centro",
        ["Ver-o-Peso", "Cidade Velha", "Batista Campos", "Nazare", "Ver-o-Peso"],
        [4, 6, 5, 7], False),
    ("L4 - Universitario",
        ["Sao Bras", "Guama", "UFPA", "Batista Campos"],
        [8, 4, 6], True),
    ("L5 - Pedreira",
        ["Sao Bras", "Pedreira", "Telegrafo", "Coqueiro"],
        [7, 5, 9], True),
    ("L6 - Expresso Industrial",
        ["Aguas Lindas", "Distrito Industrial"],
        [11], False),
]


def add_arco(g, u, v, tempo, linha, mao_dupla):
    g.setdefault(u, [])
    g.setdefault(v, [])
    g[u].append((v, tempo, linha))
    if mao_dupla:
        g[v].append((u, tempo, linha))


def construir_grafo(linhas):
    g = {}
    for nome, paradas, tempos, mao_dupla in linhas:
        for i in range(len(paradas) - 1):
            add_arco(g, paradas[i], paradas[i + 1], tempos[i], nome, mao_dupla)
    return g


def dijkstra(g, origem):
    dist = {u: float("inf") for u in g}
    ant = {u: None for u in g}
    dist[origem] = 0
    fila = [(0, origem)]
    while fila:
        d, u = heapq.heappop(fila)
        if d > dist[u]:
            continue
        for v, tempo, linha in g[u]:
            if d + tempo < dist[v]:
                dist[v] = d + tempo
                ant[v] = (u, linha)
                heapq.heappush(fila, (dist[v], v))
    return dist, ant


def bfs(g, origem, destino):
    ant = {origem: None}
    fila = deque([origem])
    while fila:
        u = fila.popleft()
        if u == destino:
            return ant
        for v, _, linha in g[u]:
            if v not in ant:
                ant[v] = (u, linha)
                fila.append(v)
    return ant


def reconstruir(ant, destino):
    if destino not in ant:
        return None
    caminho = []
    atual = destino
    while atual is not None:
        pai = ant[atual]
        caminho.append((atual, pai[1] if pai else None))
        atual = pai[0] if pai else None
    caminho.reverse()
    return caminho


def contar_baldeacoes(caminho):
    linhas = [l for _, l in caminho if l]
    return sum(1 for i in range(1, len(linhas)) if linhas[i] != linhas[i - 1])


def transpor(g):
    gt = {u: [] for u in g}
    for u in g:
        for v, tempo, linha in g[u]:
            gt[v].append((u, tempo, linha))
    return gt


def kosaraju(g):
    visitado = set()
    ordem = []

    def dfs1(u):
        pilha = [(u, iter(g[u]))]
        visitado.add(u)
        while pilha:
            no, viz = pilha[-1]
            avancou = False
            for v, _, _ in viz:
                if v not in visitado:
                    visitado.add(v)
                    pilha.append((v, iter(g[v])))
                    avancou = True
                    break
            if not avancou:
                ordem.append(pilha.pop()[0])

    for u in g:
        if u not in visitado:
            dfs1(u)

    gt = transpor(g)
    visitado.clear()
    componentes = []
    for u in reversed(ordem):
        if u in visitado:
            continue
        comp = []
        pilha = [u]
        visitado.add(u)
        while pilha:
            no = pilha.pop()
            comp.append(no)
            for v, _, _ in gt[no]:
                if v not in visitado:
                    visitado.add(v)
                    pilha.append(v)
        componentes.append(comp)
    return componentes


def conexo_fracamente(g):
    nao_dirigido = {u: set() for u in g}
    for u in g:
        for v, _, _ in g[u]:
            nao_dirigido[u].add(v)
            nao_dirigido[v].add(u)
    inicio = next(iter(g))
    visitado = {inicio}
    fila = deque([inicio])
    while fila:
        u = fila.popleft()
        for v in nao_dirigido[u]:
            if v not in visitado:
                visitado.add(v)
                fila.append(v)
    return len(visitado) == len(g)


def encontrar_circuito(g, origem, minimo=3):
    caminho = []
    em_caminho = set()

    def dfs(u, anterior):
        caminho.append(u)
        em_caminho.add(u)
        for v, _, _ in g[u]:
            if v == anterior:
                continue
            if v in em_caminho:
                i = caminho.index(v)
                if len(caminho) - i >= minimo:
                    return caminho[i:] + [v]
            else:
                achado = dfs(v, u)
                if achado:
                    return achado
        caminho.pop()
        em_caminho.discard(u)
        return None

    return dfs(origem, None)


def formatar(caminho):
    partes = [caminho[0][0]]
    for parada, linha in caminho[1:]:
        partes.append(f"--[{linha}]--> {parada}")
    return " ".join(partes)


def main():
    g = construir_grafo(LINHAS)
    arcos = sum(len(v) for v in g.values())
    print(f"Digrafo ponderado: |V| = {len(g)}, |A| = {arcos}")

    origem, destino = "Icoaraci", "UFPA"

    dist, ant = dijkstra(g, origem)
    print(f"\nDijkstra ({origem} -> {destino}): {dist[destino]} min")
    caminho = reconstruir(ant, destino)
    print(formatar(caminho))
    print(f"Trechos: {len(caminho) - 1} | Baldeacoes: {contar_baldeacoes(caminho)}")

    caminho_bfs = reconstruir(bfs(g, origem, destino), destino)
    tempo_bfs = 0
    for i in range(1, len(caminho_bfs)):
        u, v = caminho_bfs[i - 1][0], caminho_bfs[i][0]
        tempo_bfs += min(t for w, t, _ in g[u] if w == v)
    print(f"\nBFS ({origem} -> {destino}): {len(caminho_bfs) - 1} trechos")
    print(formatar(caminho_bfs))
    print(f"Tempo: {tempo_bfs} min | Baldeacoes: {contar_baldeacoes(caminho_bfs)}")

    print("\nComponentes fortemente conexas:")
    for i, comp in enumerate(kosaraju(g), 1):
        print(f"  C{i} ({len(comp)}): {', '.join(sorted(comp))}")
    print(f"Fortemente conexo: {len(kosaraju(g)) == 1}")
    print(f"Fracamente conexo: {conexo_fracamente(g)}")

    circuito = encontrar_circuito(g, "Ver-o-Peso")
    print(f"\nCircuito encontrado: {' -> '.join(circuito)}")

    inalcancaveis = [u for u in g if dijkstra(g, u)[0]["Icoaraci"] == float("inf")]
    print(f"Sem caminho ate Icoaraci: {inalcancaveis}")


if __name__ == "__main__":
    main()
