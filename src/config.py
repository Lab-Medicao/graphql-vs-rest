import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    REST_BASE_URL = 'https://api.github.com'
    GRAPHQL_URL = 'https://api.github.com/graphql'
    
    # Experiment settings
    REPETITIONS = 50
    WARMUP_REQUESTS = 15
    REQUEST_INTERVAL = 0.1  # seconds
    TIMEOUT = 30  # seconds
    CONCURRENT_CLIENTS = [1, 10, 50]
    QUERY_TYPES = ['simple', 'nested', 'aggregated']
    CACHE_STATES = ['cold', 'warm']
    
    # Output settings
    RESULTS_DIR = './results'
    CSV_HEADERS = [
        'timestamp', 'api_type', 'query_type', 'concurrent_clients', 
        'cache_state', 'response_time_ms', 'payload_size_bytes', 'status_code'
    ]