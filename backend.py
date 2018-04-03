import psycopg2

def connect():
    conn = psycopg2.connect("dbname=theCellar user=postgres")

def getCompany():
    conn = psycopg2.connect("dbname=theCellar user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM company")
    return cur.fetchall()

def addCompany(companyName, about):
    conn = psycopg2.connect("dbname=theCellar user=postgres")
    cur = conn.cursor()
    sql = "INSERT INTO COMPANY (NAME,ABOUT,RATE,NUM_RATE) VALUES (%s,%s,%s,%s);"
    cur.execute(sql, (companyName, about, 0, 0))


