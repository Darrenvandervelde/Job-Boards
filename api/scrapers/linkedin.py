import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import uuid


def scrape_linkedin(keyword: str, location: str, limit=20):

    jobs = []

    url = (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={quote(keyword)}"
        f"&location={quote(location)}"
    )


    headers = {

        "User-Agent":
        (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120 Safari/537.36"
        ),

        "Accept-Language":
        "en-GB,en;q=0.9"

    }


    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )


        response.raise_for_status()


    except Exception as e:

        print(
            "LinkedIn request failed:",
            e
        )

        return []



    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    cards = soup.select(
        ".base-card"
    )


    for card in cards[:limit]:

        try:

            title = card.select_one(
                ".base-search-card__title"
            )


            company = card.select_one(
                ".base-search-card__subtitle"
            )


            location_text = card.select_one(
                ".job-search-card__location"
            )


            link = card.select_one(
                "a"
            )


            posted = card.select_one(
                "time"
            )


            job_title = (
                title.text.strip()
                if title else ""
            )


            company_name = (
                company.text.strip()
                if company else ""
            )


            job_location = (
                location_text.text.strip()
                if location_text else ""
            )


            job_url = (
                link["href"].split("?")[0]
                if link and link.get("href")
                else ""
            )


            posted_date = (
                posted.text.strip()
                if posted else ""
            )


            text = (
                job_title +
                job_location
            ).lower()



            remote = "On-site"


            if "remote" in text:

                remote = "Remote"

            elif "hybrid" in text:

                remote = "Hybrid"



            jobs.append({

                "id": str(uuid.uuid4()),

                "title": job_title,

                "company": company_name,

                "location": job_location,

                "salary": "Not Listed",

                "posted": posted_date,

                "logo": "",

                "url": job_url,

                "remote": remote,

                "type": "Unknown",

                "source": "LinkedIn"

            })


        except Exception as e:

            print(
                "LinkedIn parse error:",
                e
            )

            continue



    return jobs