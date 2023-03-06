import sys
from PyQt6.QtWidgets import  QApplication,QMainWindow,QTableWidgetItem,QTableWidget
from PyQt6 import  uic, QtCore
from model import BookStatus, BorrowedBook, LibraryAcess
import userDAO

class Library(QMainWindow):
    def __init__(self):
        super(Library, self).__init__()
        uic.loadUi('display/library.ui',self)

        self.book_btn.clicked.connect(self.showBookStatus)
        self.bookstatus = BookStatus()

        self.borrowedbook = BorrowedBook()
        self.borrowed_btn.clicked.connect(self.showBorrowedBook)

        self.access = LibraryAcess()
        self.access_btn.clicked.connect(self.showAccess)
    def showAccess(self):
        self.access.show()
        self.access.button.clicked.connect(self.processAccess)

    def showBorrowedBook(self):
        self.borrowedbook.show()
        self.borrowedbook.button.clicked.connect(self.processBorrowedBook)

    def processBorrowedBook(self):
        if self.borrowedbook.seeall.isChecked():
            myresult = userDAO.getBorrowedBook()
            self.borrowedbook.hide()

            self.show_table.setColumnCount(3)
            column_name = ['Book code', 'Student code','Date and time']
            self.show_table.setHorizontalHeaderLabels(column_name)
            self.show_table.setColumnCount(3)
            self.show_table.setRowCount(0)
            self.show_table.show()
            for row_num, row_data in enumerate(myresult):
                self.show_table.insertRow(row_num)
                for col_num, col_data in enumerate(row_data):
                    self.show_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
        else:
            stu_code = self.borrowedbook.stu_code.text()
            book_code = self.borrowedbook.book_code.text()

            if self.borrowedbook.giveback.isChecked():
                userDAO.giveBookBack(book_code)

                self.borrowedbook.stu_code.setText('')
                self.borrowedbook.book_code.setText('')
                self.borrowedbook.alert.setText('')
                self.borrowedbook.hide()
                return


            print(book_code)
            check_exist = userDAO.checkExistBook(book_code)
            if check_exist == False:
                # self.borrowedbook.alert.setText('This book is borrowed or not exist!')
                return
            self.borrowedbook.alert.setText('')
            userDAO.insertBorrowedBook(book_code, stu_code)

            self.borrowedbook.stu_code.setText('')
            self.borrowedbook.book_code.setText('')
            self.borrowedbook.alert.setText('')
            self.borrowedbook.hide()
    def processAccess(self):

        stu_code = self.access.stu_code.text()
        print(stu_code)
        if self.access.in_radio.isChecked():
            userDAO.accessInLibrary(stu_code)
        elif self.access.out_radio.isChecked():
            userDAO.accessOutLibrary(stu_code)
        else:
            myresult = userDAO.getStudentAccess()
            self.show_table.setColumnCount(3)
            column_name = ['Student code', 'Time in','Time out']
            self.show_table.setHorizontalHeaderLabels(column_name)
            self.show_table.setColumnCount(3)
            self.show_table.setRowCount(0)
            self.show_table.show()
            for row_num, row_data in enumerate(myresult):
                self.show_table.insertRow(row_num)
                for col_num, col_data in enumerate(row_data):
                    self.show_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

        self.access.stu_code.setText('')
        self.access.hide()

    def showBookStatus(self):
        self.bookstatus.show()
        self.bookstatus.button.clicked.connect(self.processBookStatus)
    def processBookStatus(self):
        myresult = 0
        if self.bookstatus.borrow.isChecked():
            myresult = userDAO.getInfoBook('borrowed')
        if self.bookstatus.exist.isChecked():
            myresult = userDAO.getInfoBook('exist')
        if self.bookstatus.all.isChecked():
            myresult = userDAO.getInfoBook('all')

        self.bookstatus.hide()

        self.show_table.setColumnCount(3)
        column_name = ['Book code', 'Name','State']
        self.show_table.setHorizontalHeaderLabels(column_name)
        self.show_table.setColumnCount(3)
        self.show_table.setRowCount(0)
        self.show_table.show()
        for row_num, row_data in enumerate(myresult):
            self.show_table.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.show_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
