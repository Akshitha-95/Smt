from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
from tkcalendar import DateEntry
from itertools import chain
import sys
import os
import pathlib
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
#from googlesearch import search
#Thanks To Mark Arvin
root = Tk()
root.title("Smart Inventory System")

width = 1024
height = 520
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")

#========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()
#PRODUCT_NAME = StringVar()
#PRODUCT_PRICE = IntVar()
#PRODUCT_QTY = IntVar()
SEARCH = StringVar()

#User Data
EMP_NAME = StringVar()
EMP_ID = IntVar()
EMP_USER_NAME = StringVar()
PRIVILAGE = StringVar()
SECRET_QUESTION = StringVar()
SECRET_ANSWER = StringVar()
EMP_PASSWORD = StringVar()
EMP_CONFIRM_PASSWORD = StringVar()
CHANGE_PASSWORD_DATE = StringVar()

#Fprget Password Data
FP_EMP_NAME = StringVar()
FP_EMP_ID = IntVar()
FP_EMP_USER_NAME = StringVar()
FP_PRIVILAGE = StringVar()
FP_SECRET_QUESTION = StringVar()
FP_SECRET_ANSWER = StringVar()
FP_EMP_PASSWORD = StringVar()
FP_EMP_CONFIRM_PASSWORD = StringVar()

#Add New Stock
Part_Number = StringVar()
Part_Manufecturer = StringVar()
Part_Description = StringVar()
Total_Qty = IntVar()
Calibration_EndDate = StringVar()
Price_Per_Piece = IntVar()
Price_In_Bulk = IntVar()
Remarks = StringVar()

#Stock Inventory
PART_NO = StringVar()
PART_MANUFACTURER = StringVar()
PART_DESARIPTION = StringVar()
TOTAL_QTY = IntVar()
CALIBRATION_ENDDATE = StringVar()
PRICE_PER_PIECE = IntVar()
PRICE_IN_BULK = IntVar()
REMARKS = StringVar()    
REQUIRED_QTY = IntVar()
PURPOSE = StringVar()

#Update Inventory
Item_Number = StringVar()
Item_Manufacturer = StringVar()
Product_Description = StringVar()
Total_Quantity = IntVar()
Calib_EndDate = StringVar()
Price_Piece = IntVar()
Price_Bulk = IntVar()
Re_Marks = StringVar()    
Req_Qty = IntVar()

#Get Stock
PART_NUMBER = StringVar()
MANUFACTURER = StringVar()
REQUIRED_QUANTITY = IntVar()
#========================================METHODS==========================================

def Database():
    global conn, cursor, DATA, DATA1
    conn = sqlite3.connect("Inventory_Master.db")
    cursor = conn.cursor()
    #cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
	
    cursor.execute("CREATE TABLE IF NOT EXISTS `new_user` (change_password_date TEXT, emp_id INTEGER PRIMARY KEY NOT NULL, emp_name TEXT, user_name TEXT, privilage TEXT, secret_question TEXT, secret_answer TEXT, password TEXT)")
    #cursor.execute("CREATE TABLE IF NOT EXISTS `Login` (Emp_Name TEXT,Emp_id INTEGER PRIMARY KEY NOT NULL, Username TEXT Secondary KEY NOT NULL,Privileges TEXT,\
                   #Secret_Question TEXT,Secret_Ans TEXT, Password TEXT, Confirm_Pass TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `Master` (part_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Manufacturer_Partno INTEGER Secondary KEY NOT NULL,\
                   Part_Manufacturer TEXT, Part_Description TEXT, Total_Qty TEXT, Calibration_EndDate TEXT, price_of_per_pice TEXT, Price_of_Bulk TEXT, Remarks TEXT)")
    #cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = 'admin'")
    cursor.execute("CREATE TABLE IF NOT EXISTS `Stock` (part_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Manufacturer_Partno INTEGER SECONDARY KEY,\
                   Part_Manufacturer TEXT, Part_Description TEXT, Total_Qty TEXT, Calibration_EndDate TEXT, price_of_per_pice TEXT, Price_of_Bulk TEXT,\
                   Remarks TEXT, Required_Qty TEXT, Purpose TEXT)")
    #if cursor.fetchone() is None:
      #  cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', 'admin')")
       # conn.commit()

def Exit():
    result = tkMessageBox.askquestion('Smart Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        path=pathlib.Path("links.txt")
        if path.exists():
             os.remove("links.txt")
             os.system('TASKKILL /F /IM python.exe')
             root.destroy()
             exit()
        else:
            root.destroy()
            exit()

def Exit2():
    result = tkMessageBox.askquestion('Smart Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()

def Check(input):
        if input.isdigit():
            return True

        elif input == "":
            return True

        else:
            tkMessageBox.showinfo('Stock Inventory', "Please enter digit!")
            return False

def canceldata():
    USERNAME.set("")
    PASSWORD.set("")

def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("Smart Inventory System/Account Login")
    width = 500
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()
    
def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=10)
    lbl_text = Label(TopLoginForm, text="Smart INVENTORY SYSTEM - LOGIN", font=('Cambria', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)

    lbl_username = Label(MidLoginForm, text="Username:", font=('Cambria', 16), bd=8)
    lbl_username.grid(row=0, sticky=W)
    lbl_password = Label(MidLoginForm, text="Password:", font=('Cambria', 16), bd=8)
    lbl_password.grid(row=1, sticky=W)
    
    lbl_result = Label(MidLoginForm, text="", font=('Cambria', 16))
    lbl_result.grid(row=3, columnspan=3)
    
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('Cambria', 16), width=12)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('Cambria', 16), width=12, show="*")
    password.grid(row=1, column=1)
    
    btn_login = Button(MidLoginForm, text="Login", font=('Cambria', 14), width=10, bg="#009ACD", command=Login)
    btn_login.grid(row=2, column=0, pady=30)
    btn_login.bind('<Return>', Login)

    btn_clear = Button(MidLoginForm, text="Clear", font=('Cambria', 14), width=10, bg="#009ACD", command=canceldata)
    btn_clear.grid(row=2, column=1, pady=30)

    btn_cancel = Button(MidLoginForm, text="Cancel", font=('Cambria', 14), width=10, bg="#009ACD", command=lambda: [loginform.withdraw(), root.deiconify()])
    btn_cancel.grid(row=2, column=2, pady=30)
    loginform.protocol("WM_DELETE_WINDOW", exitloginform)
    
def exitloginform():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        loginform.withdraw()
        root.deiconify()


def nu_cleardata():
    EMP_NAME.set("")
    EMP_ID.set("")
    EMP_USER_NAME.set("")
    PRIVILAGE.set('Select privilage')
    SECRET_QUESTION.set('Select Question')
    SECRET_ANSWER.set("")
    EMP_PASSWORD.set("")
    EMP_CONFIRM_PASSWORD.set("")

def ShowAddUser():
    global adduserform
    adduserform = Toplevel()
    adduserform.title("Smart Inventory System/New User Page")
    width = 700
    height = 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    adduserform.resizable(0, 0)
    adduserform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    AddUserForm()

