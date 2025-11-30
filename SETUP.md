# Setup do Experimento

## Pré-requisitos

1. **Python** (versão 3.8 ou superior)
2. **Token do GitHub** com acesso às APIs REST e GraphQL

## Configuração

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar token do GitHub
1. Acesse: https://github.com/settings/tokens
2. Gere um Personal Access Token com as permissões:
   - `public_repo` (para acessar repositórios públicos)
   - `read:user` (para informações de usuário)
3. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edite o arquivo `.env` e adicione seu token:
   ```
   GITHUB_TOKEN=seu_token_aqui
   ```

### 3. Testar configuração
```bash
python src/test_setup.py
```

Este comando irá:
- Verificar se o token está configurado
- Testar conexão com as APIs REST e GraphQL
- Executar todas as consultas de teste
- Validar se o ambiente está pronto

### 4. Executar experimento
```bash
python src/experiment.py
```

## Estrutura do Projeto

```
src/
├── config.py          # Configurações do experimento
├── queries.py         # Consultas REST e GraphQL
├── clients.py         # Clientes HTTP para ambas APIs
├── data_collector.py  # Coleta e armazenamento de dados
├── experiment.py      # Script principal do experimento
└── test_setup.py      # Teste de configuração

results/               # Arquivos CSV com resultados
```

## Resultados

Os resultados são salvos em `results/experiment_YYYY-MM-DD-HH-MM-SS.csv` com as colunas:
- `timestamp`: momento da medição
- `api_type`: REST ou GraphQL
- `query_type`: simple, nested, aggregated
- `concurrent_clients`: 1, 10, ou 50
- `cache_state`: cold ou warm
- `response_time_ms`: tempo de resposta em milissegundos
- `payload_size_bytes`: tamanho da resposta em bytes
- `status_code`: código HTTP da resposta

## Limitações

- **Rate Limit**: GitHub permite 5000 requisições/hora por token
- **Tempo estimado**: 4-6 horas para experimento completo
- **Rede**: Execute em ambiente estável para resultados consistentes