from datetime import datetime


def isValidTime(startTime, endTime):
    if startTime <= datetime.now():
        return {"errors": "Invalid start time"}, 400
    elif startTime >= endTime:
        return {"errors": "Invalid end time"}, 400
