import requests
import time
import random

URL = "http://localhost:8000/api/products/"  
TOTAL_REQUESTS = 4000
BATCH_SIZE = 5000          
PAUSE_BETWEEN_BATCHES = 15 
SMALL_JITTER = (0.001, 0.01)  
MAX_RETRIES_429 = 3
RETRY_SLEEP_429 = 10      
PROGRESS_EVERY = 1000      

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def send_request(session, attempt_index):
    """Envia uma única requisição com tentativa de retry para 429."""
    retries = 0
    while True:
        try:
            headers = {"X-Forwarded-For": random_ip(), "Accept": "application/json"}
            r = session.get(URL, headers=headers, timeout=10)
            status = r.status_code
            return status, r
        except requests.RequestException as e:
            return None, e

def main():
    session = requests.Session()
    counts = {"total": 0, "2xx": 0, "4xx": 0, "5xx": 0, "429": 0, "errors": 0}
    start_all = time.time()

    batches = TOTAL_REQUESTS // BATCH_SIZE
    remainder = TOTAL_REQUESTS % BATCH_SIZE
    if remainder:
        batches += 1

    sent = 0
    for b in range(batches):
        to_send = BATCH_SIZE if (b < batches - 1 or remainder == 0) else remainder
        if to_send == 0:
            break

        print(f"\n=== Batch {b+1}/{batches}: enviando {to_send} requests ===")
        start_batch = time.time()

        for i in range(to_send):
            global_index = sent + 1
            retries_429 = 0
            while True:
                status, resp = send_request(session, global_index)
                counts["total"] += 1
                if status is None:
                    counts["errors"] += 1
                    print(f"[{global_index}/{TOTAL_REQUESTS}] Erro de conexão: {resp}")
                    break

                if status == 429:
                    counts["429"] += 1
                    retries_429 += 1
                    if retries_429 <= MAX_RETRIES_429:
                        print(f"[{global_index}/{TOTAL_REQUESTS}] 429 recebido — retry {retries_429}/{MAX_RETRIES_429} (dormir {RETRY_SLEEP_429}s)")
                        time.sleep(RETRY_SLEEP_429)
                        continue
                    else:
                        break

                if 200 <= status < 300:
                    counts["2xx"] += 1
                elif 400 <= status < 500:
                    counts["4xx"] += 1
                elif 500 <= status < 600:
                    counts["5xx"] += 1
                break

            sent += 1

            time.sleep(random.uniform(*SMALL_JITTER))

            if global_index % PROGRESS_EVERY == 0 or global_index == TOTAL_REQUESTS:
                elapsed = time.time() - start_all
                print(f"[{global_index}/{TOTAL_REQUESTS}] elapsed={elapsed:.1f}s 2xx={counts['2xx']} 4xx={counts['4xx']} 5xx={counts['5xx']} 429={counts['429']} errors={counts['errors']}")

        end_batch = time.time()
        print(f"=== Batch {b+1} finalizado em {end_batch - start_batch:.1f}s ===")

        if sent < TOTAL_REQUESTS:
            print(f"Dormindo {PAUSE_BETWEEN_BATCHES}s antes do próximo batch...\n")
            time.sleep(PAUSE_BETWEEN_BATCHES)

    total_time = time.time() - start_all
    print("\n--- Summary ---")
    print(f"Total requests attempted: {counts['total']}")
    print(f"2xx: {counts['2xx']}, 4xx: {counts['4xx']}, 5xx: {counts['5xx']}, 429: {counts['429']}, errors: {counts['errors']}")
    print(f"Total time: {total_time:.1f}s, avg req/sec: {counts['total'] / total_time:.2f}")

if __name__ == "__main__":
    main()
