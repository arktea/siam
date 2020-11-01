import os

ENV = os.environ.get("ENV", "test")
TABLE = os.environ.get("TABLE", f"PERMISSION_{ENV}")

DYNAMODB_CONFIG = [
    dict(),
    dict(endpoint_url=os.environ.get("ENDPOINT_URL", "http://dynamodb:8000"))
][ENV == "test"]
