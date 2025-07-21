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
    # Determine the time range based on the argument
    from_time = None
    to_time = None
    
    if not arg.strip():
        print("❌ No date range specified. Use 'network --log <from> <to>' or 'network --log <day|week|month|year|hour>'")
        return
    
    if arg.strip().split()[0] == "day":
        now = datetime.now().replace(second=0, microsecond=0)
        from_time = now - timedelta(days=1)
        to_time = now
    elif arg.strip().split()[0] == "week":
        from_time = datetime.strptime(str(datetime.now() - timedelta(weeks=1))[:16], "%Y-%m-%d %H:%M")
        to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
    elif arg.strip().split()[0] == "month":
        from_time = datetime.strptime(str(datetime.now() - timedelta(days=30))[:16], "%Y-%m-%d %H:%M")
        to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
    elif arg.strip().split()[0] == "year":
        from_time = datetime.strptime(str(datetime.now() - timedelta(days=365))[:16], "%Y-%m-%d %H:%M")
        to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
    elif arg.strip().split()[0] == "hour":
        # Parse the number of hours from the argument
        try:
            hours = int(arg.strip()[5:])
            from_time = datetime.strptime(str(datetime.now() - timedelta(hours=hours))[:16], "%Y-%m-%d %H:%M")
            to_time = datetime.strptime(str(datetime.now())[:16], "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid hour format. Use 'hour <number>'.")
            return 
    else:
        tokens = arg.split()

        if len(tokens) >= 2:
            from_str = " ".join(tokens[:2])
            try:
                from_time = datetime.strptime(from_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"❌ Invalid format for 'from time': '{from_str}'")
                from_time = None

        if len(tokens) >= 4:
            to_str = " ".join(tokens[2:4])
            try:
                to_time = datetime.strptime(to_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"❌ Invalid format for 'to time': '{to_str}'")
                to_time = None

    if not to_time:
        print("❌ 'to time' is required for filtering.")
        return
    if not from_time:
        print("❌ 'from time' is required for filtering.")
        return

    print(f"Filtering from {from_time} to {to_time}")
    if from_time and to_time:
        read_network_log(from_time, to_time)
        
    
