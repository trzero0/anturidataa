
import mongoose from "mongoose"
import resultData from "./resultData"

//mongoose schema for storing analysis data to mongodb
const { Schema } = mongoose

const DataSchema = new Schema({
    //name
    name: {
        type: String,
        required: true,
        default: "results"
    },
    //sessionId for the user
    sessionId: {
        type: String,
        required: true,
    },
    //timestamp
    createdAt: {
        type: Date,
        required: true,
        default: Date.now()
    },
    //data as resultData object
    data: {
        type: [resultData.schema],
        required: true
    },
    //graphtype to use for this data (set at frontend)
    graphType: {
        type: String,
    }
    
})

DataSchema.set('toJSON', {
    transform: (doc, returnedObject) => {
      returnedObject.id = returnedObject._id.toString()
      delete returnedObject._id
      delete returnedObject.__v
    },
  })

export default mongoose.model('PostData', DataSchema)