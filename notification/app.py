from flask import Flask, jsonify, request
from mailjet_rest import Client
from bitcoin import bitcoin_price
from SECRETS import api_secret, api_key

app = Flask(__name__)
app.config['SECRET_KEY'] = '45d36a2f17a80fa-26db09f786b8a7195'

mailjet = Client(auth=(api_key, api_secret), version='v3.1')


@app.route('/api/v1.0/sendEmail', methods=["POST"])
def sendEmail():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        body = request.json
        name = body["name"]
        email = body["email"]
        symbol = body["symbol"]

        last_update, price = bitcoin_price(symbol)

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "theodondre@gmail.com",
                        "Name": "Bitcoin Master"
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": name
                        }
                    ],
                    "Subject": "Current Bitcoin Price, from Coinmarketcap!",
                    "TextPart": "Welcome! Trader",
                    "HTMLPart": f"<h3>Dear {name}</h3> , Here is the current price of {symbol}: $ {price}, last updated on: {last_update}"
                }
            ]
        }
        mailjet.send.create(data=data)
        return jsonify({"Success": "Email Sent Successfully", "Accepted": 202}), 202
    else:
        return jsonify({"Bad Request": 400}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1957)
