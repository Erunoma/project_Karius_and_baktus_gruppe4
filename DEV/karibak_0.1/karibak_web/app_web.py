import sqlite3
from bottle import default_app, route, template, run, app
import log_manager

#How to log: use log_manager.log_func(). This func has 3 string arguments: 1) is for exceptions. If not used, leave blank. 2) The message we want to log. 3) Log type (See log_manager.py)
logger=log_manager.logging.getLogger(__name__)


#DB TODO: Send log files for connection and creation
def init_db():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        logger.info(f"DB initilized.")
    except Exception as e:
        log_manager.log_func(e,"Couldn't init database.","error")

def find_db():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        name = con.execute("PRAGMA database_list;").fetchone()[2]
        log_manager.log_func("",f"Current database in use: {name}", "info")
    except Exception as e:
        log_manager.log_func(e,"Could not find the name of database", "error")

def create_db_table():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE patient(name, age, status, last_activity, time_brushed)")
        logger.info(f"New table created in {find_db()}.")
    except Exception as e:
        log_manager.log_func(e,"Could not create table","error")

def log_test():
    logger.debug("debug test 1")
    logger.info("debug test info")
    logger.warning("debug test warning")
    logger.error("debug test error")
    



def start():
    try:
        init_db()
        find_db()
        #log_test()
    except Exception as e:
        log_manager.log_func(e,"startup failed","error")
        exit()

#If running the application locally, keep this setting on 'True'. If running through pythonanywhere, set to 'False'
local_app=True
try:
    start()
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
    
except Exception as e:
    log_manager.log_func(e,"Could not determine local or online","error")








#Password: BørstDineTænder555!