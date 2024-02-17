import json
from services.db import DB
from services.valid import *
from services.auth import Auth

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
