def sqlServerConnect():
    import pyodbc

    conn = pyodbc.connect("DRIVER={ODBC driver 17 for SQL Server};SERVER=(localdb)\ProjectModels;DATABASE=PythonWebProjectDB;Trusted_Connection=yes;")
    cursor = conn.cursor()

    return cursor, conn