import sqlite3
import log_manager
import uuid
import login_manager
import time
from cryptography.fernet import Fernet


#How to log: use log_manager.log_func(). This func has 3 string arguments: 1) is for exceptions. If not used, leave blank. 2) The message we want to log. 3) Log type (See log_manager.py)
logger=log_manager.logging.getLogger(__name__)

web_db="Test.db"


#Initailize DB. Used on startup to either create one if it doesn't exist, or check if it readable.
def init_db():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        if con:
            print(log_manager.log_func("","DB initilized", "info"))
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
        cur.execute("CREATE TABLE IF NOT EXISTS users(id text PRIMARY KEY, name text, address text, current_ip text, mac text, last_activity text, length_of_brush text);")
        con.commit()
        #log_manager.log_func("", f"New table created in {find_db()}", "info")
    except Exception as e:
        print(log_manager.log_func(e,"Could not create user table","error"))
    finally:
        con.close()

#Creates a new table for admin accounts if it doesn't already exist.
def create_db_login_table():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS admins(id text PRIMARY KEY, username text NOT NULL UNIQUE, password  text NOT NULL, email text);")
        con.commit()
        #log_manager.log_func("", f"New table created in {find_db()}", "info")
    except Exception as e:
        print(log_manager.log_func(e,"Could not create login table","error"))
    finally:
        con.close()

#Adds a user to the db.
def add_user(name, address, current_ip, mac, last_activity, length_of_brush):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('INSERT INTO users(id, name, address, current_ip, mac, last_activity, length_of_brush) values (?,?,?,?,?,?,?)', 
                (generate_id(), encrypt_text(name), encrypt_text(address), current_ip, mac, last_activity, length_of_brush))
        con.commit()
        print(log_manager.log_func("","Created user in db","info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not create user","error"))
    finally:
        con.close()


#Adds an admin to the db table.
def add_admin(username, password, email):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('INSERT INTO admins(id, username, password, email) values (?,?,?,?)', 
                (generate_id(), username, login_manager.hash_password(password), email))
        con.commit()
        print(log_manager.log_func("", f"New admin created in {find_db()}", "info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not create admin","error"))
    finally:
        con.close()

#Creates the DB table for the OTP Tokens. It incases both the number and the admin.
def create_db_otp():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS otp(key text, user text, expire float);")
        con.commit()
        log_manager.log_func("", f"New table created in {find_db()}", "info")
    except Exception as e:
        print(log_manager.log_func(e,"Could not create otp table","error"))
    finally:
        con.close()

#Saves the OTP token to the user.
def save_otp(msg, username):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        print(time.time())
        cur.execute('INSERT INTO otp (key, user, expire) values (?,?,?)', (msg,username,((time.time() + 100))))
        con.commit()
        print(log_manager.log_func("", f"New key created in {find_db()}", "info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not save otp","error"))
    finally:
        con.close()

#Deletes the OTP token of the user.
def delete_otp(number):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('DELETE FROM otp WHERE key=?', (number,))
        con.commit()
        print(log_manager.log_func("",f"Deleted the key {number}","info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not delete save otp","error"))
    finally:
        con.close()

#On server startup, this function is called. It deletes all previous OTP tokens.
def delete_all_otp():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('DROP TABLE otp')
        con.commit()
        print(log_manager.log_func("",f"Deleted all OTPs as a startup procedure","info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not delete otp table","error"))
    finally:
        con.close()

#For testing purposes, this function can delete all users in a db.
def delete_all_users():
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('DROP TABLE users')
        con.commit()
        print(log_manager.log_func("",f"Deleted all users as a startup procedure","info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not delete users table","error"))
    finally:
        con.close()

#Checks the OTP code that has been typed and matches it with the user. If they are both connected, the check will be true.
def otp_check(number, username):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('Select key FROM otp WHERE key=?', (number,))
        
        key_result = cur.fetchone()
        cur.execute('Select user FROM otp WHERE key=?', (number,))
        name_result=cur.fetchone()
        cur.execute('Select expire FROM otp where key=?', (number,))
        expire_time=cur.fetchone()
        
        print(log_manager.log_func("","Checking key in database...", "info"))
        if key_result:
            print(log_manager.log_func("","Checking key with username...", "info"))
            if name_result[0] == username:
                print(log_manager.log_func("","Checking key in database...", "info"))
                if expire_time[0]>=time.time():
                    return True
        else:
            print(log_manager.log_func("","Could not check otp", "info"))
            return False
    except Exception as e:
        print(log_manager.log_func(e,"Could not check the OTP", "error"))
        return False
    finally:
        con.close()


