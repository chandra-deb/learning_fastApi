load_dotenv()

db_host = os.getenv("host")
db_name = os.getenv("dbname")
db_user = os.getenv("user")
db_password = os.getenv("password")


while True:
    try:
        conn = psycopg.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            row_factory=dict_row,
        )
        cursor = conn.cursor()
        print("Successfully connect")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(error)
        time.sleep(3)

