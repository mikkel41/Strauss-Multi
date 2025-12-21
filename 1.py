# =========================
# Imports
# =========================
import turtle
import time
import os
import requests
import csv
import subprocess
import socket
import re

# =========================
# Console title
# =========================
def set_console_title(title):
    if os.name == "nt":
        os.system(f'title "{title}"')

# =========================
# Turtle intro animation
# =========================
def intro_animation():
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.setup(width=1.0, height=1.0)
    screen.title("SmartScreen ATTACK")

    w = screen.window_width()
    h = screen.window_height()

    t = turtle.Turtle()
    t.color("purple")
    t.speed(0)
    t.width(3)
    t.hideturtle()

    a = 0
    b = 0
    scale = min(w, h) / 800

    t.penup()
    t.goto(0, h // 2 - 120)
    t.pendown()

    turtle.tracer(0)

    while b < 220:
        t.forward(a * scale)
        t.right(b)
        a += 3
        b += 1
        turtle.update()
        time.sleep(0.01)

    time.sleep(0.5)
    screen.bye()
    time.sleep(0.3)

# =========================
# Utils
# =========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

PURPLE = "\033[35m"
RESET = "\033[0m"

def p(text=""):
    print(PURPLE + text + RESET)

ASCII_HEADER = r"""
  _________ __                                         _____   __    __                 __    
 /   _____//  |_____________   __ __  ______ ______   /  _  \_/  |__/  |______    ____ |  | __
 \_____  \\   __\_  __ \__  \ |  |  \/  ___//  ___/  /  /_\  \   __\   __\__  \ _/ ___\|  |/ /
 /        \|  |  |  | \// __ \|  |  /\___ \ \___ \  /    |    \  |  |  |  / __ \\  \___|    <
/_______  /|__|  |__|  (____  /____//____  >____  > \____|__  /__|  |__| (____  /\___  >__|_ \
        \/                  \/           \/     \/          \/                \/     \/      
"""

# =========================
# Google Sheet: login check
# =========================
def check_code_google_sheet(user_code):
    SHEET_ID = "1sR8bO58zUTqqYKn0YRaOq-ta2HsgQsXf0FP6DVhARSE"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        reader = csv.reader(response.text.splitlines())
        for row in reader:
            if len(row) >= 2:
                if user_code == row[0].strip():
                    return True, row[1].strip().lower()

        return False, None
    except:
        return False, None

# =========================
# Google Sheet: Discord DB
# =========================
def search_discord_id_in_sheet(discord_id):
    SHEET_ID = "1SywSyu3ynW9cnc_WoSed7CiMSLEWeKiKUI2XR7BfLhY"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        reader = csv.reader(response.text.splitlines())
        headers = next(reader)

        search_value = f"discord:{discord_id}".lower()

        for row in reader:
            if search_value in " ".join(row).lower():
                return headers, row  # ← første match

        return None, None
    except:
        return None, None

# =========================
# WiFi scan
# =========================
def wifi_scan():
    clear()
    p("Scanning WiFi devices...\n")
    time.sleep(1)

    try:
        output = subprocess.check_output("arp -a", shell=True, text=True)
        ips = sorted(set(re.findall(r"\d+\.\d+\.\d+\.\d+", output)))
    except:
        p("Failed to scan network.")
        input("\nPress Enter...")
        return

    p(f"{'IP':<18} {'Ping':<10} Device")
    p("-" * 60)

    for ip in ips:
        try:
            ping_out = subprocess.check_output(f"ping -n 1 -w 500 {ip}", shell=True, text=True)
            ping = re.search(r"(\d+)ms", ping_out)
            ping_time = ping.group(1) + " ms" if ping else "Timeout"
        except:
            ping_time = "Timeout"

        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "Unknown"

        p(f"{ip:<18} {ping_time:<10} {hostname}")

    input("\nPress Enter...")

# =========================
# Fake tools
# =========================
def system_scan():
    clear()
    p("Scanning system...\n")
    for i in range(0, 101, 10):
        p(f"[{i}%] Processing")
        time.sleep(0.2)
    input("\nPress Enter...")

def ip_tool():
    clear()
    ip = input(PURPLE + "Enter IP: " + RESET)
    p(f"\nTarget: {ip}")
    p("Country: UNKNOWN")
    p("ISP: UNKNOWN")
    input("\nPress Enter...")

def admin_panel():
    clear()
    p("ADMIN PANEL\n")
    p("• Full access")
    input("\nPress Enter...")

def discord_lookup():
    clear()
    p("DISCORD DATABASE LOOKUP\n")
    discord_id = input(PURPLE + "Enter Discord ID: " + RESET)

    headers, row = search_discord_id_in_sheet(discord_id)

    if not row:
        p("\nNo results found.")
        input("\nPress Enter...")
        return

    p("\nMATCH FOUND:\n")
    for h, v in zip(headers, row):
        p(f"{h}: {v}")

    input("\nPress Enter...")

# =========================
# Menu
# =========================
def main_menu(permission):
    set_console_title(f"SmartScreen ATTACK | {permission.upper()}")

    while True:
        clear()
        p(ASCII_HEADER)
        p(f"Logged in as: {permission.upper()}\n")

        p("[1] System Scan")
        p("[2] WiFi Device Scan")

        if permission in ("vip", "admin"):
            p("[3] IP Information")

        if permission == "admin":
            p("[4] Admin Panel")
            p("[5] Discord Lookup")

        p("[0] Exit\n")

        choice = input(PURPLE + "Select option: " + RESET)

        if choice == "1":
            system_scan()
        elif choice == "2":
            wifi_scan()
        elif choice == "3" and permission in ("vip", "admin"):
            ip_tool()
        elif choice == "4" and permission == "admin":
            admin_panel()
        elif choice == "5" and permission == "admin":
            discord_lookup()
        elif choice == "0":
            break
        else:
            p("ACCESS DENIED OR INVALID OPTION")
            time.sleep(1.5)

# =========================
# MAIN
# =========================
set_console_title("SmartScreen ATTACK | Initializing")
intro_animation()

while True:
    clear()
    p(ASCII_HEADER)
    set_console_title("SmartScreen ATTACK | Awaiting Access Code")

    code = input(PURPLE + "Enter Access Code: " + RESET)
    ok, permission = check_code_google_sheet(code)

    if ok:
        break
    else:
        p("\nACCESS DENIED")
        time.sleep(2)

main_menu(permission)
