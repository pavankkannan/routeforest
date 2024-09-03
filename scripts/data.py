import sqlite3

def select_one_row(dbConn, sql, parameters = None):
    if (parameters == None): ## if no parameters are passed through, assigned an empty bracket for sql query
       parameters = []

    dbCursor = dbConn.cursor()

    try:
        dbCursor.execute(sql, parameters)
        row = dbCursor.fetchone()
        if row is None:
            return () ## returns empty list if nothing is found in the query
        else:
            return row ## otherwise returns the row result
    except Exception as err:
        print("select_one_row failed:", err)
        return None ## returns none in case of an error
    finally:
        dbCursor.close()
        
def select_n_rows(dbConn, sql, parameters = None):
    if (parameters == None): ## if no parameters are passed through, assigned an empty bracket for sql query
       parameters = []

    dbCursor = dbConn.cursor()

    try:
       dbCursor.execute(sql, parameters) ## runs the query
       rows = dbCursor.fetchall()
       return rows ## returns the tuple of lists from fetchall
    except Exception as err:
       print("select_n_rows failed:", err)
       return None ## returns none if invalid query or other error
    finally:
       dbCursor.close()