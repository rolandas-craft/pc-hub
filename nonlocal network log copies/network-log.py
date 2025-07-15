#!/Library/Frameworks/Python.framework/Versions/3.13/bin/python3

from datetime import datetime
import psutil

#print(f"{datetime.now()}: Script started.")  # <- This goes to .log


    
# Show network statistics
def show_network_info():
    """Show network statistics including sent and received bytes."""
    stats = psutil.net_io_counters()
    sent = stats.bytes_sent
    recv = stats.bytes_recv
    stats = psutil.net_io_counters()
    print(f"⬆️ Sent:     {sent}")
    print(f"⬇️ Received: {recv}")
    return sent, recv
    
sent, recv = show_network_info()

# Log the sent and received bytes to a file
with open("/Users/rolandas/scripts/log/network-log", "a") as f:
    f.write(f"{datetime.now()}|{sent}|{recv}\n")
