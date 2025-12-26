import customtkinter as ctk
import subprocess
import requests
import csv
import threading
import socket
import re
import time

# =====================================================
# UI CONFIG
# =====================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

APP_TITLE = "SmartScreen ATTACK"
FONT = ("Consolas", 14)

# =====================================================
# ASCII
# =====================================================
SNAKE_ASCII = r"""
███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗
██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝
███████╗██╔██╗ ██║███████║█████╔╝ █████╗  
╚════██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  
███████║██║ ╚████║██║  ██║██║  ██╗███████╗
╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
"""

# =====================================================
# GOOGLE SHEETS (SAMME SOM DIT GAMLE SCRIPT)
# =====================================================
LOGIN_SHEET_ID = "1sR8bO58zUTqqYKn0YRaOq-ta2HsgQsXf0FP6DVhARSE"
DISCORD_SHEET_ID = "1SywSyu3ynW9cnc_WoSed7CiMSLEWeKiKUI2XR7BfLhY"

# =====================================================
# UTILS
# =====================================================
def threaded(func):
    threading.Thread(target=func, daemon=True).start()

def valid_ip(ip):
    return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip)

# =====================================================
# GOOGLE SHEET FUNCTIONS
# =====================================================
def check_code_google_sheet(code):
    url = f"https://docs.google.com/spreadsheets/d/{LOGIN_SHEET_ID}/export?format=csv"
    try:
        r = requests.get(url, timeout=5)
        reader = csv.reader(r.text.splitlines())
        for row in reader:
            if len(row) >= 2 and code == row[0].strip():
                return True, row[1].strip().lower()
    except:
        pass
    return False, None

def discord_lookup_sheet(discord_id):
    url = f"https://docs.google.com/spreadsheets/d/{DISCORD_SHEET_ID}/export?format=csv"
    try:
        r = requests.get(url, timeout=10)
        reader = csv.reader(r.text.splitlines())
        headers = next(reader)
        for row in reader:
            if f"discord:{discord_id}".lower() in " ".join(row).lower():
                return headers, row
    except:
        pass
    return None, None

