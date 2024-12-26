
import mongoose from "mongoose"
import resultData from "./resultData"

const { Schema } = mongoose

const DataSchema = new Schema({
    name: {
        type: String,
        required: true,
        default: "results"
    },
    sessionId: {
        type: String,
        required: true,
    },
    createdAt: {
        type: Date,
        required: true,
        default: Date.now()
    },
    data: {
        type: [resultData.schema],
        required: true
    },
    
})

DataSchema.set('toJSON', {
    transform: (doc, returnedObject) => {
      returnedObject.id = returnedObject._id.toString()
      delete returnedObject._id
      delete returnedObject.__v
    },
  })

export default mongoose.model('PostData', DataSchema)