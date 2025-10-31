import subprocess, tempfile, re, os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def parse_sherlock_output(text):
    urls = re.findall(r"https?://[^\s,;]+", text)
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u.rstrip(".,;"))
    return out

def run_sherlock(username, timeout=120):
    tmpdir = tempfile.mkdtemp(prefix="sherlock_out_")
    out_path = Path(tmpdir) / f"{username}.txt"
    cmd = ["sherlock", username, "--print-found", "--output", str(out_path)]

    console.print(f"[bold blue]Running Sherlock for username:[/bold blue] [cyan]{username}[/cyan]\n")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        console.print("[red]Sherlock timed out. Try increasing timeout or run with fewer sites.[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Error launching Sherlock:[/red] {e}")
        return None

    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    try:
        if out_path.exists():
            text += "\n" + out_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        pass

    try:
        if out_path.exists():
            out_path.unlink()
        os.rmdir(tmpdir)
    except Exception:
        pass

    return parse_sherlock_output(text)

def display_results(username, urls):
    console.print(f"\n🔍 [bold cyan]Sherlock results for username:[/bold cyan] {username}\n")
    table = Table(title="Verified Username Footprint (Sherlock)", show_lines=True)
    table.add_column("Platform / Host", style="bold white")
    table.add_column("Profile URL", style="cyan", overflow="fold")

    if not urls:
        table.add_row("-", "[yellow]No profiles found (or Sherlock failed)[/yellow]")
        console.print(table)
        return

    for u in urls:
        host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        table.add_row(host, f"[link={u}]{u}[/link]")

    console.print(table)

def run_username_scan():
    username = input("Enter username to probe: ").strip()
    if not username:
        console.print("[red]No username provided.[/red]")
        return
    urls = run_sherlock(username)
    display_results(username, urls)