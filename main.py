import cmd
import subprocess
from datetime import datetime
from datetime import timedelta
import psutil
import re
import geocoder
import os
import platform
import requests

## My modules
from utils import network_utils
from utils import toolkit

    
# Get location info using ip-api.com
def get_location_info():
    """Get IP-based location using ip-api.com"""
    try:
        response = requests.get("http://ip-api.com/json", timeout=5)
        data = response.json()
        if data['status'] == 'success':
            city = data.get('city', 'Unknown')
            country = data.get('country', 'Unknown')
            lat = data.get('lat')
            lon = data.get('lon')
            return (city, country, [lat, lon])
        else:
            return ('Unknown', 'Unknown', None)
    except Exception as e:
        return ('Error', 'Error', None)
    
# Parse time intervals like "3d", "2h", "5m", etc.
def parse_time_interval(s):
    """Parse a time interval string into a timedelta object."""
    match = re.match(r"(\d+)([smhd])", s.strip().lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    if unit == 's':
        return timedelta(seconds=value)
    elif unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    elif unit == 'mo':
        return timedelta(days=30 * value)  # Approximate
    elif unit == 'y':
        return timedelta(days=365 * value)  # Approximate
    
# Create a new note in macOS Notes app
def add_note(title, body):
    """Create a new note in macOS Notes app."""
    # Escape double quotes and backslashes inside body
    safe_body = body.replace("\\", "\\\\").replace('"', '\\"')

    script = f'''
    tell application "Notes"
        activate
        tell account "iCloud"
            set theNote to make new note at folder "Notes" with properties {{name:"{title}", body:"{safe_body}"}} 
            show theNote
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', script])
    
# System info 
def get_system_info(arg):
    """Get system information based on the argument."""
    if arg == 'cpu':
        return psutil.cpu_percent(interval=1)
    elif arg == 'memory':
        return psutil.virtual_memory().percent
    elif arg == 'disk':
        return psutil.disk_usage('/').percent
    else:
        raise ValueError("Invalid argument. Use 'cpu', 'memory', or 'disk'.")
    
# Get battery status on macOS
def get_battery_status():
    """Get battery status on macOS."""
    output = subprocess.check_output(['pmset', '-g', 'batt']).decode('utf-8')
    lines = output.strip().split('\n')

    if len(lines) > 1:
        info = lines[1]
        parts = info.split('\t')[-1].split('; ')
        percent = parts[0].strip()
        status = parts[1].strip()
        print(f"🔋 Battery: {percent} ({status})")
    else:
        print("🔌 No battery info found.")
        
# Get clean uptime      
def get_clean_uptime():
    """Get system uptime in a clean format."""
    output = subprocess.check_output(['uptime']).decode('utf-8')
    up_part = output.split(' up ')[1].split(',')[0:2]
    uptime = ', '.join(up_part).strip()
    print(f"⏱️ Uptime: {uptime}")
    


# Custom shell class
class MyShell(cmd.Cmd):
    """Custom shell for PC-Hub with various commands."""
    prompt = '[📟 PC-Hub] > '
    command_count = 0
    last_note_title = None
    
    def precmd(self, line):
        """Pre-command processing to handle command count and last note."""
        # Count commands for dashboard
        self.command_count += 1
        return line

        
    ## List all commands
    def do_commands(self, arg):
        """List all user commands"""
        print("📜 [PC-Hub] Available commands:")
        for attr in dir(self):
            if attr.startswith("do_") and not attr.startswith("do__"):
                cmd_name = attr[3:]
                if not cmd_name.startswith("help"):  # Skip help or hidden ones
                    print(f"• {cmd_name}")
                            
    ## dashboard command
    def do_db(self, arg):
        """Show the dashboard with system and user info."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("\n📊 [PC-Hub] Dashboard")
        print("────────────────────────────")
        print(f"🕒 Time:        {now}")

        location_info = get_location_info()
        print(f"📍 Location:   {location_info[0]}, {location_info[1]}")
        if location_info[2]:
            print(f"🌍 Coordinates: {location_info[2]}")
        else:
            print("🌍 Coordinates: Unknown")

        print(f"📟 Commands:    {self.command_count}")
        if self.last_note_title:
            print(f"📓 Last note:   {self.last_note_title}")
        else:
            print("📓 Last note:   (none)")

        print("")
        print("🖥️  System:")
        print(f"   CPU Usage:   {get_system_info('cpu')}%")
        print(f"   Memory Usage: {get_system_info('memory')}%")
        print(f"   Battery Status: ", end="")
        get_battery_status()
        print(f"   Uptime: ", end="")
        get_clean_uptime()
        print("")
        

    def do_clock(self, arg):
        """Show current time."""
        from datetime import datetime
        now = datetime.now()
        print(f"🕒 [PC-Hub] Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        

    def do_network(self, arg):
        """Show network statistics."""
        network_utils.show_network_info()
    

    def do_exit(self, arg):
        """Exit the shell."""
        print("📟 [PC-Hub] Session terminated.")
        return True

    def do_q(self, arg):
        """Exit the shell. Alias for 'exit'."""
        return self.do_exit(arg)  # Alias
    
    def do_note(self, arg):
        """Create a new note. Usage: note --<title> --<body>"""
        parts = arg.split('--')

        # Clean up leading/trailing whitespace from each part
        parts = [p.strip() for p in parts if p.strip()]

        # Assign values
        title = parts[0] if len(parts) > 0 else "Untitled"
        body = parts[1] if len(parts) > 1 else "Empty note."
        
        if not title:
            title = "Untitled"
        self.last_note_title = title
        
        add_note(title, body)
        
    def do_clear(self, arg):
        """Clear the terminal screen."""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        
    def do_network_log(self, arg):
        """Read and display the network log with optional date filters."""

        tokens = arg.split()
        from_time = None
        to_time = None

        def parse_datetime(parts):
            formats = [
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d %H",
                "%Y-%m-%d",
                "%Y-%m",
                "%Y"
            ]
            dt_str = " ".join(parts)
            print(f"Parsing datetime from: {dt_str}")
            for fmt in formats:
                try:
                    return datetime.strptime(dt_str, fmt)
                except ValueError:
                    continue
            return None

        # Try parsing based on number of tokens
        if len(tokens) == 1:
            from_time = parse_datetime(tokens[:1])
        elif len(tokens) == 2:
            to_time = parse_datetime(tokens[0:2])

        elif len(tokens) in (3, 4):
            from_time = parse_datetime(tokens[:2])
            to_time = parse_datetime(tokens[2:4]) if len(tokens) == 4 else None
        
        print(f"📊 [PC-Hub] Reading network log from {from_time} to {to_time}")
        #network_utils.read_network_log(from_time, to_time)

            
if __name__ == '__main__':
    print("\n📟 [PC-Hub] Welcome to PC-Hub! Type 'help' for commands.")
    
    shell = MyShell()

    shell.onecmd("db")  

    MyShell().cmdloop()