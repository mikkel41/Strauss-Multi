
# Snake Multi Tool
# NOTE: This file is provided as a ready-to-run program.

import turtle
import time
import os
import requests
import csv
import subprocess
import socket
import re
import sys

# =========================
# Console title
# =========================
def set_console_title(title):
    if os.name == "nt":
        os.system(f'title "{title}"')

# =========================
# Turtle intro animation (Snake)
# =========================
def intro_animation():
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.setup(width=1.0, height=1.0)
    screen.title("Snake Tool")

    w = screen.window_width()
    h = screen.window_height()

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color("purple")
    t.width(6)

    text_t = turtle.Turtle()
    text_t.hideturtle()
    text_t.color("white")

    start_x = -w//2 + 50
    mid_x = 0
    end_x = w//2 - 50
    y = 0

    turtle.tracer(0)
    x = start_x
    while x < mid_x:
        t.goto(x, y)
        text_t.clear()
        text_t.write("Snake Tool", align="center", font=("Courier", 28, "bold"))
        turtle.update()
        x += 10
        time.sleep(0.01)

    # pause at center, show only "Snake"
    text_t.clear()
    text_t.write("Snake", align="center", font=("Courier", 36, "bold"))
    turtle.update()
    time.sleep(1.2)

    while x < end_x:
        t.goto(x, y)
        text_t.clear()
        text_t.write("Snake Tool", align="center", font=("Courier", 28, "bold"))
        turtle.update()
        x += 10
        time.sleep(0.01)

    time.sleep(0.5)
    screen.bye()

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
███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗
██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝
███████╗██╔██╗ ██║███████║█████╔╝ █████╗  
╚════██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  
███████║██║ ╚████║██║  ██║██║  ██╗███████╗
╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
Snake Multi Tool
"""

# =========================
# Google Sheet: login check
# =========================
def check_code_google_sheet(user_code):
    SHEET_ID = "1sR8bO58zUTqqYKn0YRaOq-ta2HsgQsXf0FP6DVhARSE"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    try:
        r = requests.get(url, timeout=5)
        reader = csv.reader(r.text.splitlines())
        for row in reader:
            if len(row) >= 2 and row[0].strip() == user_code:
                return True, row[1].strip().lower()
        return False, None
    except:
        return False, None

# =========================
# Admin Port Scanner
# =========================
def port_scanner_admin():
    clear()
    target = input(PURPLE + "Target IP: " + RESET)
    p("\nScanning ports 1-10000 (open only)\n")
    open_ports = []
    for port in range(1, 10001):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.05)
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                p(f"OPEN  -> {port}")
            s.close()
        except:
            pass
    if not open_ports:
        p("\nNo open ports found.")
    input("\nPress Enter...")

# =========================
# Example User Tools
# =========================
def dns_lookup():
    clear()
    host = input(PURPLE + "Hostname: " + RESET)
    try:
        ip = socket.gethostbyname(host)
        p(f"IP: {ip}")
    except:
        p("Lookup failed.")
    input("\nPress Enter...")

def whoami():
    clear()
    p("Session info")
    p(f"OS: {os.name}")
    p(f"Python: {sys.version.split()[0]}")
    input("\nPress Enter...")

# =========================
# Menu
# =========================
def main_menu(permission):
    while True:
        clear()
        p(ASCII_HEADER)
        p(f"Logged in as: {permission.upper()}\n")
        p("[1] DNS Lookup")
        p("[2] Session Info")
        if permission == "admin":
            p("[9] Admin Port Scanner")
        p("[0] Exit")
        c = input(PURPLE + "Select: " + RESET)
        if c == "1":
            dns_lookup()
        elif c == "2":
            whoami()
        elif c == "9" and permission == "admin":
            port_scanner_admin()
        elif c == "0":
            break

# =========================
# MAIN
# =========================
set_console_title("Snake Multi Tool | Initializing")
intro_animation()

while True:
    clear()
    p(ASCII_HEADER)
    code = input(PURPLE + "Enter Access Code: " + RESET)
    ok, permission = check_code_google_sheet(code)
    if ok:
        break
    p("ACCESS DENIED")
    time.sleep(2)

main_menu(permission)
