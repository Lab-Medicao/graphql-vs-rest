# GraphQL vs REST: Experimento Controlado

Este projeto compara desempenho entre consultas via GraphQL e REST na API do GitHub, com fluxo completo de coleta, análise e geração de gráficos.

Para detalhes metodológicos, resultados e discussão completos, consulte o relatório técnico:

- Relatório Técnico: `REPORT.md`

## Visão Geral do Projeto

- Objetivo: medir diferenças de desempenho (tempo de resposta e tamanho de payload) entre GraphQL e REST em cenários equivalentes.
- Linguagem: Python (coleta, análise e visualização).
- Saídas: CSV em `results/`, gráficos em `results/plots/`, análise em `analyzers/analysis_report.md`.

## Arquitetura e Organização

- `src/`:
  - `main.py`: orquestrador do fluxo (coleta → análise → gráficos) com logs.
  - `design.py` e `design_snapshot.md`: sumarização do desenho experimental e snapshot em Markdown.
  - `configs/`: configuração (`config.py`), geradores de requisição (`request_generators.py`).
- `collectors/`:
  - `collector.py`: coletor; executa tratamentos concorrentes e grava CSV incremental.
- `analyzers/`:
  - `analyze_results.py`: análise estatística e geração de gráficos (labels em português), escreve `analysis_report.md` e imagens em `src/results/plots/`.
- `results/`: arquivos CSV por execução.
- `logs/`: `pipeline.log` (orquestração) e `experiment.log` (coleta).
- `tests/`: testes unitários sem rede (estrutura e config).
- `.github/workflows/ci.yml`: pipeline CI com `pytest`.

## Setup Rápido

- Pré-requisitos: Python 3.11+, `GITHUB_TOKEN` configurado em `.env`
- Instalar dependências:

```bash
"$PWD/.venv/Scripts/python.exe" -m pip install -r requirements.txt
```

- Rodar testes:

```bash
"$PWD/.venv/Scripts/python.exe" -m pytest -q
```

## Execução

- Pipeline completa (coleta → análise → gráficos):

```bash
"$PWD/.venv/Scripts/python.exe" -m src.main
```

- Apenas coleta:

```bash
"$PWD/.venv/Scripts/python.exe" -m src.run_experiment
```

- Apenas análise/gráficos:

```bash
"$PWD/.venv/Scripts/python.exe" -m analyzers.analyze_results
```

## Saídas

- CSV: `results/experiment_YYYY-MM-DDTHH-MM-SS.csv`
- Gráficos: `results/plots/`
- Análise: `analyzers/analysis_report.md`

## CI e Testes

- GitHub Actions: `.github/workflows/ci.yml` roda `pytest`
- Testes unitários: `tests/` com validações básicas de módulos

## Observações

- Respeite rate limit do GitHub (~5000 req/h)
- Ajuste parâmetros em `src/config.py`

---

## Desenho do Experimento

Conteúdo derivado de `src/design_snapshot.md`:

### Hipóteses

- RQ1 — H0: Não há diferença significativa nos tempos de resposta entre GraphQL e REST.
- RQ1 — H1: GraphQL apresenta tempos de resposta significativamente menores do que REST.
- RQ2 — H0: Não há diferença significativa no tamanho dos payloads entre GraphQL e REST.
- RQ2 — H1: GraphQL apresenta payloads significativamente menores do que REST.

### Variáveis

- Independentes: `api_type` (REST, GraphQL), `query_type` (simple, nested, aggregated), `cache_state` (cold, warm), `concurrent_clients` (níveis de carga)
- Dependentes: `response_time_ms`, `payload_size_bytes`

### Tratamentos

- Comparação REST vs GraphQL
- Cache ligado (warm) vs desligado (cold)
- Níveis de carga: valores de `concurrent_clients`

### Objetos experimentais

- REST: `simple`, `nested`, `aggregated` conforme endpoints definidos
- GraphQL: queries equivalentes conforme definidas

### Tipo de Projeto Experimental

Fatorial completo e balanceado, entre-sujeitos por tratamento (combinações de `api_type`, `query_type`, `cache_state` e níveis de `concurrent_clients`). Medições repetidas por cliente em cada tratamento.

### Quantidade de medições (N)

N por cliente definido por `config['experiment']['repetitions']`, visando estabilidade estatística e poder do teste (tipicamente N≥50 por condição em testes não-paramétricos).

### Ameaças à validade

- Conclusão: viés de implementação; interpretação indevida sem tamanho de efeito.
- Interna: variações de rede/latência; caching em camadas não controladas.
- Externa: generalização limitada além do GitHub API.
- Estatística: não-normalidade; outliers; heterocedasticidade sob alta concorrência.

Para a versão completa e discutida, consulte `REPORT.md`.
