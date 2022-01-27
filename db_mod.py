from MySQLdb import *

def get_customer(id):

    if id.isnumeric():
        cur.execute('SELECT * FROM CUSTOMERS WHERE ID=' + id)
        res = cur.fetchall()
        if res == ():
            res = None
    else:
        res = None

    return res

def get_account(id):
    cur.execute("SELECT * FROM ACCOUNTS WHERE CUST_ID={}".format(id))
    return cur.fetchall()

def update_balance(bal, num):
    cur.execute("UPDATE ACCOUNTS SET BALANCE={} WHERE NUMBER='{}'".format(bal, num))
    db.commit()

def update_status(st, id):
    cur.execute("UPDATE CUSTOMERS SET STATUS='{}' WHERE ID='{}'".format(st, id))
    db.commit()

db = connect(
  host="localhost",
  user="root",
  password="root"
)

cur = db.cursor()
cur.execute('USE BANK')

