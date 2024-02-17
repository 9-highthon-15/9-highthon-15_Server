from flask import Flask, request
from flask_restx import Api, Resource, reqparse, fields
from models import *
from services.auth import Auth

app = Flask(__name__)
auth = Auth()

api = Api(
    app,
    version="1.0",
    title="API Swagger Docs",
    description="Highthon-team15 APP REST API",
    doc="/swagger",
)

basicSpace = api.namespace("/", description="기본 API")
authSpace = api.namespace("auth", description="인증 API")


@basicSpace.route("/")
class BasicSpace(Resource):
    def get(self):
        return "Hello World!"


@authSpace.route("/signup")
class SignUp(Resource):

    @authSpace.doc(responses={200: "Success, User Token Return"})
    @authSpace.doc(responses={400: "Bad request"})
    @authSpace.expect(
        authSpace.model(
            "SignUp",
            strict=True,
            model=signUpModel,
        ),
        validate=True,
    )
    def post(self):
        result = auth.signup(request.json)
        if result["result"]:
            return result
        else:
            return result, 400


@authSpace.route("/signin")
class SignIn(Resource):
    @authSpace.doc(responses={200: "Success, User Token Return"})
    @authSpace.doc(responses={400: "Bad request"})
    @authSpace.expect(
        authSpace.model(
            "SignIn",
            strict=True,
            model=loginModel,
        ),
        validate=True,
    )
    def post(self):
        result = auth.login(request.json)
        if result["result"]:
            return result
        else:
            return result, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
