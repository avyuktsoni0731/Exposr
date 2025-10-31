import asyncio
import sys
from hibp_fetcher import fetch_hibp_data

async def check_email(email: str):
    data = await fetch_hibp_data(email)
    if not data:
        print("No data or blocked.")
        return

    breaches = data.get("Breaches", [])
    pastes = data.get("Pastes")

    if breaches:
        print(f"\n⚠️ Found {len(breaches)} breach(es):\n")
        for b in breaches:
            print(f"🕵️ {b['Title']} ({b['Domain']})")
            print(f"   - Breach date: {b['BreachDate']}")
            print(f"   - Compromised Data: {', '.join(b['DataClasses'])}")
            print(f"   - Description: {b['Description']}")
            print(f"   - Pwn Count: {b['PwnCount']}")
            print()
    else:
        print("✅ No breaches found!")

    if pastes:
        print(f"🧾 Found {len(pastes)} paste(s).")
    else:
        print("🧾 No pastes found.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py email <email>")
        return

    command, arg = sys.argv[1], sys.argv[2]

    if command == "email":
        asyncio.run(check_email(arg))
    else:
        print("Unknown command:", command)

if __name__ == "__main__":
    main()
