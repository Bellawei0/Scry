import pymysql

connection = pymysql.connect(
    host = "cmpe172.cxubifgi6ctr.us-west-1.rds.amazonaws.com",
    port = 3306,
    user = 'admin',
    password = 'Cascade5995$$$',
    db = 'bank',
    charset = "utf8mb4",
    cursorclass = pymysql.cursors.DictCursor

)

try:
    cursorObject = connection.cursor()
    query = "CREATE TABLE Poop(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"
    cursorObject.execute(query)
    query = "show tables"
    rows = cursorObject.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connection.close()