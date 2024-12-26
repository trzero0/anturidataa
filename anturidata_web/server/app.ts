const express = require('express')
const cors = require("cors")
const MongoStore = require('connect-mongo');
const session = require('express-session');
import fileRouter from "./api/router"
import connectDB from "./util/db";

const app = express()

const corsOptions = {
    origin: ["http://localhost:5173"],
    credentials: true
};

app.use(cors(corsOptions));

app.use(express.json())

app.use(session({
    secret: process.env.SESSION_SECRET, // using env file secret
    resave: false,
    saveUninitialized: true,
    httpOnly: true,
    store: MongoStore.create({
        mongoUrl: process.env.MONGO_DB_URI, // using env file secret
        collectionName: 'sessions',
        ttl: 3600000 // 1 hour session duration
    }),
    cookie: {
        maxAge: 3600 * 24 * 365 * 10 * 1000, // 10 years in milliseconds
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production'
    }
}));

app.use('/', fileRouter)

// Here we listen to the requests that come to the server.
connectDB()

app.listen(3001, () => {
    console.log('Server is running on http://localhost:3001');
})
