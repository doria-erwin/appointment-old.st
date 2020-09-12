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


def isValidDates(request):
    try:
        start = datetime.strptime('{}'.format(
            request.args.get('startDate')), '%Y-%m-%d')
    except:
        return response("invalid startDate format should be YYYY-mm-dd", False, 422)

    try:
        end = datetime.strptime('{}'.format(
            request.args.get('endDate')), '%Y-%m-%d')
    except:
        return response("invalid endDate format should be YYYY-mm-dd", False, 422)

    if start > end:
        return response("invalid endDate", False, 422)
    elif start == end:
        return response("startDate and endDate should not be equal", False, 422)
    elif start is None or end is None:
        return response("required query parameters startDate and endDate", False, 422)
