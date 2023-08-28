from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from routers.redirect import router as redirect_router
from routes import router as api_router
from utils.mongo_client import client

origins = ["*"]

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
    global code_generator
    try:
        # Send a ping to initialise the connection
        client.admin.command("ping")
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=e)


@app.on_event("shutdown")
def shutdown_event():
    client.close()


@app.get("/health")
def health():
    return {"health": "ok"}


app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(redirect_router, tags=["redirect"])
