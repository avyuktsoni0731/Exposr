import asyncio, datetime
from rich.console import Console
from hibp_fetcher import fetch_hibp_data
from username_scanner import run_sherlock
from password_scanner import pwned_password_count

console = Console()

async def generate_report():
    email = input("Enter email (or leave blank to skip): ").strip()
    username = input("Enter username (or leave blank to skip): ").strip()
    password = input("Enter password to check (or leave blank to skip): ").strip()

    console.print(f"\n🧾 [bold cyan]Generating OSINT Report for[/bold cyan] {email or username} ...")

    hibp_data = await fetch_hibp_data(email) if email else None
    breaches = hibp_data.get("Breaches", []) if isinstance(hibp_data, dict) else []

    profiles = run_sherlock(username) if username else []

    pw_count = None
    if password:
        console.print("🔐 Checking password (privacy-safe k-anonymity)...")
        pw_count = pwned_password_count(password)

    now = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    html = f"""<html><head><meta charset="utf-8"><title>OSINT Report - {email or username}</title>
    <style>
      body{{font-family:Arial;color:#222;background:#f6f6f6;padding:18px}}
      .sec{{background:#fff;padding:12px;border-radius:8px;margin-bottom:14px;box-shadow:0 1px 3px #ccc}}
      a{{color:#0366d6;text-decoration:none}}
    </style></head><body>
    <h1>🔍 OSINT Report</h1>
    <p><b>Generated:</b> {now}</p>
    <p><b>Email:</b> {email or '-'}<br><b>Username:</b> {username or '-'}</p>

    <div class='sec'><h2>📧 Breach Summary ({len(breaches)} found)</h2>"""
    for b in breaches:
        title = b.get("Title") or b.get("Name") or "Unknown"
        domain = b.get("Domain") or "N/A"
        date = b.get("BreachDate") or ""
        data = ", ".join(b.get("DataClasses") or [])
        pcount = f"{b.get('PwnCount'):,}" if b.get("PwnCount") else "—"
        desc = (b.get("Description") or "")[:800].replace("\n", "<br>")
        html += f"<div style='border-bottom:1px solid #eee;padding:8px 0;'><b>{title}</b> ({domain})<br><small>{date} • {data} • PwnCount: {pcount}</small><p>{desc}</p></div>"

    html += "</div><div class='sec'><h2>🕵️ Profiles Found (Sherlock)</h2><ul>"
    for u in profiles:
        html += f"<li><a href='{u}' target='_blank'>{u}</a></li>"
    html += "</ul></div>"

    html += "<div class='sec'><h2>🔐 Password Check</h2>"
    if not password:
        html += "<p>No password provided.</p>"
    elif pw_count is None:
        html += "<p>Check unavailable or password not found in known breaches.</p>"
    else:
        html += f"<p style='color:red;'>Password found <b>{pw_count:,}</b> times in known breaches — change it immediately.</p>"
    html += "</div>"

    html += "<div class='sec'><h2>🔧 Quick Actions</h2><ul>"
    if pw_count and pw_count > 0:
        html += "<li>Change the compromised password immediately.</li>"
    if any("password" in (d or "").lower() for b in breaches for d in (b.get("DataClasses") or [])):
        html += "<li>Some breaches included passwords — rotate affected accounts.</li>"
    if breaches:
        html += "<li>Enable 2FA on important accounts (email, social, etc.).</li>"
    html += "<li>Monitor for new breaches regularly.</li></ul></div></body></html>"

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)
    console.print(f"\n✅ [green]Report saved as 'report.html'[/green]\n")