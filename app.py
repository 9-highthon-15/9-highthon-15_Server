import werkzeug
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_restx import Api, Resource, reqparse, fields

from models import *
from services.auth import Auth
from services.post import Post

app = Flask(__name__)
auth = Auth()
post = Post()

api = Api(
    app,
    version="1.0",
    title="API Swagger Docs",
    description="Highthon-team15 APP REST API",
    doc="/swagger",
    authorizations={
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
    },
)

basicSpace = api.namespace("/", description="기본 API")
authSpace = api.namespace("auth", description="인증 API")
postSpace = api.namespace("post", description="게시글 API")
searchSpace = api.namespace("search", description="검색 API")


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


@basicSpace.route("/saveImage")
class SaveImage(Resource):
    @basicSpace.doc(security="Bearer Auth")
    @basicSpace.doc(responses={200: "Success, No Return"})
    @basicSpace.doc(responses={400: "Bad request"})
    @basicSpace.doc(responses={401: "Unauthorized"})
    def post(self):
        token = request.headers.get("Authorization")
        if not token:
            return {
                "result": False,
                "code": "UNAUTHORIZED",
                "message": "Unauthorized",
            }, 401

        parser = reqparse.RequestParser()
        parser.add_argument(
            "file",
            type=werkzeug.datastructures.FileStorage,
            required=True,
            location="files",
        )
        args = parser.parse_args()

        result = auth.saveImage(token, args["file"])

        if result["result"]:
            return result
        else:
            return result, 400


@postSpace.route("/write")
class Write(Resource):
    @postSpace.doc(security="Bearer Auth")
    @postSpace.doc(responses={200: "Success, Post ID Return"})
    @postSpace.doc(responses={400: "Bad request"})
    @postSpace.doc(responses={401: "Unauthorized"})
    @postSpace.expect(
        postSpace.model(
            "Write",
            strict=True,
            model=writeModel,
        ),
        validate=True,
    )
    def post(self):
        token = request.headers.get("Authorization")
        if not token:
            return {
                "result": False,
                "code": "UNAUTHORIZED",
                "message": "Unauthorized",
            }, 401
        result = post.write(request.json, token)
        if result["result"]:
            return result
        else:
            return result, 400


@postSpace.route("/read/<int:id>")
class Read(Resource):
    @postSpace.doc(responses={200: "Success, Post Data Return"})
    @postSpace.doc(responses={400: "Bad request"})
    def get(self, id):
        result = post.read({"id": id})
        if result["result"]:
            return result
        else:
            return result, 400


@postSpace.route("/read")
class ReadAll(Resource):
    @postSpace.doc(responses={200: "Success, Post Data Return"})
    @postSpace.doc(responses={400: "Bad request"})
    def get(self):
        result = post.readAll()
        if result["result"]:
            return result
        else:
            return result, 400


@searchSpace.route("/")
class Search(Resource):
    @searchSpace.doc(responses={200: "Success, Post Data Return"})
    @searchSpace.doc(responses={400: "Bad request"})
    @searchSpace.doc(params={"keyword": "검색 키워드"})
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("keyword", type=str, required=True)
        args = parser.parse_args()

        result = post.search(args)
        if result["result"]:
            return result
        else:
            return result, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