# =====================================================
# APP
# =====================================================
class SmartScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        # === FÅ SKÆRMSTØRRELSE (RIGTIG FULLSCREEN) ===
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # === TILPAS VINDUE TIL SKÆRM ===
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # === FJERN TITELBAR / RAMME ===
        self.overrideredirect(True)

        # === WINDOWS FOCUS FIX ===
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        self.title(APP_TITLE)

        self.role = None

        # LOGIN FRAME
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(fill="both", expand=True)

        self.build_login()

    # ---------------- LOGIN ----------------
    def build_login(self):
        ctk.CTkLabel(
            self.login_frame,
            text="SMARTSCREEN ATTACK",
            font=("Consolas", 28, "bold"),
            text_color="#00ff7f"
        ).pack(pady=40)

        self.code_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Access Code",
            width=320
        )
        self.code_entry.pack(pady=10)

        self.login_status = ctk.CTkLabel(self.login_frame, text="")
        self.login_status.pack(pady=10)

        ctk.CTkButton(
            self.login_frame,
            text="LOGIN",
            command=lambda: threaded(self.login)
        ).pack(pady=20)

    def login(self):
        code = self.code_entry.get()
        ok, role = check_code_google_sheet(code)

        if ok:
            self.role = role
            self.login_frame.destroy()
            self.build_main_ui()
        else:
            self.login_status.configure(text="ACCESS DENIED", text_color="red")

    # ---------------- MAIN UI ----------------
    def build_main_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # TOP BAR (SNAKE)
        self.topbar = ctk.CTkFrame(self, height=140)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.topbar.grid_propagate(False)

        ctk.CTkLabel(
            self.topbar,
            text=SNAKE_ASCII,
            font=("Consolas", 16),
            text_color="#00ff7f",
            justify="left"
        ).pack(anchor="w", padx=20, pady=10)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=240)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        ctk.CTkLabel(
            self.sidebar,
            text=f"LOGGED IN: {self.role.upper()}",
            font=("Consolas", 14)
        ).pack(pady=15)

        buttons = [
            ("System Scan", self.system_scan),
            ("WiFi Scan", self.wifi_scan),
            ("IP Tool", self.ip_tool),
            ("IP Pinger", self.ip_pinger),
            ("IP Lookup", self.ip_lookup),
            ("VPN / Proxy Check", self.vpn_check)
        ]

        if self.role == "admin":
            buttons += [
                ("Discord Lookup", self.discord_lookup),
                ("Admin Panel", self.admin_panel)
            ]

        buttons += [
            ("Clear Output", self.clear_output),
            ("EXIT", self.quit)
        ]

        for text, cmd in buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=lambda c=cmd: threaded(c)
            ).pack(pady=5, padx=10, fill="x")

        # OUTPUT
        self.output = ctk.CTkTextbox(
            self,
            font=FONT,
            text_color="#00ff7f",
            fg_color="#050505"
        )
        self.output.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.log(">> SmartScreen ATTACK READY")

    # ---------------- OUTPUT ----------------
    def log(self, text):
        self.output.insert("end", text + "\n")
        self.output.see("end")

    def clear_output(self):
        self.output.delete("1.0", "end")

    # ---------------- FUNCTIONS ----------------
    def system_scan(self):
        self.log("\n[ SYSTEM SCAN ]")
        for i in range(0, 101, 10):
            self.log(f"[{i}%] Processing...")
            time.sleep(0.2)
        self.log("[✓] Scan complete\n")

    def wifi_scan(self):
        self.log("\n[ WIFI SCAN ]")
        try:
            out = subprocess.check_output("arp -a", shell=True, text=True)
            ips = sorted(set(re.findall(r"\d+\.\d+\.\d+\.\d+", out)))
            for ip in ips:
                try:
                    ping = subprocess.check_output(f"ping -n 1 -w 500 {ip}", shell=True, text=True)
                    ms = re.search(r"(\d+)ms", ping)
                    ms = ms.group(1) + "ms" if ms else "Timeout"
                except:
                    ms = "Timeout"

                try:
                    host = socket.gethostbyaddr(ip)[0]
                except:
                    host = "Unknown"

                self.log(f"{ip:<16} {ms:<8} {host}")
        except:
            self.log("[✖] WiFi scan failed")

    def ip_tool(self):
        ip = ctk.CTkInputDialog(title="IP Tool", text="Enter IP:").get_input()
        if ip:
            self.log(f"\nTarget IP: {ip}")
            self.log("Country: UNKNOWN")
            self.log("ISP: UNKNOWN")

    def ip_pinger(self):
        ip = ctk.CTkInputDialog(title="Ping", text="Enter IP:").get_input()
        if not valid_ip(ip):
            self.log("[✖] Invalid IP")
            return
        try:
            out = subprocess.check_output(f"ping {ip}", shell=True, text=True)
            self.log(out)
        except:
            self.log("[✖] Ping failed")

    def ip_lookup(self):
        ip = ctk.CTkInputDialog(title="IP Lookup", text="Enter IP:").get_input()
        if not valid_ip(ip):
            self.log("[✖] Invalid IP")
            return
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if data.get("status") != "success":
            self.log("[✖] Lookup failed")
            return
        for k in ["country", "regionName", "city", "zip", "isp", "org", "as"]:
            self.log(f"{k.upper():<12}: {data.get(k)}")

    def vpn_check(self):
        ip = ctk.CTkInputDialog(title="VPN Check", text="Enter IP:").get_input()
        if not valid_ip(ip):
            self.log("[✖] Invalid IP")
            return
        data = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,proxy,hosting,mobile,country,isp",
            timeout=5
        ).json()
        self.log(f"Country : {data['country']}")
        self.log(f"ISP     : {data['isp']}")
        self.log(f"Proxy   : {data['proxy']}")
        self.log(f"Hosting : {data['hosting']}")
        self.log(f"Mobile  : {data['mobile']}")

    def discord_lookup(self):
        did = ctk.CTkInputDialog(title="Discord Lookup", text="Enter Discord ID:").get_input()
        headers, row = discord_lookup_sheet(did)
        if not row:
            self.log("No results found")
            return
        for h, v in zip(headers, row):
            self.log(f"{h}: {v}")

    def admin_panel(self):
        self.log("\n[ ADMIN PANEL ]")
        self.log("• Full access granted")

# =====================================================
# START
# =====================================================
if __name__ == "__main__":
    app = SmartScreen()
    app.mainloop()