def AddUserForm():
    global lbl_result
    TopAddUser = Frame(adduserform, width=600, height=100, bd=1, relief=SOLID)
    TopAddUser.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddUser, text="NEW USER", font=('Cambria', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddUser = Frame(adduserform, width=600)
    MidAddUser.pack(side=TOP, pady=10)
    
    lbl_empname = Label(MidAddUser, text="Emp Name * :", font=('Cambria', 15), bd=10)
    lbl_empname.grid(row=0, sticky=W)
    lbl_empid = Label(MidAddUser, text="Emp ID * :", font=('Cambria', 15), bd=10)
    lbl_empid.grid(row=1, sticky=W)
    lbl_username = Label(MidAddUser, text="Username * :", font=('Cambria', 15), bd=10)
    lbl_username.grid(row=2, sticky=W)
    lbl_privilage = Label(MidAddUser, text="Privilage * :", font=('Cambria', 15), bd=10)
    lbl_privilage.grid(row=3, sticky=W)
    lbl_secretquestion = Label(MidAddUser, text="Secret Question * :", font=('Cambria', 15), bd=10)
    lbl_secretquestion.grid(row=4, sticky=W)
    lbl_secretanswer = Label(MidAddUser, text="Secret Answer * :", font=('Cambria', 15), bd=10)
    lbl_secretanswer.grid(row=5, sticky=W)
    lbl_password = Label(MidAddUser, text="Password * :", font=('Cambria', 15), bd=10)
    lbl_password.grid(row=6, sticky=W)
    lbl_confirmpassword = Label(MidAddUser, text="Confirm Password * :", font=('Cambria', 15), bd=10)
    lbl_confirmpassword.grid(row=7, sticky=W)

    lbl_result = Label(MidAddUser, text="", font=('Cambria', 16))
    lbl_result.grid(row=9, columnspan=3)

    empname = Entry(MidAddUser, textvariable=EMP_NAME, font=('Cambria', 15), width=15)
    empname.grid(row=0, column=1)

    empid = Entry(MidAddUser, textvariable=EMP_ID, font=('Cambria', 15), width=15)
    empid.grid(row=1, column=1)

    username = Entry(MidAddUser, textvariable=EMP_USER_NAME, font=('Cambria', 15), width=15)
    username.grid(row=2, column=1)

    choices = {'Manager', 'Employee'}
    PRIVILAGE.set('Select privilage')
    popupMenu = OptionMenu(MidAddUser, PRIVILAGE, *choices)
    popupMenu.grid(row=3, column=1)
    popupMenu.config(font=('Cambria', 10), width=20)

    choices = {'Year of joining the current company?',
               'What is your pet name?',
               'What is your higher secondary school name?',
               'What is your mother’s maiden name?',
               'What was your favorite food as child?'}
    SECRET_QUESTION.set('Select Question')
    popupMenu = OptionMenu(MidAddUser, SECRET_QUESTION, *choices)
    popupMenu.grid(row=4, column=1)
    popupMenu.config(font=('Cambria', 10), width=35)
    
    secretanswer = Entry(MidAddUser, textvariable=SECRET_ANSWER, font=('Cambria', 15), width=15)
    secretanswer.grid(row=5, column=1)
    
    password = Entry(MidAddUser, textvariable=EMP_PASSWORD, show="*", font=('Cambria', 15), width=15)
    password.grid(row=6, column=1)
    
    confirmpassword = Entry(MidAddUser, textvariable=EMP_CONFIRM_PASSWORD, show="*", font=('Cambria', 15), width=15)
    confirmpassword.grid(row=7, column=1)
    
    btn_add = Button(MidAddUser, text="Add", font=('Cambria', 14), width=10, bg="#009ACD", command=AddUser)
    btn_add.grid(row=8, column=0, pady=30)
    
    btn_clear = Button(MidAddUser, text="Clear", font=('Cambria', 14), width=10, bg="#009ACD", command=nu_cleardata)
    btn_clear.grid(row=8, column=1, pady=30)

    btn_cancel = Button(MidAddUser, text="Cancel", font=('Cambria', 14), width=10, bg="#009ACD", command=lambda: [adduserform.withdraw(), root.deiconify()])
    btn_cancel.grid(row=8, column=2, pady=30)
    adduserform.protocol("WM_DELETE_WINDOW", exitadduserform)
    
def exitadduserform():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        adduserform.withdraw()
        root.deiconify()

def AddUser():
    global DATA, strftime
    Database()
    DATA = cursor.execute("select * from new_user")
    userinfo = DATA.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    emp_name = EMP_NAME.get()
    emp_id = EMP_ID.get()
    user_name = EMP_USER_NAME.get()
    #user_name = EMP_USER_NAME.lower()
    privilege = PRIVILAGE.get()
    secret_question = SECRET_QUESTION.get()
    secret_answer = SECRET_ANSWER.get()
    password = EMP_PASSWORD.get()
    confirm_password = EMP_CONFIRM_PASSWORD.get()
    now = datetime.now()
    change_password_date = now.strftime("%Y-%m-%d %H:%M:%S")
    #print("change_password_date =", change_password_date)
    #change_password_date = date.today()
    special_sym = ['$', '@', '#', '%']
    res = user_name in chain(*userinfo)
    res1 = emp_id in chain(*userinfo)
    #yearlen = (len(str(secretanswer)))
    #Precheck Condition
    for i in range(len(userinfo)):
        if emp_name == "" or user_name == "" or emp_id == "" or privilege == 'Select privilage':
            lbl_result.config(text="* Mandatory feilds should not be empty", fg="red")
            #tkMessageBox.showinfo("New User", " * Mandatory feilds should not be empty")
            break

        elif secret_question == 'Select Question' or secret_answer == "":
            lbl_result.config(text="* Mandatory feilds should not be empty", fg="red")
            #tkMessageBox.showinfo("New User", " * Mandatory feilds should not be empty")
            break

        elif password == "" or confirm_password == "":
            lbl_result.config(text="* Mandatory feilds should not be empty", fg="red")
            #tkMessageBox.showinfo("New User", " * Mandatory feilds should not be empty")
            break

        elif res == True and user_name != "":
            lbl_result.config(text="Username already exist", fg="red")
            #tkMessageBox.showinfo('New User', "Username already exist")
            break

        elif  res1 == True  and emp_id != "":
            lbl_result.config(text="Employee Id already exist", fg="red")
            #tkMessageBox.showinfo('New User', "Employee Id already exist")
            break

        elif any(char.isdigit() for char in emp_name):
            lbl_result.config(text="Please Enter Correct Employee Name", fg="red")
            #tkMessageBox.showinfo('New User', "Please Enter Correct Employee Name")
            break

        elif any(char.isdigit() for char in user_name):
            lbl_result.config(text="Please Enter Correct Employee Username\n(Accept only Characters)", fg="red")
            #tkMessageBox.showinfo('New User',
                               # "Please Enter Correct Employee Username\n(Accept only Characters)")
            break

        elif any(char.isalpha() for char in str(emp_id)):
            lbl_result.config(text="Please Enter Correct Employee ID", fg="red")
            #tkMessageBox.showinfo('New User', "Please Enter Correct Employee ID")
            break

        elif secret_question == 'Year of joining the current company?' and any(char.isalpha() for char in secret_answer):
            lbl_result.config(text="Enter the Correct Answer \n in 'YYYY' format", fg="red")
            #tkMessageBox.showinfo('New User', "Enter the Correct Answer \n in 'YYYY' format")
            break

        elif secret_question != 'Year of joining the current company?'and any(char.isdigit() for char in secret_answer):
            lbl_result.config(text="Enter the Correct Answer in string format", fg="red")
            #tkMessageBox.showinfo('New User', "Enter the Correct Answer in string format")
            break

        elif secret_question == 'Year of joining the current company?'and len(str(secret_answer)) != 4:
            lbl_result.config(text="Enter the Correct secret Answer \n in 'YYYY' format", fg="red")
            #tkMessageBox.showinfo('New User',
                             #   "Enter the Correct secret Answer \n in 'YYYY' format")
            break

        elif len(str(emp_id)) >= 8:
            lbl_result.config(text="EmpID is restricted \n to 8 charcters", fg="red")
            #tkMessageBox.showinfo('New User', "EmpID is restricted \n to 8 charcters")
            break

        elif len(password) < 8:
            lbl_result.config(text="Password length should be \n at least 8", fg="red")
            #tkMessageBox.showinfo("New User", "Password length should be \n at least 8")
            break

        elif len(password) > 20:
            lbl_result.config(text="Password length should not \n be greater than 20", fg="red")
            #tkMessageBox.showinfo("New User", "Password length should not \n be greater than 20")
            break

        elif not any(char.isdigit() for char in password):
            lbl_result.config(text="Password should have at \n least one numeral", fg="red")
            #tkMessageBox.showinfo("New User", "Password should have at \n least one numeral")
            break

        elif not any(char.isupper() for char in password):
            lbl_result.config(text="Password should have at least \n one uppercase letter", fg="red")
            #tkMessageBox.showinfo("New User", "Password should have at least \n one uppercase letter")
            break

        elif not any(char.islower() for char in password):
            lbl_result.config(text="Password should have at least \n one lowercase letter", fg="red")
            #tkMessageBox.showinfo("New User", "Password should have at least \n one lowercase letter")
            break

        elif not any(char in special_sym for char in password):
            lbl_result.config(text="Password should have at \n least one of the symbols \n $ @ # %", fg="red")
            #tkMessageBox.showinfo("New User",
                              #  "Password should have at \n least one of the symbols \n $ @ # %")
            break

        elif  password != confirm_password:
            lbl_result.config(text="Password and Confirm Password \n did not match", fg="red")
            #tkMessageBox.showinfo("New User", "Password and Confirm Password \n did not match")
            break

        elif i == (len(userinfo)-1):

            Database()
            cursor.execute("INSERT INTO `new_user` (emp_name, emp_id, user_name, privilage, secret_question, secret_answer, password) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   (str(EMP_NAME.get()), int(EMP_ID.get()), str(EMP_USER_NAME.get()), str(PRIVILAGE.get()), str(SECRET_QUESTION.get()), str(SECRET_ANSWER.get()), str(EMP_PASSWORD.get())))
            cursor.execute("Update new_user Set change_password_date=? Where emp_id=?",(change_password_date, emp_id))
            conn.commit()
            EMP_NAME.set("")
            EMP_ID.set("")
            EMP_USER_NAME.set("")
            PRIVILAGE.set("")
            SECRET_QUESTION.set("")
            SECRET_ANSWER.set("")
            EMP_PASSWORD.set("")
            CHANGE_PASSWORD_DATE.set("")
            cursor.close()
            conn.close()
            lbl_result.config(text="Added Successfully \n Add new user or Press Cancel to exit", fg="red")
            #tkMessageBox.showinfo("New User", "Added Successfully \n Add new user or Press Cancel to exit")
            nu_cleardata()

def fp_cleardata():
    FP_EMP_ID.set("")
    FP_EMP_USER_NAME.set("")
    FP_SECRET_QUESTION.set('Select Question')
    FP_SECRET_ANSWER.set("")
    FP_EMP_PASSWORD.set("")
    FP_EMP_CONFIRM_PASSWORD.set("")

def ShowForgetPassword():
    global forgetpasswordform
    forgetpasswordform = Toplevel()
    forgetpasswordform.title("Smart Inventory System/Forget Password Page")
    width = 700
    height = 450
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    forgetpasswordform.resizable(0, 0)
    forgetpasswordform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    ForgetPasswordForm()

def ForgetPasswordForm():
    global lbl_result
    TopForgetPassword = Frame(forgetpasswordform, width=600, height=100, bd=1, relief=SOLID)
    TopForgetPassword.pack(side=TOP, pady=10)
    lbl_text = Label(TopForgetPassword, text="FORGET PASSWORD", font=('Cambria', 15), width=600)
    lbl_text.pack(fill=X)
    MidForgetPassword = Frame(forgetpasswordform, width=600)
    MidForgetPassword.pack(side=TOP, pady=10)
    
    lbl_empid = Label(MidForgetPassword, text="Emp ID * :", font=('Cambria', 15), bd=10)
    lbl_empid.grid(row=0, sticky=W)
    lbl_username = Label(MidForgetPassword, text="Username * :", font=('Cambria', 15), bd=10)
    lbl_username.grid(row=1, sticky=W)
    lbl_secretquestion = Label(MidForgetPassword, text="Secret Question * :", font=('Cambria', 15), bd=10)
    lbl_secretquestion.grid(row=2, sticky=W)
    lbl_secretanswer = Label(MidForgetPassword, text="Secret Answer * :", font=('Cambria', 15), bd=10)
    lbl_secretanswer.grid(row=3, sticky=W)
    lbl_password = Label(MidForgetPassword, text="Password * :", font=('Cambria', 15), bd=10)
    lbl_password.grid(row=4, sticky=W)
    lbl_confirmpassword = Label(MidForgetPassword, text="Confirm Password * :", font=('Cambria', 15), bd=10)
    lbl_confirmpassword.grid(row=5, sticky=W)

    lbl_result = Label(MidForgetPassword, text="", font=('Cambria', 16))
    lbl_result.grid(row=7, columnspan=3)

    empid = Entry(MidForgetPassword, textvariable=FP_EMP_ID, font=('Cambria', 15), width=15)
    empid.grid(row=0, column=1)

    username = Entry(MidForgetPassword, textvariable=FP_EMP_USER_NAME, font=('Cambria', 15), width=15)
    username.grid(row=1, column=1)

  #privilage = Entry(MidAddUser, textvariable=PRIVILAGE, font=('arial', 15), width=15)
    #privilage.grid(row=3, column=1)

    choices = {'Year of joining the current company?',
               'What is your pet name?',
               'What is your higher secondary school name?',
               'What is your mother’s maiden name?',
               'What was your favorite food as child?'}
    FP_SECRET_QUESTION.set('Select Question')
    popupMenu = OptionMenu(MidForgetPassword, FP_SECRET_QUESTION, *choices)
    popupMenu.grid(row=2, column=1)
    popupMenu.config(font=('Cambria', 10), width=35)

    #secretquestion = Entry(MidAddUser, textvariable=SECRET_QUESTION, font=('arial', 15), width=15)
    #secretquestion.grid(row=4, column=1)
    
    secretanswer = Entry(MidForgetPassword, textvariable=FP_SECRET_ANSWER, font=('Cambria', 15), width=15)
    secretanswer.grid(row=3, column=1)
    
    password = Entry(MidForgetPassword, textvariable=FP_EMP_PASSWORD, show="*", font=('Cambria', 15), width=15)
    password.grid(row=4, column=1)
    
    confirmpassword = Entry(MidForgetPassword, textvariable=FP_EMP_CONFIRM_PASSWORD, show="*", font=('Cambria', 15), width=15)
    confirmpassword.grid(row=5, column=1)
    
    btn_update = Button(MidForgetPassword, text="UPDATE", font=('Cambria', 14), width=10, bg="#009ACD", command=ForgetPassword)
    btn_update.grid(row=6, column=0, pady=30)
    
    btn_clear = Button(MidForgetPassword, text="Clear", font=('Cambria', 14), width=10, bg="#009ACD", command=fp_cleardata)
    btn_clear.grid(row=6, column=1, pady=30)

    btn_close = Button(MidForgetPassword, text="Close", font=('Cambria', 14), width=10, bg="#009ACD", command=lambda: [forgetpasswordform.withdraw(), root.deiconify()])
    btn_close.grid(row=6, column=2, pady=30)

    forgetpasswordform.protocol("WM_DELETE_WINDOW", exitforgetpasswordform)
    
def exitforgetpasswordform():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        forgetpasswordform.withdraw()
        root.deiconify()

def ForgetPassword():
    Database()
    DATA1 = cursor.execute("select * from new_user")
    userinfofp = DATA1.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    #emp_name = EMP_NAME.get()
    emp_id = FP_EMP_ID.get()
    user_name = FP_EMP_USER_NAME.get()
    #user_name = EMP_USER_NAME.lower()
    #privilege = PRIVILAGE.get()
    secret_question = FP_SECRET_QUESTION.get()
    secret_answer = FP_SECRET_ANSWER.get()
    password = FP_EMP_PASSWORD.get()
    confirm_password = FP_EMP_CONFIRM_PASSWORD.get()
    now = datetime.now()
    change_password_date = now.strftime("%Y-%m-%d %H:%M:%S")
    special_sym = ['$', '@', '#', '%']
    res = user_name in chain(*userinfofp)
    #print("user_name =", res)
    res1 = emp_id in chain(*userinfofp)
    #print("emp_id =", res1)
    res2 = secret_question in chain(*userinfofp)
    res3 = secret_answer in chain(*userinfofp)
    #yearlen = (len(str(secretanswer)))
    #Precheck Condition
    for i in range(len(userinfofp)):
        if user_name == "" or emp_id == "":
            lbl_result.config(text="* Mandatory feilds should not be empty", fg="red")
            #tkMessageBox.showinfo("Forget Password", " * Mandatory feilds should not be empty 1")
            break

        elif secret_question == 'Select Question' or secret_answer == "":
            lbl_result.config(text="* Mandatory feilds should not be empty", fg="red")
            #tkMessageBox.showinfo("Forget Password", " * Mandatory feilds should not be empty 2")
            break

        elif password == "" or confirm_password == "":
            lbl_result.config(text="* Mandatory feilds should not be empty", fg="red")
            #tkMessageBox.showinfo("Forget Password", " * Mandatory feilds should not be empty 3")
            break

        elif  res != True and user_name != "":
            lbl_result.config(text="Invalid Username", fg="red")
            #tkMessageBox.showinfo('Forget Password', "Invalid Username")
            break

        elif res1 != True and emp_id != "":
            lbl_result.config(text="Invalid Employee Id", fg="red")
            #tkMessageBox.showinfo('Forget Password', "Invalid Employee Id")
            break

        elif res2 != True and secret_question != "":
            lbl_result.config(text="Invalid Secret Question", fg="red")
            #tkMessageBox.showinfo('Forget Password', "Invalid Secret Question")
            break

        elif res3 != True and secret_answer != "":
            lbl_result.config(text="Invalid Secret Answer", fg="red")
            #tkMessageBox.showinfo('Forget Password', "Invalid Secret Answer")
            break

        elif len(str(emp_id)) >= 8:
            lbl_result.config(text="EmpID is restricted \n to 8 charcters", fg="red")
            #tkMessageBox.showinfo('Forget Password', "EmpID is restricted \n to 8 charcters")
            break

        elif len(password) < 8:
            lbl_result.config(text="Password length should be \n at least 8", fg="red")
            #tkMessageBox.showinfo("Forget Password", "Password length should be \n at least 8")
            break

        elif len(password) > 20:
            lbl_result.config(text="Password length should not \n be greater than 20", fg="red")
            #tkMessageBox.showinfo("Forget Password", "Password length should not \n be greater than 20")
            break

        elif not any(char.isdigit() for char in password):
            lbl_result.config(text="Password should have at \n least one numeral", fg="red")
            #tkMessageBox.showinfo("Forget Password", "Password should have at \n least one numeral")
            break

        elif not any(char.isupper() for char in password):
            lbl_result.config(text="Password should have at least \n one uppercase letter", fg="red")
            #tkMessageBox.showinfo("Forget_Password", "Password should have at least \n one uppercase letter")
            break

        elif not any(char.islower() for char in password):
            lbl_result.config(text="Password should have at least \n one lowercase letter", fg="red")
            #tkMessageBox.showinfo("Forget Password", "Password should have at least \n one lowercase letter")
            break

        elif not any(char in special_sym for char in password):
            lbl_result.config(text="Password should have at \n least one of the symbols \n $ @ # %", fg="red")
            #tkMessageBox.showinfo("Forget Password",
                          #      "Password should have at \n least one of the symbols \n $ @ # %")
            break

        elif  password != confirm_password:
            lbl_result.config(text="Password and Confirm Password \n did not match", fg="red")
            #tkMessageBox.showinfo("Forget Password", "Password and Confirm Password \n did not match")
            break

        elif str(emp_id) in str(userinfofp[i][1]) and user_name not in userinfofp[i][3]:
            print(emp_id,userinfofp[i][1])
            lbl_result.config(text="Invalid User Name", fg="red")
            #tkMessageBox.showinfo('Forget Password', 'Invalid User Name')
            break

        elif str(emp_id) in str(userinfofp[i][1]) and secret_question not in userinfofp[i][5]:
            lbl_result.config(text="Invalid Secret Question", fg="red")
            #tkMessageBox.showinfo('Forget Password', 'Invalid Secret Question')
            break

        elif str(emp_id) in str(userinfofp[i][1]) and secret_answer not in userinfofp[i][6]:
            lbl_result.config(text="Invalid Secret Answer", fg="red")
            #tkMessageBox.showinfo('Forget Password', 'Invalid Secret Answer')
            break

        elif str(emp_id) in str(userinfofp[i][1]) and password in userinfofp[i][7]:
            lbl_result.config(text="New Password Cannot Be The Same As \n The Last Three Passwords", fg="red")
            #tkMessageBox.showinfo('Forget Password',
                            #   'New Password Cannot Be The Same As \n The Last Three Passwords')

        elif i == (len(userinfofp)-1):

            Database()
            cursor.execute("Update new_user Set password=?, change_password_date=? Where emp_id=?",(password, change_password_date, emp_id))
            conn.commit()
            cursor.close()
            conn.close()
            lbl_result.config(text="Password Updated Successfully \n Press Cancel to exit", fg="red")
            #tkMessageBox.showinfo("Forget Password", "Password Updated Successfully")
            fp_cleardata()

def Home():
          
    global Home
    Home = Tk()
    Home.title("Smart Inventory System/Home")
    width = 1024
    height = 520
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)
    Title = Frame(Home, bd=1, relief=SOLID)
    Title.pack(pady=10)
    lbl_display = Label(Title, text="Smart Inventory System", font=('Cambria', 45))
    lbl_display.pack()
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="Stock Inventory", command=ShowStock)
    filemenu2.add_command(label="Update Inventory Stock", command=UpdateStock)
    filemenu2.add_command(label="View", command=ShowView)
    menubar.add_cascade(label="Account", menu=filemenu)
    menubar.add_cascade(label="Inventory", menu=filemenu2)
    Home.config(menu=menubar)
    Home.config(bg="#6666ff")

        
