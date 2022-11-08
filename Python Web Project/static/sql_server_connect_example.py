def sqlServerConnect():
    import pyodbc

    conn = pyodbc.connect("DRIVER={SQL Server};SERVER=YOURSERVERNAME;DATABASE=YOURDATABASENAME;UID=YOURUSERID;PWD=YOURUSERPASSWORD")
    cursor = conn.cursor()

    return cursor, conn