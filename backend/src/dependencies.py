""" FastAPI application dependencies that are shared within the entire application """
# pylint: disable=too-few-public-methods
# Disabling too few public metods due to utilizing Pydantic/FastAPI BaseSettings class
import gridfs
from pydantic import BaseSettings
from pymongo import MongoClient

from .core.annotation import AnnotationQueue
from .database import Database


class Settings(BaseSettings):
    """
    Settings for Rosalution.  See https://fastapi.tiangolo.com/advanced/settings/
    for more details.
    """
    mongodb_host: str = "rosalution-db"
    mongodb_db: str = "rosalution_db"


settings = Settings()

mongodb_connection_uri = f"mongodb://{settings.mongodb_host}/{settings.mongodb_db}"
mongodb_client = MongoClient(mongodb_connection_uri)
bucket = gridfs.GridFS(mongodb_client.rosalution_db)

# Database/Repositories
database = Database(mongodb_client, bucket)

# Queue that processess annotation tasks safely between threads
annotation_queue = AnnotationQueue()
