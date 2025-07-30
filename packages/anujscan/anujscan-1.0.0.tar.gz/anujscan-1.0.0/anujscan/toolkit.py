from anujscan.modules import (
    port_scanner,
    banner_grabber,
    brute_forcer,
    subdomain_scanner,
    dir_bruteforce,
    whois_lookup
)


def main():
    while True:
        print("\n=== AnujScan: Penetration Testing Toolkit ===")
        print("1. Port Scanner")
        print("2. Banner Grabber")
        print("3. Web Login Brute Forcer")
        print("4. Subdomain Scanner")
        print("5. Directory Bruteforcer")
        print("6. WHOIS Lookup")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            port_scanner.run()
        elif choice == '2':
            banner_grabber.run()
        elif choice == '3':
            brute_forcer.run()
        elif choice == '4':
            subdomain_scanner.run()
        elif choice == '5':
            dir_bruteforce.run()
        elif choice == '6':
            whois_lookup.run()
        elif choice == '7':
            print("Exiting AnujScan. Hack the world ethically 🔐")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
