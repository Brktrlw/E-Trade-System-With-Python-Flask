from errorLogger import BaseErrorLogger
from datetime import datetime
import sqlite3
import mysql.connector

class DatabaseLoggers(BaseErrorLogger):
    @staticmethod
    def databaseLogger(exception):
        errorTime=datetime.now()
        try:
            connection=sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"INSERT INTO Errors ('ErrorMessage','ErrorTime') VALUES ('{exception}','{errorTime}')")
            connection.commit()

            #mysqlConnection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            #mysqlCursor = mysqlConnection.cursor()
            #mysqlCursor.execute(f"INSERT INTO Errors (ErrorMessage,ErrorTime) VALUES ('{exception}','{errorTime}')")
            #mysqlConnection.commit()
        except:
            pass
        finally:
            connection.close()
            #mysqlConnection.close()







