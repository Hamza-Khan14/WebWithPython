# First we get our tools ready
import datetime  # This helps us know what time it is
import time     # This helps us count seconds
from rich import print  # This makes our clock look pretty
from rich.panel import Panel  # This makes the box around our clock
from rich.live import Live   # This keeps our clock running smoothly
from rich.console import Console  # This is like our clock's display screen

# Make our display screen ready
console = Console()

# This is our clock maker - it builds a new clock display every second
def generate_clock():
    # Gets the current time and stores it in x
    x = datetime.datetime.now()
    
    # Panel() creates a box that:
    return Panel(
        # Makes "Date:" bold and green, then shows date in cyan
        # strftime('%Y-%m-%d') formats date like 2024-01-15
        f"[bold green]Date:[/bold green] [cyan]{x.strftime('%Y-%m-%d')}[/cyan]\n"
        
        # Makes "Time:" bold and green, then shows time in cyan
        # strftime('%H:%M:%S') formats time like 14:30:45
        f"[bold green]Time:[/bold green] [cyan]{x.strftime('%H:%M:%S')}[/cyan]",
        
        # Puts "Clock" at the top of our box
        title="Clock",
        
        # Makes the box outline blue
        border_style="blue"
    )

# Live() keeps our clock running continuously
with Live(generate_clock(), refresh_per_second=1) as live:
    # Keep running forever
    while True:
        # live.update() calls generate_clock() to:
        # 1. Check the new time
        # 2. Create new box with new time
        # 3. Show new time in place of old time
        live.update(generate_clock())
        
        # Take a one-second break, then repeat
        time.sleep(1)
