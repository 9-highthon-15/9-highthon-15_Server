import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

CF_ACCESS_KEY = os.getenv("CF_ACCESS_KEY")
CF_SECRET_KEY = os.getenv("CF_SECRET_KEY")

CF_BUCKET = os.getenv("CF_BUCKET")
CF_PUBLIC = os.getenv("CF_PUBLIC")
CF_ENDPOINT = os.getenv("CF_ENDPOINT")
