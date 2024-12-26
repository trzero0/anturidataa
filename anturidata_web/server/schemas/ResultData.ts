import mongoose from "mongoose"

//mongoose schema for data and its variables
const { Schema } = mongoose

const resultDataSchema = new Schema({
    //dates to analyse
    dates: {
        type: [String],
    },
    //zones to analyse
    zones: {
        type: [String],
    },
    //variables such as temperature or humidity
    variables: {
        type: [String]
    },
    //data gotten from the analysis
    jsonData:{
        type: [Object]
    }
})


resultDataSchema.set('toJSON', {
    transform: (doc, returnedObject) => {
      returnedObject.id = returnedObject._id.toString()
      delete returnedObject._id
      delete returnedObject.__v
    },
  })

export default mongoose.model('ResultData', resultDataSchema)