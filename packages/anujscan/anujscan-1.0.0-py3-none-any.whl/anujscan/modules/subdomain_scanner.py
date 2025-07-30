import requests
import importlib.resources

def run():
    print("\n=== AnujScan | Subdomain Scanner ===")
    domain = input("Enter the target domain (e.g., example.com): ").strip()

    try:
        with importlib.resources.open_text("anujscan.data", "common.txt") as f:
            subdomains = f.read().splitlines()
    except FileNotFoundError:
        print("[!] Wordlist not found.")
        return
    except Exception as e:
        print(f"[!] Failed to load wordlist: {e}")
        return

    print(f"\n[+] Scanning subdomains for: {domain}\n")

    for sub in subdomains:
        url = f"http://{sub}.{domain}"
        try:
            response = requests.get(url, timeout=2)
            print(f"[FOUND] {url} - Status: {response.status_code}")
        except requests.ConnectionError:
            pass
        except Exception as e:
            print(f"[!] Error checking {url}: {e}")
