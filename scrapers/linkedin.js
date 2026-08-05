import axios from "axios";
import cheerio from "cheerio";


export async function scrapeLinkedIn(
    keyword,
    location
){


    const url =
    `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(keyword)}&location=${encodeURIComponent(location)}`;



    const response =
    await axios.get(
        url,
        {

            headers:{

                "User-Agent":
                "Mozilla/5.0"

            }

        }
    );



    const $ =
    cheerio.load(
        response.data
    );


    const jobs=[];



    $(".base-card").each(
        (i,element)=>{


            const title =
            $(element)
            .find(".base-search-card__title")
            .text()
            .trim();



            const company =
            $(element)
            .find(".base-search-card__subtitle")
            .text()
            .trim();



            const location =
            $(element)
            .find(".job-search-card__location")
            .text()
            .trim();



            if(title){

                jobs.push({

                    title,

                    company,

                    location,

                    source:"LinkedIn"

                });

            }


        }
    );



    return jobs;

}