def ShowStock():
    Clear()
    global getstockform
    getstockform = Toplevel()
    getstockform.title("Smart Inventory System/Stock Inventory")
    width = 700
    height = 680
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    getstockform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    getstockform.resizable(0, 0)
    GetStockForm()

def GetStockForm():
    TopGetStock = Frame(getstockform, width=600, height=100, bd=1, relief=SOLID)
    TopGetStock.pack(side=TOP, pady=10)
    lbl_text = Label(TopGetStock, text="Stock Inventory", font=('Cambria', 18), width=600)
    lbl_text.pack(fill=X)
    MidStock = Frame(getstockform, width=700)
    MidStock.pack(side=TOP, pady=10)

    lbl_number = Label(MidStock, text="Item Part Number:", font=('Cambria', 18), bd=10)
    lbl_number.grid(row=0, sticky=W)
    lbl_productdesc = Label(MidStock, text="Item Description:", font=('Cambria', 18), bd=10)
    lbl_productdesc.grid(row=1, sticky=W)
    lbl_manufacturer = Label(MidStock, text="Part Manufacturer:", font=('Cambria', 18), bd=10)
    lbl_manufacturer.grid(row=2, sticky=W)
    lbl_tqty = Label(MidStock, text="Total Quantity Available:", font=('Cambria', 18), bd=10)
    lbl_tqty.grid(row=3, sticky=W)
    lbl_calibration = Label(MidStock, text="Calibration EndDate:", font=('Cambria', 18), bd=10)
    lbl_calibration.grid(row=4, sticky=W)
    lbl_price = Label(MidStock, text="Price Per Piece:", font=('Cambria', 18), bd=10)
    lbl_price.grid(row=5, sticky=W)
    lbl_bulk = Label(MidStock, text="Price In Bulk:", font=('Cambria', 18), bd=10)
    lbl_bulk.grid(row=6, sticky=W)
    lbl_rqty = Label(MidStock, text="Required Quantity:", font=('Cambria', 18), bd=10)
    lbl_rqty.grid(row=7, sticky=W)
    lbl_purpose = Label(MidStock, text="Purpose:", font=('Cambria', 18), bd=10)
    lbl_purpose.grid(row=8, sticky=W)

    Database()
    cursor.execute("SELECT  Manufacturer_Partno FROM `Master`")
    itemno = cursor.fetchall()
    cursor.close()
    conn.close()

    choices = {*itemno}
    PART_NO.set('Select Item Number')
    popupMenu = OptionMenu(MidStock, PART_NO, *choices, command=StockDisplay)
    popupMenu.grid(row=0, column=1)
    popupMenu.config(font=('Cambria', 16), width=19)

    itemdesc = Entry(MidStock, textvariable=PART_DESARIPTION, font=('Cambria', 18), width=20)
    itemdesc.grid(row=1, column=1)
    itemdesc.config(state='disabled')

    manufacturer = Entry(MidStock, textvariable=PART_MANUFACTURER, font=('Cambria', 18), width=20)
    manufacturer.grid(row=2, column=1)
    manufacturer.config(state='disabled')

    reg = MidStock.register(Check)
    totalqty = Entry(MidStock, validate="key", validatecommand=(reg, '%P'), textvariable=TOTAL_QTY, font=('Cambria', 18), width=20)
    totalqty.grid(row=3, column=1)
    totalqty.config(state='disabled')

    enddate = Entry(MidStock, textvariable=CALIBRATION_ENDDATE, font=('Cambria', 18), width=20)
    enddate.grid(row=4, column=1)
    enddate.config(state='disabled')

    priceperpiece = Entry(MidStock, validate="key", validatecommand=(reg, '%P'), textvariable=PRICE_PER_PIECE, font=('Cambria', 18), width=20)
    priceperpiece.grid(row=5, column=1)
    priceperpiece.config(state='disabled')

    priceinbulk = Entry(MidStock, validate="key", validatecommand=(reg, '%P'), textvariable=PRICE_IN_BULK, font=('Cambria', 18), width=20)
    priceinbulk.grid(row=6, column=1)
    priceinbulk.config(state='disabled')
    
    requiredqty = Entry(MidStock, validate="key", validatecommand=(reg, '%P'), textvariable=REQUIRED_QTY, font=('Cambria', 18), width=20)
    requiredqty.grid(row=7, column=1)
    
    choices = {'Project' , 'Production' , 'Replacement'}
    PURPOSE.set('Select Purpose')
    popupMenu = OptionMenu(MidStock, PURPOSE, *choices)
    popupMenu.grid(row=8, column=1)
    popupMenu.config(font=('Cambria', 18), width=17)
    
    btn_stock = Button(MidStock, text="Get Stock", font=('Cambria', 16), width=10, bg="#009ACD", command=GetStock)
    btn_stock.grid(row=9, column=0, pady=30)
    btn_stock.bind('<Return>', GetStock)
    btn_clear = Button(MidStock, text="Clear", font=('Cambria', 16), width=10, bg="#009ACD", command=Clear)
    btn_clear.grid(row=9, column=1, pady=30)
    btn_close = Button(MidStock, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=lambda: [getstockform.withdraw(), Home.deiconify()])
    btn_close.grid(row=9, column=2, pady=30)

    #getstockform.overrideredirect(True)
    getstockform.protocol("WM_DELETE_WINDOW", exitgetstockform)
    
