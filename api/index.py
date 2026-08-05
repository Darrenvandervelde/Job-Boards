from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scrapers.linkedin import scrape_linkedin


app = FastAPI(
    title="LinkedIn Job Scraper API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/")
def home():

    return {
        "status":"online",
        "service":"LinkedIn scraper"
    }



@app.get("/api/jobs")
def jobs(

    keyword:str = Query(
        "software developer"
    ),

    location:str = Query(
        "London"
    )

):

    results = scrape_linkedin(
        keyword,
        location
    )


    return {

        "count":len(results),

        "source":
        "LinkedIn",

        "jobs":
        results

    }