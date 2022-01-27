import db_mod as dm

class Customer:

    def __init__(self, info=None):
        if info is not None:
            self.id = info[0][0]
            self.pin = info[0][1]
            self.name = info[0][2]
            self.gender = info[0][3]
            self.status = info[0][4]

class Account:

    def __init__(self, info=None):
        if info is not None:
            self.number = info[0]
            self.cust_id = info[1]
            self.type = info[2]
            self.balance = info[3]

customer = Customer()
account = Account()

def validate_id(id):
    global customer
    cus = dm.get_customer(id)

    if cus is not None:
        if cus[0][4] == 'B':
            return -1
        customer = Customer(cus)
        return 1
    else:
        return False

def validate_pin(pin):
    global customer
    if pin.isnumeric():
        return pin == customer.pin
    return False

def debit_amount(amt, at):
    global account
    res = dm.get_account(customer.id)

    if len(res) == 1:
        account = Account(res[0])
        account.balance -= float(amt)
    else:
        if res[0][2] == at:
            account = Account(res[0])
            account.balance -= float(amt)
        else:
            account = Account(res[1])
            account.balance -= float(amt)

    dm.update_balance(get_balance(), get_acc_no())

def deposit_amount(amt, at):
    global account
    res = dm.get_account(customer.id)

    if len(res) == 1:
        account = Account(res[0])
        account.balance += float(amt)
        return
    else:
        if res[0][2] == at:
            account = Account(res[0])
            account.balance += float(amt)
        else:
            account = Account(res[1])
            account.balance += float(amt)

    dm.update_balance(get_balance(), get_acc_no())

def get_gender():
    return customer.gender

def get_name():
    return customer.name

def get_acc_no():
    return account.number

def get_balance():
    return account.balance

def block_account():
    dm.update_status('B', customer.id)

def unblock_account():
    dm.update_status('U', customer.id)
