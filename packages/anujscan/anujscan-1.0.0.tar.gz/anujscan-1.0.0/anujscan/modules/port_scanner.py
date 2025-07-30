import socket

def run():
    print("\n=== AnujScan | Port Scanner ===")
    target = input("Enter target IP or domain (e.g., scanme.nmap.org): ").strip()
    port_range = input("Enter port range (e.g., 20-100): ").strip()

    try:
        start_port, end_port = map(int, port_range.split('-'))
    except:
        print("[!] Invalid port range format. Use like 20-100.")
        return

    print(f"\n[+] Scanning {target} from port {start_port} to {end_port}...\n")

    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((target, port))
            print(f"[OPEN] Port {port}")
            sock.close()
        except:
            pass

    print("\n[✓] Scan completed.")
