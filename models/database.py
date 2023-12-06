from typing import Annotated
import motor.motor_asyncio
from pydantic import BeforeValidator
from config.settings import get_settings

settings = get_settings()
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client["kt"]
PyObjectId = Annotated[str, BeforeValidator(str)]
