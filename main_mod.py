from tkinter import *
import handler_mod as hm
from datetime import datetime

main_win = Tk()
main_win.geometry('600x500')
main_win.title('ATM')

frame = Frame(main_win)
frame.pack(padx=20, pady=20)

head_label = Label(frame, text='WELCOME', font=('arial', 20, 'bold'))
head_label.grid(row=0, column=1, pady=20)
info_label = Label(frame, text='Enter ID:', font=('arial', 15))
info_label.grid(row=1, column=1, pady=20)
input_entry = Entry(frame, font=('arial', 15))
input_entry.grid(row=2, column=1, pady=20)
msg_label = Label(frame, font=('arial', 15))
msg_label.grid(row=3, column=1, pady=20)

stage = 1
attempts = 3
choice = 0
acc_type = 0

def validate_id(id):

    global stage

    res = hm.validate_id(id)

    if res == 1:
        stage = 2
        head_label.config(text='')
        info_label.config(text='Enter PIN:', fg='black')
        input_entry.grid(row=2, column=1)
        input_entry.delete(0, 'end')
        input_entry.config(show='x')
        msg_label.config(text='')
        exit_button.grid(row=4, column=0)
    elif res == -1:
        msg_label.config(text='Account Blocked', fg='red')
    else:
        msg_label.config(text='Invalid input', fg='red')

def validate_pin(pin):

    global stage
    global attempts

    if hm.validate_pin(pin):
        stage = 3
        head_label.config(
            text='Hello '
                 + ('Mr. ' if hm.get_gender() == 'M' else 'Ms. ')
                 + hm.get_name()
        )
        info_label.config(text='Select your option:\n\n1. Debit.\n2. Deposit.', fg='black')
        input_entry.delete(0, 'end')
        input_entry.config(show='')
        msg_label.config(text='')
    else:
        input_entry.delete(0, 'end')
        if (attempts > 0):
            msg_label.config(
                text='Incorrect PIN\nRemaining attempts: '
                     + str(attempts),
                fg='red'
            )
            attempts -= 1
        else:
            stage = 1
            attempts = 3
            hm.block_account()
            head_label.config(text='')
            info_label.config(text='Account BLOCKED', fg='red')
            input_entry.grid_forget()
            cont_button.grid_forget()
            msg_label.config(text='')

def get_choice(ch):

    global stage
    stage = 4

    if ch == '1':
        head_label.config(text='')
        info_label.config(text='Select account type:\n\n1. Current.\n2. Savings.', fg='black')
        input_entry.delete(0, 'end')
        msg_label.config(text='')
        return 1
    elif ch == '2':
        head_label.config(text='')
        info_label.config(text='Select account type:\n\n1. Current.\n2. Savings.', fg='black')
        input_entry.delete(0, 'end')
        msg_label.config(text='')
        return 2
    else:
        stage = 3
        input_entry.delete(0, 'end')
        msg_label.config(text='Invalid input', fg='red')

def get_acc_type(ch):

    global stage
    stage = 5

    head_label.config(text='')
    info_label.config(text='Enter amount:', fg='black')
    input_entry.delete(0, 'end')

    if ch == '1':
        return 'C'
    else:
        return 'S'

def make_transaction(amt, ch, at):

    dt = datetime.now()

    if not amt.isnumeric() or not amt.isdecimal():
        msg_label.config(text='Invalid input', fg='red')
        input_entry.delete(0, 'end')
        return

    if ch == 1:
        hm.debit_amount(amt, at)
        info_label.config(text='Debit successful', fg='green')
        msg_label.config(
            text=('₹{} debited from account: xxxxxx{}\non {} {} {}, {}:{} {}\nCurrent balance: ₹{}'
                .format(
                    amt, hm.get_acc_no()[-4:],
                    dt.strftime('%d'), dt.strftime('%b'), dt.strftime('%Y'),
                    dt.strftime('%I'), dt.strftime('%M'), dt.strftime('%p'),
                    hm.get_balance())
                ),
            fg='black',
        )
    else:
        hm.deposit_amount(amt, at)
        info_label.config(text='Deposit successful', fg='green')
        msg_label.config(
            text=('₹{} deposited to account: xxxxxx{}\non {} {} {}, {}:{} {}\nCurrent balance: ₹{}'
                .format(
                    amt, hm.get_acc_no()[-4:],
                    dt.strftime('%d'), dt.strftime('%b'), dt.strftime('%Y'),
                    dt.strftime('%I'), dt.strftime('%M'), dt.strftime('%p'),
                    hm.get_balance())
                ),
            fg='black',
        )

    input_entry.delete(0, 'end')
    input_entry.grid_forget()
    cont_button.grid_forget()

def enter_pressed():

    global stage
    global choice
    global acc_type
    input_str = input_entry.get()

    if stage == 1:
        validate_id(input_str)

    elif stage == 2:
        validate_pin(input_str)

    elif stage == 3:
        choice = get_choice(input_str)

    elif stage == 4:
        acc_type = get_acc_type(input_str)

    elif stage == 5:
        make_transaction(input_str, choice, acc_type)

def exit_pressed():

    global stage
    stage = 1

    head_label.config(text='WELCOME')
    head_label.grid(row=0, column=1, pady=20)
    info_label.config(text='Enter ID:', fg='black')
    info_label.grid(row=1, column=1, pady=20)
    input_entry.delete(0, 'end')
    input_entry.config(show='')
    input_entry.grid(row=2, column=1, pady=20)
    msg_label.config(text='')
    cont_button.grid(row=4, column=2)

exit_button = Button(frame, text='Exit', font=('arial', 15), command=exit_pressed)
exit_button.grid(row=4, column=0)
cont_button = Button(frame, text='Continue', font=('arial', 15), command=enter_pressed)
cont_button.grid(row=4, column=2)

main_win.mainloop()
