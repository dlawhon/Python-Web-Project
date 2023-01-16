from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import json




class User:

    def __init__(self, params):

        cursor, conn = sqlServerConnect()

        cursor.execute("SELECT * FROM users WHERE username = ?", params.get('username'))
        results = cursor.fetchone()

        if results:
            #We need to return the user's info and set the class
            self.ID = results.ID
            self.firstName = results.first_name
            self.lastName = results.last_name
            self.username = results.username
            self.email = results.email

            return results
        else:
            #We need to add a new user

            userPassword=generate_password_hash(params.get('userPassword'), method='sha256')

            cursor.execute("INSERT INTO users (first_name, last_name, username, email, hash) VALUES (?,?,?,?,?)", params.get('userFirstName'), params.get('userLastName'), params.get('username'), params.get('userEmail'), userPassword);
            cursor.commit()

            cursor.execute("SELECT @@IDENTITY AS ID;")
            newID = cursor.fetchone()[0]

            self.ID = newID
            self.firstName = params.get('userFirstName')
            self.lastName = params.get('userLastName')
            self.username = params.get('username')
            self.email = params.get('userEmail')

            loginUser(newID)

    def setUsername(passUsername):
        self.username = passUsername

    def getUsername(self):
        return self.username

    def allInfo(self):
        return self




def sqlServerConnect():
    import pyodbc

    conn = pyodbc.connect("DRIVER={ODBC driver 17 for SQL Server};SERVER=(localdb)\ProjectModels;DATABASE=PythonWebProjectDB;Trusted_Connection=yes;")
    cursor = conn.cursor()

    return cursor, conn

def findUser(passUsername):

    cursor, conn = sqlServerConnect()

    cursor.execute("SELECT * FROM users WHERE username = ? ", passUsername)
    results = cursor.fetchone()

    if results:
        return results
    else:
        return None

def loginUser(passUserID):

    cursor, conn = sqlServerConnect()

    cursor.execute("SELECT * FROM users WHERE ID = ? ", passUserID)
    results = cursor.fetchone()

    if results:

        session.permanent = True
        session["userID"] = results.ID
        session["userFirstName"] = results.first_name
        session["userLastName"] = results.last_name
        session["userName"] = results.username
        session["userEmail"] = results.email

        return True
    else:
        return False


def registerUser(passUsername):

    #cursor, conn = sqlServerConnect()

    newUser = User(user)

    session.permanent = True
    session["userID"] = results.ID
    session["userFirstName"] = results.first_name
    session["userLastName"] = results.last_name
    session["userName"] = results.username
    session["userEmail"] = results.email

def logoutUser():

    #session.clear()
    session.pop("userID", None)
    session.pop("userFirstName", None)
    session.pop("userLastName", None)
    session.pop("userName", None)
    session.pop("userEmail", None)
    return True

def getUsers():

    cursor, conn = sqlServerConnect()

    cursor.execute("SELECT id, first_name, last_name, username, email FROM users")
    rows = cursor.fetchall()

    rowarray_list = []
    for row in rows:
        t = (row[0], row[1], row[2], row[3], row[4])
        rowarray_list.append(t)

    final_array = {'data': rowarray_list}
    j = json.dumps(final_array, indent=4, sort_keys=True, default=str)

    if rows:
        return final_array
    else:
        return None


def getProjects():

    cursor, conn = sqlServerConnect()

    cursor.execute("SELECT ID, project_name, project_description, project_length, project_owner, creation_date FROM projects")
    rows = cursor.fetchall()

    rowarray_list = []
    for row in rows:
        t = (row[0], row[1], row[2], row[3], row[4], row[5])
        rowarray_list.append(t)

    final_array = {'data': rowarray_list}
    j = json.dumps(final_array, indent=4, sort_keys=True, default=str)

    if rows:
        return final_array
    else:
        return None

def checkSession():
    
    if "userName" in session:
        return True
    else:
        return False