def exitgetstockform():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        getstockform.withdraw()
        Home.deiconify()

def GetStock(event=None):
    itemno = PART_NO.get()
    if itemno != 'Select Item Number':
        itemno = eval(itemno)
        itemno = (itemno[0])
    partdescrip = PART_DESARIPTION.get()
    partmanufacturer = PART_MANUFACTURER.get()
    tlqty = TOTAL_QTY.get()
    date = CALIBRATION_ENDDATE.get()
    pricepiece = PRICE_PER_PIECE.get()
    bulk = PRICE_IN_BULK.get()
    reqdqty = REQUIRED_QTY.get()
    purpose = PURPOSE.get()

    if itemno == 'Select Item Number' or reqdqty == 0 or purpose == 'Select Purpose':
        tkMessageBox.showinfo('Stock Inventory', "Please fill all the fields!")

    #elif reqdqty != 0 and not any(char.isdigit() for char in reqdqty):
        #tkMessageBox.showinfo('Stock Inventory', "Enter correct required quantity")

    elif reqdqty > tlqty:
        result = tkMessageBox.askquestion('Stock Inventory',"Inventory stock for selected part number is low Would you like to order")
        if result == 'yes':
            getstockform.withdraw()
            ShowOrder()

    elif tlqty >= reqdqty:
        Database()
        cursor.execute("SELECT  Remarks FROM `Master` where Manufacturer_Partno=?", (itemno,))
        remarks = cursor.fetchall()
        remarks = (remarks[0])
        remarks = (remarks[0])
        print(remarks)
        cursor.execute("INSERT INTO `Stock` (Manufacturer_Partno, Part_Manufacturer, Part_Description, Total_Qty, Calibration_EndDate, price_of_per_pice,\
                       Price_of_Bulk, Required_Qty, Remarks, Purpose) VALUES(?,?,?,?,?,?,?,?,?,?)",
                       (itemno, partmanufacturer, partdescrip, tlqty, date, pricepiece, bulk, reqdqty, remarks, purpose))
        conn.commit()
        cursor.close()
        conn.close()
        tkMessageBox.showinfo('Stock Inventory', "Stock updated successfully")
        Clear()
        #getstockform.withdraw()
        #Home.deiconify()

