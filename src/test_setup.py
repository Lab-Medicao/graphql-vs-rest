from clients import RestClient, GraphQLClient
from queries import REST_QUERIES, GRAPHQL_QUERIES
from config import Config

def test_setup():
    print('Testing experimental setup...\n')
    
    # Check GitHub token
    if not Config.GITHUB_TOKEN:
        print('❌ GitHub token not found. Please set GITHUB_TOKEN in .env file')
        return False
    print('✅ GitHub token configured')
    
    # Test REST client
    print('\nTesting REST API...')
    rest_client = RestClient()
    
    try:
        result = rest_client.make_request(REST_QUERIES['simple']['url'])
        if result['success']:
            print('✅ REST API connection successful')
            print(f'   Response time: {result["response_time"]}ms')
            print(f'   Payload size: {result["payload_size"]} bytes')
        else:
            print('❌ REST API test failed:', result.get('error', 'Unknown error'))
            return False
    except Exception as e:
        print('❌ REST API test failed:', str(e))
        return False
    
    # Test GraphQL client
    print('\nTesting GraphQL API...')
    graphql_client = GraphQLClient()
    
    try:
        result = graphql_client.make_request(GRAPHQL_QUERIES['simple'])
        if result['success']:
            print('✅ GraphQL API connection successful')
            print(f'   Response time: {result["response_time"]}ms')
            print(f'   Payload size: {result["payload_size"]} bytes')
        else:
            print('❌ GraphQL API test failed:', result.get('error', 'Unknown error'))
            return False
    except Exception as e:
        print('❌ GraphQL API test failed:', str(e))
        return False
    
    # Test all query types
    print('\nTesting all query types...')
    
    for query_type in ['simple', 'nested', 'aggregated']:
        print(f'\nTesting {query_type} queries:')
        
        # Test REST
        try:
            if query_type == 'aggregated':
                rest_result = rest_client.make_aggregated_request(REST_QUERIES[query_type]['urls'])
            else:
                rest_result = rest_client.make_request(REST_QUERIES[query_type]['url'])
            
            if rest_result['success']:
                print(f'✅ REST {query_type}: {rest_result["response_time"]}ms, {rest_result["payload_size"]} bytes')
            else:
                print(f'❌ REST {query_type} failed:', rest_result.get('error', 'Unknown error'))
        except Exception as e:
            print(f'❌ REST {query_type} failed:', str(e))
        
        # Test GraphQL
        try:
            graphql_result = graphql_client.make_request(GRAPHQL_QUERIES[query_type])
            
            if graphql_result['success']:
                print(f'✅ GraphQL {query_type}: {graphql_result["response_time"]}ms, {graphql_result["payload_size"]} bytes')
            else:
                print(f'❌ GraphQL {query_type} failed:', graphql_result.get('error', 'Unknown error'))
        except Exception as e:
            print(f'❌ GraphQL {query_type} failed:', str(e))
    
    print('\n✅ Setup test completed successfully!')
    print('\nYou can now run the full experiment with: python src/experiment.py')
    
    return True

if __name__ == '__main__':
    test_setup()