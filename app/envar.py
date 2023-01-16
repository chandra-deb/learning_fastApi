import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("host")
db_name = os.getenv("dbname")
db_user = os.getenv("user")
db_password = os.getenv("password")
