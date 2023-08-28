import os

from fastapi import HTTPException
from logger import logger
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = os.environ.get("MONGO_URI")


def connect():
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi("1"))
        return client
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=e)


client = connect()
