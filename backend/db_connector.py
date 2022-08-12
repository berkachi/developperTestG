from genericpath import exists
import logging
import sqlite3
from sqlite3 import Connection, Cursor

logging.getLogger().addHandler(logging.StreamHandler())

class DBConnector:

    def createConnection(dbFile):
        #connect database to SQLite database

        fileExists = exists(dbFile)
      
        if fileExists:
            try:
                con = sqlite3.connect(dbFile)
                logging.debug("Successfully connected to DB: "+dbFile)
                return con
         
            except:
                logging.exception("Could not connect to DB: "+dbFile)
                raise DBConnectionFail()

        else:
            raise DBFileNotFound()

    def iterator(dbFile, query):
        #iterate over results of a databse query

        con = DBConnector.createConnection(dbFile=dbFile)
   
        if con is not None:
            iterate = con.cursor()
            return iterate



class DBFileNotFound(Exception):
    #File is not Found

    def __init__(self,message="Database File Not Found !"):
        self.message = message
        super().__init__(self.message)



class DBConnectionFail(Exception):
    #Connection to DB didn't work

    def __init__(self, message="Couldn't Connect To Dabase !"):
        self.message=message
        super().__init__(self.message)



    