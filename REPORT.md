# Relatório Técnico: GraphQL vs Rest - Um experimento controlado

## 1. Informações do grupo

- Curso: Engenharia de Software
- Disciplina: Laboratório de Experimentação de Software
- Período: 6° Período
- Professor(a): Prof. Dr. João Paulo Carneiro Aramuni
- Membros do Grupo: Ana Luiza Machado Alves, Lucas Henrique Chaves Barros, Raquel de Almeida Calazans

---

## 2. Introdução

Este relatório apresenta um experimento controlado comparando desempenho entre GraphQL e REST na API do GitHub. O objetivo é avaliar tempos de resposta e tamanho de payload sob diferentes condições de cache e carga concorrente, seguindo um desenho experimental fatorial e balanceado.

### 2.1. Questões de Pesquisa (Research Questions – RQs)

As questões de pesquisa foram definidas para guiar a investigação e estruturar a análise dos dados coletados:

Questões de Pesquisa (RQs):

| RQ   | Pergunta                                                    |
| ---- | ----------------------------------------------------------- |
| RQ01 | Respostas GraphQL são mais rápidas que REST?                |
| RQ02 | Respostas GraphQL têm tamanho de payload menor do que REST? |

### 2.2. Hipóteses

Hipóteses formais para cada RQ:

H0 (RQ1): Não há diferença significativa nos tempos de resposta entre GraphQL e REST.
H1 (RQ1): GraphQL apresenta tempos de resposta significativamente menores do que REST.

H0 (RQ2): Não há diferença significativa no tamanho dos payloads entre GraphQL e REST.
H1 (RQ2): GraphQL apresenta payloads significativamente menores do que REST.

Observações: Hipóteses focadas em desempenho de API, não em maturidade de repositórios.

---

## 3. Tecnologias e ferramentas utilizadas

- Linguagem de Programação: Python
- Bibliotecas: requests, gql, pandas, scipy, matplotlib, seaborn
- APIs utilizadas: GitHub GraphQL API, GitHub REST API
- Dependências: definidas em `requirements.txt`

---

## 4. Metodologia

O experimento segue as etapas: desenho, preparação, execução, análise e relatório. Os scripts estão em `src/`. A coleta consiste em executar consultas equivalentes REST e GraphQL contra a API do GitHub em diferentes tratamentos (cache cold/warm, níveis de carga 1/10/50 e tipos de consulta simple/nested/aggregated). Resultados são salvos em CSV com colunas: `timestamp, api_type, query_type, concurrent_clients, cache_state, response_time_ms, payload_size_bytes, status_code`.

---

### 4.1 Coleta de dados

Consultas e endpoints definidos em `src/queries.py`. Clientes REST/GraphQL em `src/clients.py`. Geração de requisições em `src/request_generators.py`. Execução em `src/run_experiment.py`.

---

### 4.2 Tratamentos e controle

Projeto fatorial completo e balanceado, entre-sujeitos por tratamento: `api_type` (REST/GraphQL) × `query_type` (simple/nested/aggregated) × `cache_state` (cold/warm) × `concurrent_clients` (1/10/50). Warm-up aplicado quando `cache_state=warm`. Número de repetições por cliente configurado em `src/config.py`.

---

### 4.3 Medições e amostragem

Medições registradas por cliente e por repetição. CSV incremental com as colunas padronizadas. Amostragem suficiente por tratamento configurada via `repetitions`.

---

### 4.4 Métricas

Métricas do experimento GraphQL vs REST:

#### Métricas (Lab)

| Código | Métrica            | Descrição                                    |
| ------ | ------------------ | -------------------------------------------- |
| M01    | response_time_ms   | Tempo de resposta observado em milissegundos |
| M02    | payload_size_bytes | Tamanho do payload observado em bytes        |
| F01    | status_code        | Código HTTP de retorno                       |
| F02    | cache_state        | Estado de cache: cold/warm                   |
| F03    | concurrent_clients | Número de clientes concorrentes              |
| F04    | query_type         | Tipo de consulta: simple/nested/aggregated   |
| F05    | api_type           | Tipo de API: REST/GraphQL                    |

#### Métricas adicionais (opcional)

| Código | Métrica                   | Descrição                                 |
| ------ | ------------------------- | ----------------------------------------- |
| A01    | tamanho de efeito (delta) | Estimativa com delta de Cliff             |
| A02    | distribuição normal       | Verificação Shapiro para escolha do teste |

