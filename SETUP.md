# Setup do Experimento

## Pré-requisitos

1. **Node.js** (versão 16 ou superior)
2. **Token do GitHub** com acesso às APIs REST e GraphQL

## Configuração

### 1. Instalar dependências
```bash
npm install
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
npm test
```

Este comando irá:
- Verificar se o token está configurado
- Testar conexão com as APIs REST e GraphQL
- Executar todas as consultas de teste
- Validar se o ambiente está pronto

### 4. Executar experimento
```bash
npm start
```

## Estrutura do Projeto

```
src/
├── config.js          # Configurações do experimento
├── queries.js         # Consultas REST e GraphQL
├── clients.js         # Clientes HTTP para ambas APIs
├── data-collector.js  # Coleta e armazenamento de dados
├── experiment.js      # Script principal do experimento
└── test-setup.js      # Teste de configuração

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