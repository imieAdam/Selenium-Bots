import json
from datetime import datetime

def getConfigJsonData():
    with open(r".\config.json", "r+") as f:
        data = json.load(f)
        return data

def formatDateTimeString()->str:
    return '%Y-%m-%dT%H:%M:%S.%f'

def bookedDateTimeValid(bookedDateTime):
    return True if datetime.strptime(bookedDateTime, formatDateTimeString) < datetime.now() else False

def writeToConfig(data):
    with open(r".\config.json", "w") as f:    
        json.dump(data, f,  indent=4)

formatDateTimeString = '%Y-%m-%dT%H:%M:%S.%f'