#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import re

from lib.find_ext import get_extension

load_dotenv(override=True)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

BASE = "https://marisaoj.com"

def sanitize(s):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', s)

def main():
    os.makedirs("codes", exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()

        print("[+] Logging in...")
        page.goto(f"{BASE}/login")
        page.fill("#id_username", USERNAME)
        page.fill("#id_password", PASSWORD)
        page.click("#inner-form input[type=\"submit\"][value=\"Login\"]")
        page.wait_for_load_state("networkidle")

        print("[+] Loading AC submissions...")
        
        for pcnt in range(1, 1000):
            page.goto(f"{BASE}/user/{USERNAME}/submissions/{pcnt}")
            page.wait_for_selector("tbody tr")
            rows = page.locator("tbody tr")

            total = rows.count()

            for i in range(total):
                row = rows.nth(i)
                status_td = row.locator("td:last-child")
                if "AC" not in status_td.get_attribute("class"): 
                    continue
                
                submission_id = row.locator("td:first-child a").inner_text().strip()
                pid = row.locator("td:nth-child(2) a").inner_text().strip()
                language_text = row.locator("td:nth-child(3)").inner_text().strip()
                
                src_url = BASE + f"/submission/{submission_id}"
                problem_code = row.locator("td:nth-child(2) a").get_attribute("href").rsplit('/', 1)[1]

                print(f"[+] Downloading \"{pid}\" / submission {submission_id}")

                page.goto(src_url)
                page.wait_for_selector("pre.prettyprint")

                code = page.locator("pre.prettyprint").inner_text().encode("ascii", errors="ignore").decode("ascii")
                
                file_path = f"codes/{problem_code}{get_extension(language_text)}"
                if(not os.path.exists(file_path)):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(code)
                else:
                    print(f"[-] File {file_path} already exists, skipping...")
                    
                page.go_back()

        print("[+] DONE! All AC codes saved in /codes folder.")

if __name__ == "__main__":
    main()
