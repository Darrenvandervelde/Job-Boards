import cors from "cors";
import { scrapeLinkedIn } from "../scrapers/linkedin.js";


const corsMiddleware = cors({
    origin:"*"
});


export default async function handler(req,res){

    corsMiddleware(
        req,
        res,
        async()=>{

            try{


                const keyword =
                req.query.keyword ||
                "software developer";


                const location =
                req.query.location ||
                "London";


                const jobs =
                await scrapeLinkedIn(
                    keyword,
                    location
                );


                res.status(200).json({

                    success:true,

                    source:"LinkedIn",

                    count:jobs.length,

                    jobs

                });



            }
            catch(error){


                console.error(error);


                res.status(500).json({

                    success:false,

                    error:error.message

                });


            }

        }
    );

}