import requests
import importlib.resources

def run():
    print("\n=== AnujScan | Directory Bruteforcer ===")
    url = input("Enter the base URL (e.g., http://example.com): ").strip()

    try:
        with importlib.resources.open_text("anujscan.data", "common.txt") as f:
            dirs = f.read().splitlines()
    except FileNotFoundError:
        print("[!] Wordlist not found.")
        return
    except Exception as e:
        print(f"[!] Failed to load wordlist: {e}")
        return

    print(f"\n[+] Bruteforcing directories on: {url}\n")

    if not url.endswith("/"):
        url += "/"

    for dir_name in dirs:
        target_url = url + dir_name
        try:
            response = requests.get(target_url, timeout=2)
            if response.status_code in [200, 301, 403]:
                print(f"[FOUND] {target_url} - Status: {response.status_code}")
        except requests.RequestException:
            pass
