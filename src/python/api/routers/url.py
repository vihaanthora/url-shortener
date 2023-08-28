from fastapi import APIRouter, HTTPException
from logger import logger
from models.url import URL
from utils.code_generator import code_generator
from utils.mongo_client import client

router = APIRouter()


# endpoint that encodes a url and stores it's mapping in the db
@router.post("/shorten")
def shorten_url(url_data: URL):
    original = str(url_data.original).rstrip("/")
    if original is None:
        logger.info("Original url is not provided!")
        return {"shortened": "error"}
    custom = url_data.custom
    db = client.url_shortener
    mappings = db.mappings
    code = ""
    if custom == "":
        custom = None
    if (
        custom is not None
        and mappings.find_one({"shortened": "_" + custom}) is not None
    ):
        row = mappings.find_one({"shortened": "_" + custom})
        if row["original"] != original:
            logger.info("Custom string already exists in the db, please enter another!")
            return {"shortened": "error"}
        else:
            return {"shortened": custom}

    existing = mappings.find_one({"original": original})
    if existing is not None and custom is None and existing["shortened"][0] != "_":
        code = existing["shortened"]
        logger.info(f"Given url already exists in the db, reusing the mapping!")
    else:  # even if a custom url exists, we will create a new mapping
        if custom is not None:
            code = "_" + custom  # '_' is used to indicate that the code is custom
        else:
            code = code_generator.generate_code(original)
        document = {"original": original, "shortened": code}
        logger.info(document)
        try:
            mappings.insert_one(document)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=e)
    logger.info(f"Total records are: {mappings.count_documents({})}")
    if code[0] == "_":
        code = code[1:]
    return {"shortened": code}


# fetches total number of urls stored in db
@router.get("/total")
def get_total():
    db = client.url_shortener
    mappings = db.mappings
    return {"total": mappings.count_documents({})}
