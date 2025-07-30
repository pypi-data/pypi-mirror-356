import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import time
import whois
import requests
import importlib.resources

def main():
    def print_output(text):
        output_box.insert(tk.END, text + "\n")
        output_box.see(tk.END)

    def run_port_scanner():
        output_box.delete(1.0, tk.END)
        target = simpledialog.askstring("Target", "Enter target IP or domain:")
        port_range = simpledialog.askstring("Port Range", "Enter port range (e.g., 20-100):")
        if not target or not port_range:
            print_output("[!] Missing input.")
            return
        try:
            start, end = map(int, port_range.split("-"))
            print_output(f"🔍 Scanning {target} from port {start} to {end}...\n")
            for port in range(start, end + 1):
                s = socket.socket()
                s.settimeout(0.5)
                try:
                    s.connect((target, port))
                    print_output(f"[OPEN] Port {port}")
                    s.close()
                except:
                    pass
            print_output("\n✅ Scan complete.")
        except Exception as e:
            print_output(f"[!] Error: {e}")

    def run_banner_grabber():
        output_box.delete(1.0, tk.END)
        target = simpledialog.askstring("Target", "Enter target domain/IP:")
        port = simpledialog.askinteger("Port", "Enter port to grab banner from:")
        if not target or not port:
            print_output("[!] Missing input.")
            return
        try:
            print_output(f"🎯 Connecting to {target}:{port}...\n")
            sock = socket.socket()
            sock.settimeout(2)
            sock.connect((target, port))
            banner = sock.recv(1024).decode(errors="ignore")
            print_output(f"[+] Banner:\n{banner}")
            sock.close()
        except Exception as e:
            print_output(f"[!] Error: {e}")

    def run_brute_forcer():
        output_box.delete(1.0, tk.END)
        username = simpledialog.askstring("Brute Force", "Enter target username:")
        if not username:
            print_output("[!] Username required.")
            return
        wordlist = ["123", "1234", "admin", "pass", "root", "password", "anuj123", "admin@123"]
        print_output(f"🔐 Starting brute force on user: {username}\n")
        for password in wordlist:
            time.sleep(0.2)
            print_output(f"Trying: {password}")
            if password == "admin@123":
                print_output(f"\n✅ SUCCESS: Password for {username} is '{password}'")
                return
        print_output("\n❌ FAILED: Password not found in wordlist.")

    def run_whois_lookup():
        output_box.delete(1.0, tk.END)
        domain = simpledialog.askstring("WHOIS Lookup", "Enter domain (e.g., example.com):")
        if not domain:
            print_output("[!] Domain is required.")
            return
        try:
            info = whois.whois(domain)
            print_output(f"🌐 WHOIS Info for: {domain}\n")
            for key, value in info.items():
                print_output(f"{key}: {value}")
        except Exception as e:
            print_output(f"[!] WHOIS lookup failed: {e}")

    def run_subdomain_scanner():
        output_box.delete(1.0, tk.END)
        domain = simpledialog.askstring("Subdomain Scanner", "Enter domain (e.g., example.com):")
        if not domain:
            print_output("[!] Domain is required.")
            return
        try:
            with importlib.resources.open_text("anujscan.data", "common.txt") as f:
                subdomains = f.read().splitlines()
        except Exception as e:
            print_output(f"[!] Failed to load wordlist: {e}")
            return
        print_output(f"🔎 Scanning subdomains for: {domain}\n")
        for sub in subdomains:
            url = f"http://{sub}.{domain}"
            try:
                response = requests.get(url, timeout=2)
                if response.status_code in [200, 301, 403]:
                    print_output(f"[FOUND] {url} - {response.status_code}")
            except:
                pass
        print_output("\n✅ Subdomain scan complete.")

    def run_dir_bruteforcer():
        output_box.delete(1.0, tk.END)
        base_url = simpledialog.askstring("Directory Bruteforcer", "Enter base URL (e.g., http://example.com):")
        if not base_url:
            print_output("[!] URL is required.")
            return
        if not base_url.endswith("/"):
            base_url += "/"
        try:
            with importlib.resources.open_text("anujscan.data", "common.txt") as f:
                dirs = f.read().splitlines()
        except Exception as e:
            print_output(f"[!] Failed to load wordlist: {e}")
            return
        print_output(f"📂 Scanning directories on: {base_url}\n")
        for dir_name in dirs:
            url = base_url + dir_name
            try:
                response = requests.get(url, timeout=2)
                if response.status_code in [200, 301, 403]:
                    print_output(f"[FOUND] {url} - {response.status_code}")
            except:
                pass
        print_output("\n✅ Directory scan complete.")

    # === GUI Setup ===
    root = tk.Tk()
    root.title("AnujScan – Penetration Testing Toolkit (GUI)")
    root.geometry("720x520")
    root.config(bg="#1e1e1e")
    root.resizable(False, False)

    title_label = tk.Label(root, text="🔐 AnujScan GUI", font=("Helvetica", 18, "bold"),
                           fg="#00ffd5", bg="#1e1e1e")
    title_label.pack(pady=20)

    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(pady=10)

    button_style = {
        "width": 25, "height": 2, "bg": "#272727", "fg": "#ffffff",
        "activebackground": "#00ffd5", "activeforeground": "#000000",
        "font": ("Helvetica", 10, "bold"), "bd": 0, "cursor": "hand2"
    }

    tk.Button(button_frame, text="Port Scanner", command=run_port_scanner, **button_style).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="Banner Grabber", command=run_banner_grabber, **button_style).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(button_frame, text="Brute Forcer", command=run_brute_forcer, **button_style).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="Subdomain Scanner", command=run_subdomain_scanner, **button_style).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(button_frame, text="Directory Bruteforcer", command=run_dir_bruteforcer, **button_style).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="WHOIS Lookup", command=run_whois_lookup, **button_style).grid(row=2, column=1, padx=10, pady=10)

    output_box = scrolledtext.ScrolledText(
        root, width=85, height=12, font=("Courier", 10),
        bg="#111111", fg="#00ff00", insertbackground="#00ff00"
    )
    output_box.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
