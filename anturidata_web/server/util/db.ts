import mongoose from "mongoose"
const dotenv = require('dotenv')

//establish mongodb connection
export default async function connectDB(uri = process.env.MONGO_DB_URI as string) {
    mongoose.connect(uri = process.env.MONGO_DB_URI as string).then(()=>{
        console.log("Connected to database");
    }).catch((error)=>{
        console.log("Connection failed", error);
    });
}
