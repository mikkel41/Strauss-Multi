import turtle
import time
import webbrowser

# ================= CONFIG =================
DISCORD_URL = "https://discord.gg/m5cdVhcCsd"
WEBSITE_URL = "https://snakesquad.gg"

STATUS = "MAINTENANCE MODE"
ETA = "Unknown – Check Discord"
VERSION = "Snake Squad Loader v1.0.0"

PURPLE = "#9b5cff"
SOFT_PURPLE = "#c7a6ff"
DARK_BG = "#0b0614"

# Discord link position (for clicking)
DISCORD_X = -420
DISCORD_Y = -120

# ================= SCREEN =================
screen = turtle.Screen()
screen.title("Snake Squad | Under Maintenance")
screen.bgcolor(DARK_BG)
screen.setup(width=1.0, height=1.0)  # FULLSCREEN
screen.tracer(0)

# ================= TEXT WRITER =================
writer = turtle.Turtle()
writer.hideturtle()
writer.penup()
writer.color(PURPLE)

def draw_text():
    writer.clear()

    # Title
    writer.goto(0, 280)
    writer.write("SNAKE SQUAD", align="center",
                 font=("Courier", 38, "bold"))

    writer.goto(0, 235)
    writer.write("UNDER MAINTENANCE", align="center",
                 font=("Courier", 18, "normal"))

    # Description
    writer.goto(0, 185)
    writer.write("Our systems are currently undergoing maintenance.",
                 align="center", font=("Courier", 14, "normal"))

    writer.goto(0, 155)
    writer.write("The program is temporarily unavailable.",
                 align="center", font=("Courier", 14, "normal"))

    # Info panel
    writer.color(SOFT_PURPLE)

    writer.goto(-420, 60)
    writer.write(f"STATUS  : {STATUS}", align="left",
                 font=("Courier", 14, "normal"))

    writer.goto(-420, 30)
    writer.write(f"ETA     : {ETA}", align="left",
                 font=("Courier", 14, "normal"))

    writer.goto(-420, 0)
    writer.write(f"VERSION : {VERSION}", align="left",
                 font=("Courier", 14, "normal"))

    writer.goto(-420, -60)
    writer.write("For updates, announcements and support:",
                 align="left", font=("Courier", 14, "normal"))

    # Clickable Discord link
    writer.goto(DISCORD_X, DISCORD_Y)
    writer.write(f"Discord : {DISCORD_URL}",
                 align="left",
                 font=("Courier", 14, "underline"))

    # Website (non-clickable, info only)
    writer.goto(-420, -150)
    writer.write(f"Website : {WEBSITE_URL}",
                 align="left", font=("Courier", 14, "normal"))

    # Footer
    writer.color(PURPLE)
    writer.goto(0, -300)
    writer.write("© Snake Squad – Protecting the FiveM Community",
                 align="center", font=("Courier", 10, "normal"))

# ================= CLICK HANDLER =================
def handle_click(x, y):
    # Bounding box around Discord text
    if -430 < x < 350 and -140 < y < -105:
        webbrowser.open(DISCORD_URL)

screen.onclick(handle_click)

# ================= TURTLE ANIMATION =================
spinner = turtle.Turtle()
spinner.shape("turtle")
spinner.color(PURPLE)
spinner.penup()
spinner.goto(0, -20)
spinner.speed(0)

# ================= MAIN LOOP =================
draw_text()

while True:
    spinner.right(2)
    screen.update()
    time.sleep(0.01)