> [!NOTE]
> Adapte ou acrescente métricas conforme o seu dataset.

---

### 4.5 Cálculo e testes estatísticos

Para cada RQ, comparamos grupos REST vs GraphQL usando t-test (se normalidade) ou Mann-Whitney (caso contrário). Estatísticas descritivas incluem média, mediana, desvio padrão e percentis. O tamanho de efeito é estimado com delta de Cliff. Implementação em `src/analyze_results.py`.

---

### 4.6 Execução

Script de execução: `src/run_experiment.py`. Saída: CSV em `results/experiment_YYYY-MM-DDTHH-MM-SS.csv`. Design snapshot em `src/design_snapshot.md`.

---

### 4.7 Relação das RQs com as Métricas

As RQs foram associadas às métricas definidas na seção 4.4, garantindo investigação sistemática e mensurável.

A tabela a seguir apresenta a relação entre cada questão de pesquisa e as métricas utilizadas para sua avaliação:

Relação das RQs com Métricas:

| RQ   | Pergunta                            | Métrica utilizada  | Código da Métrica |
| ---- | ----------------------------------- | ------------------ | ----------------- |
| RQ01 | GraphQL é mais rápido que REST?     | Tempo de resposta  | M01               |
| RQ02 | GraphQL tem payload menor que REST? | Tamanho do payload | M02               |

---

## 5. Resultados

Resultados gerados a partir do CSV `results/experiment_YYYY-MM-DDTHH-MM-SS.csv` e analisados por `src/analyze_results.py`.

---

### 5.1 Visualizações

Visualizações produzidas:

- Boxplot: `src/plots/boxplot_response_time.png` (Tempo de resposta por tipo de API e cache)
- Histograma: `src/plots/hist_payload.png` (Distribuição do tamanho do payload)
- Barras: `src/plots/bar_means.png` (Média de tempo de resposta por tratamento)

---

### 5.2 Estatísticas Descritivas

Estatísticas descritivas calculadas sobre `response_time_ms` e `payload_size_bytes` (média, mediana, desvio padrão, percentis) estão detalhadas em `src/analysis_report.md`.

| Métrica                | Código | Média       | Mediana     | Desvio Padrão | P25         | P75         |
| ---------------------- | ------ | ----------- | ----------- | ------------- | ----------- | ----------- |
| Tempo de resposta (ms) | M01    | ver análise | ver análise | ver análise   | ver análise | ver análise |
| Tamanho do payload (B) | M02    | ver análise | ver análise | ver análise   | ver análise | ver análise |

Observação: gráficos estão incluídos na seção 5.1.

---

### 5.3 Testes estatísticos

Resultados dos testes e decisões para H0/H1 estão em `src/analysis_report.md`, incluindo método utilizado (t-test ou Mann-Whitney), estatística, p-valor e tamanho de efeito aproximado.

---

### 5.4 Discussão dos resultados

Compare os resultados obtidos com as hipóteses H0/H1 das RQs. Discuta possíveis causas para diferenças observadas (ex.: conteúdo das consultas, estrutura dos dados retornados pela API, efeitos de cache, variabilidade de rede), e relacione com ameaças à validade (interna, externa, de conclusão e estatística).

---

## 6. Conclusão

Resumo das principais descobertas do experimento.

- Principais insights:

  - Comparações REST vs GraphQL por tratamento com estatísticas e testes.
  - Efeitos de cache e carga concorrente sobre tempo de resposta e payload.
  - Decisão sobre H0/H1 para RQ1 e RQ2 com base em p-valor e tamanho de efeito.

- Problemas e dificuldades enfrentadas:

  - Limites de taxa da API do GitHub e variabilidade de rede.
  - Efeitos de cache invisíveis (CDN/servidor) e heterogeneidade dos dados retornados.

- Sugestões para trabalhos futuros:
  - Ampliar conjunto de endpoints/queries e replicar em outros domínios.
  - Controlar mais estritamente caching e latência de rede (ambiente controlado).
  - Incluir métricas de overhead de serialização e compressão.

---

## 7. Referências

Referências:

- GitHub API Documentation: https://docs.github.com/en/graphql
- Biblioteca Pandas: https://pandas.pydata.org/
- SciPy: https://scipy.org/
- Seaborn: https://seaborn.pydata.org/

---

## 8. Apêndices

- Scripts utilizados para coleta e análise de dados: `src/`
- Consultas GraphQL e endpoints REST: `src/queries.py`
- Arquivos CSV gerados: `results/`

---
