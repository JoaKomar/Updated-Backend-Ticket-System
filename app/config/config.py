from dotenv import load_dotenv
import os

load_dotenv()

#DB and API .env
DATABASE_URL = os.getenv("DATABASE_URL")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY_TOKEN = os.getenv("SECRET_KEY_TOKEN")
