from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str

    salary: Optional[str] = "Not Listed"
    posted: Optional[str] = ""

    logo: Optional[str] = ""
    url: HttpUrl

    remote: Optional[str] = "On-site"
    type: Optional[str] = "Unknown"

    source: str


class SearchResponse(BaseModel):
    keyword: str
    location: str


class Breakdown(BaseModel):
    linkedin: int = 0
    reed: int = 0
    indeed: int = 0
    totaljobs: int = 0
    cvlibrary: int = 0
    glassdoor: int = 0


class SourceError(BaseModel):
    source: str
    message: str


class JobsResponse(BaseModel):
    success: bool

    search: SearchResponse

    scrapedAt: str

    total: int

    breakdown: Breakdown

    jobs: List[Job]

    errors: List[SourceError] = []