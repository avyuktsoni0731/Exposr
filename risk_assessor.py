# risk_assessor.py
import asyncio, hashlib, requests, json, time
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from hibp_fetcher import fetch_hibp_data

console = Console()

# --- Helper: check password in PwnedPasswords (k-anonymity) ---
def pwned_password_count(password: str):
    if not password:
        return None
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Exposr"})
        for line in r.text.splitlines():
            if suffix in line:
                return int(line.split(":")[1])
        return 0
    except:
        return None

# --- Risk score calculation (simplified) ---
def compute_risk(breaches, pw_count):
    score = 0
    flags = {"recent": False, "passwords": False, "pwleak": pw_count and pw_count > 0}
    if breaches:
        score += min(len(breaches) * 10, 40)
        for b in breaches:
            dc = [d.lower() for d in b.get("DataClasses", [])]
            if "password" in " ".join(dc):
                flags["passwords"] = True
                score += 10
            try:
                d = datetime.strptime(b["BreachDate"], "%Y-%m-%d")
                if d > datetime.utcnow() - timedelta(days=365):
                    flags["recent"] = True
                    score += 15
            except:
                pass
    if flags["pwleak"]:
        score += 35
    score = min(100, score)
    return score, flags

# --- Pretty displays ---
def summary_table(breaches):
    table = Table(title="🕵️ Breach Summary", show_lines=True)
    table.add_column("Name", style="bold white")
    table.add_column("Date", justify="center")
    table.add_column("Data Types")
    table.add_column("PwnCount", justify="right")
    for b in breaches:
        table.add_row(
            b.get("Title", b.get("Name", "Unknown")),
            b.get("BreachDate", "-"),
            ", ".join(b.get("DataClasses", [])),
            f"{b.get('PwnCount', 0):,}"
        )
    return table

def score_panel(score):
    if score >= 70:
        style, lvl = "bold white on red", "HIGH"
    elif score >= 40:
        style, lvl = "bold black on yellow", "MEDIUM"
    else:
        style, lvl = "bold white on green", "LOW"
    return Panel(f"Risk Score: [bold]{score}[/bold]\nExposure Level: {lvl}", title="🚨 RISK ASSESSMENT", style=style)

# --- Runner ---
def run_risk_assessment():
    console.print("[bold cyan] Exposr — Compromise Risk Assessment[/bold cyan]")
    email = input("Enter email to assess: ").strip()
    pw = input("Optionally enter a password to check (hashed locally): ").strip()

    console.print("\nFetching breach data from HIBP...")
    try:
        data = asyncio.run(fetch_hibp_data(email))
        breaches = data.get("Breaches", []) if isinstance(data, dict) else []
    except Exception as e:
        console.print(f"[red]Error fetching HIBP: {e}[/red]")
        breaches = []

    pw_count = None
    if pw:
        console.print("Checking password exposure via PwnedPasswords...")
        pw_count = pwned_password_count(pw)
        if pw_count is None:
            console.print("[yellow]Couldn’t check password (network or API issue).[/yellow]")
        elif pw_count == 0:
            console.print("[green]Password NOT found in breaches.[/green]")
        else:
            console.print(f"[red]Password found {pw_count} times![/red]")

    score, flags = compute_risk(breaches, pw_count)
    console.print()
    console.print(score_panel(score))
    console.print(summary_table(breaches))

    console.print("\n[bold]Recommended Actions:[/bold]")
    if not breaches and not pw_count:
        console.print("✅ No breaches or leaks detected.")
        return
    if flags["pwleak"]:
        console.print("• Change your password immediately and avoid reuse.")
    if flags["passwords"]:
        console.print("• Some breaches included passwords — rotate them now.")
    if flags["recent"]:
        console.print("• A recent breach affected you — prioritize these accounts.")
    console.print("• Enable 2FA on important services.")
    console.print("• Re-check periodically for new breaches.")

    if input("\nExport to JSON? (y/N): ").lower() == "y":
        fname = f"exposr_{email.replace('@','_')}.json"
        json.dump({"email": email, "score": score, "flags": flags, "breaches": breaches, "pw_count": pw_count, "ts": time.time()}, open(fname, "w"), indent=2)
        console.print(f"[green]Saved to {fname}[/green]")

if __name__ == "__main__":
    run_risk_assessment()
