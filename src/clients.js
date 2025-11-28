const axios = require('axios');
const { GraphQLClient } = require('graphql-request');
const config = require('./config');

class RestClient {
  constructor() {
    this.client = axios.create({
      baseURL: config.github.restBaseUrl,
      headers: {
        'Authorization': `token ${config.github.token}`,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GraphQL-vs-REST-Experiment'
      },
      timeout: config.experiment.timeout
    });
  }

  async makeRequest(url) {
    const startTime = Date.now();
    try {
      const response = await this.client.get(url);
      const endTime = Date.now();
      
      return {
        responseTime: endTime - startTime,
        payloadSize: JSON.stringify(response.data).length,
        statusCode: response.status,
        success: true,
        data: response.data
      };
    } catch (error) {
      const endTime = Date.now();
      return {
        responseTime: endTime - startTime,
        payloadSize: 0,
        statusCode: error.response?.status || 0,
        success: false,
        error: error.message
      };
    }
  }

  async makeAggregatedRequest(urls) {
    const startTime = Date.now();
    try {
      const promises = urls.map(url => this.client.get(url));
      const responses = await Promise.all(promises);
      const endTime = Date.now();
      
      const combinedData = responses.map(r => r.data);
      
      return {
        responseTime: endTime - startTime,
        payloadSize: JSON.stringify(combinedData).length,
        statusCode: 200,
        success: true,
        data: combinedData
      };
    } catch (error) {
      const endTime = Date.now();
      return {
        responseTime: endTime - startTime,
        payloadSize: 0,
        statusCode: error.response?.status || 0,
        success: false,
        error: error.message
      };
    }
  }
}

class GraphQLClientWrapper {
  constructor() {
    this.client = new GraphQLClient(config.github.graphqlUrl, {
      headers: {
        'Authorization': `Bearer ${config.github.token}`,
        'User-Agent': 'GraphQL-vs-REST-Experiment'
      },
      timeout: config.experiment.timeout
    });
  }

  async makeRequest(query) {
    const startTime = Date.now();
    try {
      const data = await this.client.request(query);
      const endTime = Date.now();
      
      return {
        responseTime: endTime - startTime,
        payloadSize: JSON.stringify(data).length,
        statusCode: 200,
        success: true,
        data: data
      };
    } catch (error) {
      const endTime = Date.now();
      return {
        responseTime: endTime - startTime,
        payloadSize: 0,
        statusCode: error.response?.status || 0,
        success: false,
        error: error.message
      };
    }
  }
}

module.exports = { RestClient, GraphQLClientWrapper };