#Gets the email from the user by connecting to the database.
def get_email(username):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        cur.execute('Select email FROM admins WHERE username=?', (username,))
        result = cur.fetchone()
        if result:
            return str(result[0])
        else:
            return None
    except Exception as e:
        print(log_manager.log_func(e,"Could not check the email", "error"))
        return None
    finally:
        con.close()

    
#Changes the info of a non-admin user. 
def change_user_info(id, name, age, gender, address, device, ip, mac, last_activity, length_of_brush):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor()
        if name:
            cur.execute('UPDATE users SET name=? WHERE id=?', (name,id))
            print(log_manager.log_func("",f"updated name of id: {id}","info"))
        if age:
            cur.execute('UPDATE users SET age=? WHERE id=?', (age, id))
        if gender:
            cur.execute('UPDATE users SET gender=? WHERE id=?', (gender, id))
        if address:
            cur.execute('UPDATE users SET address=? WHERE id=?', (address, id))
        if device:
            cur.execute('UPDATE users SET device=? WHERE id=?', (device, id))
        if ip:
            cur.execute('UPDATE users SET current_ip=? WHERE id=?', (ip,id))
        if mac:
            cur.execute('UPDATE users SET mac=? WHERE id=?', (mac,id))
        if last_activity:
            cur.execute('UPDATE users SET last_activity=? WHERE id=?', (last_activity,id))
        if length_of_brush:
            cur.execute('UPDATE users SET length_of_brush=? WHERE id=?', (length_of_brush,id))
        con.commit()

        print(log_manager.log_func("",f"changed user info for {id}","info"))
    except Exception as e:
        print(log_manager.log_func(e,"Could not change user settings","error"))
    finally:
        con.close()
   


#Data to be sent from the esp: [Password(str), user_id(str), ip(str), mac(str), last_activity(str), lenght of brush(str)]
def upload_to_db(data):
    change_user_info(data[1],"","","","","",data[2], data[3], data[4],data[5])
    print("sending data to be uploaded:")
            
# check if user and password match
def check_admin_user(username, password):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor() 
        cur.execute('Select password FROM admins WHERE username=?', (username,))
        result = cur.fetchone()
        hashed_password = result[0]
        print(f'This is the hashed password: {hashed_password}')
        if login_manager.decrypt_password(hashed_password,password)==True:
            return True
        else:
            return False
    except Exception as e:
        print(log_manager.log_func(e,"Could not check for admin","error"))
        return False
    finally:
        con.close()

#After data has been aquiared from the holder, this function is called.
#It is used to seperate and display all current registered users, to be used for the website.
def init_holders():
    try:
        holders=[]
        
        con = sqlite3.connect(web_db)
        cur = con.cursor() 
        cur.execute('Select * from users')
        result = cur.fetchall()
  
        for user in result:
            new_list=[]
            print(f'this is before:{new_list}')
            for entry in user:
                if type(entry) is bytes:
                    entry=decrypt_text(entry)
                new_list.append(entry)
            print(f'This is after: {new_list}')
            holders.append(new_list)
        
        return holders
            
    except Exception as e:
        print(log_manager.log_func(e,"Could not initialize holders","error"))
    finally:
        con.close()


def get_user_ip(id):
    try:
        con = sqlite3.connect(web_db)
        cur = con.cursor() 
        cur.execute('Select current_ip from users Where id=?',(id,))
        result = cur.fetchone()
        return result[0]
    except Exception as e:
        print(log_manager.log_func(e,"Could not get details of user","error"))


#Generates a unique id. They go something like this:  4feb8613-e1d6-4457-87ad-e738d3dda8d3      
def generate_id():
    id = str(uuid.uuid4())
    return id
 
#Encrypts a string with Fernet. Used to protect important database data.
def encrypt_text(text):
    try:
        with open ('db_key.key', 'rb') as file:
            key=file.read()
            encrypt_key=Fernet(key)
            b = bytes(text, 'utf-8')
        return encrypt_key.encrypt(b)
    except Exception as e:
        print(log_manager.log_func(e,"Could not encrypt text","error"))
    
#Used to decrypt a variable in the database.
def decrypt_text(text):
    try:
        with open ('db_key.key', 'rb') as file:
            key=file.read()
            encrypt_key=Fernet(key)
            decrypted_string= encrypt_key.decrypt(text).decode('utf-8')
        return str(decrypted_string)
    except Exception as e:
        print(log_manager.log_func(e,"Could not decrypt text","error"))

#Used to genereate a key that will be used to encrypt and decrypt everything. They key is stored in a file. 
def generate_key():
    key = Fernet.generate_key()
    with open ('db_key.key', 'wb') as f:
        f.write(key)
    print(log_manager.log_func("","Encryption key generated and put into file","info"))
