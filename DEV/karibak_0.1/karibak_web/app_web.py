import sqlite3
from bottle import default_app, route, template, run, app, request, post, Bottle, url, response, redirect, TEMPLATE_PATH, abort, get, static_file
import log_manager
import db_manager
import login_manager
import bottle_session
import socket
from threading import Thread
import time


app = Bottle()
plugin = bottle_session.SessionPlugin(cookie_lifetime=600)
app.install(plugin)

data_pass="a4a6d723-8ece-4c24-b662-0285cf9f1e50"


#How to log: use log_manager.log_func(). This func has 3 string arguments: 1) is for exceptions. If not used, leave blank. 2) The message we want to log. 3) Log type (See log_manager.py)
logger=log_manager.logging.getLogger(__name__)


#This is the first function that triggers when the program starts up before the Bottle website goes online.
#If it can't complete all code in here, the program cannot start.
def start():
    try:
        #db_manager.generate_key()
        db_manager.init_db()
        db_manager.find_db()
        #db_manager.delete_all_users()
        db_manager.create_db_user_table()
        db_manager.create_db_login_table()
        db_manager.delete_all_otp()
        db_manager.create_db_otp()
        init_socket_thread() 
        db_manager.update_time_test("4a8e5bf7-b83d-4d90-9f0c-c3fab3c2ce6b")
        #db_manager.add_user("Hanne Olsen", "Rullebjerg 54, 2650", "ip_variable", "mac_variable", 0, "length_variable", "tb_temp_variable")
        #db_manager.add_user("Birke Olsen", "Rullebjerg 54, 2650", "ip_variable", "mac_variable", "acitvity_variable", "length_variable")

        #db_manager.change_user_info("4feb8613-e1d6-4457-87ad-e738d3dda8d3", "emil", "69", "female", "Holgasville 25", "", "", "", "")
        #db_manager.add_admin("hashed_oliver", "999", "oliver.boots@hotmail.com")
        #log_test()
    except Exception as e:
        print(log_manager.log_func(e,"startup failed","error"))
        exit()

#The login screen. The user inputs the username and password. If they are correct, they will be redirected to the verification page.
@route('/login', method=["POST", "GET"])
def login():
    session_cookie = request.get_cookie('karibak_login')
    #print(session_cookie)
    if request.method=="POST":
        username=request.forms["username"]
        password=request.forms["password"]
        #print(login_manager.check_for_regex(username))
        if login_manager.check_for_regex(username) == True and login_manager.check_for_regex(password) == True: 
            if db_manager.check_admin_user(username,password) == True:
                print(log_manager.log_func("",f"Admin user {username} log in requested","info"))
                login_manager.send_mail(db_manager.get_email(username), username)
                
                redirect(f'/verify/{username}')
            else:
                return redirect('/login')

    if  session_cookie == 'karibak_id':
        return redirect('/home')
    else:
       
        return template("templates/login.html")

#The verification page. The user gets sent an email with a number. If they put in the correct number, they will be logged in and redirected to the home page.
@route('/verify/<username>',method=["POST", "GET"])
def verify(username):
    if request.method=="POST":
        number=request.forms["number"]
        #print(f'This is the username otp thingy... {username}')
        if login_manager.check_for_regex(number) == True: 
            if db_manager.otp_check(number, username)==True:
                db_manager.delete_otp(number)
                response.set_cookie('karibak_login', 'karibak_id', path='/')
                print(log_manager.log_func("",f"Correct key. User logged in","info"))
                redirect('/home')
            else:
                print(log_manager.log_func("",f"Incorrect key or it has expired. User sent back to login","warning"))
                redirect('/login')
    
    return template('templates/verify.html', username=username)
    
#This is the landing page after login
#TODO: Take out the time and make it appear as its own variable for the holder
@route('/home', method=["POST","GET"])
def home():
    session=request.get_cookie('karibak_login')
    print(f"Session:{session}")
    
    if session=='karibak_id':
        holders=db_manager.init_holders()
        if request.method=="POST":
                try:
                    if request.forms["direct_button"]:
                        id=request.forms["direct_button"]
                        try:
                            init_sending_thread(id)
                        except:
                            print("init_sending_thread error")
                        return template("templates/dashboard.html", holders=holders, alerted=True)
                except Exception as e:
                    print(e)
              
                if request.forms["direct_button1"]:
                    db_user_count=int(request.forms["direct_button1"])
        
                        
                    redirect(f"/home/settings/{holders[db_user_count][0]}_{holders[db_user_count][1]}_{holders[db_user_count][2]}")
                else:
                    return template("templates/dashboard.html", holders=holders, alerted=False)
        else:
            return template("templates/dashboard.html", holders=holders, alerted=False)
    else:
        redirect('/login')
    
    

