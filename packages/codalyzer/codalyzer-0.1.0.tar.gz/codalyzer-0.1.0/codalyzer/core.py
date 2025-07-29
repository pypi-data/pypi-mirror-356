import os
import re
import sys
import socket
import threading
import numpy as np
import matplotlib.pyplot as plt

from colorama import Fore, Style, init
from tqdm import tqdm
from tabulate import tabulate
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from rich.console import Console
from rich.panel import Panel
from rich import box
import psutil
import requests

init(autoreset=True)
console = Console()

def count_code_stats(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    blank_lines = sum(1 for l in lines if l.strip() == '')
    comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
    function_lines = sum(1 for l in lines if l.strip().startswith('def '))
    class_lines = sum(1 for l in lines if l.strip().startswith('class '))
    average_length = np.mean([len(l.strip()) for l in lines if l.strip() != ''])

    return {
        "Total Lines": total_lines,
        "Blank Lines": blank_lines,
        "Comment Lines": comment_lines,
        "Function Count": function_lines,
        "Class Count": class_lines,
        "Average Line Length": round(average_length, 2)
    }

def visualize_stats(stats):
    labels = list(stats.keys())
    values = list(stats.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.title('Code Statistics')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def display_stats_table(stats):
    table = tabulate(stats.items(), headers=['Metric', 'Value'], tablefmt='fancy_grid')
    print(Fore.CYAN + table)

def color_highlight_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    print(highlight(code, PythonLexer(), TerminalFormatter()))

def monitor_resources():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    console.print(Panel(f"🧠 CPU: {cpu}% | 🧬 RAM: {ram}%", title="System Monitor", box=box.ROUNDED))

def socket_sync_server(port=65432):
    def handler():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', port))
        s.listen()
        print(Fore.YELLOW + f"[Socket] Listening on port {port}")
        conn, addr = s.accept()
        print(Fore.GREEN + f"[Socket] Connection from {addr}")
        data = conn.recv(1024).decode()
        print(Fore.MAGENTA + f"[Socket] Received: {data}")
        conn.sendall(b"ACK")
        conn.close()

    thread = threading.Thread(target=handler)
    thread.start()

def fetch_pypi_info(package):
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            info = response.json()['info']
            console.print(Panel(f"{info['name']} - {info['version']}\n{info['summary']}", title="PyPI Package", box=box.DOUBLE))
        else:
            print(Fore.RED + f"Failed to fetch info for {package}")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

def analyze_file(file_path):
    print(Fore.BLUE + f"\nAnalyzing: {file_path}")
    stats = count_code_stats(file_path)
    display_stats_table(stats)
    regex_summary(file_path) 
    visualize_stats(stats)
    color_highlight_code(file_path)
    monitor_resources()
    socket_sync_server()
    fetch_pypi_info("matplotlib")

def regex_summary(file_path):
    print(Fore.CYAN + Style.BRIGHT + "\n🔍 Regex Match Summary:")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    patterns = {
        "Functions (def)": r'^\s*def\s+\w+\(.*?\):',
        "Classes (class)": r'^\s*class\s+\w+\(?.*?\)?:',
        "TODO Comments": r'#\s*TODO[:]?.*'
    }

    for title, pattern in patterns.items():
        matches = re.findall(pattern, content, re.MULTILINE)
        color = Fore.GREEN if "def" in title else (Fore.MAGENTA if "class" in title else Fore.YELLOW)
        print(f"{color}{Style.BRIGHT}{title}: {len(matches)} match(es)")
        for match in matches:
            print(f"{color}  ➤ {Style.NORMAL}{match.strip()}")

def progress_simulation():
    print(Fore.YELLOW + "\nSimulating processing...")
    for _ in tqdm(range(100), desc="Analyzing"):
        pass

def main():
    console.print(Panel.fit("🔎 Welcome to Codalyzer!", style="bold green"))

    if len(sys.argv) != 2:
        print(Fore.RED + "Usage: python -m codalyzer.core <file_to_analyze.py>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(Fore.RED + "Error: File not found.")
        sys.exit(1)

    progress_simulation()
    analyze_file(file_path)

if __name__ == '__main__':
    main()