def StockDisplay(event):
    partnumber = PART_NO.get()
    partnumber = eval(partnumber)
    partnumber = (partnumber[0])

    Database()
    cursor.execute("SELECT Part_Description, Part_Manufacturer, Total_Qty, Calibration_EndDate, price_of_per_pice, Price_of_Bulk FROM `Master` where Manufacturer_Partno=?",
                   (partnumber,))
    fetch = cursor.fetchall()
    partdescription = fetch[0][0]
    manufact = fetch[0][1]
    qty = fetch[0][2]
    calb = fetch[0][3]
    price = fetch[0][4]
    bulk = fetch[0][5]
    cursor.close()
    conn.close()

    PART_DESARIPTION.set(partdescription)
    PART_MANUFACTURER.set(manufact)
    TOTAL_QTY.set(qty)
    CALIBRATION_ENDDATE.set(calb)
    PRICE_PER_PIECE.set(price)
    PRICE_IN_BULK.set(bulk)

def Clear():
    PART_NO.set("Select Item Number")
    PART_DESARIPTION.set("")
    PART_MANUFACTURER.set("")
    TOTAL_QTY.set(0)
    CALIBRATION_ENDDATE.set("")
    PRICE_PER_PIECE.set(0)
    PRICE_IN_BULK.set(0)
    REQUIRED_QTY.set(0)
    PURPOSE.set("Select Purpose")

