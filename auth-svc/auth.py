import os
from flask import Flask, request
from flask_mysqldb import MySQL
from access_token import Tokens

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


@server.route("/api/v1.0/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing Credentials", 401
    # check DB for username and password
    cur = mysql.connection.cursor()
    results = cur.execute("SELECT email, password FROM user WHERE email=%s", (auth.username,))
    if results > 0:
        users_row = cur.fetchone()
        email = users_row[0]
        password = users_row[1]
        if auth.username != email or auth.password != password:
            return "Invalid Credentials", 401
        else:
            return Tokens.create_access_token(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid Credentials", 401


@server.route("/api/v1.0/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "Missing Credentials", 401
    encoded_jwt = encoded_jwt.split(" ")[1]
    return Tokens.decode_access_token(encoded_jwt, os.environ.get("JWT_SECRET"))


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=5000)
