from playwright.sync_api import sync_playwright
from urllib.parse import quote
import uuid


def scrape_linkedin(keyword: str, location: str, limit=20):

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )


        context = browser.new_context(
            viewport={
                "width":1600,
                "height":900
            },

            locale="en-GB",

            user_agent=(
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/137 Safari/537.36"
            )
        )


        page = context.new_page()


        url = (
            "https://www.linkedin.com/jobs/search/"
            f"?keywords={quote(keyword)}"
            f"&location={quote(location)}"
        )


        try:

            page.goto(
                url,
                wait_until="networkidle",
                timeout=60000
            )


            page.wait_for_timeout(3000)


        except:

            browser.close()
            return []


        try:

            page.locator(
                "button[action-type='ACCEPT']"
            ).click(timeout=3000)

        except:
            pass



        cards = page.locator(
            ".base-card"
        )


        count = min(
            cards.count(),
            limit
        )


        for i in range(count):

            try:

                card = cards.nth(i)


                title = (
                    card.locator(
                        ".base-search-card__title"
                    )
                    .inner_text()
                    .strip()
                )


                company = (
                    card.locator(
                        ".base-search-card__subtitle"
                    )
                    .inner_text()
                    .strip()
                )


                location_text = (
                    card.locator(
                        ".job-search-card__location"
                    )
                    .inner_text()
                    .strip()
                )


                posted = ""

                try:

                    posted = (
                        card.locator(
                            "time"
                        )
                        .inner_text()
                        .strip()
                    )

                except:
                    pass



                link = ""

                try:

                    link = (
                        card.locator(
                            "a"
                        )
                        .first
                        .get_attribute(
                            "href"
                        )
                    )

                    if link:
                        link = link.split("?")[0]

                except:
                    pass



                text = (
                    title +
                    location_text
                ).lower()



                remote = "On-site"


                if "remote" in text:

                    remote="Remote"


                elif "hybrid" in text:

                    remote="Hybrid"



                jobs.append({

                    "id":str(uuid.uuid4()),

                    "title":title,

                    "company":company,

                    "location":location_text,

                    "salary":"Not Listed",

                    "posted":posted,

                    "logo":"",

                    "url":link,

                    "remote":remote,

                    "type":"Unknown",

                    "source":"LinkedIn"

                })


            except Exception:

                continue



        browser.close()



    # remove duplicates

    results={}


    for job in jobs:

        if job["url"]:

            results[job["url"]] = job



    return list(results.values())