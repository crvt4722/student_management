import re

def isBirthDay(s):
    if len(s) != 10:
        return False
    arr = s.split('/')
    if len(arr) != 3:
        return False
    if len(arr[0]) != 2 or len(arr[1]) !=2 or len(arr[2])!=4 :
        return False

    try:
        day = int(arr[0])
        month = int(arr[1])
        year = int(arr[2])

        if day <=0 or day > 31:
            return False
        if month <= 0 or month > 12:
            return False
        if year < 1900:
            return False

        return True
    except:
        pass
    return False

def isDateTimeFormat(limit_time):
    try:
        date, time = limit_time.split()
        if len(date) != 10:
            return False
        if len(time) != 8:
            return False
        if len(limit_time) != 19:
            return False

        y, m, d = date.split('-')

        try:
            y = int(y)
            m = int(m)
            d = int(d)

            if y < 1900:
                return False
            if m <= 0 or m > 12:
                return False
            if d < 1 or d > 31:
                return False
        except:
            return False

        try:
            h, m, s = time.split(':')
            h = int(h)
            m = int(m)
            s = int(s)
            if h < 0 or h > 24:
                return False
            if m < 0 or m > 60:
                return False
            if s < 0 or s > 60:
                return False
        except:
            return False
    except:
        return False
    return True

def isStudentCode(stu_code = ''):
    #b20dccn606
    if len(stu_code) != 10:
        return False

    year = stu_code[1:3]
    faculty = stu_code[5:7]
    id = stu_code[7:]
    try:
        year= int(year)
        id = int(id)
        if year == 0 :
            return False
        if id == 0:
            return False
    except:
        return False
    x = re.findall('[A-Z]+',faculty)
    if len(x) == 0:
        return False
    return stu_code[0] == 'B' and stu_code[3:5] == 'DC'

