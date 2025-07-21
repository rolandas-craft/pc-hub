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
    

# Read network log
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

# Read the log file
def read_network_log(from_time=None, to_time=None):
    print(f"Filtering from {from_time} to {to_time}")
    """Read and display network log from a file, optionally filtered by datetime."""

    log_path = "/Users/rolandas/scripts/log/network-log"
    if not os.path.exists(log_path):
        print("No network log found.")
        return

    # Adjust to_time if only from_time is provided and to_time is None
    if from_time and not to_time:
        to_time = datetime.now().replace(second=0, microsecond=0)
        
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
            
def network_log(self, arg):
    print(f"Network log requested with argument: {arg}")
    def parse_datetime(parts):
        # Try parsing datetime from the provided parts
        formats = [
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H",
            "%Y-%m-%d",
            "%Y-%m",
            "%Y"
        ]
        dt_str = " ".join(parts)
        
        for fmt in formats:
            try:
                return datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
        return None
    
    # Determine the time range based on the argument
    if arg.strip() == "day":
        from_time = datetime.strptime(str(datetime.now() - timedelta(days=1))[:16], "%Y-%m-%d %H:%M")
        to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
    elif arg.strip() == "week":
        from_time = datetime.strptime(str(datetime.now() - timedelta(weeks=1))[:16], "%Y-%m-%d %H:%M")
        to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
    elif arg.strip() == "month":
        from_time = datetime.strptime(str(datetime.now() - timedelta(days=30))[:16], "%Y-%m-%d %H:%M")
        to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
    elif arg.strip() == "year":
        from_time = datetime.strptime(str(datetime.now() - timedelta(days=365))[:16], "%Y-%m-%d %H:%M")
        to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
    elif arg.strip()[:5] == "hours":
        # Parse the number of hours from the argument
        try:
            hours = int(arg.strip()[6:])
            from_time = datetime.strptime(str(datetime.now() - timedelta(hours=hours))[:16], "%Y-%m-%d %H:%M")
            to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid hour format. Use 'hours <number>'.")
            return 
    else:
        # Parse custom date range from the argument
        tokens = arg.split()
        from_time = None 
        to_time = None

        # Try parsing based on number of tokens
        print(f"Tokens: {tokens}")
        if len(tokens) == 1:
            from_time = parse_datetime(tokens[:1])

        elif len(tokens) == 2:
            from_time = parse_datetime(tokens[0:2])
            print(f"from_time: {from_time}")

        elif len(tokens) == 3:
            from_time = parse_datetime(tokens[0:2])
            to_time = parse_datetime(tokens[2:3])

        elif len(tokens) >= 4:
            from_time = parse_datetime(tokens[0:2])
            to_time = parse_datetime(tokens[2:4])
            
    print(f"Filtering1 from {from_time} to {to_time}")
    
    read_network_log(from_time, to_time)
    
