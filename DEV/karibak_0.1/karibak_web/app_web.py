import sqlite3
from bottle import route, run, template

#TODO SQLite database

#TODO Initiate Website with Bottle 
@route('/home')
def home():
    return 'Hello World!'



#Password: BørstDineTænder555!