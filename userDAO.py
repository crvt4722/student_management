import mysql.connector

mydb = mysql.connector.connect(user='root',password='04072002',host='localhost',database='student_management')
mycursor = mydb.cursor()

def getIdLec(email_phone):
    sql = 'SELECT id FROM lecturer WHERE email_phone = %s'
    val = (email_phone,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()

    return list(myresult[0])[0]

def insertRollcall(attend_code,sbj_code,lec_id):
    sql = 'INSERT INTO rollcall VALUES(%s,%s,%s)'
    val = (attend_code,sbj_code,lec_id)
    mycursor.execute(sql,val)
    mydb.commit()

def insertSubject(lec_id , sbj_code):
    sql = 'SELECT * FROM subject WHERE sbj_code = %s'
    val = (sbj_code,)
    mycursor.execute(sql,val)

    if len(mycursor.fetchall()) == 0:
        sql = 'INSERT INTO subject VALUES(%s,%s)'
        val = (lec_id, sbj_code)
        mycursor.execute(sql, val)
        mydb.commit()

def isValidSbjCode(lec_id,sbj_code):
    sql = 'SELECT * FROM subject WHERE lec_id = %s AND sbj_code = %s'
    val = (lec_id,sbj_code,)
    mycursor.execute(sql,val)
    if len(list(mycursor.fetchall())) == 0 :
        return False
    return True

def insertAttendance(stu_code, sbj_code,attend_code):
    try:
        sql = 'INSERT INTO attendance VALUES(%s,%s,%s,now())'
        val = (stu_code, sbj_code, attend_code)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    except:
        return False

def isValidRollCall(attend_code,sbj_code):
    sql = 'SELECT * FROM rollcall WHERE attend_code = %s AND sbj_code = %s'
    val = (attend_code,sbj_code,)
    mycursor.execute(sql,val)
    if len(mycursor.fetchall()) == 0:
        return False
    return True

def isValidAttendanceCode(attend_code):
    sql = 'SELECT * FROM rollcall WHERE attend_code = %s'
    val = (attend_code,)
    mycursor.execute(sql, val)
    if len(mycursor.fetchall()) == 0:
        return False
    return True

def getAllAbsence(attend_code,add_or_not):
    sql = ''' SELECT DISTINCT id,absent FROM student,attendance
                  WHERE student.sbj_code = attendance.sbj_code
                  AND id NOT IN (SELECT stu_code FROM attendance WHERE attend_code = %s)'''
    val = (attend_code,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    if add_or_not == True:
        for row in range(len(myresult)):
            sql = 'UPDATE student SET absent = {} WHERE id = %s'.format(str(int(myresult[row][1]) + 1))
            # print(int(myresult[row][1]))
            val = (myresult[row][0],)
            mycursor.execute(sql, val)
            mydb.commit()
    return myresult

def getAbsenceBeforeTime(limit_time,attend_code,add_or_not):
    sql = ''' SELECT DISTINCT id,absent FROM student,attendance
                  WHERE student.sbj_code = attendance.sbj_code 
                  AND id NOT IN (SELECT stu_code FROM attendance WHERE attend_code = %s AND date_time < %s)'''
    val = (attend_code,limit_time,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    if add_or_not == True:
        for row in range(len(myresult)):
            sql = 'UPDATE student SET absent = {} WHERE id = %s'.format(myresult[row][1] + 1)
            val = (myresult[row][0],)
            mycursor.execute(sql, val)
            mydb.commit()
    return myresult

def refreshBan():
    sql = 'UPDATE student SET banned = %s WHERE absent >=3'
    val = ('Yes',)
    mycursor.execute(sql, val)
    mydb.commit()

# In library

def getInfoBook(status):
    if status != 'all':
        sql = 'SELECT * FROM library_book WHERE status = %s'
        val = (status,)
        mycursor.execute(sql, val)
    else:
        sql = 'SELECT * FROM library_book'
        mycursor.execute(sql)
    return mycursor.fetchall()

def getBorrowedBook():
    sql = 'SELECT * FROM book_borrowed'
    mycursor.execute(sql)
    return mycursor.fetchall()

def checkExistBook(book_code):
    sql = 'SELECT * FROM library_book WHERE book_code = %s AND status = %s'
    val = (book_code,'exist',)
    mycursor.execute(sql,val)
    return len(mycursor.fetchall()) > 0

def insertBorrowedBook(book_code, stu_code ):
    sql = 'INSERT INTO book_borrowed VALUES (%s,%s,now())'
    val = (book_code,stu_code)
    mycursor.execute(sql,val)
    mydb.commit()

    sql = 'UPDATE library_book SET status = %s WHERE book_code = %s'
    val = ('borrowed',book_code,)
    mycursor.execute(sql,val)
    mydb.commit()

def giveBookBack(book_code):
    sql  = 'DELETE FROM book_borrowed WHERE book_code = %s'
    val = (book_code,)
    mycursor.execute(sql, val)
    mydb.commit()

    sql = 'UPDATE library_book SET status = %s WHERE book_code = %s'
    val = ('exist', book_code,)
    mycursor.execute(sql, val)
    mydb.commit()

def accessInLibrary(stu_code):
    if stu_code == '':
        return
    sql = 'INSERT INTO library_access VALUES(%s,now(),null)'
    val = (stu_code,)
    mycursor.execute(sql,val)
    mydb.commit()

def accessOutLibrary(stu_code):
    if stu_code =='':
        return
    sql = 'UPDATE library_access SET time_out = now() WHERE stu_code = %s'
    val = (stu_code,)
    mycursor.execute(sql,val)
    mydb.commit()

def getStudentAccess():
    sql = 'SELECT * FROM library_access'
    mycursor.execute(sql)
    return mycursor.fetchall()

def isDuplicateStudentCode(stu_code):
    sql = 'SELECT * FROM student WHERE id = %s'
    val = (stu_code,)
    mycursor.execute(sql,val)

    return len(mycursor.fetchall()) > 0

def getFullName (stu_code):
    sql = 'SELECT fullname FROM student WHERE id = %s'
    val = (stu_code,)
    mycursor.execute(sql,val)

    return mycursor.fetchall()[0][0]

def showAll():
    sql = 'SELECT * FROM student'
    mycursor.execute(sql)
    return mycursor.fetchall()

def showBasedOnSbj(sbj_code):
    sql = 'SELECT * FROM student WHERE sbj_code = %s'
    val = (sbj_code,)
    mycursor.execute(sql, val)
    return mycursor.fetchall()

def insertStudent(a,b,c,d,e,f,g,h):
    sql = 'INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s,0,%s,%s)'
    val = (a,b,c,d,e,f,g,h)
    mycursor.execute(sql, val)
    mydb.commit()

def deleteStudent(stu_code):
    sql = 'set sql_safe_updates = 0'
    mycursor.execute(sql)

    sql = 'delete from student where id = %s'
    val = (stu_code,)
    mycursor.execute(sql, val)
    mydb.commit()

def updateStudent(gpa,stu_code):
    sql = 'set sql_safe_updates = 0'
    mycursor.execute(sql)

    sql = 'update student set gpa = %s where id = %s'
    val = (gpa,stu_code,)

    mycursor.execute(sql, val)
    mydb.commit()