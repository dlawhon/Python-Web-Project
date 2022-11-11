from flask import session

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
        session["userName"] = results.username
        session["userEmail"] = results.email

        return True
    else:
        return False

def logoutUser():

    #session.clear()
    session.pop("userID", None)
    session.pop("userName", None)
    session.pop("userEmail", None)
    return True

class User:

    def __init__(self, passUsername, passEmail=None):

        cursor, conn = sqlServerConnect()

        cursor.execute("SELECT * FROM users WHERE username = ?", passUsername)
        results = cursor.fetchone()

        if results:
            #We need to return the user's info and set the class
            self.email = results.ID
            self.username = results.username
            self.email = results.email

            return results
        else:
            #We need to add a new user
            cursor.execute("INSERT INTO users (username, email) VALUES (?,?)", passUsername, passEmail);
            cursor.commit()

            cursor.execute("SELECT @@IDENTITY AS ID;")
            newID = cursor.fetchone()[0]

            self.email = newID
            self.username = passUsername
            self.email = passEmail

            loginUser(newID)

    def setUsername(passUsername):
        self.username = passUsername

    def getUsername(self):
        return self.username

    def allInfo(self):
        return self

def checkSession():
    
    if "userName" in session:
        return True
    else:
        return False


