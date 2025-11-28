const fs = require('fs-extra');
const path = require('path');
const config = require('./config');

class DataCollector {
  constructor() {
    this.results = [];
    this.filename = this.generateFilename();
    this.ensureResultsDir();
  }

  generateFilename() {
    const now = new Date();
    const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, 19);
    return `experiment_${timestamp}.csv`;
  }

  async ensureResultsDir() {
    await fs.ensureDir(config.output.resultsDir);
  }

  addResult(apiType, queryType, concurrentClients, cacheState, result) {
    const record = {
      timestamp: new Date().toISOString(),
      api_type: apiType,
      query_type: queryType,
      concurrent_clients: concurrentClients,
      cache_state: cacheState,
      response_time_ms: result.responseTime,
      payload_size_bytes: result.payloadSize,
      status_code: result.statusCode
    };
    
    this.results.push(record);
  }

  async saveResults() {
    const filepath = path.join(config.output.resultsDir, this.filename);
    
    // Create CSV content
    const headers = config.output.csvHeaders.join(',');
    const rows = this.results.map(record => 
      config.output.csvHeaders.map(header => record[header]).join(',')
    );
    
    const csvContent = [headers, ...rows].join('\n');
    
    await fs.writeFile(filepath, csvContent);
    console.log(`Results saved to: ${filepath}`);
    return filepath;
  }

  getStats() {
    return {
      totalMeasurements: this.results.length,
      successfulRequests: this.results.filter(r => r.status_code === 200).length,
      failedRequests: this.results.filter(r => r.status_code !== 200).length,
      avgResponseTime: this.results.reduce((sum, r) => sum + r.response_time_ms, 0) / this.results.length,
      avgPayloadSize: this.results.reduce((sum, r) => sum + r.payload_size_bytes, 0) / this.results.length
    };
  }
}

module.exports = DataCollector;