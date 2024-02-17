import json
from services.db import DB
from services.valid import *
from services.auth import Auth
from services.utils import timeDiff

db = DB()
auth = Auth()


class Post:
    def __init__(self):
        pass

    def write(self, data, token):
        uuid = auth.userCheck(token)
        if uuid["result"] == False:
            return uuid
        uuid = uuid["message"]

        validResult = writeValidator(
            data["title"], data["content"], data["tags"], data["give"]
        )
        if validResult[0] is False:
            return {
                "result": False,
                "code": f"VALIDATION_ERROR_{validResult[1].upper()}",
                "message": validResult[2],
            }

        tags = json.dumps(data["tags"])

        query = """
            INSERT INTO post (uuid, title, content, tags, give)
            VALUES (?, ?, ?, ?, ?)
        """
        db.execute(query, (uuid, data["title"], data["content"], tags, data["give"]))

        query = """
            SELECT id FROM post WHERE uuid = ? ORDER BY id DESC
        """
        result = db.query(query, (uuid,))

        if not result:
            return {
                "result": False,
                "code": "DB_ERROR",
                "message": "DB Error",
            }

        return {
            "result": True,
            "id": result[0][0],
        }

    def read(self, data):
        postID = data["id"]
        query = """
            SELECT * FROM post WHERE id = ?
        """
        result = db.query(query, (postID,))
        if not result:
            return {
                "result": False,
                "code": "POST_NOT_EXIST",
                "message": "Post Not Exist",
            }
        postResult = result[0]

        query = """
            SELECT nickname, image FROM user WHERE uuid = ?
        """
        userResult = db.query(query, (postResult[1],))
        if not userResult:
            return {
                "result": False,
                "code": "USER_NOT_EXIST",
                "message": "User Not Exist",
            }
        userResult = list(userResult[0])

        return {
            "result": True,
            "id": postResult[0],
            "author": userResult[0],
            "authorImage": userResult[1],
            "title": postResult[2],
            "content": postResult[3],
            "tags": json.loads(postResult[4]),
            "give": postResult[5],
            "created_at": timeDiff(postResult[6]),
        }

    def readAll(self):
        query = """
            SELECT * FROM post ORDER BY id DESC
        """
        result = db.query(query)
        if not result:
            return {
                "result": False,
                "code": "POST_NOT_EXIST",
                "message": "Post Not Exist",
            }
        postResult = []
        for post in result:
            query = """
                SELECT nickname, image FROM user WHERE uuid = ?
            """
            userResult = db.query(query, (post[1],))
            if not userResult:
                return {
                    "result": False,
                    "code": "USER_NOT_EXIST",
                    "message": "User Not Exist",
                }
            userResult = list(userResult[0])

            postResult.append(
                {
                    "id": post[0],
                    "author": userResult[0],
                    "authorImage": userResult[1],
                    "title": post[2],
                    # "content": post[3],
                    "tags": json.loads(post[4]),
                    "give": post[5],
                    "created_at": timeDiff(post[6]),
                }
            )

        return {
            "result": True,
            "posts": postResult,
        }

    def search(self, data):
        keyword = data["keyword"]
        query = """
            SELECT * FROM post WHERE title LIKE ? OR tags LIKE ? ORDER BY id DESC
        """
        result = db.query(
            query,
            (
                f"%{keyword}%",
                f"%{keyword}%",
            ),
        )
        if not result:
            return {
                "result": False,
                "code": "POST_NOT_EXIST",
                "message": "Post Not Exist",
            }

        postResult = []
        for post in result:
            query = """
                SELECT nickname, image FROM user WHERE uuid = ?
            """
            userResult = db.query(query, (post[1],))
            if not userResult:
                return {
                    "result": False,
                    "code": "SEARCH_ERROR_USER_NOT_EXIST",
                    "message": "Search Error - User Not Exist",
                }
            userResult = list(userResult[0])

            postResult.append(
                {
                    "id": post[0],
                    "author": userResult[0],
                    "authorImage": userResult[1],
                    "title": post[2],
                    # "content": post[3],
                    "tags": json.loads(post[4]),
                    "give": post[5],
                    "created_at": timeDiff(post[6]),
                }
            )

        return {
            "result": True,
            "posts": postResult,
        }
