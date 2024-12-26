require('dotenv').config({path: '../.env'});
import { resolve } from "node:path";
import executePython from '../util/pythonScripts/execute';
import PostData from '../schemas/PostData';
import resultData from '../schemas/resultData';
process.env.GOOGLE_APPLICATION_CREDENTIALS = resolve(__dirname, '../util/pythonScripts/anturiPy/prj-mtp-jaak-leht-ufl-a50dabd764ca.json');


const getResults = async (req, res) => {
    try {
        const data = await PostData.find({})
        return(res.json(data))
    } catch (error) {
        console.error("Failed to fetch results:", error);
        return res.status(500).json({message: 'Error fetching data', error});
    }

}


//testifunktio
const postTest = async (req, res) => {
    const new_data = new PostData ({
        name: "moi",
        sessionId: "sfsfsdf",
        data: new resultData ({
            dates: "x-y",
            zones: ["x","t"],
            variables: ["d", "c"],
            jsonData: {
                moi: "moi",
                test: "testt"
            }
        })

    })

    try{
        const result = new_data.save()
        return res.status(200).send(result)

    }catch (error){
        return res.status(500).send(error)
    }


}

// POST requests for track-session and results, result variables go into the python code and return a json.dumps() object wich is JSON data.
// the track-session is used to track the session ID and the session data, to make sure wich client/user we will send the results to.
const trackSession = async (req, res) => {
    const sessionId = req.sessionID;
    const sessionData = req.session;

    console.log(`Client's session ID: ${sessionId}`);
    console.log(`Client's session data:`, sessionData);

    return res.send({ message: 'Session tracked', sessionId });
}


const postResults = async (req, res) => {
    const {  dates, zoneOne, zoneTwo, variableOne, variableTwo, analysisType, jsonData } = req.body;

    console.log(`Received data for id: ${dates}, ${zoneOne}, ${zoneTwo}, ${variableOne}, ${variableTwo}, ${jsonData}, ${analysisType}`);

    try {
        if (analysisType === 'ARIMA') {
            // Execute Python script to get results
            const result = await executePython(resolve(__dirname, '../util/pythonScripts/anturiPy/analyysiNodejs.py'), [dates, zoneOne, zoneTwo, variableOne, variableTwo, analysisType, jsonData])
            const postData = new PostData({
                sessionId: req.sessionID,
                data: result
            });

            // Save the new data to MongoDB
            const savedData = await postData.save();

            // Send the new data back to the client
            return res.status(201).json({message: 'Data saved', data: savedData.data});
        }
        if (analysisType === 'TimeSeries') {
            // Execute Python script to get results
            const result = await executePython(resolve(__dirname, '../util/pythonScripts/anturiPy/analyysiTimeSeries.py'), [dates, zoneOne, zoneTwo, variableOne, variableTwo, analysisType, jsonData])
            const postData = new PostData({
                sessionId: req.sessionID,
                data: result
            });
            // Save the new data to MongoDB
            const savedData = await postData.save();

            // Send the new data back to the client
            return res.status(201).json({message: 'Data saved', data: savedData.data});
        }
    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: 'Error saving data' });
    }
}


export { getResults, trackSession, postResults, postTest }