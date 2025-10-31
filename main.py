import asyncio
import sys
import re
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from hibp_fetcher import fetch_hibp_data

console = Console()

def format_date(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%d %b %Y")
    except Exception:
        return date_str

def clean_description(desc):
    desc = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', r"[cyan]\1[/cyan]", desc)
    desc = re.sub(r"<[^>]+>", "", desc)
    return desc.strip()

async def check_email(email: str):
    console.print(f"🔍 [bold yellow]Fetching breach info for[/bold yellow] [cyan]{email}[/cyan] ...\n")
    data = await fetch_hibp_data(email)

    if not data:
        console.print("[red]❌ No data or blocked by HIBP.[/red]")
        return

    breaches = data.get("Breaches", [])
    pastes = data.get("Pastes")

    if breaches:
        console.print(f"⚠️ [bold red]Found {len(breaches)} breach(es):[/bold red]\n")

        for b in breaches:
            table = Table(show_header=False, box=None)
            table.add_row("🕵️ [bold cyan]Title[/bold cyan]", f"[white]{b['Title']}[/white]")
            table.add_row("🌐 [bold cyan]Domain[/bold cyan]", f"[green]{b['Domain'] or 'N/A'}[/green]")
            table.add_row("📅 [bold cyan]Breach Date[/bold cyan]", f"[magenta]{format_date(b['BreachDate'])}[/magenta]")
            table.add_row("💾 [bold cyan]Compromised Data[/bold cyan]", f"[white]{', '.join(b['DataClasses'])}[/white]")
            table.add_row("👥 [bold cyan]Pwn Count[/bold cyan]", f"[yellow]{b['PwnCount']:,}[/yellow]")
            desc = clean_description(b.get("Description", ""))
            table.add_row("📝 [bold cyan]Description[/bold cyan]", f"[white]{desc}[/white]")

            console.print(Panel(table, title=f"🕵️ [bold red]{b['Title']}[/bold red]", border_style="bright_yellow"))
    else:
        console.print("[bold green]✅ No breaches found![/bold green]")

    console.print()
    if pastes:
        console.print(f"🧾 [yellow]Found {len(pastes)} paste(s).[/yellow]")
    else:
        console.print("[bold blue]🧾 No pastes found.[/bold blue]")

def main():
    if len(sys.argv) < 3:
        console.print("[bold red]Usage:[/bold red] python main.py email <email>")
        return

    command, arg = sys.argv[1], sys.argv[2]
    if command == "email":
        asyncio.run(check_email(arg))
    else:
        console.print(f"[red]Unknown command:[/red] {command}")

if __name__ == "__main__":
    main()
