from login import Login
from function import Function
from library import Library
from model import RollCall, Register
from faceRecognition import  faceRecognition, takePhotos,trainData
from PyQt6.QtWidgets import  QApplication,QMainWindow,QMessageBox
import sys
import mysql.connector
import userDAO
from encode_decode import encodeStudent,decodeStudent
from validate import isStudentCode

mydb = mysql.connector.connect(user='root',password='04072002',host='localhost',database='student_management')
mycursor = mydb.cursor()

class UI():
    def __init__(self):
        self.login = Login()
        self.login.show()

        self.register = Register()
        self.function = Function()
        self.rollcall = RollCall()
        self.library = Library()
        self.login.register_btn.clicked.connect(self.changeRegister)
        self.login.login_btn.clicked.connect(self.processLogin)
        self.login.rollcall_btn.clicked.connect(self.processTakeRollCall)

        self.register.button.clicked.connect(self.processRegister)
        self.register.login_btn.clicked.connect(self.changeLogin)

        self.function.logout_btn.clicked.connect(self.processLogout)
        self.function.library_btn.clicked.connect(self.processLibrary)

        self.rollcall.back_btn.clicked.connect(self.backToLogin)

        self.library.back_btn.clicked.connect(self.fromLibraryBackFunction)

    def processLibrary(self):
        self.function.hide()
        self.library.show()

    def fromLibraryBackFunction(self):
        self.library.hide()
        self.function.show()

    def processLogout(self):
        self.function.hide()
        self.login.show()

    def changeLogin(self):
        self.register.hide()
        self.login.show()

    def backToLogin(self):
        self.rollcall.alert.setText('')
        self.rollcall.sbj_code.setText('')
        self.rollcall.stu_code.setText('')
        self.rollcall.attend_code.setText('')

        self.rollcall.hide()
        self.login.show()


    def processRegister(self):
        self.register.alert.setText('')

        if self.register.fullname.text() =='' or self.register.email_phone.text()=='' or self.register.lecturer_code.text()=='' or self.register.password.text()=='':
            self.register.alert.setText('Please fill all the necessary information!')
            return

        sql = 'SELECT * FROM lecturer WHERE email_phone = %s'
        val = (self.register.email_phone.text(),)
        mycursor.execute(sql, val)
        if len(mycursor.fetchall()) > 0:
            self.register.alert.setText('Email/phone is duplicate!')
            return

        sql = 'SELECT * FROM lecturer WHERE id = %s'
        val = (self.register.lecturer_code.text(),)
        mycursor.execute(sql, val)

        if len(mycursor.fetchall()) > 0:
            self.register.alert.setText('Lecturer code is currently used!')
            return

        pw = self.register.password.text()
        pw_cf = self.register.password_confirmed.text()
        if pw != pw_cf:
            self.register.alert.setText('Confirm the password again!')
            return

        self.register.alert.setText('')
        sql = 'INSERT INTO lecturer VALUES (%s,%s,%s,%s,%s,%s,%s)'
        gender = ''
        if (self.register.male.isChecked()):
            gender = 'male'
        else:
            gender = 'female'
        val = (self.register.lecturer_code.text(), self.register.fullname.text(), gender, self.register.university.currentText(),
               self.register.faculty.currentText(), self.register.password.text(), self.register.email_phone.text())

        mycursor.execute(sql, val)
        mydb.commit()

        self.register.hide()
        self.login.show()

    def changeRegister(self):
        self.login.hide()
        self.register.show()

    def processLogin(self):
        if self.login.isTrueInfo():
            self.login.alert.setText('')
            self.login.hide()
            self.function.show()
        pass

    def processTakeRollCall(self):
        self.login.hide()
        self.rollcall.show()
        # self.rollcall.button.clicked.connect(self.processAttendance)
        self.rollcall.face_recognition.clicked.connect(self.processFaceRecognition)
        self.rollcall.take_photo.clicked.connect(self.processTakePhoto)

    def processTakePhoto(self):
        stu_code = self.rollcall.stu_code.text()
        sbj_code = self.rollcall.sbj_code.text()

        if isStudentCode(stu_code) == False:
            self.rollcall.alert.setText('Invalid student code!!!')
            return
        self.rollcall.alert.setText('')
        takePhotos(encodeStudent(stu_code))
        trainData()


    def processFaceRecognition(self):
        stu_code = self.rollcall.stu_code.text()
        sbj_code = self.rollcall.sbj_code.text()
        attend_code = self.rollcall.attend_code.text()

        if isStudentCode(stu_code) == False:
            self.rollcall.alert.setText('Invalid student code!!!')
            return
        self.rollcall.alert.setText('')

        result = userDAO.isValidRollCall(attend_code, sbj_code)
        if result == False:
            self.rollcall.alert.setText('Invalid subject code or attendance code !!!')
            return
        elif isStudentCode(stu_code) == False:
            self.rollcall.alert.setText('Invalid student code!!!')
            return

        result_face_recognition = faceRecognition()
        if stu_code != result_face_recognition:
            self.rollcall.alert.setText('You are not ' + stu_code+' !!!')
            return
        self.rollcall.alert.setText('')
        result = userDAO.insertAttendance(stu_code, sbj_code, attend_code)
        if result:
            self.rollcall.alert.setText('Successful !!!')
            stu_code = self.rollcall.stu_code.setText('')
            sbj_code = self.rollcall.sbj_code.setText('')
        else:
            self.rollcall.alert.setText('Try again or you have taken a roll call successfully!')

    # def processAttendance(self):
    #     stu_code = self.rollcall.stu_code.text()
    #     sbj_code = self.rollcall.sbj_code.text()
    #     attend_code = self.rollcall.attend_code.text()
    #
    #     result = userDAO.isValidRollCall(attend_code,sbj_code)
    #     if result == False:
    #         self.rollcall.alert.setText('Invalid subject code or attendance code !!!')
    #     elif isStudentCode(stu_code) == False:
    #         self.rollcall.alert.setText('Invalid student code!!!')
    #     else :
    #         result = userDAO.insertAttendance(stu_code, sbj_code, attend_code)
    #         if result:
    #             self.rollcall.alert.setText('Successful !!!')
    #             stu_code = self.rollcall.stu_code.setText('')
    #             sbj_code = self.rollcall.sbj_code.setText('')
    #         else:
    #             self.rollcall.alert.setText('Try again!')

if __name__ =='__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QMainWindow{
            border-image: url(display/bg1.jpg); 
        }
        QPushButton{
            font-weight:bold;
        }
        QLabel{
            font-weight:bold;
        }
        QRadioButton{
            font-weight:bold;
        }
    ''')
    ui = UI()
    sys.exit(app.exec())