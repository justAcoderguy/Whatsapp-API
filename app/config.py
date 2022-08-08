import os
from pickle import FALSE
from dotenv import load_dotenv
load_dotenv()

DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECURITY_KEY')
uri = os.environ.get("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
SQLALCHEMY_DATABASE_URI = uri

