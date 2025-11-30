import time
import random
import asyncio
from concurrent.futures import ThreadPoolExecutor
from clients import RestClient, GraphQLClient
from queries import REST_QUERIES, GRAPHQL_QUERIES
from data_collector import DataCollector
from config import Config

class ExperimentRunner:
    def __init__(self):
        self.rest_client = RestClient()
        self.graphql_client = GraphQLClient()
        self.data_collector = DataCollector()
    
    def run_warmup(self, api_type, query_type):
        print(f"Running warmup for {api_type} - {query_type}...")
        
        for i in range(Config.WARMUP_REQUESTS):
            if api_type == 'REST':
                self._execute_rest_query(query_type)
            else:
                self._execute_graphql_query(query_type)
            time.sleep(Config.REQUEST_INTERVAL)
    
    def _execute_rest_query(self, query_type):
        query = REST_QUERIES[query_type]
        
        if query_type == 'aggregated':
            return self.rest_client.make_aggregated_request(query['urls'])
        else:
            return self.rest_client.make_request(query['url'])
    
    def _execute_graphql_query(self, query_type):
        query = GRAPHQL_QUERIES[query_type]
        return self.graphql_client.make_request(query)
    
    def run_treatment(self, api_type, query_type, concurrent_clients, cache_state):
        print(f"Running treatment: {api_type} - {query_type} - {concurrent_clients} clients - {cache_state} cache")
        
        # Warmup if cache is warm
        if cache_state == 'warm':
            self.run_warmup(api_type, query_type)
        
        # Run concurrent measurements
        with ThreadPoolExecutor(max_workers=concurrent_clients) as executor:
            futures = []
            for client in range(concurrent_clients):
                future = executor.submit(
                    self._run_client_measurements,
                    api_type, query_type, concurrent_clients, cache_state
                )
                futures.append(future)
            
            # Wait for all clients to complete
            for future in futures:
                future.result()
    
    def _run_client_measurements(self, api_type, query_type, concurrent_clients, cache_state):
        for rep in range(Config.REPETITIONS):
            if api_type == 'REST':
                result = self._execute_rest_query(query_type)
            else:
                result = self._execute_graphql_query(query_type)
            
            self.data_collector.add_result(
                api_type, query_type, concurrent_clients, cache_state, result
            )
            
            if rep < Config.REPETITIONS - 1:
                time.sleep(Config.REQUEST_INTERVAL)
    
    def _generate_treatments(self):
        treatments = []
        
        for query_type in Config.QUERY_TYPES:
            for concurrent_clients in Config.CONCURRENT_CLIENTS:
                for cache_state in Config.CACHE_STATES:
                    treatments.append({
                        'api_type': 'REST',
                        'query_type': query_type,
                        'concurrent_clients': concurrent_clients,
                        'cache_state': cache_state
                    })
                    treatments.append({
                        'api_type': 'GraphQL',
                        'query_type': query_type,
                        'concurrent_clients': concurrent_clients,
                        'cache_state': cache_state
                    })
        
        # Randomize treatment order
        random.shuffle(treatments)
        return treatments
    
    def run(self):
        print('Starting GraphQL vs REST experiment...')
        print(f'Configuration: {Config.REPETITIONS} repetitions per treatment')
        
        treatments = self._generate_treatments()
        print(f'Total treatments to execute: {len(treatments)}')
        
        for i, treatment in enumerate(treatments):
            print(f'\nProgress: {i + 1}/{len(treatments)}')
            
            self.run_treatment(
                treatment['api_type'],
                treatment['query_type'],
                treatment['concurrent_clients'],
                treatment['cache_state']
            )
            
            # Stabilization interval between treatments
            if i < len(treatments) - 1:
                print('Stabilization interval...')
                time.sleep(30)  # 30 seconds
        
        stats = self.data_collector.get_stats()
        print('\nExperiment completed!')
        print('Statistics:', stats)
        
        filepath = self.data_collector.save_results()
        print(f'Results saved to: {filepath}')

if __name__ == '__main__':
    experiment = ExperimentRunner()
    experiment.run()