import os
import psutil
from utils import toolkit
from datetime import datetime,timedelta

# Network info
def show_network_info():
    """Show network statistics including sent and received bytes."""
    stats = psutil.net_io_counters()
    sent = stats.bytes_sent
    recv = stats.bytes_recv
    stats = psutil.net_io_counters()
    print(f"⬆️ Sent:     {toolkit.format_bytes(sent)}")
    print(f"⬇️ Received: {toolkit.format_bytes(recv)}")
    


def read_network_log(from_time=None, to_time=None):
    """Read and display network log from a file, optionally filtered by datetime."""

    log_path = "/Users/rolandas/scripts/log/network-log"
    if not os.path.exists(log_path):
        print("No network log found.")
        return

    if from_time or to_time:
        print(f"Filtering from {from_time or 'beginning'} to {to_time or 'end'}")

    print("📊 [PC-Hub] Network Log:")
    print("────────────────────────────")

def read_network_log(from_time=None, to_time=None):
    """Read and display network log from a file, optionally filtered by datetime."""

    log_path = "/Users/rolandas/scripts/log/network-log"
    if not os.path.exists(log_path):
        print("No network log found.")
        return

    # Adjust to_time if only from_time is provided and to_time is None
    if from_time and not to_time:
        # Round from_time to day start if it's just a date
        to_time = from_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    print(f"Filtering from {from_time} to {to_time}")

    print("📊 [PC-Hub] Network Log:")
    print("────────────────────────────")

    with open(log_path, "r") as f:
        for line in f:
            timestamp_str, sent, recv = line.strip().split("|")
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

            if from_time and timestamp < from_time:
                continue
            if to_time and timestamp >= to_time:
                continue

            print(f"Time: {timestamp_str}, "
                  f"Sent: {toolkit.format_bytes(int(sent))}, "
                  f"Received: {toolkit.format_bytes(int(recv))}")