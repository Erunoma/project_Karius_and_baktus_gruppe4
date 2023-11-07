import sqlite3
import log_manager
import uuid

#How to log: use log_manager.log_func(). This func has 3 string arguments: 1) is for exceptions. If not used, leave blank. 2) The message we want to log. 3) Log type (See log_manager.py)
logger=log_manager.logging.getLogger(__name__)

def init_db():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        logger.info(f"DB initilized.")
        con.close()
    except Exception as e:
        log_manager.log_func(e,"Couldn't init database.","error")


def find_db():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        name = con.execute("PRAGMA database_list;").fetchone()[2]
        con.close
        return name
    except Exception as e:
        log_manager.log_func(e,"Could not find the name of database", "error")

def create_db_table():
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(id text PRIMARY KEY, name text, age text, gender text, address text, device text, ip text, mac text, last_activity text, pictures text);")
        con.commit()
        con.close()
        log_manager.log_func("", f"New table created in {find_db()}", "info")
    except Exception as e:
        log_manager.log_func(e,"Could not create table","error")



def add_user(name, age, gender, address, device, ip, mac):
    try:
        con = sqlite3.connect("Test.db")
        cur = con.cursor()
        cur.execute('INSERT INTO users(id, name, age, gender, address, device, ip, mac, last_activity, pictures) values (?,?,?,?,?,?,?,?,?,?)', 
                (generate_id(), name, age, gender, address, device, ip, mac, "", ""))
        con.commit()
        con.close()
        log_manager.log_func("", f"New user created in {find_db()}", "info")
    except Exception as e:
        log_manager.log_func(e,"Could not create user","error")



#TODO DB: Add a function to modify these user settings.
#TODO DB: Encrpyt the DB
       
def generate_id():
    id = str(uuid.uuid4())
    return id