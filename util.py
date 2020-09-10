from datetime import datetime


def isBetween(start, date, end):
    return start < date < end


def isValidTime(startTime, endTime):
    validStarts = [datetime.strptime('{} 08:59:00'.format(
        startTime.date()), '%Y-%m-%d %H:%M:%S'), datetime.strptime('{} 16:31:00'.format(
            startTime.date()), '%Y-%m-%d %H:%M:%S')]

    validEnd = [datetime.strptime('{} 09:29:00'.format(
        startTime.date()), '%Y-%m-%d %H:%M:%S'), datetime.strptime('{} 17:01:00'.format(
            startTime.date()), '%Y-%m-%d %H:%M:%S')]

    if startTime <= datetime.now():
        return {"errors": "Invalid start time"}, 400
    elif startTime >= endTime:
        return {"errors": "Invalid end time"}, 400
    elif startTime.strftime("%a") == 'SUN':
        return {"errors": "Invalid date should Mon - Sat only"}, 400
    elif not isBetween(validStarts[0], startTime, validStarts[1]):
        return {"errors": "Start time should be 9:00am - 4:30pm"}, 400
    elif not isBetween(validEnd[0], endTime, validEnd[1]):
        return {"errors": "End time should be 9:30am - 5:00pm"}, 400