def ShowOrder():
    global orderform
    orderform = Toplevel()
    orderform.title("Smart Inventory System/Stock Inventory")
    width = 700
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    orderform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    orderform.resizable(0, 0)
    OrderForm()
    
def OrderForm():
    TopOrder = Frame(orderform, width=600, height=100, bd=1, relief=SOLID)
    TopOrder.pack(side=TOP, pady=10)
    lbl_text = Label(TopOrder, text="Stock Inventory", font=('Cambria', 18), width=600)
    lbl_text.pack(fill=X)
    MidOrder = Frame(orderform, width=700)
    MidOrder.pack(side=TOP, pady=50)
    
    lbl_partno = Label(MidOrder, text="Item Part Number:", font=('Cambria', 18), bd=10)
    lbl_partno.grid(row=1, sticky=W)
    lbl_manufact = Label(MidOrder, text="Manufacturer:", font=('Cambria', 18), bd=10)
    lbl_manufact.grid(row=2, sticky=W)
    lbl_quantity = Label(MidOrder, text="Required Quantity:", font=('Cambria', 18), bd=10)
    lbl_quantity.grid(row=3, sticky=W)

    itempartno = PART_NO.get()
    itempartno = eval(itempartno)
    itempartno = (itempartno[0])
    PART_NUMBER.set(itempartno)
    partnumber = Entry(MidOrder, textvariable=PART_NUMBER, font=('Cambria', 18), width=19)
    partnumber.grid(row=1, column=1)
    partnumber.config(state='disabled')

    choices = {'Digi key', 'Mouser Electronic', 'Elements 14', 'Arrow Electronic', 'Verical', 'Quest Electronic', 'Avnet'}
    MANUFACTURER.set('Select Manufacturer')
    popupMenu = OptionMenu(MidOrder, MANUFACTURER, *choices)
    popupMenu.grid(row=2, column=1)
    popupMenu.config(font=('Cambria', 16), width=18)

    reg = MidOrder.register(Check)
    requiredqty = Entry(MidOrder, validate="key", validatecommand=(reg, '%P'), textvariable=REQUIRED_QUANTITY, font=('Cambria', 18), width=19)
    requiredqty.grid(row=3, column=1)
   
    btn_search = Button(MidOrder, text="Search", font=('Cambria', 16), width=10, bg="#009ACD", command=StockSearch)
    btn_search.grid(row=4,column=0, pady=30)
    btn_search.bind('<Return>', Search)
    btn_clear = Button(MidOrder, text="Clear", font=('Cambria', 16), width=10, bg="#009ACD", command=Cancel)
    btn_clear.grid(row=4, column=1, pady=30)
    btn_close = Button(MidOrder, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=lambda: [orderform.withdraw(), Home.deiconify()])
    btn_close.grid(row=4, column=2, pady=30)

    orderform.protocol("WM_DELETE_WINDOW", exitorderform)
    
def exitorderform():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        orderform.withdraw()
        Home.deiconify()

def Cancel():
    REQUIRED_QUANTITY.set(0)
    MANUFACTURER.set('Select Manufacturer')

def StockSearch(event=None):
    global itemno, manufact, reqty, listlinks
    itemno = PART_NUMBER.get()
    manufact = MANUFACTURER.get()
    reqty = REQUIRED_QUANTITY.get()

    if itemno == "" or manufact == "Select Manufacturer" or reqty == 0:
        tkMessageBox.showinfo("Smart Inventory System", "All fields are mandatory")

    #elif reqty != 0 and not any(char.isdigit() for char in reqty):
        #tkMessageBox.showinfo('Stock Inventory', "Enter correct required quantity")

    else:
        try:
            from googlesearch import search 
        except ImportError:
            print("No module named 'google' found")
        listlinks = []
        query = itemno
        for j in search(query, tld="co.in", num=10, stop=10, pause=2):
            #Create and write to txt file
            #print(j)
            listlinks.append(j)
        with open("links.txt",'w',encoding = 'utf-8') as f:
            for i in listlinks:
                f.write(i + "\n")
        if  listlinks == []:
            tkMessageBox.showinfo("Link", " Manufecturer link not found - please make sure partno. is correct")
            return
        else:    
            result = tkMessageBox.askquestion('Email Notification', 'Would you like to Send Email to Procurment team?', icon="warning")
            if result == 'yes': 
                SearchForm()
            else:
                return
	
def SearchForm():
    # Function to read the contacts from a given contact file and return a
    # list of names and email addresses
    global itemno, manufact, reqty, listlinks
    subject = "Procurment Notification..."
    body = "Hi All,\n Please find the attached link of different manufecture to procure below Item: \n Part NO. -  ", itemno, "\n Required Quntity - ", reqty, "\n \n Note: Please do not reply to this message"
    body=body[0] + body[1] + body[2] + str(body[3]) + body[4]
    body=str(body)
    sender_email = "bababus0614@gmail.com"
    receiver_email = "ankit.shukla@altran.com"
    password = "Mylife@02"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "links.txt"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()

    print("Starting to send")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    print ("Sent email") 
    tkMessageBox.showinfo('Email notification', "Email Sent to Procurment team")


def UpdateStock():
    UpdateClear()
    global updateform
    updateform = Toplevel()
    updateform.title("Smart Inventory System/Update Inventory stock")
    width = 700
    height = 650
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    updateform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateform.resizable(0, 0)
    UpdateStockForm()

