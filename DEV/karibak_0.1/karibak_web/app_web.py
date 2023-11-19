import sqlite3
from bottle import default_app, route, template, run, app, request, post, Bottle, url, response, redirect, TEMPLATE_PATH
import log_manager
import db_manager
import login_manager

app = Bottle()




#How to log: use log_manager.log_func(). This func has 3 string arguments: 1) is for exceptions. If not used, leave blank. 2) The message we want to log. 3) Log type (See log_manager.py)
logger=log_manager.logging.getLogger(__name__)



def log_test():
    print(log_manager.log_func("","startup failed","error"))
    
def start():
    try:
        db_manager.init_db()
        db_manager.find_db()
        db_manager.create_db_user_table()
        db_manager.create_db_login_table()
        db_manager.create_db_otp()
        #db_manager.add_user("Bob","21", "Male","Kaktusbæk 54, Rødby","ESP32-5130","150.122.69.123","9c:51:6f:19:3c:0f")
        #db_manager.change_user_info("4feb8613-e1d6-4457-87ad-e738d3dda8d3", "emil", "69", "female", "Holgasville 25", "", "", "", "")
        #db_manager.add_admin("oliver", "123", "oliver.boots@hotmail.com")
        #log_test()
    except Exception as e:
        print(log_manager.log_func(e,"startup failed","error"))
        exit()

@route('/login', method=["POST", "GET"])
def login():
    if request.method=="POST":
        username=request.forms["username"]
        password=request.forms["password"]
        print(db_manager.check_admin_user(username,password))
        if db_manager.check_admin_user(username,password) == True:
            login_manager.send_mail(db_manager.get_email(username))
            redirect('/verify')
        else:
            return redirect('/login')


    return template("templates/login.html")

@route('/verify',method=["POST", "GET"])
def verify():
    if request.method=="POST":
        number=request.forms["number"]
        if db_manager.otp_check(number)==True:
            db_manager.delete_otp(number)
            redirect('/base')
        else:
            redirect('/login')
    return template('templates/verify.html')

@route('/base')
def home():
     return template("templates/base.html")
@route('/')
def index():
     return redirect('/login')


            


#If running the application locally, keep this setting on 'True'. If running through pythonanywhere, set to 'False'
local_app=True
try:
    start()
    if local_app==False:
        application = default_app()
    elif local_app==True:
        run(host='localhost', port=8000, debug=True)  
                
except Exception as e:
    print(log_manager.log_func(e,"Could not determine local or online","error"))
    exit()




#Password: BørstDineTænder555!