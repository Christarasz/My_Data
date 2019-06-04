from tkinter import *
import datetime
import pytz
import pickle
import mysql.connector

myDb=mysql.connector.connect(

    host="localhost",
    user="root",
    password="Database_Name",
    database="Users"
)

mycursor=myDb.cursor()

#mycursor.execute("CREATE DATABASE Users")
#mycursor.execute("use Users")
#mycursor.execute("CREATE TABLE Clients(id  INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
#"name VARCHAR(255),"
#"surname VARCHAR(255),"
#"password INTEGER(10),"
#"balance INTEGER (10))")

#mycursor.execute("CREATE TABLE WITHDRAW(id  INTEGER (10) ,password integer (10), withdraw INTEGER(10),date_dep VARCHAR(255))")
#mycursor.execute("CREATE TABLE DEPOSIT(id  INTEGER (10) ,password integer (10), Deposit INTEGER(10),date_withd VARCHAR(255))")
sqlFormula="INSERT INTO Clients (name,surname,password,balance) VALUES (%s,%s,%s,%s)"

try:
    passwords_list,names_list,surnames_list= pickle.load(open('python_data', "rb"))
except (OSError, IOError) as e:
    passwords_list=[]
    names_list=[]
    surnames_list=[]

class Account:

    @staticmethod
    def _current_time():
        utc_time = datetime.datetime.utcnow()
        return pytz.utc.localize(utc_time)

    def __init__(self, name, surname, password, balance):
        self.name = name
        self.surname = surname
        self.password = password
        self.__balance = balance
        self._transaction_list = [Account._current_time(), balance]

    def Mysql(self):
        obj_info=[self.name,self.surname,self.password,self.__balance]

        if not (self.password in passwords_list):
            passwords_list.append(self.password)
            names_list.append(self.name)
            surnames_list.append(self.surname)
            text_Info.delete('1.0',END)
            text_Info.update()
            text_Info.insert(END,"Account created for:\n " + self.name + "\n " + self.surname)

            with open('python_data', 'wb') as f:
                pickle.dump([passwords_list,names_list,surnames_list], f)

            mycursor.execute(sqlFormula,obj_info)
            myDb.commit()
        elif (self.password in passwords_list):
            pos=passwords_list.index(self.password)
            if (self.name!=names_list[pos] or self.surname!=surnames_list[pos]):
                text_Info.delete('1.0',END)
                text_Info.update()
                text_Info.insert(END,"This password \nbelongs to another\nuser")
            elif(self.name==names_list[pos] and self.surname==surnames_list[pos]):
                text_Info.delete('1.0',END)
                text_Info.update()
                text_Info.insert(END,("Welcome \n {} \n {}".format(self.name,self.surname)))

    def deposit(self, amount):
        if amount > 0:
            sqlFormula_dep="INSERT INTO deposit (id,password,Deposit,date_withd) VALUES (%s,%s,%s,%s)"
            sql="SELECT id from clients where password={}".format(self.password)
            mycursor.execute(sql)
            id=mycursor.fetchone()
            dep_info=[id[0],self.password,amount,Account._current_time()]
            mycursor.execute(sqlFormula_dep,dep_info)

            sql=("UPDATE clients SET balance=balance +{} WHERE password={}".format(amount,self.password))
            mycursor.execute(sql)
            myDb.commit()

            sql=("SELECT balance from clients WHERE password={}".format(self.password))
            mycursor.execute(sql)
            bal=mycursor.fetchone()
            bal_print=bal[0]

            text_Balance.delete('1.0',END)
            text_Balance.update()
            text_Balance.insert(END,bal_print)

    def withdraw(self, amount):
        if 0 < amount < self.__balance:
            sqlFormula_withd="INSERT INTO withdraw (id,password,withdraw,date_dep) VALUES (%s,%s,%s,%s)"
            sql="SELECT id from clients where password={}".format(self.password)
            mycursor.execute(sql)
            id=mycursor.fetchone()
            withd_info=[id[0],self.password,amount,Account._current_time()]
            mycursor.execute(sqlFormula_withd,withd_info)

            sql=("UPDATE clients SET balance=balance -{} WHERE password={}".format(amount,self.password))
            mycursor.execute(sql)

            myDb.commit()

            sql=("SELECT balance from clients WHERE password={}".format(self.password))
            mycursor.execute(sql)
            bal=mycursor.fetchone()
            bal_print=bal[0]

            text_Balance.delete('1.0',END)
            text_Balance.update()
            text_Balance.insert( END,bal_print)

        else:
            print("The amount must be greater than zero and no more than your account balance")

def create_Acount():
    name=str(entry_name.get())
    surname=str(entry_surname.get())
    password=int(entry_password.get())
    balance=0

    obj=Account(name,surname,password,balance)
    obj.Mysql()
    sql=("SELECT balance from clients where password={}".format(password))
    mycursor.execute(sql)
    bal=mycursor.fetchone()
    balance=bal[0]
    text_Balance.delete('1.0',END)
    text_Balance.update()
    text_Balance.insert( END,balance)

