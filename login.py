from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import mysql.connector
mydb = mysql.connector.connect(user='root',password='04072002',host='localhost',database='student_management')
mycursor = mydb.cursor()

profile = ''

class Login(QtWidgets.QMainWindow):
    global profile
    def __init__(self):
        super().__init__()
        uic.loadUi("display/login.ui",self)

    def isTrueInfo(self):
        global profile
        sql = 'SELECT * FROM lecturer WHERE email_phone = %s'
        email_phone = self.username.text()
        password = self.password.text()

        val = (email_phone,)
        mycursor.execute(sql, val)
        result_1 = mycursor.fetchall()

        sql = 'SELECT * FROM lecturer WHERE email_phone = %s AND password = %s'
        val = (email_phone, password,)
        mycursor.execute(sql, val)
        result_2 = mycursor.fetchall()

        if len(result_1) == 0:
            self.alert.setText("Email/phone is invalid!")
            return False
        elif len(result_2) == 0:
            self.alert.setText("Password is incorrect!")
            return False

        profile = email_phone
        self.alert.setText('')
        return True

def getProfile():
    return profile

