import socket
import threading
from datetime import datetime

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
        sock.close()
    except:
        pass

def port_scanner(target, start_port=1, end_port=1024):
    print(f"\nStarting scan on {target} at {datetime.now()}")
    print("-" * 50)
    
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port))
        threads.append(thread)
        thread.start()
        
        # Limit threads to avoid crashing
        if len(threads) >= 200:
            for t in threads:
                t.join()
            threads = []
    
    for t in threads:
        t.join()
    
    print("-" * 50)
    print("Scan completed!")

# Usage
if __name__ == "__main__":
    target = input("Enter target IP or domain: ").strip()
    port_scanner(target, 1, 500)  # You can change range