import requests
import time
import json
import asyncio
import aiohttp
from config import Config

class RestClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {Config.GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GraphQL-vs-REST-Experiment'
        })
        self.base_url = Config.REST_BASE_URL
    
    def make_request(self, url):
        start_time = time.time()
        try:
            response = self.session.get(
                f"{self.base_url}{url}",
                timeout=Config.TIMEOUT
            )
            end_time = time.time()
            
            response_time = int((end_time - start_time) * 1000)  # ms
            payload_size = len(response.text.encode('utf-8'))
            
            return {
                'response_time': response_time,
                'payload_size': payload_size,
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'data': response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            end_time = time.time()
            return {
                'response_time': int((end_time - start_time) * 1000),
                'payload_size': 0,
                'status_code': 0,
                'success': False,
                'error': str(e)
            }
    
    def make_aggregated_request(self, urls):
        start_time = time.time()
        try:
            responses = []
            for url in urls:
                response = self.session.get(
                    f"{self.base_url}{url}",
                    timeout=Config.TIMEOUT
                )
                if response.status_code == 200:
                    responses.append(response.json())
                else:
                    raise Exception(f"Request failed with status {response.status_code}")
            
            end_time = time.time()
            combined_data = json.dumps(responses)
            
            return {
                'response_time': int((end_time - start_time) * 1000),
                'payload_size': len(combined_data.encode('utf-8')),
                'status_code': 200,
                'success': True,
                'data': responses
            }
        except Exception as e:
            end_time = time.time()
            return {
                'response_time': int((end_time - start_time) * 1000),
                'payload_size': 0,
                'status_code': 0,
                'success': False,
                'error': str(e)
            }

class GraphQLClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {Config.GITHUB_TOKEN}',
            'Content-Type': 'application/json',
            'User-Agent': 'GraphQL-vs-REST-Experiment'
        })
        self.url = Config.GRAPHQL_URL
    
    def make_request(self, query):
        start_time = time.time()
        try:
            payload = {'query': query}
            response = self.session.post(
                self.url,
                json=payload,
                timeout=Config.TIMEOUT
            )
            end_time = time.time()
            
            response_time = int((end_time - start_time) * 1000)  # ms
            payload_size = len(response.text.encode('utf-8'))
            
            return {
                'response_time': response_time,
                'payload_size': payload_size,
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'data': response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            end_time = time.time()
            return {
                'response_time': int((end_time - start_time) * 1000),
                'payload_size': 0,
                'status_code': 0,
                'success': False,
                'error': str(e)
            }