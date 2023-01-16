import jwt
import datetime
from jwt import ExpiredSignatureError, InvalidTokenError

ACCESS_TOKEN_EXPIRE_DAYS = 1


class Tokens:
    @staticmethod
    def create_access_token(username, secret, authz):
        try:
            payload = {
                "username": username,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
                "iat": datetime.datetime.utcnow(),
                "admin": authz,
            }
            return jwt.encode(payload, secret, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_access_token(encoded_jwt, secret):
        try:
            decoded = jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
        except ExpiredSignatureError:
            return "Signature expired. Please log in again", 403
        except InvalidTokenError:
            return "Invalid token. Please log in again", 403
        return decoded, 200