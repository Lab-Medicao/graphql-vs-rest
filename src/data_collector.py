import csv
import os
from datetime import datetime
from config import Config

class DataCollector:
    def __init__(self):
        self.results = []
        self.filename = self._generate_filename()
        self._ensure_results_dir()
    
    def _generate_filename(self):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return f'experiment_{timestamp}.csv'
    
    def _ensure_results_dir(self):
        os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    def add_result(self, api_type, query_type, concurrent_clients, cache_state, result):
        record = {
            'timestamp': datetime.now().isoformat(),
            'api_type': api_type,
            'query_type': query_type,
            'concurrent_clients': concurrent_clients,
            'cache_state': cache_state,
            'response_time_ms': result['response_time'],
            'payload_size_bytes': result['payload_size'],
            'status_code': result['status_code']
        }
        self.results.append(record)
    
    def save_results(self):
        filepath = os.path.join(Config.RESULTS_DIR, self.filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Config.CSV_HEADERS)
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"Results saved to: {filepath}")
        return filepath
    
    def get_stats(self):
        if not self.results:
            return {}
        
        successful = [r for r in self.results if r['status_code'] == 200]
        failed = [r for r in self.results if r['status_code'] != 200]
        
        avg_response_time = sum(r['response_time_ms'] for r in self.results) / len(self.results)
        avg_payload_size = sum(r['payload_size_bytes'] for r in self.results) / len(self.results)
        
        return {
            'total_measurements': len(self.results),
            'successful_requests': len(successful),
            'failed_requests': len(failed),
            'success_rate': len(successful) / len(self.results) * 100,
            'avg_response_time_ms': round(avg_response_time, 2),
            'avg_payload_size_bytes': round(avg_payload_size, 2)
        }