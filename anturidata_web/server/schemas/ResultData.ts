import mongoose from "mongoose"

const { Schema } = mongoose

const resultDataSchema = new Schema({
    dates: {
        type: [String],
    },
    zones: {
        type: [String],
    },
    variables: {
        type: [String]
    },
    analysisType: {
        type: [String]
    },
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