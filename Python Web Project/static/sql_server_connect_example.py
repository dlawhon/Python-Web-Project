def sqlServerConnect():
    import pyodbc

    conn = pyodbc.connect("DRIVER={SQL Server};SERVER=YOURSERVERNAME;DATABASE=YOURDATABASENAME;UID=YOURUSERID;PWD=YOURUSERPASSWORD")
    cursor = conn.cursor()

    return cursor, conn

#ODBC driver 17 for SQL Server for local db connections
#SQL Server for normal connections