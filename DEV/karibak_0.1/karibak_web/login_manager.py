import smtplib
import random
from bottle import default_app, route, template, run, app, request, post, Bottle, url, response, redirect, TEMPLATE_PATH
import db_manager
import log_manager
from flask_bcrypt import Bcrypt
import re

app = Bottle()
bcrypt = Bcrypt(app)


#How to log: use log_manager.log_func(). This func has 3 string arguments: 1) is for exceptions. If not used, leave blank. 2) The message we want to log. 3) Log type (See log_manager.py)
logger=log_manager.logging.getLogger(__name__)

#TODO: Create a session function
#TODO: Auto delete number


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT=587
SMTP_USERNAME="karibak.server@gmail.com"
SMTP_PASSWORD="uzjx ilgq jpbb bpse"


#Creates a random number for use in the OTP authentication.
def rand_otp():
    try:
        randnumber=random.randint(100,999)
    
        print(f"The random number: {int(randnumber)}")
        if db_manager.otp_check(randnumber) == True:
            rand_otp()
        else:
            return randnumber
    except Exception as e:
        print(log_manager.log_func(e,"Could not fetch a random number","error"))
        return None

#This function sends an email from the mail server with a number to the users email.
def send_mail(recipient, username):
    try:
        msg=str(random.randint(100,999))
        #print(f"The message:{msg}")
        with smtplib.SMTP(SMTP_SERVER,SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME,recipient,msg)
            print(log_manager.log_func("","Sending mail to user","info"))
            db_manager.save_otp(msg, username)
    except Exception as e:
        print(log_manager.log_func(e,"Could not send email","error"))

#This function hashes a password. For use in database login.
def hash_password(password):
    try:
        print(log_manager.log_func("",f"{password} hashed...","info"))
        return bcrypt.generate_password_hash(password).decode('utf-8')
        
    except Exception as e:
        print(log_manager.log_func(e,f"Could not hash password","error"))

#This function decrypts a hashed password with the input password from the website. For use in database login
def decrypt_password(hashed_password, password):
    try:
      return bcrypt.check_password_hash(hashed_password, password)
    except Exception as e:
        print(log_manager.log_func(e,f"Could not decrypt password","error"))  

def check_for_regex(text):
    try:
        match = re.search('^[A-Za-z0-9_-]+$',text)
        if match == None:
            print(log_manager.log_func("",f"Regex Error found with text: {text}","warning"))
            return False
        else:
            print(log_manager.log_func("",f"Regex accepted: {text}","info"))
            return True
    except Exception as e:
        print(log_manager.log_func(e,f"Could not check for regex","error"))  