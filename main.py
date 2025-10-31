from rich.console import Console
from username_scanner import run_username_scan
from hibp_fetcher import run_hibp_check

console = Console()

def main():
    console.print("[bold blue]Exposr — Data Breach & Username Scanner[/bold blue]\n")
    console.print("1️⃣  Check data breaches (HIBP)\n2️⃣  Probe username across platforms\n3️⃣  Exit\n")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        run_hibp_check()
    elif choice == "2":
        run_username_scan()
    else:
        console.print("[bold red]Exiting...[/bold red]")

if __name__ == "__main__":
    main()