# netspeedo/cli.py

"""
Netspeedo: A real-time network performance monitor for the terminal.

This script provides a command-line interface (CLI) to monitor network
speed, data usage, latency, and connection status.
"""

import time
import re
import platform
import subprocess
from typing import Dict, Any, Optional

import psutil
import requests
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.text import Text

# --- Constants for Configuration ---
# These are placed at the top for easy modification.
PING_HOST = "8.8.8.8"  # Google's public DNS, highly reliable.
IP_API_URL = "https://api.ipify.org?format=json"

# Type hint for our network statistics dictionary for better code clarity.
NetworkStats = Dict[str, Dict[str, Any]]


def get_public_ip() -> Optional[str]:
    """
    Fetches the public IP address from an external API.

    Returns:
        Optional[str]: The public IP address as a string, or None if fetching fails.
    """
    try:
        response = requests.get(IP_API_URL, timeout=3)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()["ip"]
    except (requests.RequestException, KeyError):
        return "N/A"


def get_latency(host: str) -> Optional[str]:
    """
    Pings a host to determine the connection latency.

    Args:
        host (str): The hostname or IP address to ping.

    Returns:
        Optional[str]: The latency in milliseconds as a formatted string, or 'N/A' on failure.
    """
    # Determine the ping command based on the operating system.
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '2', host] # -w 2 sets a 2-second timeout

    try:
        # Execute the ping command, capturing the output.
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True, # Raises CalledProcessError if ping fails
            timeout=3
        )
        # Search for the time value in the output using regex. Works across OS.
        match = re.search(r"time[=<]([\d.]+)\s*ms", result.stdout)
        if match:
            return f"{float(match.group(1)):.2f} ms"
        return "N/A"
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return "N/A"


def format_speed(bits: float) -> str:
    """Formats speed in bits to a human-readable format (Kbps, Mbps, etc.)."""
    if bits < 1000:
        return f"{bits:.2f} bps"
    elif bits < 1_000_000:
        return f"{bits/1000:.2f} Kbps"
    elif bits < 1_000_000_000:
        return f"{bits/1_000_000:.2f} Mbps"
    else:
        return f"{bits/1_000_000_000:.2f} Gbps"


def generate_layout(stats: NetworkStats, ip: Optional[str], latency: Optional[str]) -> Layout:
    """Creates the Rich Layout for the terminal display."""
    layout = Layout()

    # The layout is split into a header and the main content table.
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main"),
    )

    # --- Header Panel ---
    is_online = latency != "N/A"
    status = "[bold green]Online[/]" if is_online else "[bold red]Offline[/]"
    ip_text = f"[bold cyan]{ip}[/]" if ip else "[dim]Fetching...[/]"
    latency_text = f"[bold yellow]{latency}[/]" if latency else "[dim]Pinging...[/]"

    header_text = Text(
        f"Status: {status}  ·  Public IP: {ip_text}  ·  Latency: {latency_text}",
        justify="center",
    )
    header_panel = Panel(header_text, title="Netspeedo - Real-time Network Monitor", border_style="blue")
    layout["header"].update(header_panel)

    # --- Main Content Table ---
    table = Table(show_header=True, header_style="bold magenta", border_style="dim")
    table.add_column("Interface", justify="left", style="cyan", no_wrap=True)
    table.add_column("Download Speed", justify="center", style="green")
    table.add_column("Upload Speed", justify="center", style="magenta")
    table.add_column("Data Downloaded", justify="right", style="green")
    table.add_column("Data Uploaded", justify="right", style="magenta")

    for interface, data in stats.items():
        table.add_row(
            interface,
            format_speed(data['down_speed_bits']),
            format_speed(data['up_speed_bits']),
            f"{data['total_down_mb']:.2f} MB",
            f"{data['total_up_mb']:.2f} MB"
        )

    layout["main"].update(Panel(table, border_style="blue"))
    return layout


def main():
    """
    The main function that runs the monitoring loop.
    It initializes stats, handles the update loop, and manages the live display.
    """
    console = Console()
    last_io_counters = psutil.net_io_counters(pernic=True)
    public_ip = get_public_ip() # Fetch once at the start for speed

    try:
        with Live(generate_layout({}, None, None), refresh_per_second=1, screen=True, console=console) as live:
            update_counter = 0
            while True:
                # --- Data Gathering ---
                current_io_counters = psutil.net_io_counters(pernic=True)
                stats: NetworkStats = {}
                latency = get_latency(PING_HOST) # Check latency every cycle

                # Update IP and latency periodically, not every second, to reduce API calls.
                if update_counter % 30 == 0: # Update every 30 seconds
                    public_ip = get_public_ip()
                update_counter += 1

                for interface, data in current_io_counters.items():
                    if interface in last_io_counters:
                        last_data = last_io_counters[interface]
                        down_speed = data.bytes_recv - last_data.bytes_recv
                        up_speed = data.bytes_sent - last_data.bytes_sent

                        stats[interface] = {
                            "down_speed_bits": down_speed * 8,
                            "up_speed_bits": up_speed * 8,
                            "total_down_mb": data.bytes_recv / (1024 * 1024),
                            "total_up_mb": data.bytes_sent / (1024 * 1024),
                        }

                last_io_counters = current_io_counters

                # --- Update Display ---
                live.update(generate_layout(stats, public_ip, latency))
                time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Netspeedo stopped.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred: {e}[/bold red]")

# This allows the script to be run directly for testing purposes
if __name__ == "__main__":
    main()
