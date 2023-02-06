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


class Project:

    def __init__(self, params):

        cursor, conn = sqlServerConnect()

        cursor.execute("SELECT * FROM projects WHERE id = ?", params.get('id'))
        results = cursor.fetchone()

        if results:
            #We need to return the project's info and set the class
            self.ID = results.ID
            self.project_name = results.project_name
            self.project_description = results.project_description
            self.project_length = results.project_length
            self.project_owner = results.project_owner
            self.disabled = results.disabled
            self.creation_date = results.creation_date

           #return results

    def disable(self):

        cursor, conn = sqlServerConnect()

        cursor.execute("UPDATE projects SET disabled = 1 WHERE ID = ?", self.ID)

        conn.commit()

    
    def activate(self):

        cursor, conn = sqlServerConnect()

        cursor.execute("UPDATE projects SET disabled = 0 WHERE ID = ?", self.ID)

        conn.commit()

    def allInfo(self):
        return self.project_name

    def getSteps(self):

        cursor, conn = sqlServerConnect()

        cursor.execute("SELECT * FROM project_steps WHERE parent_project = ? ORDER BY step_order ASC", self.ID)
        results = cursor.fetchall()

        if results:
            return results
        else:
            empty = []
            return empty



class ProjectStep:

    def __init__(self, params):

        cursor, conn = sqlServerConnect()

        cursor.execute("SELECT * FROM project_steps WHERE id = ?", params.get('id'))
        results = cursor.fetchone()

        if results:
            #We need to return the project's info and set the class
            self.ID = results.ID
            self.parent_project = results.parent_project
            self.step_description = results.step_description
            self.step_order = results.step_order
            self.step_owner = results.step_owner
            self.step_priority = results.step_priority
            self.step_color = results.step_color
            self.creation_date = results.creation_date

    def complete(self):

        cursor, conn = sqlServerConnect()

        cursor.execute("UPDATE project_steps SET step_completion = 1 WHERE ID = ?", self.ID)

        conn.commit()
        







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


def getProjects(status):

    cursor, conn = sqlServerConnect()

    if status == 'active':
        status = 0
    else:
        status = 1

    cursor.execute("SELECT p.ID, p.project_name, p.project_description, p.project_length, u.username AS project_owner, p.creation_date, '', '' FROM projects p LEFT JOIN users u ON u.ID = p.project_owner WHERE p.disabled = ? ", status)
    rows = cursor.fetchall()

    rowarray_list = []
    for row in rows:
        t = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        rowarray_list.append(t)

    final_array = {'data': rowarray_list}
    j = json.dumps(final_array, indent=4, sort_keys=True, default=str)

    if rows:
        return final_array
    else:
        return rowarray_list

def checkSession():
    
    if "userName" in session:
        return True
    else:
        return False




