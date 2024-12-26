import time
import json

# Example data to return at the end
data = {
    "message": "Process completed successfully.",
    "temperature": 22.5,
    "humidity": 60
}

# Output the final data as JSON at the end
print(json.dumps(data))