def UpdateStockForm():
    TopUpdate = Frame(updateform, width=600, height=100, bd=1, relief=SOLID)
    TopUpdate.pack(side=TOP, pady=10)
    lbl_text = Label(TopUpdate, text="Update Inventory Stock", font=('Cambria', 18), width=600)
    lbl_text.pack(fill=X)
    MidUpdate = Frame(updateform, width=600)
    MidUpdate.pack(side=TOP, pady=10)

    lbl_number = Label(MidUpdate, text="Item Part Number:", font=('Cambria', 18), bd=10)
    lbl_number.grid(row=0, sticky=W)
    lbl_productname = Label(MidUpdate, text="Item Name:", font=('Cambria', 18), bd=10)
    lbl_productname.grid(row=1, sticky=W)
    lbl_manufacturer = Label(MidUpdate, text="Part Manufacturer:", font=('Cambria', 18), bd=10)
    lbl_manufacturer.grid(row=2, sticky=W)
    lbl_tqty = Label(MidUpdate, text="Total Quantity Available:", font=('Cambria', 18), bd=10)
    lbl_tqty.grid(row=3, sticky=W)
    lbl_calibration = Label(MidUpdate, text="Calibration EndDate:", font=('Cambria', 18), bd=10)
    lbl_calibration.grid(row=4, sticky=W)
    lbl_price = Label(MidUpdate, text="Price Per Piece:", font=('Cambria', 18), bd=10)
    lbl_price.grid(row=5, sticky=W)
    lbl_bulk = Label(MidUpdate, text="Price In Bulk:", font=('Cambria', 18), bd=10)
    lbl_bulk.grid(row=6, sticky=W)
    lbl_remarks = Label(MidUpdate, text="Remarks:", font=('Cambria', 18), bd=10)
    lbl_remarks.grid(row=7, sticky=W)

    Database()
    cursor.execute("SELECT Manufacturer_Partno FROM `Master`")
    itemnumber = cursor.fetchall()
    cursor.close()
    conn.close()

    choices = {*itemnumber}
    Item_Number.set('Select Part Number')
    popupMenu = OptionMenu(MidUpdate, Item_Number, *choices, command=UpdateDisplay)
    popupMenu.grid(row=0, column=1)
    popupMenu.config(font=('Cambria', 16), width=16)

    itemname = Entry(MidUpdate, textvariable=Product_Description, font=('Cambria', 18), width=18)
    itemname.grid(row=1, column=1)

    manufacturer = Entry(MidUpdate, textvariable=Item_Manufacturer, font=('Cambria', 18), width=18)
    manufacturer.grid(row=2, column=1)

    reg = MidUpdate.register(Check)
    totalqty = Entry(MidUpdate, validate="key", validatecommand=(reg, '%P'), textvariable=Total_Quantity, font=('Cambria', 18), width=18)
    totalqty.grid(row=3, column=1)

    enddate = DateEntry(MidUpdate, locale='en_US', date_pattern='MM/dd/yyyy', textvariable=Calib_EndDate)
    enddate.grid(row=4, column=1)
    enddate.config(width=35)

    priceperpiece = Entry(MidUpdate, validate="key", validatecommand=(reg, '%P'), textvariable=Price_Piece, font=('Cambria', 18), width=18)
    priceperpiece.grid(row=5, column=1)

    priceinbulk = Entry(MidUpdate, validate="key", validatecommand=(reg, '%P'), textvariable=Price_Bulk, font=('Cambria', 18), width=18)
    priceinbulk.grid(row=6, column=1)
    
    remarks = Entry(MidUpdate, textvariable=Re_Marks, font=('Cambria', 18), width=18)
    remarks.grid(row=7, column=1)
    
    btn_update = Button(MidUpdate, text="Update", font=('Cambria', 16), width=10, bg="#009ACD", command=Update)
    btn_update.grid(row=9,column=0, pady=30)
    btn_update.bind('<Return>', GetStock)
    btn_clear = Button(MidUpdate, text="Clear", font=('Cambria', 16), width=10, bg="#009ACD", command=UpdateClear)
    btn_clear.grid(row=9, column=1, pady=30)
    btn_close = Button(MidUpdate, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=lambda: [updateform.withdraw(), Home.deiconify()])
    btn_close.grid(row=9, column=2, pady=30)
    #updateform.protocol("WM_DELETE_WINDOW", updateform.withdraw())

    updateform.protocol("WM_DELETE_WINDOW", exitupdateform)
    
def exitupdateform():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        updateform.withdraw()
        Home.deiconify()

def UpdateDisplay(event):
    partnumber = Item_Number.get()
    if partnumber != 'Select Part Number':
        partnumber = eval(partnumber)
        partnumber = (partnumber[0])

    Database()
    cursor.execute("SELECT Part_Description, Part_Manufacturer, Total_Qty, Calibration_EndDate, price_of_per_pice, Price_of_Bulk, Remarks FROM `Master` where Manufacturer_Partno=?",
                   (partnumber,))
    fetch = cursor.fetchall()
    partname = fetch[0][0]
    manufact = fetch[0][1]
    qty = fetch[0][2]
    calb = fetch[0][3]
    price = fetch[0][4]
    bulk = fetch[0][5]
    remarks = fetch[0][6]
    cursor.close()
    conn.close()

    Product_Description.set(partname)
    Item_Manufacturer.set(manufact)
    Total_Quantity.set(qty)
    Calib_EndDate.set(calb)
    Price_Piece.set(price)
    Price_Bulk.set(bulk)
    Re_Marks.set(remarks)

def UpdateClear():
    Item_Number.set('Select Part Number')
    Product_Description.set("")
    Item_Manufacturer.set("")
    Total_Quantity.set(0)
    Price_Piece.set(0)
    Price_Bulk.set(0)
    Re_Marks.set("")

def Update():
    partno = Item_Number.get()
    if partno != 'Select Part Number':
        partno = eval(partno)
        partno = (partno[0])

    manufacturer = Item_Manufacturer.get()
    description = Product_Description.get()
    quantity = Total_Quantity.get()
    enddate = Calib_EndDate.get()
    price = Price_Piece.get()
    bulk = Price_Bulk.get()
    remarks = Re_Marks.get()
    
    Database()
    cursor.execute("select * from Master")
    stockdetails = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    for i in range(len(stockdetails)):
        if partno == 'Select Part Number' or manufacturer == "" or description == "" or quantity == 0 or price == 0 or bulk == 0 or remarks == "":
            tkMessageBox.showinfo("Update Inventory Stock", "Please Fill All Fields")

        #elif quantity != 0 and not any(char.isdigit() for char in quantity):
            #tkMessageBox.showinfo('Smart Inventory System/Update Inventory', "Enter correct Total quantity")

        #elif price != 0 and not any(char.isdigit() for char in price):
            #tkMessageBox.showinfo('Smart Inventory System/Update Inventory', "Enter correct price per piece quantity")

        #elif bulk != 0 and not any(char.isdigit() for char in bulk):
            #tkMessageBox.showinfo('Smart Inventory System/Update Inventory', "Enter correct price in bulk quantity")

        elif i == (len(stockdetails)-1):
            Database()
            cursor.execute("Update Master Set Part_Manufacturer=?, Part_Description=?, Total_Qty=?, Calibration_EndDate=?, price_of_per_pice=?, Price_of_Bulk=?,\
                           Remarks=? Where Manufacturer_Partno=?",(manufacturer , description, quantity, enddate, price, bulk, remarks, partno,))
            conn.commit()
            cursor.close()
            conn.close()
            tkMessageBox.showinfo("Update Inventory Stock", "Successfully updated stock details")
            UpdateClear()

def ShowAddNew():
    AddClear()
    global addnewform
    addnewform = Toplevel()
    addnewform.title("Smart Inventory System/Add new")
    width = 700
    height = 600
    #screen_width = root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

def AddNewForm():
    TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text="Add New Product", font=('Cambria', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=600)
    MidAddNew.pack(side=TOP, pady=10)
    
    lbl_partnumber = Label(MidAddNew, text="Part Number:", font=('Cambria', 18), bd=10)
    lbl_partnumber.grid(row=0, sticky=W)
    lbl_partmanu = Label(MidAddNew, text="Part Manufacturer:", font=('Cambria', 18), bd=10)
    lbl_partmanu.grid(row=1, sticky=W)
    lbl_partdesc = Label(MidAddNew, text="Part Description:", font=('Cambria', 18), bd=10)
    lbl_partdesc.grid(row=2, sticky=W)
    lbl_Totalqty = Label(MidAddNew, text="Total Qty:", font=('Cambria', 18), bd=10)
    lbl_Totalqty.grid(row=3, sticky=W)
    lbl_Calibenddate = Label(MidAddNew, text="Calibration End Date:", font=('Cambria', 18), bd=10)
    lbl_Calibenddate.grid(row=4, sticky=W)
    lbl_priceperpice = Label(MidAddNew, text="Price Per Piece:", font=('Cambria', 18), bd=10)
    lbl_priceperpice.grid(row=5, sticky=W)
    lbl_priceinbulk = Label(MidAddNew, text="Price In Bulk:", font=('Cambria', 18), bd=10)
    lbl_priceinbulk.grid(row=6, sticky=W)
    lbl_remarks = Label(MidAddNew, text="Remarks:", font=('Cambria', 18), bd=10)
    lbl_remarks.grid(row=7, sticky=W)

    reg = MidAddNew.register(Check)
    partnumber = Entry(MidAddNew, textvariable=Part_Number, font=('Cambria', 18), width=20)
    partnumber.grid(row=0, column=1)
    partmanu = Entry(MidAddNew, textvariable=Part_Manufecturer, font=('Cambria', 18), width=20)
    partmanu.grid(row=1, column=1)
    partdesc = Entry(MidAddNew, textvariable=Part_Description, font=('Cambria', 18), width=20)
    partdesc.grid(row=2, column=1)
    Totalqty = Entry(MidAddNew, validate="key", validatecommand=(reg, '%P'), textvariable=Total_Qty, font=('Cambria', 18), width=20)
    Totalqty.grid(row=3, column=1)
    #Calibenddate = Entry(MidAddNew, textvariable=Calibration_EndDate, font=('Cambria', 18), width=15)
    #Calibenddate.grid(row=4, column=1)
    
    Calibenddate = DateEntry(MidAddNew, locale='en_US', date_pattern='MM/dd/yyyy', textvariable=Calibration_EndDate)
    Calibenddate.grid(row=4, column=1)
    Calibenddate.config(width=40, state='enabled')
    
    priceperpice = Entry(MidAddNew, validate="key", validatecommand=(reg, '%P'), textvariable=Price_Per_Piece, font=('Cambria', 18), width=20)
    priceperpice.grid(row=5, column=1)
    priceinbulk = Entry(MidAddNew, validate="key", validatecommand=(reg, '%P'), textvariable=Price_In_Bulk, font=('Cambria', 18), width=20)
    priceinbulk.grid(row=6, column=1)
    remarks = Entry(MidAddNew, textvariable=Remarks, font=('Cambria', 18), width=20)
    remarks.grid(row=7, column=1)
    
    btn_add = Button(MidAddNew, text="Save", font=('Cambria', 16), width=10, bg="#009ACD", command=AddNew)
    btn_add.grid(row=8, column=0, pady=30)
    btn_clear = Button(MidAddNew, text="Clear", font=('Cambria', 16), width=10, bg="#009ACD", command=AddClear)
    btn_clear.grid(row=8, column=1, pady=30)
    btn_close = Button(MidAddNew, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=lambda: [addnewform.withdraw(), Home.deiconify()])
    btn_close.grid(row=8, column=2, pady=30)

    addnewform.protocol("WM_DELETE_WINDOW", exitaddnewform)
    
