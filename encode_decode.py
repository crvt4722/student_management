def encodeStudent(stu_code = ''):
    #b20dccn606
    try:
        year = stu_code[1:3]
        faculty = stu_code[5:7]
        id = stu_code[7:]

        code = year+id
        if faculty == 'CN':
            code += '1'
        if faculty == 'AT':
            code += '2'
        if faculty == 'MR':
            code += '3'
        return int(code)
    except:
        return -1

def decodeStudent(id = 0):
    stu_code = str(id)
    year = stu_code[:2]
    stt = stu_code[2:5]
    department = stu_code[-1]
    faculty = ''
    if department == '1':
        faculty = 'CN'
    if department == '2':
        faculty ='AT'
    if department == '3':
        faculty = 'MR'
    return 'B' + year +'DC'+faculty+stt
