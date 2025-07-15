import os
import psutil
from utils import toolkit

# Network info
def show_network_info():
    """Show network statistics including sent and received bytes."""
    stats = psutil.net_io_counters()
    sent = stats.bytes_sent
    recv = stats.bytes_recv
    stats = psutil.net_io_counters()
    print(f"⬆️ Sent:     {toolkit.format_bytes(sent)}")
    print(f"⬇️ Received: {toolkit.format_bytes(recv)}")

def read_network_log():
    """Read and display network log from a file."""
    if not os.path.exists("/Users/rolandas/scripts/log/network-log"):
        print("No network log found.")
        return
    
    print("📊 [PC-Hub] Network Log:")
    print("────────────────────────────")
    
    # Read the log file
    with open("/Users/rolandas/scripts/log/network-log", "r") as f:
        for line in f:
            timestamp, sent, recv = line.strip().split("|")
            print(f"Time: {timestamp}, "
                  f"Sent: {toolkit.format_bytes(int(sent))}, "
                  f"Received: {toolkit.format_bytes(int(recv))}")