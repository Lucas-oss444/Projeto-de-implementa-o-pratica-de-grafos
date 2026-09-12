# Rede de Transporte Urbano Modelada como Dígrafo

Modelagem e implementação de um sistema de transporte público simplificado usando grafos. Trabalho da disciplina de Teoria dos Grafos.

A rede é fictícia, inspirada na malha de Belém (PA), com 15 paradas distribuídas em 6 linhas.

## Modelagem

O sistema é representado por um multidígrafo ponderado e rotulado:

**G = (V, A, w, l)**

- **V**: paradas e estações. |V| = 15
- **A**: arcos, um para cada trecho servido diretamente por uma linha. |A| = 31
- **w: A -> R+**: tempo médio de percurso do trecho, em minutos
- **l: A -> L**: linha responsável pelo trecho

### Por que dígrafo

As linhas L3 (Circular Centro) e L6 (Expresso Industrial) operam em sentido único. Um grafo não-dirigido produziria caminhos que não existem na operação real. Trechos de mão dupla são representados por dois arcos antiparalelos.

### Por que multigrafo

Ver-o-Peso e Nazaré são ligados pela L1 (mão dupla) e pela L3 (mão única), com pesos e rótulos distintos. São dois arcos diferentes entre o mesmo par de vértices.

### Estrutura de dados: lista de adjacência

Implementada como um dicionário `{parada: [(destino, tempo, linha), ...]}`.

O grau médio da rede é aproximadamente 2 x 31 / 15 = 4,1. Redes de transporte são esparsas por natureza: uma parada conecta a poucas vizinhas, independentemente do tamanho da malha. Uma matriz de adjacência ocuparia |V|^2 = 225 posições para armazenar 31 arcos, e degradaria o Dijkstra de O((|V| + |A|) log |V|) para O(|V|^2). Em escala real a diferença é decisiva.

A lista de adjacência também acomoda arcos paralelos sem tratamento especial, o que uma matriz de adjacência simples não faz.

## Algoritmos implementados

### Dijkstra - caminho mais curto ponderado

Calcula o trajeto de menor tempo total a partir de uma origem. Usa fila de prioridade e relaxamento de arestas. Ao remover um vértice da fila, sua distância já é definitiva, propriedade que só vale porque todos os pesos são não-negativos. Como tempo de viagem nunca é negativo, não há necessidade de Bellman-Ford.

Complexidade: O((|V| + |A|) log |V|).

### BFS - caminho com menor número de trechos

Percorre o grafo em largura ignorando os pesos, ou seja, tratando todo arco como custo 1. É o caso particular do Dijkstra com pesos uniformes.

Complexidade: O(|V| + |A|).

### Kosaraju - componentes fortemente conexas

Duas passagens de busca em profundidade: a primeira registra a ordem de finalização dos vértices, a segunda percorre o grafo transposto na ordem inversa. Cada árvore da segunda passagem é uma componente fortemente conexa.

Complexidade: O(|V| + |A|).

### DFS - detecção de circuito

Busca em profundidade mantendo o caminho corrente. Um arco que aponta para um vértice ainda no caminho fecha um circuito.

Como cada trecho de mão dupla gera um circuito trivial de comprimento 2 (u -> v -> u), a busca proíbe retornar imediatamente pelo arco inverso e exige circuitos de comprimento mínimo 3.

## Conceitos da disciplina demonstrados

| Conceito | Onde aparece |
|---|---|
| Dígrafo | Linhas de sentido único (L3 e L6) |
| Grafo ponderado | Tempo de percurso em cada arco |
| Multigrafo | Ver-o-Peso e Nazaré ligados por L1 e L3 |
| Caminho | Dijkstra e BFS |
| Conexidade forte | Kosaraju: 2 componentes |
| Conexidade fraca | Verificada sobre o grafo subjacente não-dirigido |
| Circuito | DFS sobre a malha central |
| Lista de adjacência | Estrutura base de todo o programa |

## Execução

Requer apenas Python 3. Nenhuma dependência externa.

```
python rede_transporte.py
```

## Saída

```
Digrafo ponderado: |V| = 15, |A| = 31

Dijkstra (Icoaraci -> UFPA): 45 min
Icoaraci --[L2]--> Coqueiro --[L5]--> Telegrafo --[L5]--> Pedreira --[L5]--> Sao Bras --[L4]--> Guama --[L4]--> UFPA
Trechos: 6 | Baldeacoes: 2

BFS (Icoaraci -> UFPA): 5 trechos
Icoaraci --[L2]--> Coqueiro --[L2]--> Entroncamento --[L1]--> Sao Bras --[L4]--> Guama --[L4]--> UFPA
Tempo: 49 min | Baldeacoes: 2

Componentes fortemente conexas:
  C1 (14): todas as paradas exceto Distrito Industrial
  C2 (1): Distrito Industrial
Fortemente conexo: False
Fracamente conexo: True

Circuito encontrado: Sao Bras -> Entroncamento -> Coqueiro -> Telegrafo -> Pedreira -> Sao Bras
Sem caminho ate Icoaraci: ['Distrito Industrial']
```

## Leitura dos resultados

**Caminho mais curto e caminho com menos trechos são objetivos distintos.** Para o par Icoaraci - UFPA, o trajeto mais rápido tem 6 trechos e 45 minutos, enquanto o trajeto com menos trechos tem 5 trechos e 49 minutos. A rota mais rápida passa por Telégrafo e Pedreira, evitando o trecho lento entre Coqueiro e Entroncamento.

**A rede é fracamente conexa, mas não fortemente conexa.** O Distrito Industrial forma uma componente isolada de um único vértice: a L6 é expressa de sentido único, então é possível chegar até lá e impossível voltar de lá pela malha modelada. A distinção entre conexidade forte e fraca tem consequência operacional direta.

## Limitações do modelo

- Os tempos de percurso são fixos, sem variação por horário ou congestionamento
- O tempo de espera pelo próximo veículo não é modelado
- A contagem de baldeações é feita sobre o caminho já escolhido pelos algoritmos, e não minimizada. Minimizar baldeações exige expandir o grafo para estados (parada, linha), com custo 1 na troca de linha e 0 na permanência
- Os dados da rede são fictícios e não correspondem a itinerários reais

## Arquivos

- `rede_transporte.py`: implementação completa
- `README.md`: este documento
