from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from scrapers.linkedin import scrape_linkedin


app = FastAPI(
    title="LinkedIn Job Scraper API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():

    return {
        "status": "online",
        "service": "LinkedIn scraper API"
    }



@app.get("/api/jobs")
def jobs(

    keyword: str = Query(
        "software developer"
    ),

    location: str = Query(
        "London"
    )

):

    try:

        results = scrape_linkedin(
            keyword,
            location
        )


        return {

            "success": True,

            "count": len(results),

            "source": "LinkedIn",

            "jobs": results

        }


    except Exception as e:

        return {

            "success": False,

            "error": str(e),

            "jobs": []

        }



handler = Mangum(app)