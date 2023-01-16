### Python Application to Email Current Bitcoin Price
  - Docker and Kubernetes

### Python Demo
  - Symbols: `BTC, ETH, USDT, DOGE, LTC`
```python
import requests
import json

url = "http://0.0.0.0:1957/api/v1.0/sendEmail"

payload = json.dumps({
  "name": "World Boss",
  "email": "user.aerogramme@gmail.com",
  "symbol": "BTC"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


```

### Curl Demo
```shell
curl --location --request POST 'http://0.0.0.0:1957/api/v1.0/sendEmail' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "World Boss",
    "email": "user.aerogramme@gmail.com",
    "symbol": "BTC"
}'
```

### References
  - https://pro.coinmarketcap.com/signup/
  - https://www.mailjet.com/
  - https://github.com/mailjet/mailjet-apiv3-python