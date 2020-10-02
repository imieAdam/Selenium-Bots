import json
from datetime import datetime

def getConfigJsonData(jsonFile):
    with open(jsonFile, "r+") as f:
        data = json.load(f)
        return data

def checkBookedDate(data) ->str:
    if (data['services'][0]['service']['bookedDateTime'] and
    datetime.strptime(data['services'][0]['service']['bookedDateTime'], '%Y-%m-%dT%H:%M:%S.%f') < datetime.now()):
        data['services'][0]['service']['bookedDateTime'] = ""
    return data


def formatDateTimeString()->str:
    return '%Y-%m-%dT%H:%M:%S.%f'

def bookedDateTimeValid(bookedDateTime):
    return True if datetime.strptime(bookedDateTime, formatDateTimeString) < datetime.now() else False

def writeToConfig(jsonFile, data):
    with open(jsonFile, "w") as f:    
        json.dump(data, f,  indent=4)

formatDateTimeString = '%Y-%m-%dT%H:%M:%S.%f'