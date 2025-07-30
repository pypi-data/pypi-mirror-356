def check_login(username, password):
    # Simulated login check
    correct_username = "admin"
    correct_password = "1234"
    return username == correct_username and password == correct_password

def run():
    print("\n=== AnujScan | Web Login Brute Forcer (Simulated) ===")
    username = input("Enter target username: ").strip()

    wordlist = ["admin", "root", "pass123", "123", "1234", "password", "letmein"]

    for pwd in wordlist:
        print(f"[*] Trying: {pwd}")
        if check_login(username, pwd):
            print(f"[+] SUCCESS! Password for '{username}' is: {pwd}")
            return
    print("[-] Failed: No matching password found in wordlist.")
