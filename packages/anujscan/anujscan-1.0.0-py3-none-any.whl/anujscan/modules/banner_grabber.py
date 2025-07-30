import socket

def run():
    print("\n=== AnujScan | Banner Grabber ===")
    target = input("Enter target IP or domain: ").strip()
    port = input("Enter port to grab banner from (e.g., 21, 22, 80): ").strip()

    try:
        port = int(port)
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((target, port))
        banner = sock.recv(1024).decode(errors="ignore")
        print(f"\n[+] Banner from {target}:{port}:\n{banner}")
        sock.close()
    except Exception as e:
        print(f"[!] Could not grab banner: {e}")
