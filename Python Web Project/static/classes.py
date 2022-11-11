def sqlServerConnect():
    import pyodbc

    conn = pyodbc.connect("DRIVER={ODBC driver 17 for SQL Server};SERVER=(localdb)\ProjectModels;DATABASE=PythonWebProjectDB;Trusted_Connection=yes;")
    cursor = conn.cursor()

    return cursor, conn

# #conn = pyodbc.connect('DRIVER={SQL Server};''SERVER=DESKTOP-M5804D6\LOCALDB#1C80D2FA;''DATABASE=PythonWebProjectDB;''''''Trusted_Connection=no;')