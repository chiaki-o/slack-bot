import mysql.connector as mydb
 
def db_connect():
    con = mydb.connect(
        host='localhost',
        port='3306',
        user='c-oishi',
        passwd='01290922',
        database='slackbot'
    )
    con.ping(reconnect=True)
    cur = con.cursor()
    return con, cur

    def db_close(cur, con):
        cur.close()
    con.close()