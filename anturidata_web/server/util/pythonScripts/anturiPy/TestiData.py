import json
import pandas as pd
import sys
import os
import requests

dates = sys.argv[1]
zoneOne = sys.argv[2]
zoneTwo = sys.argv[3]
variableOne = sys.argv[4]
variableTwo = sys.argv[5]
jsonData = sys.argv[6]

data = {
           "dates": [2024-11-10,2024-11-11,2024-11-12],
           "zoneOne": "zone1",
           "zoneTwo": "zone2",
           "variableOne": "temperature",
           "variableTwo": "humidity",
           "jsonData": [
               {
                   "zone": "zone1",
                   "forecast": [
                       ["2024-11-01", -1.23],
                       ["2024-11-02", 2.34],
                       ["2024-11-03", 1.45],
                       ["2024-11-04", -0.67],
                       ["2024-11-05", -1.12],
                       ["2024-11-06", 3.21],
                       ["2024-11-07", 2.12],
                       ["2024-11-08", -0.89],
                       ["2024-11-09", 0.45],
                       ["2024-11-10", -1.56],
                       ["2024-11-11", 1.23],
                       ["2024-11-12", 0.67]
                   ]
               },
               {
                   "zone": "zone2",
                   "forecast": [
                       ["2024-11-01", 0.34],
                       ["2024-11-02", -1.56],
                       ["2024-11-03", 2.34],
                       ["2024-11-04", 1.23],
                       ["2024-11-05", -0.89],
                       ["2024-11-06", 1.56],
                       ["2024-11-07", 0.45],
                       ["2024-11-08", -1.23],
                       ["2024-11-09", 2.12],
                       ["2024-11-10", 0.56],
                       ["2024-11-11", -0.34],
                       ["2024-11-12", 1.78]
                   ]
               }
           ]
       }



print(json.dumps(data))