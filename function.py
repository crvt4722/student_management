import sys
from PyQt6.QtWidgets import  QApplication,QMainWindow,QTableWidgetItem,QTableWidget
from PyQt6 import  uic, QtCore

import validate
from model import Add, Delete, Update, Show, CreateCode, Absence
import mysql.connector
from validate import isBirthDay, isDateTimeFormat
from login import getProfile
import userDAO

mydb = mysql.connector.connect(user='root',password='04072002',host='localhost',database='student_management')
mycursor = mydb.cursor()

class Function(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display/function.ui",self)


        self.add = Add()
        self.add_btn.clicked.connect(self.addWindow)

        self.delete = Delete()
        self.delete_btn.clicked.connect(self.deleteWindow)

        self.update = Update()
        self.update_btn.clicked.connect(self.updateWindow)

        self.show_table.hide()
        self.show_btn.clicked.connect(self.showWindow)
        self.show_ = Show()

        self.createcode = CreateCode()
        self.rollcall_btn.clicked.connect(self.showCreateCode)

        self.absence = Absence()
        self.absence_btn.clicked.connect(self.showAbsence)

        self.refresh_btn.clicked.connect(self.refresh)

    def refresh(self):
        userDAO.refreshBan()

    def showAbsence(self):
        self.absence.show()
        self.absence.button.clicked.connect(self.processAbsense)

    def processAbsense(self):
        attend_code = self.absence.attend_code.text()
        print(attend_code)
        limit_time = self.absence.limit_time.text()
        add_or_not = self.absence.add_absence.isChecked()
        if userDAO.isValidAttendanceCode(attend_code) == False:
            self.absence.alert.setText('Attend code is invalid!')
            return
        if self.absence.none_check.isChecked() == False:
            if isDateTimeFormat(limit_time) == False:
                self.absence.alert.setText('Please input correct the datetime format!')
                return
            myresult = userDAO.getAbsenceBeforeTime(limit_time,attend_code,add_or_not)
        else:
            myresult = userDAO.getAllAbsence(attend_code,add_or_not)

        self.absence.hide()
        column_name = ['Student code','Absent']
        self.show_table.setHorizontalHeaderLabels(column_name)
        self.show_table.setColumnCount(2)
        self.show_table.setRowCount(0)
        self.show_table.show()
        for row_num, row_data in enumerate(myresult):
            self.show_table.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.show_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))



    def showCreateCode(self):
        self.createcode.show()

        lec_id = userDAO.getIdLec(getProfile())
        self.createcode.attend_code.setText(lec_id)

        self.createcode.button.clicked.connect(self.processCreateCode)
    def showWindow(self):
        self.show_.show()
        self.show_.button.clicked.connect(self.processShow)
    def addWindow(self):
        self.add.show()
        self.add.button.clicked.connect(self.processAdd)

    def deleteWindow(self):
        self.delete.show()
        self.delete.button.clicked.connect(self.processDelete)

    def updateWindow(self):
        self.update.show()
        self.update.button.clicked.connect(self.processUpdate)

    def processAdd(self):
        birth = self.add.birthday.text()
        if userDAO.isDuplicateStudentCode(self.add.stu_code.text()):
            self.add.alert.setText('Student code is duplicate!')
            return

        if self.add.stu_code.text() =='' or self.add.fullname.text() =='' or self.add.gpa.text() =='' or self.add.sbj_code.text()=='' or birth=='':
            self.add.alert.setText('Please fill all the necessary information!')
            return

        if isBirthDay(birth) == False:
            self.add.alert.setText("Invalid birthday!")
            return

        self.add.alert.setText('')
        userDAO.insertStudent(self.add.stu_code.text(),self.add.fullname.text(),birth,self.add.class_name.text(),self.add.gpa.text(),'No',self.add.sbj_code.text(),getProfile())

        userDAO.insertSubject(userDAO.getIdLec(getProfile()),self.add.sbj_code.text())

        self.add.fullname.setText('')
        self.add.birthday.setText('')
        self.add.stu_code.setText('')
        self.add.class_name.setText('')
        self.add.gpa.setText('')
        self.add.sbj_code.setText('')
        self.add.hide()

    def processDelete(self):
        userDAO.deleteStudent(self.delete.stu_code.text())

        self.delete.stu_code.setText('')
        self.delete.hide()

    def processUpdate(self):
        userDAO.updateStudent(self.update.gpa.text(),self.update.stu_code.text())

        self.update.gpa.setText('')
        self.update.stu_code.setText('')
        self.update.hide()

    def processShow(self):
        # self.show_.hide()
        column_name = ['id', 'fullname', 'birthday', 'class', 'gpa', 'banned', 'absence', 'sbj_code', 'lecturer_code']

        if self.show_.all.isChecked():
            result = userDAO.showAll()
        else:
            sbj_code = self.show_.sbj_code.text()
            result = userDAO.showBasedOnSbj(sbj_code)
        self.show_table.setColumnCount(9)
        self.show_table.setHorizontalHeaderLabels(column_name)
        self.show_table.setColumnCount(9)
        self.show_table.setRowCount(0)
        self.show_table.show()
        for row_num, row_data in enumerate(result):
            self.show_table.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.show_table.setItem(row_num,col_num,QTableWidgetItem(str(col_data)))
        self.show_.hide()

    def processCreateCode(self):
        attend_code = self.createcode.attend_code.text()
        sbj_code = self.createcode.sbj_code.text()
        lec_id = userDAO.getIdLec(getProfile())

        if userDAO.isValidSbjCode(lec_id,sbj_code) == False:
            self.createcode.alert.setText('The subject code does not exist!')
            return

        self.createcode.alert.setText('')
        userDAO.insertRollcall(attend_code,sbj_code,lec_id)
        self.createcode.attend_code.setText('')
        self.createcode.sbj_code.setText('')
        self.createcode.hide()