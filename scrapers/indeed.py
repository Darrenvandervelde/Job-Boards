from playwright.sync_api import sync_playwright
from urllib.parse import quote
import uuid

def scrape_indeed(keyword: str, location: str):
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        context = browser.new_context(
            viewport={"width": 1600, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36",
            locale="en-GB"
        )
        page = context.new_page()
        url = (
            "https://uk.indeed.com/jobs"
            f"?q={quote(keyword)}"
            f"&l={quote(location)}"
        )
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )
        # Accept cookies if required
        try:
            page.locator(
                "#onetrust-accept-btn-handler"
            ).click(timeout=4000)
        except:
            pass
        # Wait for jobs
        page.wait_for_timeout(2000)
        page.wait_for_selector(
            ".job_seen_beacon, .resultContent",
            timeout=15000
        )
        cards = page.locator(
            ".job_seen_beacon, .resultContent"
        )
        count = cards.count()
        for i in range(count):
            card = cards.nth(i)
            try:
                title = ""
                company = ""
                location_text = ""
                salary = "Not Listed"
                posted = ""
                logo = ""
                job_type = "Unknown"
                # ----------------------------
                # TITLE
                # ----------------------------
                try:
                    title = card.locator(
                        "h2.jobTitle a"
                    ).inner_text().strip()
                except:
                    pass
                # ----------------------------
                # COMPANY
                # ----------------------------
                try:
                    company = card.locator(
                        ".companyName"
                    ).inner_text().strip()
                except:
                    pass
                # ----------------------------
                # LOCATION
                # ----------------------------
                try:
                    location_text = card.locator(
                        ".companyLocation"
                    ).inner_text().strip()
                except:
                    pass
                # ----------------------------
                # SALARY
                # ----------------------------
                try:
                    salary = card.locator(
                        ".salary-snippet-container"
                    ).inner_text().strip()
                except:
                    pass
                # ----------------------------
                # POSTED
                # ----------------------------
                try:
                    posted = card.locator(
                        ".date"
                    ).inner_text().strip()
                except:
                    pass
                # ----------------------------
                # URL
                # ----------------------------
                job_url = ""
                try:
                    href = card.locator(
                        "h2.jobTitle a"
                    ).get_attribute("href")
                    if href:
                        if href.startswith("http"):
                            job_url = href
                        else:
                            job_url = "https://uk.indeed.com" + href
                except:
                    pass
                # ----------------------------
                # LOGO
                # ----------------------------
                try:
                    logo = card.locator("img").get_attribute("src")
                except:
                    pass
                # ----------------------------
                # REMOTE
                # ----------------------------
                remote = "On-site"
                text = (
                    title
                    + " "
                    + location_text
                ).lower()
                if "remote" in text:
                    remote = "Remote"
                elif "hybrid" in text:
                    remote = "Hybrid"
                # ----------------------------
                # TYPE
                # ----------------------------
                try:
                    attrs = card.locator(
                        ".attribute_snippet"
                    ).all_inner_texts()
                    joined = " ".join(attrs).lower()
                    if "full-time" in joined:
                        job_type = "Full-time"
                    elif "part-time" in joined:
                        job_type = "Part-time"
                    elif "contract" in joined:
                        job_type = "Contract"
                    elif "temporary" in joined:
                        job_type = "Temporary"
                    elif "internship" in joined:
                        job_type = "Internship"
                except:
                    pass
                if title:
                    jobs.append({
                        "id": str(uuid.uuid4()),
                        "title": title,
                        "company": company,
                        "location": location_text,
                        "salary": salary,
                        "posted": posted,
                        "logo": logo or "",
                        "url": job_url,
                        "remote": remote,
                        "type": job_type,
                        "source": "Indeed"
                    })
            except:
                continue
        browser.close()

    # Remove duplicates
    unique = {}
    for job in jobs:
        unique[job["url"]] = job
    return list(unique.values())