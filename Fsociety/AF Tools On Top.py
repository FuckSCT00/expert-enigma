import os
import sys
import socket
import subprocess
import time
import threading
import re
from pystyle import Colors, Cursor, System, Colorate


TOOLS = [
    ("IP Info", "ip_info"), ("Get IP", "get_ip"), ("Token Decrypt", "token_decrypt"),
    ("Token Checker", "token_checker"), ("Token Info", "token_generator"), ("Badge Changer", "badge_changer"),
    ("Status Rotator", "status_rotator"), ("Server Info", "server_info"), ("Webhook Info", "webhook_info"),
    ("Webhook Spammer", "webhook_spammer"), ("Scrapper Proxy", "scrapper_proxy"), ("Email Info", "email_info"),
    ("Instagram Info", "instagram_user_info"), ("Number Info", "number_info"), ("Auto Login", "auto_login"),
    ("Token Gen", "token_generator"), ("Mass Report", "discord_massreport"), ("Website Info", "website_info"),
    ("Token MassDM", "token_massdm"), ("Snapchat Info", "snapchat_user_info"), ("FiveM Server", "server_info_fivem"),
    ("Steam Info", "steam_user_info"), ("TikTok Info", "tiktok_user_info"), ("Bot Inviter", "invite_bot_to_id"),
    ("IP Scanner", "ip_scanner"), ("Roblox Info", "roblox_search"), ("Telegram Info", "telegram_search"),
    ("Discord ID", "disc_id")
]

current_page = 0
items_per_page = 15

logo = r"""
 █████╗ ███████╗      ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔══██╗██╔════╝      ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
███████║█████╗           ██║   ██║   ██║██║   ██║██║     ███████╗
██╔══██║██╔══╝           ██║   ██║   ██║██║   ██║██║     ╚════██║
██║  ██║██║              ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚═╝  ╚═╝╚═╝              ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
               Fsociety & By 505  Terminal Edition
"""


def strip_ansi(text):
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)


def center_text(text: str) -> str:
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80

    lines = text.splitlines()
    if not lines:
        return ""

    max_len = max(len(strip_ansi(line)) for line in lines)
    centered_lines = []

    for line in lines:
        padding = max((width - max_len) // 2, 0)
        centered_lines.append(" " * padding + line)

    return "\n".join(centered_lines)


# =========================
# 🔵 BOOT SCREEN ANIMÉ
# =========================
def animated_logo_infinite(stop_event):
    press_text = "Press ENTER to start"
    colors = [Colors.blue, Colors.cyan]
    i = 0

    loading = 0

    while not stop_event.is_set():
        os.system('cls' if os.name == 'nt' else 'clear')

        try:
            term_height = os.get_terminal_size().lines
        except:
            term_height = 24

        padding_top = max((term_height - 14) // 2, 0)
        print("\n" * padding_top)

        # Logo animation
        color = colors[i % 2]
        i += 1

        print(Colorate.Color(color, center_text(logo), True))

        # Fake loading bar
        bar = "[" + ("#" * loading).ljust(20) + "]"
        print("\n" + center_text(Colorate.Color(Colors.white, bar, True)))

        loading = (loading + 1) % 21

        print("\n" + center_text(Colorate.Color(Colors.white, press_text, True)))

        time.sleep(0.25)

        if stop_event.is_set():
            break


def display_menu():
    os.system('cls' if os.name == 'nt' else 'clear')

    start = current_page * items_per_page
    page_tools = TOOLS[start:start + items_per_page]

    print(Colorate.Color(Colors.blue, center_text(logo), True))

    devs = f"Developers: @Fsociety & @505 | Page {current_page + 1}/2"
    print(center_text(f"{Colors.white}{devs}{Colors.reset}"))

    grid_lines = []

    for i in range(5):
        row_parts = []

        for j in range(3):
            idx_in_page = i + (j * 5)

            if idx_in_page < len(page_tools):
                global_idx = start + idx_in_page
                name = page_tools[idx_in_page][0]
                num = f"{global_idx + 1:02}"

                item = f"{Colors.blue}[{num}]{Colors.reset} {name:<20}"
                row_parts.append(item)

        if row_parts:
            grid_lines.append(" ".join(row_parts))

    print(center_text("\n".join(grid_lines)))

    nav = "[z] Previous | [e] Next | [quit] Quit"
    print("\n" + center_text(f"{Colors.blue}{nav}{Colors.reset}"))


def execute_tool(choice):
    try:
        choice_num = int(choice.strip())
        index = choice_num - 1

        if 0 <= index < len(TOOLS):
            name, tool_file = TOOLS[index]
            path = os.path.join("utils", f"{tool_file}.py")

            if os.path.exists(path):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Colorate.Color(Colors.blue, f"\n [!] Starting: {name}...", True))

                subprocess.run([sys.executable, path])

                print(f"\n{Colors.blue}Press ENTER to return...{Colors.reset}")
                input()
            else:
                print(f"\n [!] File not found: utils/{tool_file}.py")
                time.sleep(2)

    except:
        pass


def main():
    global current_page

    System.Title("AF Tools V2 - Made by @Fsociety & @505")
    Cursor.HideCursor()

    stop_event = threading.Event()
    t = threading.Thread(target=animated_logo_infinite, args=(stop_event,), daemon=True)
    t.start()

    input()
    stop_event.set()
    t.join()

    Cursor.ShowCursor()

    while True:
        display_menu()

        pc_name = socket.gethostname()
        prompt = f"\n {Colors.blue}┌───({Colors.white}{pc_name}@{Colors.blue})\n └─> {Colors.reset}"

        choice = input(prompt).lower()

        if choice == "quit":
            break
        elif choice in ["z", "next"]:
            current_page = (current_page + 1) % 2
        elif choice in ["e", "back"]:
            current_page = (current_page - 1) % 2
        else:
            execute_tool(choice)


if __name__ == "__main__":
    main()