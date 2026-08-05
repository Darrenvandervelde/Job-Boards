import requests
from bs4 import BeautifulSoup

from models.job import Job


def scrape_linkedin(
        keyword="software developer",
        location="London"
):

    jobs = []

    url = (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={keyword.replace(' ','%20')}"
        f"&location={location.replace(' ','%20')}"
    )


    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }


    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )


    if response.status_code != 200:
        return []


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    cards = soup.select(
        "div.base-card"
    )


    for card in cards[:20]:

        title = card.select_one(
            "h3"
        )

        company = card.select_one(
            "h4"
        )

        location = card.select_one(
            ".job-search-card__location"
        )

        link = card.select_one(
            "a"
        )


        jobs.append(
            Job(
                title=
                title.text.strip()
                if title else "Unknown",

                company=
                company.text.strip()
                if company else "Unknown",

                location=
                location.text.strip()
                if location else "Unknown",

                url=
                link["href"]
                if link else None
            )
        )


    return jobs