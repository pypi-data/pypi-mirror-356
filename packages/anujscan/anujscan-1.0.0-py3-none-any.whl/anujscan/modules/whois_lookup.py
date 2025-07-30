import whois

def run():
    print("\n=== AnujScan | WHOIS Lookup ===")
    domain = input("Enter a domain (e.g., example.com): ").strip()

    try:
        info = whois.whois(domain)
        print("\n[+] WHOIS Information:\n")
        for key, value in info.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"[!] WHOIS lookup failed: {e}")