def exitaddnewform():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        addnewform.withdraw()
        Home.deiconify()

def AddClear():
    Part_Number.set("")
    Part_Manufecturer.set("")
    Part_Description.set("")
    Total_Qty.set(0)
    Price_Per_Piece.set(0)
    Price_In_Bulk.set(0)
    Remarks.set("")
    
def AddNew():
    Database()
    if Part_Number.get() == "" or Part_Manufecturer.get() == "" or Part_Description.get() == "" or Total_Qty.get() == 0 or Calibration_EndDate.get() == "" or Price_Per_Piece.get() == 0 or Price_In_Bulk.get() == 0 or Remarks.get() == "":
        tkMessageBox.showinfo('Add Inventory Data', "All Fields Are Mendetory!")
        return
        print("all fields mandate")

    #elif  Total_Qty.get() != 0 and not any(char.isdigit() for char in Total_Qty.get()):
            #tkMessageBox.showinfo('Add Inventory Data', "Enter correct total quntity quantity")

    #elif Price_Per_Piece.get() != 0 and not any(char.isdigit() for char in Price_Per_Piece.get()):
            #tkMessageBox.showinfo('Add Inventory Data', "Enter correct price per piece quantity")

    #elif Price_In_Bulk.get() != 0 and not any(char.isdigit() for char in Price_In_Bulk.get()):
            #tkMessageBox.showinfo('Add Inventory Data', "Enter correct price in bulk quantity")
    
    else:
        cursor.execute("INSERT INTO `Master` (Manufacturer_Partno, Part_Manufacturer, Part_Description, Total_Qty, Calibration_EndDate, price_of_per_pice,\
                       Price_of_Bulk, Remarks) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (str(Part_Number.get()), str(Part_Manufecturer.get()), str(Part_Description.get()), int(Total_Qty.get()), str(Calibration_EndDate.get()), int(Price_Per_Piece.get()), int(Price_In_Bulk.get()), str(Remarks.get())))
        conn.commit()
        tkMessageBox.showinfo('Add Inventory Data', "Record Added successfully!")
        AddClear()
        cursor.close()
        conn.close()

def ViewForm():
    SEARCH.set("")
    global tree
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="View Products", font=('Cambria', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Cambria', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('Cambria', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_close = Button(LeftViewForm, text="Close", command=lambda: [viewform.withdraw(), Home.deiconify()])
    btn_close.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("Part_Id", "Manufecturer_Partno", "Part_Manufecturer", "Part_Description", "Total_Qty", "Calibration_EndDate", "Price_Per_Piece", "Price_In_Bulk", "Remarks"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Part_Id', text="Part_Id",anchor=W)
    tree.heading('Manufecturer_Partno', text="Manufecturer_Partno",anchor=W)
    tree.heading('Part_Manufecturer', text="Part_Manufecturer",anchor=W)
    tree.heading('Part_Description', text="Part_Description",anchor=W)
    tree.heading('Total_Qty', text="Total_Qty",anchor=W)
    tree.heading('Calibration_EndDate', text="Calibration_EndDate",anchor=W)
    tree.heading('Price_Per_Piece', text="Price_Per_Piece",anchor=W)
    tree.heading('Price_In_Bulk', text="Price_In_Bulk",anchor=W)
    tree.heading('Remarks', text="Remarks",anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=50)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=200)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.column('#7', stretch=NO, minwidth=0, width=120)
    tree.column('#8', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()
    viewform.protocol("WM_DELETE_WINDOW", exitviewform)
    
def exitviewform():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        viewform.withdraw()
        Home.deiconify()
        
def DisplayData():
    Database()
    cursor.execute("SELECT * FROM `Master`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `Master` WHERE `Manufacturer_Partno` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
    else:
         tkMessageBox.showinfo('Smart Inventory System', "Please enter any keyword to search!")
         

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")

def Delete():
    if not tree.selection():
        tkMessageBox.showinfo('Smart Inventory System', "Please select the row to delete the record!")
        print("ERROR")
    else:
        result = tkMessageBox.askquestion('Smart Inventory System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `Master` WHERE `part_id` = %d" % selecteditem[0])
            print(selecteditem[1])
            conn.commit()
            cursor.close()
            conn.close()
    

def ShowView():
    global viewform
    viewform = Toplevel()
    viewform.title("Smart Inventory System/View Product")
    width = 800
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()

def Logout():
    result = tkMessageBox.askquestion('Smart Inventory System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        #Home.destroy()
  
def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        #tkMessageBox.showinfo('Account Login', " Please complete the required field!")
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `new_user` WHERE `user_name` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `new_user` WHERE `user_name` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            #lbl_result.config(text="")
            ShowHome()
            #ShowAddNew()
            
        else:
            #tkMessageBox.showinfo('Account Login', " Invalid username or password")
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 
    
def ShowHome():
    try:
        root.withdraw()
        loginform.destroy()
        Home()
    except:
        print("Error")

def on_closing():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
         root.destroy()
         path=pathlib.Path("links.txt")
         if path.exists():
             os.remove("links.txt")
             os.system('TASKKILL /F /IM python.exe')
         else:
             os.system('TASKKILL /F /IM python.exe')
root.protocol("WM_DELETE_WINDOW", on_closing)

#========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Account", command=ShowLoginForm)
filemenu.add_command(label="Add New User ", command=ShowAddUser)
filemenu.add_command(label="Forgot Password", command=ShowForgetPassword)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
#root.attributes('-disabled', True)
#root.overrideredirect(True)
#========================================FRAME============================================
Title = Frame(root, bd=1, relief=SOLID)
Title.pack(pady=10)

#========================================LABEL WIDGET=====================================
lbl_display = Label(Title, text="Smart Inventory System", font=('Cambria', 40))
lbl_display.pack()

#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
