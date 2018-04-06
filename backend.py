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
    command = "SELECT * FROM REVIEW WHERE CNAME = ''{}';'".format(companyName)
    cur.execute(command)
    reviews = cur.fetchall()
    return reviews

