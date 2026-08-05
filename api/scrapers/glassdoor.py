from playwright.sync_api import sync_playwright
from urllib.parse import quote
import uuid


def scrape_glassdoor(keyword: str, location: str, limit=20):

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
            "https://www.glassdoor.co.uk/Job/"
            f"{quote(keyword)}-jobs-SRCH_KO0,"
            f"{len(keyword)}.htm"
            f"?locT=C&locKeyword={quote(location)}"
        )



        try:

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )


            page.wait_for_timeout(5000)



        except:

            browser.close()
            return []



        # Accept cookies

        try:

            page.locator(
                "button"
            ).filter(
                has_text="Accept"
            ).click(
                timeout=3000
            )


        except:

            pass



        try:

            page.wait_for_selector(
                "[data-test='jobListing']",
                timeout=15000
            )


        except:

            browser.close()
            return []



        cards = page.locator(
            "[data-test='jobListing']"
        )



        count = min(
            cards.count(),
            limit
        )



        for i in range(count):

            card = cards.nth(i)


            try:

                title = ""

                company = ""

                location_text = ""

                salary = "Not Listed"

                posted = ""

                job_url = ""

                remote = "On-site"



                try:

                    title = (
                        card.locator(
                            "[data-test='job-title']"
                        )
                        .inner_text()
                        .strip()
                    )

                except:

                    pass



                try:

                    company = (
                        card.locator(
                            "[data-test='employer-name']"
                        )
                        .inner_text()
                        .strip()
                    )

                except:

                    pass



                try:

                    location_text = (
                        card.locator(
                            "[data-test='emp-location']"
                        )
                        .inner_text()
                        .strip()
                    )

                except:

                    pass



                try:

                    salary = (
                        card.locator(
                            "[data-test='detailSalary']"
                        )
                        .inner_text()
                        .strip()
                    )

                except:

                    pass



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



                try:

                    href = (
                        card.locator(
                            "a"
                        )
                        .first
                        .get_attribute(
                            "href"
                        )
                    )


                    if href:

                        if href.startswith("/"):

                            job_url = (
                                "https://www.glassdoor.co.uk"
                                + href
                            )

                        else:

                            job_url = href


                except:

                    pass



                text = (
                    title +
                    " " +
                    location_text
                ).lower()



                if "remote" in text:

                    remote="Remote"


                elif "hybrid" in text:

                    remote="Hybrid"



                if title:

                    jobs.append({

                        "id":str(uuid.uuid4()),

                        "title":title,

                        "company":company,

                        "location":location_text,

                        "salary":salary,

                        "posted":posted,

                        "logo":"",

                        "url":job_url,

                        "remote":remote,

                        "type":"Unknown",

                        "source":"Glassdoor"

                    })



            except:

                continue



        browser.close()



    unique = {}

    for job in jobs:

        if job["url"]:

            unique[job["url"]] = job



    return list(unique.values())