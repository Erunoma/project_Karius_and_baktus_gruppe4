import sqlite3
from bottle import default_app, route, template, run, app
import log_manager

logger=log_manager.logging.getLogger(__name__)

#DB TODO: Send log files for connection and creation
def init_db():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        logger.info(f"DB initilized.")
    except:
        logger.error(f"Can't init database")

def find_db():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        name = con.execute("PRAGMA database_list;").fetchone()[2]
        logger.info(f"Current database in use: {name}")
    except:
        logger.warning(f"Could not find the name of database")

def create_db_table():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE patient(name, age, status, last_activity, time_brushed)")
        logger.info(f"New table created in {find_db()}.")
    except:
        logger.error(f"Can't create new table.")

def log_test():
    logger.debug("debug test 1")
    logger.info("debug test info")
    logger.warning("debug test warning")
    logger.error("debug test error")


def start():
    try:
        init_db()
        find_db()
        log_test()
    except:
        logger.warning(f"Some functions failed")

#If running the application locally, keep this setting on 'True'. If running through pythonanywhere, set to 'False'
local_app=True
try:
    if local_app==False:
        @route('/')
        def hello_world():
            return 'Hello from Bottle!'

        application = default_app()
    else:
        @route('/')
        def home():
            return template("test.html")
        run(host='localhost', port=8000, debug=True)
    start()
except:
    logger.error(f"cant find location")








#Password: BørstDineTænder555!