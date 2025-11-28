require('dotenv').config();

const config = {
  github: {
    token: process.env.GITHUB_TOKEN,
    restBaseUrl: 'https://api.github.com',
    graphqlUrl: 'https://api.github.com/graphql'
  },
  experiment: {
    repetitions: 50,
    warmupRequests: 15,
    requestInterval: 100, // ms
    timeout: 30000, // 30s
    concurrentClients: [1, 10, 50],
    queryTypes: ['simple', 'nested', 'aggregated'],
    cacheStates: ['cold', 'warm']
  },
  output: {
    resultsDir: './results',
    csvHeaders: ['timestamp', 'api_type', 'query_type', 'concurrent_clients', 'cache_state', 'response_time_ms', 'payload_size_bytes', 'status_code']
  }
};

module.exports = config;