#This section is the website page code for settings. When the admin clicks to config a holder, this page pops up.
#Here, the admin can administer details about the holder, and send the updated data to the holder, if its on and
#hasn't changed its IP.
@route('/home/settings/<id>', method=["POST", "GET"])
def setting(id):
    session=request.get_cookie('karibak_login')
    print(f"Session:{session}")
    if session=='karibak_id':
        id=str(id)
        settings_list=id.split("_")
        if request.method=="GET":

            return template("templates/settings.html", id=id, settings_list=settings_list)
        
        if request.method=="POST":
            
            username=request.forms['username']
            location=request.forms['location']
            try:

                db_manager.change_user_info(settings_list[0], db_manager.encrypt_text(username), "","",db_manager.encrypt_text(location), "", "", "", "", "", "")
                    
            except Exception as e:
                print(log_manager.log_func(e,"An error occured with the inputed information","info"))
            redirect('/home')
                
       
        
                
    else:
        return redirect('/login')


#This code sends the data to the holder. It finds the correct holder from the settings page.
def holder_connect(ip, port, data):
    try:
        print("Starting the connection sequence")
        print(db_manager.decrypt_text(ip), port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket aligned")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(1)
        bool_data=[]
        bool_data.append(data)
        try:
            s.connect((db_manager.decrypt_text(ip), port))
        except:
            print("Error")
        print("Connected to holder...")
        s.sendall(str.encode("\n".join([str(bool_data[0])])))
        print(log_manager.log_func("",f"Values sent:{bool_data}","info"))
        msg = s.recv(1024).decode()
        print(log_manager.log_func("",f"Callback: {msg}","info"))
    except ConnectionRefusedError as e:
        print(log_manager.log_func(e,"Connection refused","error"))
    except TimeoutError as e:
        print(log_manager.log_func(e,"Connection timed out to holder","error"))
    except Exception as e:
        print(log_manager.log_func(e,"There was an error in running the send code","error"))
    finally:
        print("Thread closed")
        s.close()
        


@route()

#This is the default start page. Connections are automaticcly redirected to /login.
@route('/')
def index():
     return redirect('/login')



#https://bottlepy.org/docs/dev/async.html
#This section is the URL that only the holders can connect to. The connection is open via a socket link.
#Every holder is custom-fidded with the password and (should be) is encryptet. The server will check the password
#and then take the data. Once the data has been aquaired, it uploads them to the DB.
@route('/data_delivery', method=["GET","POST"])
def data():
    if request.method=="POST":
        init_socket_thread()

def check_pass(sentdata):
    print("Trying to check password:")
    print(sentdata[0])
    if sentdata[0]==data_pass:
        
        print("Password match")
        return True
    else:
        print(log_manager.log_func("","The password does not match. Terminating connection...", "Warning"))
        return False

#This sectio opens a socket connection. Once a connection has been detected, it takes the data and decodes it.
def init_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 3000))
    print("Listening...")
    s.listen()
    while True:
        try:
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established")
            call_back="Your call has been recieved."
            clientsocket.send(call_back.encode())
         
            sentdata=[str(i) for i in clientsocket.recv(2048).decode("utf-8").split("\n")]
            print(sentdata)
            
            if check_pass(sentdata)==True:
                db_manager.upload_to_db(sentdata)
                call_back="Data has been recieved, and Server has been updated."
            else:
                call_back="Data has been recieved, but your passcode does not match the server."

            
            clientsocket.send(call_back.encode())
    
        except Exception as e:
            print(f"Exception{e}")
        finally:
            s.close()
            init_socket_thread()
            break


#Starts a thread for the function above.
def init_socket_thread():
    th = Thread(target=init_socket)
    th.start()
    print("New thread started")

def init_sending_thread(id):
    th = Thread(target=holder_connect(db_manager.get_user_ip(id),3000,True))
    th.start()
    print("New thread started")


#If running the application locally, keep this setting on 'True'. If running through pythonanywhere, set to 'False'
local_app=True
try:
    start()
    if local_app==False:
        application = default_app()
    elif local_app==True:
        
        run(host="10.10.4.10", port=6555, debug=True)               
except Exception as e:
    print(log_manager.log_func(e,"Could not determine local or online","error"))
    exit()




#Password: BørstDineTænder555!
