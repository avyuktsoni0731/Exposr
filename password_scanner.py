import hashlib, requests
from rich.console import Console
from rich.panel import Panel

console = Console()

def pwned_password_count(password: str):
    console.print(f"🔍 [bold yellow]Checking password strength for[/bold yellow] [cyan]{password}[/cyan] ...\n")

    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Exposr/1.0"})
        count = 0
        for line in r.text.splitlines():
            if suffix in line:
                count = int(line.split(":")[1])
                break

        if count > 0:
            return count
        else:
            return None
    except Exception as e:
        console.print(f"[red]Error checking password:[/red] {e}")

def run_pwned_password_count():
    password = input("Enter password to check: ").strip()
    if not password:
        console.print("[red]No password entered![/red]")
        return

    count = pwned_password_count(password)
    if count is not None:
        console.print(Panel.fit(
            f"⚠️ [bold red]This password has appeared {count:,} times in known breaches![/bold red]\n"
            "Consider changing it immediately and avoid reusing it.",
            title="Compromised Password Detected", border_style="red"
        ))
    else:
        console.print(Panel.fit(
            "✅ [bold green]Good news![/bold green] This password was not found in any known breaches.",
            title="Password Safe", border_style="green"
        ))