# Netspeedo 📊

![PyPI version](https://img.shields.io/pypi/v/netspeedo)
![License](https://img.shields.io/github/license/rajuX75/netspeedo)
![Python versions](https://img.shields.io/pypi/pyversions/netspeedo)

A feature-rich, real-time network speed and performance monitor for your terminal, built with Python and the Rich library.

### Screenshot

```
╭────────────────── Netspeedo - Real-time Network Monitor ───────────────────╮
│                                                                            │
│  Status: [bold green]Online[/]  ·  Public IP: [bold cyan]123.45.67.89[/]  ·  Latency: [bold yellow]12.34 ms[/]   │
│                                                                            │
├───────────┬────────────────┬────────────────┬─────────────────┬───────────────┤
│ Interface │ Download Speed │ Upload Speed   │ Data Downloaded │ Data Uploaded │
├───────────┼────────────────┼────────────────┼─────────────────┼───────────────┤
│ Wi-Fi     │ 15.67 Mbps     │ 8.91 Mbps      │ 1024.56 MB      │ 256.78 MB     │
│ Ethernet  │ 0.00 bps       │ 0.00 bps       │ 0.00 MB         │ 0.00 MB       │
╰───────────┴────────────────┴────────────────┴─────────────────┴───────────────╯
```

### Features

-   **Real-time Speed**: Monitor download and upload speeds for all active network interfaces.
-   **Total Data Usage**: Tracks the total data downloaded and uploaded during the session.
-   **Public IP Display**: Shows your current public IP address.
-   **Latency Check**: Measures your connection's latency (ping) to a reliable server.
-   **Connection Status**: Clearly indicates if your internet connection is online or offline.
-   **Beautiful Terminal UI**: Uses the `rich` library for a clean, modern, and auto-updating interface.
-   **Cross-Platform**: Works on Windows, macOS, and Linux.

### Installation

You can install `netspeedo` directly from PyPI:

```bash
pip install netspeedo
```

### Usage

Simply run the command in your terminal:

```bash
netspeedo
```

Press `Ctrl+C` to exit the monitor at any time.

### Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
