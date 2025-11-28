const { RestClient, GraphQLClientWrapper } = require('./clients');
const { restQueries, graphqlQueries } = require('./queries');
const config = require('./config');

async function testSetup() {
  console.log('Testing experimental setup...\n');
  
  // Check GitHub token
  if (!config.github.token) {
    console.error('❌ GitHub token not found. Please set GITHUB_TOKEN in .env file');
    return false;
  }
  console.log('✅ GitHub token configured');
  
  // Test REST client
  console.log('\nTesting REST API...');
  const restClient = new RestClient();
  
  try {
    const result = await restClient.makeRequest(restQueries.simple.url);
    if (result.success) {
      console.log('✅ REST API connection successful');
      console.log(`   Response time: ${result.responseTime}ms`);
      console.log(`   Payload size: ${result.payloadSize} bytes`);
    } else {
      console.log('❌ REST API test failed:', result.error);
      return false;
    }
  } catch (error) {
    console.log('❌ REST API test failed:', error.message);
    return false;
  }
  
  // Test GraphQL client
  console.log('\nTesting GraphQL API...');
  const graphqlClient = new GraphQLClientWrapper();
  
  try {
    const result = await graphqlClient.makeRequest(graphqlQueries.simple);
    if (result.success) {
      console.log('✅ GraphQL API connection successful');
      console.log(`   Response time: ${result.responseTime}ms`);
      console.log(`   Payload size: ${result.payloadSize} bytes`);
    } else {
      console.log('❌ GraphQL API test failed:', result.error);
      return false;
    }
  } catch (error) {
    console.log('❌ GraphQL API test failed:', error.message);
    return false;
  }
  
  // Test all query types
  console.log('\nTesting all query types...');
  
  for (const queryType of ['simple', 'nested', 'aggregated']) {
    console.log(`\nTesting ${queryType} queries:`);
    
    // Test REST
    try {
      let restResult;
      if (queryType === 'aggregated') {
        restResult = await restClient.makeAggregatedRequest(restQueries[queryType].urls);
      } else {
        restResult = await restClient.makeRequest(restQueries[queryType].url);
      }
      
      if (restResult.success) {
        console.log(`✅ REST ${queryType}: ${restResult.responseTime}ms, ${restResult.payloadSize} bytes`);
      } else {
        console.log(`❌ REST ${queryType} failed:`, restResult.error);
      }
    } catch (error) {
      console.log(`❌ REST ${queryType} failed:`, error.message);
    }
    
    // Test GraphQL
    try {
      const graphqlResult = await graphqlClient.makeRequest(graphqlQueries[queryType]);
      
      if (graphqlResult.success) {
        console.log(`✅ GraphQL ${queryType}: ${graphqlResult.responseTime}ms, ${graphqlResult.payloadSize} bytes`);
      } else {
        console.log(`❌ GraphQL ${queryType} failed:`, graphqlResult.error);
      }
    } catch (error) {
      console.log(`❌ GraphQL ${queryType} failed:`, error.message);
    }
  }
  
  console.log('\n✅ Setup test completed successfully!');
  console.log('\nYou can now run the full experiment with: npm start');
  
  return true;
}

if (require.main === module) {
  testSetup().catch(console.error);
}

module.exports = testSetup;