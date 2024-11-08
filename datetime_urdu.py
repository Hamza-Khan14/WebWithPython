# Pehle tools import karte hain
import datetime  # Time check karne ke liye
import time     # Seconds count karne ke liye
from rich import print  # Fancy display ke liye
from rich.panel import Panel  # Box banane ke liye
from rich.live import Live   # Smooth display ke liye
from rich.console import Console  # Display screen ke liye

# Display screen banate hain
console = Console()

# Clock maker function - yeh function time aur date ko box mai sajata hai
def generate_clock():
    # datetime.now() current time nikal kar x mai rakhta hai
    x = datetime.datetime.now()
    
    # Panel() ek box banata hai jis mai:
    return Panel(
        # Date ko green aur cyan color mai sajata hai
        # strftime('%Y-%m-%d') date ko 2024-01-15 jaise format mai likhta hai
        f"[bold green]Date:[/bold green] [cyan]{x.strftime('%Y-%m-%d')}[/cyan]\n"
        
        # Time ko bhi green aur cyan color mai sajata hai
        # strftime('%H:%M:%S') time ko 14:30:45 jaise format mai likhta hai
        f"[bold green]Time:[/bold green] [cyan]{x.strftime('%H:%M:%S')}[/cyan]",
        
        # Box ke upar Clock likhta hai
        title="Clock",
        
        # Box ko blue color mai rang deta hai
        border_style="blue"
    )

# Live() function clock ko continuously chalata hai
with Live(generate_clock(), refresh_per_second=1) as live:
    # Hamesha chalta rahe is liye while True
    while True:
        # live.update() generate_clock() jo clock bananay ka Def/Function ha us ko call karta hai:
        # 1. generate_clock() naya time check karta hai
        # 2. Naye time ke sath naya box banata hai
        # 3. Purane time ki jagah naya time dikhata hai
        live.update(generate_clock())
        
        # Ek second ka break leta hai, phir cycle repeat
        time.sleep(1)
