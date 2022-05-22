#Constants
MAX_LENGTH = 200
MAX_DIGITS = 10
DECIMAL_PLACES = 2
MAX_THREADS = 30
HTTP_READ_TIMEOUT = 60

def sort_by_time_stamp(logs) -> list:
    """
    Returns list of logs Sorted by time stamp

            Parameters:
                    logs: iterable consists of logs

            Returns:
                    data (list): list of logs Sorted by time stamp
    """
    data = [log.split(" ") for log in logs]
    data = sorted(data, key=lambda elem: elem[1])
    return data

def response_format(raw_data) -> list:
    """Formats the response"""
    response = []
    for timestamp, data in raw_data.items():
        entry = {'timestamp': timestamp}
        data = {k: data[k] for k in sorted(data.keys())}
        logs = [{'exception': exception, 'count': count} for exception, count in data.items()]
        entry['logs'] = logs
        response.append(entry)
    return response

def aggregate(cleaned_logs) -> dict:
    """ Aggregates the cleaned logs
        Returns:
                    data (dict): Aggregated logs
    """
    data = {}
    for log in cleaned_logs:
        [key, text] = log
        value = data.get(key, {})
        value[text] = value.get(text, 0)+1
        data[key] = value
    return data


def transform(logs) -> list:
    """Transforms the log in a particular format
        Returns:
                    result (list): transform logs
    """
    result = []
    for log in logs:
        [_, timestamp, text] = log
        text = text.rstrip()
        timestamp = datetime.utcfromtimestamp(int(int(timestamp)/1000))
        hours, minutes = timestamp.hour, timestamp.minute
        key = ''

        if minutes >= 45:
            if hours == 23:
                key = "{:02d}:45-00:00".format(hours)
            else:
                key = "{:02d}:45-{:02d}:00".format(hours, hours+1)
        elif minutes >= 30:
            key = "{:02d}:30-{:02d}:45".format(hours, hours)
        elif minutes >= 15:
            key = "{:02d}:15-{:02d}:30".format(hours, hours)
        else:
            key = "{:02d}:00-{:02d}:15".format(hours, hours)

        result.append([key, text])
        print(key)

    return result


def normalize(expense) -> list:
    """ Normalizes expense"""
    user_balances = expense.users.all()
    dues = {}
    for user_balance in user_balances:
        dues[user_balance.user] = dues.get(user_balance.user, 0) + user_balance.amount_lent \
                                  - user_balance.amount_owed
    dues = [(k, v) for k, v in sorted(dues.items(), key=lambda item: item[1])]
    start = 0
    end = len(dues) - 1
    balances = []
    while start < end:
        amount = min(abs(dues[start][1]), abs(dues[end][1]))
        user_balance = {"from_user": dues[start][0].id, "to_user": dues[end][0].id, "amount": amount}
        balances.append(user_balance)
        dues[start] = (dues[start][0], dues[start][1] + amount)
        dues[end] = (dues[end][0], dues[end][1] - amount)
        if dues[start][1] == 0:
            start += 1
        else:
            end -= 1
    return balances


def reader(url, timeout):
    """Reads an url within specified time"""
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


def multi_threaded_reader(urls, num_threads) -> list:
    """
        Read multiple files through HTTP with threadpooling
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_url = {executor.submit(reader, url, HTTP_READ_TIMEOUT): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            result.extend(data.split("\n"))
    result = sorted(result, key=lambda elem:elem[1])
    return result