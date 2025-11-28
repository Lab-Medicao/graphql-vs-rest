const { RestClient, GraphQLClientWrapper } = require('./clients');
const { restQueries, graphqlQueries } = require('./queries');
const DataCollector = require('./data-collector');
const config = require('./config');

class ExperimentRunner {
  constructor() {
    this.restClient = new RestClient();
    this.graphqlClient = new GraphQLClientWrapper();
    this.dataCollector = new DataCollector();
  }

  async runWarmup(apiType, queryType) {
    console.log(`Running warmup for ${apiType} - ${queryType}...`);
    
    for (let i = 0; i < config.experiment.warmupRequests; i++) {
      if (apiType === 'REST') {
        await this.executeRestQuery(queryType);
      } else {
        await this.executeGraphQLQuery(queryType);
      }
      await this.sleep(config.experiment.requestInterval);
    }
  }

  async executeRestQuery(queryType) {
    const query = restQueries[queryType];
    
    if (queryType === 'aggregated') {
      return await this.restClient.makeAggregatedRequest(query.urls);
    } else {
      return await this.restClient.makeRequest(query.url);
    }
  }

  async executeGraphQLQuery(queryType) {
    const query = graphqlQueries[queryType];
    return await this.graphqlClient.makeRequest(query);
  }

  async runTreatment(apiType, queryType, concurrentClients, cacheState) {
    console.log(`Running treatment: ${apiType} - ${queryType} - ${concurrentClients} clients - ${cacheState} cache`);
    
    // Warmup if cache is warm
    if (cacheState === 'warm') {
      await this.runWarmup(apiType, queryType);
    }

    const promises = [];
    
    for (let client = 0; client < concurrentClients; client++) {
      promises.push(this.runClientMeasurements(apiType, queryType, concurrentClients, cacheState));
    }
    
    await Promise.all(promises);
  }

  async runClientMeasurements(apiType, queryType, concurrentClients, cacheState) {
    for (let rep = 0; rep < config.experiment.repetitions; rep++) {
      let result;
      
      if (apiType === 'REST') {
        result = await this.executeRestQuery(queryType);
      } else {
        result = await this.executeGraphQLQuery(queryType);
      }
      
      this.dataCollector.addResult(apiType, queryType, concurrentClients, cacheState, result);
      
      if (rep < config.experiment.repetitions - 1) {
        await this.sleep(config.experiment.requestInterval);
      }
    }
  }

  generateTreatments() {
    const treatments = [];
    
    for (const queryType of config.experiment.queryTypes) {
      for (const concurrentClients of config.experiment.concurrentClients) {
        for (const cacheState of config.experiment.cacheStates) {
          treatments.push({
            apiType: 'REST',
            queryType,
            concurrentClients,
            cacheState
          });
          treatments.push({
            apiType: 'GraphQL',
            queryType,
            concurrentClients,
            cacheState
          });
        }
      }
    }
    
    // Randomize treatment order
    return this.shuffleArray(treatments);
  }

  shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }

  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async run() {
    console.log('Starting GraphQL vs REST experiment...');
    console.log(`Configuration: ${config.experiment.repetitions} repetitions per treatment`);
    
    const treatments = this.generateTreatments();
    console.log(`Total treatments to execute: ${treatments.length}`);
    
    for (let i = 0; i < treatments.length; i++) {
      const treatment = treatments[i];
      console.log(`\nProgress: ${i + 1}/${treatments.length}`);
      
      await this.runTreatment(
        treatment.apiType,
        treatment.queryType,
        treatment.concurrentClients,
        treatment.cacheState
      );
      
      // Stabilization interval between treatments
      if (i < treatments.length - 1) {
        console.log('Stabilization interval...');
        await this.sleep(30000); // 30 seconds
      }
    }
    
    const stats = this.dataCollector.getStats();
    console.log('\nExperiment completed!');
    console.log('Statistics:', stats);
    
    const filepath = await this.dataCollector.saveResults();
    console.log(`Results saved to: ${filepath}`);
  }
}

// Run experiment if this file is executed directly
if (require.main === module) {
  const experiment = new ExperimentRunner();
  experiment.run().catch(console.error);
}

module.exports = ExperimentRunner;