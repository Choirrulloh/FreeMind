
# function create databse if not exists
# v 1.0 - final
def create():
    if not os.path.isfile("freemind.db"):
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS errorlog(
                          id INTEGER PRIMARY KEY,
                          error INTEGER,
                          date TEXT,
                          time TEXT);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS updatelog(
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          time TEXT,
                          updatetyp INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS recycleready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""") # 0 = not ready, 1 = ready
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                          drive INTEGER PRIMARY KEY,
                          total TEXT,
                          free TEXT,
                          percent INTEGER,
                          smart INTEGER);""") # id = drive
        cursor.execute("""CREATE TABLE IF NOT EXISTS backupready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""") # 0 = not ready, 1 = ready
        connection.close()



# function insert data in database
# v 1.0 - final
def insert(dbtarget, dbdata): # dbtarget: table, dbdataarray: data for table

    if dbtarget == 1: # insert backupready
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        try:
            # yapf: disable
            cursor.execute("""UPDATE backupready SET ready=?
                              WHERE id = 1""", (ready))
            connection.commit()
            connection.close()
            # yapf: enable
        except:
            # yapf: disable
            cursor.execute("""INSERT INTO backupready(id, ready)
                              VALUES(1,?)""", (ready))
            connection.commit()
            connection.close()
            # yapf: enable
    elif dbtarget == 2: # insert recycleready
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        try:
            # yapf: disable
            cursor.execute("""UPDATE recycleready SET ready=?
                              WHERE id=1""", (ready))
            connection.commit()
            connection.close()
            # yapf: enable
        except:
            # yapf: disable
            cursor.execute("""INSERT INTO recycleready(id, redeay)
                              VALUES(1,?)""", (ready))
            connection.commit()
            connection.close()
            # yapf: enable
    #else...


# function get data from database
# v 1.0 - final
def get(dbtarget):
    if dbtarget == 1: # get backupready
        try:
            connection = sqlite3.connect("freemind.db")
            cursor = connection.cursor()
            # yapf: disable
            cursor.execute("""SELECT * FROM backupready WHERE id=1""") # * should be replaced by colum
            # yapf: enable
            ready = cursor[1]
            connection.close()
        except:
            ready = "err"
        ready = str(ready)
        return ready
    elif dbtarget == 2: # get recycleready
        try:
            connection = sqlite3.connect("freemind.db")
            cursor = connection.cursor()
            # yapf: disable
            cursor.execute("""SELECT * FROM recycleready WHERE id=1""")
            # yapf: enable
            ready = cursor[1]
            connection.close()
        except:
            ready = "err"
        ready = str(ready)
        return ready
    else:
        ready = "value"
        return ready


# function insert data for logging
# v 1.1 - final
def logging(dbtarget, dbdata):
    if dbtarget == 1: # insert error
        i = 1
        dberror = int(dbdata)
        dbdate = time.strftime("%Y-%m-%d", time.gmtime())
        dbtime = time.strftime("%H-%M", time.gmtime())
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        while True:
            try:
                # yapf: disable
                cursor.execute("""INSERT INTO errorlog(id, error, date, time)
                                  VALUES(?,?,?,?)""", (i, dberror, dbdate, dbtime))
                # yapf: enable
            except:
                i += 1
                if i >= 9999:
                    break
            else:
                connection.commit()
                break
        connection.close()
        if not i >= 9999:
            result = "okay"
        else:
            result = "dbfull"
        return result
    elif dbtarget == 2: # insert update
        dbupdatetyp = dbdata # 1=FM master; 2=FM slave; 3=OS master; 4=OS slave
        i = 1
        dbupdatetyp = int(dbupdatetyp)
        dbdate = time.strftime("%Y-%m-%d", time.gmtime())
        dbtime = time.strftime("%H-%M", time.gmtime())
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        while True:
            try:
                # yapf: disable
                cursor.execute("""INSERT INTO updatelog(id, date, time, update)
                                  VALUES(?,?,?,?)""", (i, dbdate, dbtime, dbupdatetyp))
                # yapf: enable
                connection.commit()
            except:
                i += 1
                if i >= 9999:
                    break
            else:
                break
        connection.close()
        if not i >= 9999:
            result = "okay"
        else:
            result = "dbfull"
        return result


# function read logs out of database
# v 1.0 - final
def readlogs(dbtarget, dbdata):
    if dbtarget == 1: # read errors
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT COUNT(*) FROM errorlog""") # Was ist COUNT?????
        if cursor.fetchone():
            cursor.execute("""SELECT * FROM errorlog ORDER BY id ASC""")
        else:
            cursor = "error"
        connection.close()
        result = cursor
        return result
    elif dbtarget == 2: # read update
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        updatetyp = int(dbdata)
        cursor.execute("""SELECT * FROM updatelog ORDER BY id DESC""")
        for element in cursor:
            if element[3] == dbdata: # is here int() necessary
                dbres == element[1] + "+" + element[2]
                break
            else:
                pass
        connection.close()
        if "+" not in dbres:
            result = "error"
        else:
            result = dbres
        return result


# give this function 2 dates and you will get timediff
# only works with dates created with time.strftime("%Y-%m-%d", time.gmtime())
def timediff(olddate, newdate):
    olddate = str(olddate)
    newdate = str(newdate)
    olddatesplit = olddate.split("-")
    newdatesplit = newdate.split("-")
    # yapf: disable
    olddatetuple = (int(olddatesplit[0]), int(olddatesplit[1]),int(olddatesplit[2]), 0, 0, 0, 0, 0, 0)
    newdatetuple = (int(newdatesplit[0]), int(newdatesplit[1]),int(newdatesplit[2]), 0, 0, 0, 0, 0, 0)
    # yapf: enable
    olddate = time.mktime(olddatetuple)
    newdate = time.mktime(newdatetuple)
    diff = newdate - olddate
    diff = diff // 86400  # ganzzahlige division durch 24h, da Ergebnis in Sekunden
    return diff