def deposit():
    name=str(entry_name.get())
    surname=str(entry_surname.get())
    password=int(entry_password.get())
    balance=0
    amount=int(entry_Deposit.get())
    obj=Account(name,surname,password,balance)
    obj.deposit(amount)

def withdraw():
    name=str(entry_name.get())
    surname=str(entry_surname.get())
    password=int(entry_password.get())
    sql=("SELECT balance from clients where password={}".format(password))
    mycursor.execute(sql)
    bal=mycursor.fetchone()
    balance=bal[0]
    amount=int(entry_Withdraw.get())
    obj=Account(name,surname,password,balance)
    obj.withdraw(amount)

def show_user_info():
    user_password=entry1.get()
    sql_join=("SELECT e.id,e.name,e.surname,e.password,e.balance,d.Deposit,d.date_withd,f.withdraw,f.date_dep FROM clients e INNER JOIN deposit d ON e.id=d.id INNER JOIN withdraw f ON d.id=f.id WHERE f.password={}".format(int(user_password)))
    mycursor.execute(sql_join)
    res=mycursor.fetchall()
    text_info.delete('1.0',END)
    text_info.update()
    for row in res:
       text_info.insert(END,row)

################### GUI COMMANDS ##################################
master=Tk()
master.title("Project Transactions ")
master.geometry('600x400')

title_label=Label(master,text="Bank Transactions Using Python & Mysql",fg="yellow",bg="grey",font=34,width=400)
title_label.grid(row=0,column=0,columnspan=2)
######################################################## Bank Frame
leftFrame=Frame(master)
leftFrame.grid(row=1,column=0)

BankLabel=Label(leftFrame,text="Bank Accounts Server",font=26)
BankLabel.grid(row=0,column=0,columnspan=2,sticky="WE")

label_user_bank=Label(leftFrame,text="Set user's password:",fg="white",bg="grey")
label_user_bank.grid(row=1,column=0)
entry1=Entry(leftFrame)
entry1.grid(row=1,column=1)

button_user_info=Button(leftFrame,text="Show User's Info",bg="black",fg="white",command=show_user_info)
button_user_info.grid(row=2,column=0,columnspan=2,sticky="WE")

text_info=Text(leftFrame,width=50)
text_info.grid(row=3,column=0,columnspan=2)

######################################################## Users Frame

rightFrame=Frame(master)
rightFrame.grid(row=1,column=1)

UsersLabel=Label(rightFrame,text="Users Formula",font=26)
UsersLabel.grid(row=0,column=1)

label_name=Label(rightFrame,text="Name: ")
label_name.grid(row=1,column=0,sticky=W)
entry_name=Entry(rightFrame)
entry_name.grid(row=1,column=1)

label_surname=Label(rightFrame,text="Surname: ")
label_surname.grid(row=2,column=0,sticky=W)
entry_surname=Entry(rightFrame)
entry_surname.grid(row=2,column=1)

label_password=Label(rightFrame,text="Password: ")
label_password.grid(row=3,column=0,sticky=W)
entry_password=Entry(rightFrame)
entry_password.grid(row=3,column=1)

label_set=Label(rightFrame,text="Bank account",fg="white",bg="black")
label_set.grid(row=4,column=0,sticky=W)
btn_ok=Button(rightFrame,text="OK",fg="white",bg="black",width=16,command=create_Acount)
btn_ok.grid(row=4,column=1)

label_Account=Label(rightFrame,text="Account",font=26)
label_Account.grid(row=5,column=1)

label_Balance=Label(rightFrame,text="Balance: ")
label_Balance.grid(row=6,column=1)

text_Balance=Text(rightFrame,height=1,width=5)
text_Balance.grid(row=6,column=2)

label_Withdraw=Label(rightFrame,text="Withdraw: ")
label_Withdraw.grid(row=7,column=0,sticky=W)
entry_Withdraw=Entry(rightFrame)
entry_Withdraw.grid(row=7,column=1)
btn_Withdraw=Button(rightFrame,text="Apply",fg="white",bg="black",command=withdraw)
btn_Withdraw.grid(row=7,column=2)

label_Deposit=Label(rightFrame,text="Deposit: ")
label_Deposit.grid(row=8,column=0,sticky=W)
entry_Deposit=Entry(rightFrame)
entry_Deposit.grid(row=8,column=1)
btn_Deposit=Button(rightFrame,text="Apply",fg="white",bg="black",command=deposit)
btn_Deposit.grid(row=8,column=2)

text_Info=Text(rightFrame,bg="white",fg="red",height=4,width=30)
text_Info.grid(row=9,column=0,columnspan=3,sticky=W)

master.rowconfigure(0,weight=0)
master.rowconfigure(1,weight=1)

master.columnconfigure(0,weight=3)
master.columnconfigure(1,weight=1)

master.mainloop()

