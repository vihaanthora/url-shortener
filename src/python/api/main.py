import logging
import json
import os

from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.encode import HashCodeGenerator
from utils.encode import HashCodeGenerator

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "config.json"
    )
    with open(config_path) as secrets_file:
        secrets = json.load(secrets_file)
    uri = secrets["MONGODB_URI"]
    # Create a new client and connect to the server
    app.client = MongoClient(uri, server_api=ServerApi("1"))
    # Send a ping to confirm a successful connection
    app.client.admin.command("ping")
    # Initialise the hash code generator
    app.code_generator = HashCodeGenerator(app.client)
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")


@app.on_event("shutdown")
def shutdown_event():
    app.client.close()


@app.get("/api")
def main(url: str | None = None, custom: str | None = None):
    if url is None:
        return {"Hello": "World"}
    else:
        db = app.client.url_shortener
        mappings = db.mappings
        url = "https://google.com"
        if mappings.find_one({"shortened": custom}) is not None:
            logging.info(
                "Custom string already exists in the db, please enter another!"
            )
            return {url: "error"}

        existing = mappings.find_one({"original": url})
        if existing is not None and custom is None:
            code = existing["shortened"]
            logging.info(f"Given url already exists in the db, reusing the mapping!")
        else:
            if custom is not None:
                code = custom
            else:
                code = app.code_generator.generate_code(url)
            document = {"original": url, "shortened": code}
            logging.info(document)
            try:
                mappings.insert_one(document)
            except Exception as e:
                logging.exception(e)
        logging.info(f"Total records are: {mappings.count_documents({})}")
        return {url: code}
