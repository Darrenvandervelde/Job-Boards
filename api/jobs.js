/*

import cors from "cors";
import { scrapeLinkedIn } from "../scrapers/linkedin.js";


const corsMiddleware = cors();



export default async function handler(req,res){


    corsMiddleware(req,res,async()=>{


        try{


            console.log(
                "API STARTED"
            );


            console.log(
                req.query
            );


            const jobs =
            await scrapeLinkedIn(
                req.query.keyword || "developer",
                req.query.location || "London"
            );


            console.log(
                "Jobs found:",
                jobs.length
            );


            res.status(200).json({

                success:true,

                count:
                jobs.length,

                jobs

            });


        }
        catch(error){


            console.error(
                "SCRAPER ERROR:",
                error
            );


            res.status(500).json({

                success:false,

                message:error.message

            });


        }


    });


}
    */

export default function handler(req, res) {

    console.log("API HIT");

    res.status(200).json({
        success: true,
        message: "Vercel API working"
    });

}