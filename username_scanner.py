import asyncio
import httpx
import json
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

console = Console()

async def check_platform(client, platform, url):
    try:
        response = await client.get(url, timeout=8)
        if response.status_code == 200:
            return (platform, True, url)
        elif response.status_code == 404:
            return (platform, False, url)
        else:
            return (platform, None, f"HTTP {response.status_code}")
    except Exception as e:
        return (platform, None, f"{type(e).__name__}")

async def probe_username(username, sites_file="data/sites.json"):
    with open(sites_file, "r") as f:
        PLATFORMS = json.load(f)

    results = []
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Probing platforms..."),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("probe", total=len(PLATFORMS))
            for platform, pattern in PLATFORMS.items():
                url = pattern.format(user=username)
                tasks.append(check_platform(client, platform, url))

            for coro in asyncio.as_completed(tasks):
                res = await coro
                results.append(res)
                progress.update(task, advance=1)

    return results

def display_results(username, results):
    console.print(f"\n🔍 [bold cyan]Results for username:[/bold cyan] {username}\n")

    table = Table(title="Username Probe Results", show_lines=True)
    table.add_column("Platform", style="bold white")
    table.add_column("Status", style="bold")
    table.add_column("Profile / Info", style="cyan")

    for platform, found, info in results:
        if found is True:
            status = "[green]✅ Found[/green]"
            link = f"[link={info}]{info}[/link]"
        elif found is False:
            status = "[red]❌ Not Found[/red]"
            link = "-"
        else:
            status = "[yellow]⚠️ Unknown[/yellow]"
            link = f"[dim]{info}[/dim]"
        table.add_row(platform, status, link)

    console.print(table)
    console.print("[dim]All platforms checked in parallel. ⚡[/dim]")

def run_username_scan():
    username = input("Enter username to probe: ").strip()
    results = asyncio.run(probe_username(username))
    display_results(username, results)
