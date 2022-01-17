




tingo_api = "b14d5183dd5b9ed1086a2b288310e4bb24a89e23"
start_date = '2019-01-13'
ResampleFreq = 'daily' # ["resampleFreq must be in ('daily', 'weekly','monthly', 'annually')"]

import requests
headers = {
    'Content-Type': 'application/json'
}

url = f'https://api.tiingo.com/tiingo/daily/aapl/prices?startDate={start_date}&resampleFreq={ResampleFreq}&columns=open,high,low,close,volume&token={tingo_api}'

requestResponse = requests.get(url, headers=headers)
print(requestResponse.json())

print('we are done')