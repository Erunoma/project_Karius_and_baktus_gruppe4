import sqlite3
import log_manager
import uuid

#How to log: use log_manager.log_func(). This func has 3 string arguments: 1) is for exceptions. If not used, leave blank. 2) The message we want to log. 3) Log type (See log_manager.py)
logger=log_manager.logging.getLogger(__name__)

web_db="Test.db"

#Initailize DB. Used on startup to either create one if it doesn't exist, or check if it readable.
def init_db():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        logger.info(f"DB initilized.")
        con.close()
    except Exception as e:
        print(log_manager.log_func(e,"Couldn't init database.","error"))
    finally:
        con.close()

#Find the location of the db. Used mostly for logging
def find_db():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        name = con.execute("PRAGMA database_list;").fetchone()[2]
        return name
    except Exception as e:
        print(log_manager.log_func(e,"Could not find the name of database", "error"))
    finally:
        con.close()

#Creates a table of users in the db. 
def create_db_user_table():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(id text PRIMARY KEY, name text, age text, gender text, address text, device text, ip text, mac text, last_activity text, pictures text);")
        con.commit()
        #log_manager.log_func("", f"New table created in {find_db()}", "info")
    except Exception as e:
        print(log_manager.log_func(e,"Could not create user table","error"))
    finally:
        con.close()

def create_db_login_table():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS admins(id text PRIMARY KEY, username text NOT NULL UNIQUE, password  text NOT NULL, ip text);")
        con.commit()
        #log_manager.log_func("", f"New table created in {find_db()}", "info")
    except Exception as e:
        print(log_manager.log_func(e,"Could not create login table","error"))
    finally:
        con.close()

#Adds a user to the db.
def add_user(name, age, gender, address, device, ip, mac):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('INSERT INTO users(id, name, age, gender, address, device, ip, mac, last_activity, pictures) values (?,?,?,?,?,?,?,?,?,?)', 
                (generate_id(), name, age, gender, address, device, ip, mac, "", ""))
        con.commit()
        print(log_manager.log_func("", f"New user created in {find_db()}", "info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not create user","error"))
    finally:
        con.close()

def add_admin(username, password, ip):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('INSERT INTO admins(id, username, password, ip) values (?,?,?,?)', 
                (generate_id(), username, password, ip))
        con.commit()
        print(log_manager.log_func("", f"New admin created in {find_db()}", "info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not create admin","error"))
    finally:
        con.close()

#TODO DB: Add a function to modify these user settings.

def change_user_info(id, name, age, gender, address, device, ip, mac, last_activity):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        if name:
            cur.execute('UPDATE users SET name=? WHERE id=?', (name,id))
        if age:
            cur.execute('UPDATE users SET age=? WHERE id=?', (age, id))
        if gender:
            cur.execute('UPDATE users SET gender=? WHERE id=?', (gender, id))
        if address:
            cur.execute('UPDATE users SET address=? WHERE id=?', (address, id))
        if device:
            cur.execute('UPDATE users SET device=? WHERE id=?', (device, id))
        if ip:
            cur.execute('UPDATE users SET ip=? WHERE id=?', (ip,id))
        if mac:
            cur.execute('UPDATE users SET mac=? WHERE id=?', (mac,id))
        if last_activity:
            cur.execute('UPDATE users SET last_activity=? WHERE id=?', (last_activity,id))
        con.commit()

        print(log_manager.log_func("",f"changed user info for {id}","info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not change user settings","error"))
    finally:
        con.close()



#TODO DB: Encrpyt the DB
#Generates a unique id. They go something like this:  4feb8613-e1d6-4457-87ad-e738d3dda8d3      
def generate_id():
    id = str(uuid.uuid4())
    return id