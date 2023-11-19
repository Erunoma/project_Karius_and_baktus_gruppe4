import smtplib
import random
import db_manager


#TODO: Create an html home page and connect it to the application

#TODO: Create a session function and a landing page

#TODO: Setup the configuration for the login

#TODO: Create an email verification step from new IP

#TODO: Create hashed passwords using bcrypt


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT=587
SMTP_USERNAME="karibak.server@gmail.com"
SMTP_PASSWORD="uzjx ilgq jpbb bpse"

def rand_otp():
    randnumber=random.randint(100,999)
    
    print(f"The random number: {int(randnumber)}")
    if db_manager.otp_check(randnumber) == True:
        rand_otp()
    else:
        return randnumber

def send_mail(recipient):
    msg=str(random.randint(100,999))
    print(f"The message:{msg}")
    with smtplib.SMTP(SMTP_SERVER,SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME,recipient,msg)
        db_manager.save_otp(msg)

