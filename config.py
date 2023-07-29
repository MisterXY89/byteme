
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Config:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME")
        self.FLASK_SECRET = os.getenv("FLASK_SECRET")
        self.PORT = int(os.getenv("PORT"))
        self.DEBUG = True if os.getenv("DEBUG") == "True" else False