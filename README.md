# ⚡ Exposr — OSINT-Powered Digital Exposure Tracker

> **Know what the internet knows about you.**
> Exposr helps you uncover your online exposure — breached accounts, leaked passwords, and public usernames — all in one simple CLI tool.

---

## 🚀 Overview

**Exposr** is an open-source intelligence (OSINT) utility that performs a privacy self-audit.
Given your **email**, **username**, and an optional **password**, it performs:

* 🔐 **Breach Lookup** — Fetches all known data breaches your email is part of (via *HaveIBeenPwned*’s hidden `unifiedsearch` endpoint using Playwright).
* 🕵️ **Username Presence Check** — Scans major sites using *Sherlock* to find where your username exists.
* 🔑 **Password Exposure Check** — Verifies if your password has ever appeared in leaks using the *Pwned Passwords API* (with privacy-safe k-anonymity lookup).
* 🧾 **Report Generator** — Creates a detailed **HTML report** summarizing all results in a human-friendly format.

---

## 💡 Why This Project

Most people have no idea their data has already been exposed — until it’s too late.
Exposr automates the OSINT *pivoting* process — using one known identifier (like your email) to uncover connected accounts, breaches, and leaks.
It empowers everyday users to **visualize their digital footprint** and take action.

---

## 🧠 How It Works

1. **Email Breach Search**

   * Uses Playwright to simulate a browser request to HIBP’s hidden `unifiedsearch` endpoint.
   * Returns all associated breaches and exposed data fields.

2. **Username Scanning**

   * Runs Sherlock to detect where the username appears across dozens of major platforms.
   * Displays results neatly using `rich` with progress bars and colorful tables.

3. **Password Safety Check**

   * Hashes your password locally using SHA-1.
   * Sends only the first 5 characters of the hash to HIBP’s password API.
   * Returns how many times it appeared in known leaks.

4. **Report Generation**

   * Aggregates all results into a clean HTML report.
   * Each section is color-coded and timestamped for clarity.

---

## 🧩 Folder Structure

```
Exposr/
├─ main.py                # CLI entrypoint with menu
├─ hibp_fetcher.py        # Playwright-based breach lookup
├─ username_scanner.py    # Sherlock-based username scan
├─ password_scanner.py    # Pwned Passwords integration
├─ report_generator.py    # Generates final HTML report
```

---

## ⚙️ Setup & Usage

### 1️⃣ Install dependencies

```bash
pip install playwright rich
playwright install chromium
git clone https://github.com/<your-username>/Exposr.git
cd Exposr
```

### 2️⃣ Install Sherlock (for username scan)

```bash
git clone https://github.com/sherlock-project/sherlock.git
cd sherlock
pip install -r requirements.txt
cd ..
```

### 3️⃣ Run Exposr

```bash
python main.py
```

You’ll be prompted for:

* Your **email**
* Your **username**
* (Optional) **password**

Then it will fetch all data and automatically generate a detailed report:

```
report.html
```

---

## 📊 Example Output

### Breach Summary

```
🕵️ MovieBoxPro (movieboxpro.app)
   - Breach date: 15 Apr 2024
   - Data: Emails, Usernames
   - Description: Over 6M accounts scraped from a vulnerable API.
   - Pwn Count: 6,009,014
```

**📸 Example breach report screenshot:**
![Breach Summary Screenshot](https://github.com/avyuktsoni0731/Exposr/blob/main/assets/breach-report.png?raw=true)

---

### Username Check (via Sherlock)

![Sherlock Username Screenshot](https://github.com/avyuktsoni0731/Exposr/blob/main/assets/sherlock-report.png?raw=true)

---

### Password Safety

![Password Check Screenshot](https://github.com/avyuktsoni0731/Exposr/blob/main/assets/password-report.png?raw=true)
---

### Complete Report

![Complete Report Screenshot_1](https://github.com/avyuktsoni0731/Exposr/blob/main/assets/report-1.png?raw=true)
![Complete Report Screenshot_2](https://github.com/avyuktsoni0731/Exposr/blob/main/assets/report-2.png?raw=true)
---

## 🧰 Tools & Techniques

| Feature        | Tool / API                                | Notes                                      |
| -------------- | ----------------------------------------- | ------------------------------------------ |
| Breach Lookup  | Playwright + HaveIBeenPwned UnifiedSearch | Reverse-engineered via browser network tab |
| Username Scan  | Sherlock                                  | Accurate OSINT username discovery          |
| Password Check | Pwned Passwords API                       | Uses SHA-1 prefix k-anonymity              |
| CLI Formatting | Rich                                      | Colorful terminal UI                       |
| Report         | HTML Generator                            | Clean readable summary                     |

---

## 🧩 OSINT Concept: Pivoting

> **Pivoting** means taking one known piece of data (like an email) and using it to find linked accounts, leaks, and metadata.
> Exposr automates this pivot — connecting dots between your email, usernames, and password exposures.

---

## 🧗 Challenges Faced

* **Cloudflare blocking** → solved by using Playwright instead of `requests`.
* **False positives** in username checks → integrated Sherlock for accuracy.
* **Rate limits** → added caching and short delays to respect APIs.

---

## 🛡️ Privacy & Ethics

* No credentials or raw passwords are ever stored.
* All processing is done locally.
* Password checks use k-anonymity — your actual password never leaves your system.
* Intended for **personal audit use only**.

---

## 📜 License

This project is open-source under the **MIT License**.
Feel free to fork, improve, or adapt responsibly.

---

## 👨‍💻 Author

**Avyukt Soni**
💼 [LinkedIn](https://www.linkedin.com/in/avyuktsoni0731) • 🌐 [GitHub](https://github.com/avyuktsoni0731)

> “What’s exposed online should never be a mystery — make it visible, make it fixable.”
