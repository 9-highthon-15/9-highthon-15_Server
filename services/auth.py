import jwt
import uuid
import bcrypt
from services.db import DB
from services.valid import *
from services.config import JWT_SECRET

db = DB()


class Auth:
    def __init__(self):
        pass

    def signup(self, data):
        validResult = signUpValidator(
            data["email"],
            data["password"],
            data["nickname"],
            data["phone"],
            data["region"],
        )
        if validResult[0] is False:
            return {
                "result": False,
                "code": f"VALIDATION_ERROR_{validResult[1].upper()}",
                "message": validResult[2],
            }

        query = """
            SELECT uuid FROM user WHERE email = ?
        """
        result = db.query(query, (data["email"],))
        if result:
            return {
                "result": False,
                "code": "EMAIL_ALREADY_EXIST",
                "message": "Already Exist Email",
            }

        query = """
            INSERT INTO user (uuid, email, password, nickname, phone, region)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        db.execute(
            query,
            (
                str(uuid.uuid4()),
                data["email"],
                self.passwordHashing(data["password"]),
                data["nickname"],
                data["phone"],
                data["region"],
            ),
        )

        query = """
            SELECT uuid FROM user WHERE email = ?
        """
        result = db.query(query, (data["email"],))
        if not result:
            return {
                "result": False,
                "code": "AUTH_SERVER_ERROR",
                "message": "Auth Server Error",
            }

        token = self.generateToken(result[0][0])

        return {"result": True, "code": "SIGNUP_SUCCESS", "message": token}

    def login(self, data):
        query = """
            SELECT uuid, password FROM user WHERE email = ?
        """
        result = db.query(query, (data["email"],))
        if not result:
            return {
                "result": False,
                "code": "INVALID_CREDENTIAL",
                "message": "Invalid Credential",
            }

        if not self.passwordCheck(data["password"], result[0][1]):
            return {
                "result": False,
                "code": "INVALID_CREDENTIAL",
                "message": "Invalid Credential",
            }

        token = self.generateToken(result[0][0])

        return {"result": True, "code": "LOGIN_SUCCESS", "message": token}

    def generateToken(self, uuid):
        query = """
            SELECT uuid FROM user WHERE uuid = ?
        """
        result = db.query(query, (uuid,))
        if not result:
            return {
                "result": False,
                "code": "INVALID_UUID",
                "message": "Invalid UUID",
            }

        payload = {"uuid": uuid}
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return token

    def passwordHashing(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def passwordCheck(self, password, hashedPassword):
        return bcrypt.checkpw(password.encode("utf-8"), hashedPassword.encode("utf-8"))

    def userCheck(self, token):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {
                "result": False,
                "code": "EXPIRED_SIGNATURE",
                "message": "ExpiredSignatureError",
            }
        except jwt.InvalidTokenError:
            return {
                "result": False,
                "code": "INVALID_TOKEN",
                "message": "InvalidTokenError",
            }
        except:
            return {
                "result": False,
                "code": "UNKNOWN_TOKEN_ERROR",
                "message": "Unknown Token Error",
            }

        query = """
            SELECT uuid FROM user WHERE uuid = ?
        """
        result = db.query(query, (payload["uuid"],))
        if not result:
            return {
                "result": False,
                "code": "INVALID_UUID",
                "message": "Invalid UUID",
            }

        return {"result": True, "code": "USER_VALID", "message": payload["uuid"]}
