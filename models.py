from flask_restx import fields

signUpModel = {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "nickname": fields.String(required=True),
    "phone": fields.String(required=True),
    "region": fields.String(required=True),
}

loginModel = {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
}

writeModel = {
    "title": fields.String(required=True),
    "content": fields.String(required=True),
    "tags": fields.List(required=True, cls_or_instance=fields.String),
    "give": fields.Boolean(required=True),
}
