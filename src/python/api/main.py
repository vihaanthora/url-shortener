import logging
import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.encode import HashCodeGenerator
from utils.encode import HashCodeGenerator
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

origins = [
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    uri = os.environ.get("MONGO_URI")
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


# endpoint that encodes a url and stores it's mapping in the db
@app.get("/api")
def encode(url: str | None = None, custom: str | None = None):
    if url is None:
        return {"Hello": "World"}
    else:
        db = app.client.url_shortener
        mappings = db.mappings
        code = ""
        if custom == "":
            custom = None
        if custom is not None and mappings.find_one({"shortened": "_" + custom}) is not None:
            row = mappings.find_one({"shortened": "_" + custom})
            if row["original"] != url:
                logging.info(
                    "Custom string already exists in the db, please enter another!"
                )
                return {"shortened": "error"}
            else:
                return {"shortened": custom}

        existing = mappings.find_one({"original": url})
        if existing is not None and custom is None and existing["shortened"][0] != "_":
            code = existing["shortened"]
            logging.info(f"Given url already exists in the db, reusing the mapping!")
        else:  # even if a custom url exists, we will create a new mapping
            if custom is not None:
                code = "_" + custom  # '_' is used to indicate that the code is custom
            else:
                code = app.code_generator.generate_code(url)
            document = {"original": url, "shortened": code}
            logging.info(document)
            try:
                mappings.insert_one(document)
            except Exception as e:
                logging.exception(e)
                raise HTTPException(status_code=500, detail=e)
        logging.info(f"Total records are: {mappings.count_documents({})}")
        if code[0] == "_":
            code = code[1:]
        logging.info(code)
        return {"shortened": code}


# endpoint to redirect users to the main url
@app.get("/{shortened}")
def redirect(shortened: str):
    db = app.client.url_shortener
    mappings = db.mappings
    regex_pattern = f"^{shortened}$|^_{shortened}$"
    row = mappings.find_one({"shortened": {"$regex": re.compile(regex_pattern)}})
    print(shortened)
    if row is not None:
        original_url = row["original"]
        if not original_url.startswith(("http://", "https://")):
            original_url = f"http://{original_url}"
        return RedirectResponse(url=original_url, status_code=302)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
