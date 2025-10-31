import asyncio, urllib.parse, re
from playwright.async_api import async_playwright
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

console = Console()

async def fetch_hibp_data(email: str):
    """Fetch breach data from HIBP unifiedsearch using Playwright."""
    encoded = urllib.parse.quote(email)
    url = f"https://haveibeenpwned.com/unifiedsearch/{encoded}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ))
        page = await context.new_page()
        response = await page.goto(url, wait_until="networkidle")
        if not response:
            print("❌ No response received.")
            await browser.close()
            return None

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            data = await response.json()
            await browser.close()
            return data
        else:
            text = await response.text()
            print("⚠️ Non-JSON response (blocked or error):", text[:200])
            await browser.close()
            return None

def clean_description(desc):
    desc = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', r"[cyan]\1[/cyan]", desc)
    desc = re.sub(r"<[^>]+>", "", desc)
    return desc.strip()

def format_date(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%d %b %Y")
    except Exception:
        return date_str

def run_hibp_check():
    email = input("Enter email to check: ").strip()
    console.print(f"🔍 [bold yellow]Fetching breach info for[/bold yellow] [cyan]{email}[/cyan] ...\n")
    data = asyncio.run(fetch_hibp_data(email))

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