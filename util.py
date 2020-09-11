from datetime import datetime, timezone


def isBetween(start, date, end):
    return start < date < end


def response(data, status=True, code=200, key="appointment"):
    return {"data": {key if status else "errors": data}}, code


def isValidTime(startTime, endTime):
    validStarts = [datetime.strptime('{} 08:59:00'.format(
        startTime.date()), '%Y-%m-%d %H:%M:%S'), datetime.strptime('{} 16:31:00'.format(
            startTime.date()), '%Y-%m-%d %H:%M:%S')]

    validEnd = [datetime.strptime('{} 09:29:00'.format(
        startTime.date()), '%Y-%m-%d %H:%M:%S'), datetime.strptime('{} 17:01:00'.format(
            startTime.date()), '%Y-%m-%d %H:%M:%S')]

    if startTime >= endTime:
        return response("Invalid end time", False, 400)
    elif startTime.strftime("%a") == 'SUN':
        return response("Invalid date should Mon - Sat only", False, 400)
    elif not isBetween(validStarts[0], startTime, validStarts[1]):
        return response("Start time should be 9:00am - 4:30pm", False, 400)
    elif not isBetween(validEnd[0], endTime, validEnd[1]):
        return response("End time should be 9:30am - 5:00pm", False, 400)
