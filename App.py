import argparse
import socket
import sys
import threading
from datetime import datetime


def resolve_target(target: str) -> str:
    """Resolve hostname to IPv4 for consistent connect_ex behavior."""
    try:
        return socket.gethostbyname(target)
    except socket.OSError as exc:
        raise ValueError(f"Could not resolve target '{target}': {exc}") from exc


def scan_port(target_ip: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        if sock.connect_ex((target_ip, port)) == 0:
            print(f"[+] Port {port} is OPEN")
    except OSError:
        pass
    finally:
        sock.close()


def port_scanner(target: str, start_port: int = 1, end_port: int = 1024, max_threads: int = 200) -> None:
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        raise ValueError("Port range must be within 1-65535 and start <= end")

    target_ip = resolve_target(target)
    print(f"\nStarting scan on {target} ({target_ip}) at {datetime.now()}")
    print("-" * 50)

    threads: list[threading.Thread] = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target_ip, port), daemon=True)
        threads.append(thread)
        thread.start()

        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    print("-" * 50)
    print("Scan completed!")


def main() -> int:
    parser = argparse.ArgumentParser(description="Multithreaded TCP port scanner")
    parser.add_argument("target", nargs="?", help="Target IP or hostname")
    parser.add_argument("--start", type=int, default=1, help="First port (default: 1)")
    parser.add_argument("--end", type=int, default=500, help="Last port (default: 500)")
    args = parser.parse_args()

    target = (args.target or input("Enter target IP or domain: ")).strip()
    if not target:
        print("Error: target is required.", file=sys.stderr)
        return 1

    try:
        port_scanner(target, args.start, args.end)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())