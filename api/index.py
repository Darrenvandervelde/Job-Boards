from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from mangum import Mangum


# Import scrapers
from scrapers.indeed import scrape_indeed
from scrapers.linkedin import scrape_linkedin
from scrapers.reed import scrape_reed
from scrapers.totaljobs import scrape_totaljobs
from scrapers.cvlibrary import scrape_cvlibrary
from scrapers.glassdoor import scrape_glassdoor



app = FastAPI(
    title="ABS Recruitment Job API"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def deduplicate(jobs):

    seen = set()

    output = []


    for job in jobs:

        url = job.get("url")


        if url and url not in seen:

            seen.add(url)

            output.append(job)


    return output




@app.get("/")
def home():
    return {
        "status": "running",
        "service": "ABS Recruitment Job API"
    }


@app.get("/api/jobs")
def jobs(

    keyword: str = Query(
        "software developer"
    ),

    location: str = Query(
        "London"
    ),

    sources: str = Query(
        "linkedin,reed,indeed,totaljobs,cvlibrary,glassdoor"
    )

):


    requested = {

        s.strip().lower()

        for s in sources.split(",")

        if s.strip()

    }



    all_jobs = []

    errors = []




    def safe_scrape(name, func):

        try:

            return func(
                keyword,
                location
            )


        except Exception as e:


            errors.append({

                "source": name,

                "message": str(e)

            })


            return []





    with ThreadPoolExecutor(
        max_workers=6
    ) as executor:


        futures = []



        scraper_map = {


            "linkedin": scrape_linkedin,

            "reed": scrape_reed,

            "indeed": scrape_indeed,

            "totaljobs": scrape_totaljobs,

            "cvlibrary": scrape_cvlibrary,

            "glassdoor": scrape_glassdoor

        }




        for source, scraper in scraper_map.items():


            if source in requested:


                futures.append(

                    executor.submit(

                        safe_scrape,

                        source,

                        scraper

                    )

                )




        for future in futures:

            all_jobs.extend(
                future.result()
            )




    all_jobs = deduplicate(
        all_jobs
    )



    breakdown = {


        "linkedin":0,

        "reed":0,

        "indeed":0,

        "totaljobs":0,

        "cvlibrary":0,

        "glassdoor":0

    }



    for job in all_jobs:


        source = (

            job.get(
                "source",
                ""
            )

            .lower()

            .replace(
                "-",
                ""
            )

        )



        if source == "cvlibrary":

            breakdown["cvlibrary"] += 1


        elif source in breakdown:

            breakdown[source] += 1





    return {


        "success": True,


        "search": {


            "keyword": keyword,


            "location": location

        },


        "scrapedAt":

            datetime.utcnow()
            .isoformat()
            + "Z",


        "total":

            len(all_jobs),


        "breakdown":

            breakdown,


        "jobs":

            all_jobs,


        "errors":

            errors

    }
handler = Mangum(app)
