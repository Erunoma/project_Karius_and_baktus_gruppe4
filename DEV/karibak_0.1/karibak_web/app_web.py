import sqlite3
from bottle import default_app, route, template, run, app
import log_manager
from datetime import date
import time

#DB TODO: Send log files for connection and creation
def init_db():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        name = con.execute("PRAGMA database_list;").fetchone()[2]
        return name
    except:
        log_manager.logging.error("Unable to retrieve database.")

def create_db_tabel():
    con = sqlite3.connect("Test.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE patient(name, age, status, last_activity, time_brushed)")




try:
    if init_db() != None:
        print(f"The database {init_db()}")
        log_manager.logging.debug(f"<{date.today()}><{time.strftime('%H:%M:%S',time.localtime())}> Testing.")
        
        #TODO: Implement log-taking with date and time into a more intuitive format
except:
    log_manager.logging.error(f"<{date.today()}><{time.strftime('%H:%M:%S',time.localtime())}> Can't determine database in use.")

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
except:
    log_manager.logging.ERROR("Error 1: Can't determine local or hosted application")








#Password: BørstDineTænder555!