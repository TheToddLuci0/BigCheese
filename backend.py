import psycopg2


def connect():
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")


def getCompany():
    string = list()
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()
    cur.execute("SELECT * FROM company")
    output = cur.fetchall()
    #    for i in output:
    #        string[i][0].append(i[0])
    #        string[i][1].append(i[1])
    return output

def getCompanySearch(companyName):
    string = list()
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()
    cur.execute("SELECT * FROM company WHERE name = '{}'".format(companyName))
    output = cur.fetchall()
    #    for i in output:
    #        string[i][0].append(i[0])
    #        string[i][1].append(i[1])
    return output


def addCompany(companyName, about):
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()
    print(companyName, about)

    check = "SELECT EXISTS (SELECT 1 FROM COMPANY WHERE NAME = '{}');".format(companyName)
    cur.execute(check)
    result = cur.fetchone()[0]

    # return false if company exists
    if result:
        return False

    # if problems close cur and conn and reopen for next operation

    sql = "INSERT INTO COMPANY (NAME,ABOUT,RATE,NUM_RATE) VALUES (%s,%s,%s,%s);"
    cur.execute(sql, (companyName, about, 0, 0))
    conn.commit()
    cur.close()
    conn.close()

    return True

def addReview(companyName, review, score, username):
    current = getCompanySearch(companyName)

    # add review
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()
    sql = "INSERT INTO REVIEW (CNAME,REVIEW,SCORE,UNAME) VALUES ('{}','{}',{},'{}')".format(companyName, review, score, username)
    print("sql statement: {}".format(sql))
    cur.execute(sql)
    conn.commit()
    cur.close()

    # update company
    newScore = ( ((current[0][2] * current[0][3]) + score) / (current[0][3] + 1))
    cur = conn.cursor()
    update = "UPDATE COMPANY SET RATE = {}, NUM_RATE = {} WHERE NAME = '{}'".format(newScore, (current[0][3] + 1), companyName)
    print("update statement: {}".format(update))
    cur.execute(update)
    conn.commit()
    cur.close()
    conn.close()


def getReviews(companyName):
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()
    command = "SELECT * FROM REVIEW WHERE CNAME = '{}';".format(companyName)
    print(command)
    cur.execute(command)
    reviews = cur.fetchall()
    return reviews

def addCompany(companyName, about):
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()
    print(companyName, about)

    check = "SELECT EXISTS (SELECT 1 FROM COMPANY WHERE NAME = '{}');".format(companyName)
    cur.execute(check)
    result = cur.fetchone()[0]

    # return false if company exists
    if result:
        return False

    # if problems close cur and conn and reopen for next operation

    sql = "INSERT INTO COMPANY (NAME,ABOUT,RATE,NUM_RATE) VALUES (%s,%s,%s,%s);"
    cur.execute(sql, (companyName, about, 0, 0))
    conn.commit()
    cur.close()
    conn.close()
    return True

def getReviews(companyName):
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()
    command = "SELECT * FROM REVIEW WHERE CNAME = '{}';".format(companyName)
    cur.execute(command)
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return reviews

def addUser(userName, password, email, fName, lName):
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()

    check = "SELECT EXISTS (SELECT 1 FROM USERS WHERE UNAME = '{}');".format(userName)
    cur.execute(check)
    result = cur.fetchone()[0]

    # return false if user exists
    if result:
        return False

    command = "INSERT INTO USERS (UNAME, PASS, EMAIL, NUM_REVIEWS, FNAME, LNAME) VALUES ('{}','{}','{}', {},'{}','{}')".format(userName,password,email,0,fName,lName)
    print("Insert user command: {}".format(command))
    cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()
    return True

def checkPassword(email, password):
    conn = psycopg2.connect("dbname=theCellar user=postgres password=steve host=localhost")
    cur = conn.cursor()

    check = "SELECT EXISTS (SELECT 1 FROM USERS WHERE EMAIL = '{}');".format(email)
    print(check)
    cur.execute(check)
    result = cur.fetchone()[0]

    print(result)
    # return false if user exists
    if not result:
        return False

    command = "SELECT PASS FROM USERS WHERE EMAIL = '{}';".format(email)
    print(command)
    cur.execute(command)
    correctPass = cur.fetchall()
    cur.close()
    conn.close()

    print("User: {} Psql: {}".format(password, correctPass))
    if password == correctPass:
        return True
    else:
        return False
