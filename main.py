from rich.console import Console
from username_scanner import run_username_scan
from hibp_fetcher import run_hibp_check
from password_scanner import run_pwned_password_count

console = Console()

def main():
    console.print("[bold blue]Exposr — Data Breach & Username Scanner[/bold blue]\n")
    console.print("1️⃣  Check data breaches (HIBP)\n2️⃣  Sherlock username probe\n3️⃣  Compromised password check\n4️⃣  Exit\n")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        run_hibp_check()
    elif choice == "2":
        run_username_scan()
    elif choice == "3":
        run_pwned_password_count()
    else:
        console.print("[bold red]Exiting...[/bold red]")

if __name__ == "__main__":
    main()