import requests
import time
import random

URL = "http://localhost:8000/api/products/"
TOTAL_REQUESTS = 10000   
BATCHES = 10             
PAUSE = 10              

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def run_batch(batch_num, requests_per_batch):
    print(f"\n=== Iniciando batch {batch_num} ({requests_per_batch} requisições) ===")
    for i in range(requests_per_batch):
        headers = {"X-Forwarded-For": random_ip()}
        try:
            r = requests.get(URL, headers=headers, timeout=5)
            print(f"[Batch {batch_num}] Request {i+1}/{requests_per_batch} → {r.status_code}")
        except requests.RequestException as e:
            print(f"[Batch {batch_num}] Erro na requisição {i+1}: {e}")
        time.sleep(0.01) 

def main():
    requests_per_batch = TOTAL_REQUESTS // BATCHES
    for b in range(1, BATCHES+1):
        run_batch(b, requests_per_batch)
        if b < BATCHES:
            print(f"⏸ Pausando {PAUSE}s antes do próximo batch...")
            time.sleep(PAUSE)

if __name__ == "__main__":
    main()
