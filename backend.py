import psycopg2

def connect():
    conn = psycopg2.connect("dbname=theCellar user=postgres")

def getCompany():
    string = list()
    conn = psycopg2.connect("dbname=theCellar user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM company")
    output = cur.fetchall()
    for i in output:
        string.append(i[0])
    return string

def addCompany(companyName, about):
    conn = psycopg2.connect("dbname=theCellar user=postgres pass=steve")
    cur = conn.cursor()
    print(companyName, about)
    sql = "INSERT INTO COMPANY (NAME,ABOUT,RATE,NUM_RATE) VALUES (%s,%s,%s,%s);"
    cur.execute(sql, (companyName, about, 0, 0))
    conn.commit()
    cur.close()
    conn.close()

