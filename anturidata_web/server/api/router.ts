import { Router } from "express"
import { getResults,
    trackSession,
    postResults, 
    postTest} from "./controller"

const fileRouter = Router()

fileRouter.get('/', getResults)
fileRouter.get('/results', getResults)
fileRouter.get('/track-session', trackSession)
fileRouter.post('/track-session', trackSession)
fileRouter.post('/results', postResults)

fileRouter.post("/test", postTest)

export default fileRouter



