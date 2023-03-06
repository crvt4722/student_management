from PyQt6.QtWidgets import  QMainWindow,QApplication
from PyQt6 import  uic

class RollCall(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('display/attendance.ui',self)

class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display/register.ui",self)

# In function
class Add(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display/add.ui",self)

class Delete(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display/delete.ui",self)

class Update(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display/update.ui",self)

class Show(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display/showsbj.ui",self)

class CreateCode(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display/createcode.ui",self)

class Absence(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display/absence.ui",self)

# In library
class BookStatus(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('display/bookstatus.ui',self)

class BorrowedBook(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('display/borrowedbook.ui',self)

class LibraryAcess(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('display/libraryacess.ui',self)
