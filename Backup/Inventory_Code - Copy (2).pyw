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
import pandas as pd
from openpyxl import load_workbook
from pandas import DataFrame
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

windows = []
def Database():
    global conn, cursor, DATA, DATA1
    conn = sqlite3.connect("Inventory_Master.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `new_user` (change_password_date TEXT, emp_id INTEGER PRIMARY KEY NOT NULL, emp_name TEXT, user_name TEXT, privilage TEXT,\
                   secret_question TEXT, secret_answer TEXT, password TEXT)")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS `Master` (part_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Manufacturer_Partno INTEGER Secondary KEY NOT NULL,\
                   Part_Manufacturer TEXT, Part_Description TEXT, Total_Qty TEXT, Calibration_EndDate TEXT, price_of_per_pice TEXT, Price_of_Bulk TEXT, Remarks TEXT)")
   
    cursor.execute("CREATE TABLE IF NOT EXISTS `Stock` (part_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Manufacturer_Partno INTEGER SECONDARY KEY,\
                   Part_Manufacturer TEXT, Part_Description TEXT, Total_Qty TEXT, Calibration_EndDate TEXT, price_of_per_pice TEXT, Price_of_Bulk TEXT,\
                   Remarks TEXT, Required_Qty TEXT, Purpose TEXT)")


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

def canceldata():
    USERNAME.set("")
    PASSWORD.set("")

def ShowLoginForm():
    canceldata()
    global loginform
    loginform = Toplevel()
    loginform.title("Smart Inventory System/Account Login")
    width = 500
    height = 330
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
    lbl_text = Label(TopLoginForm, text="SMART INVENTORY SYSTEM - LOGIN", font=('Cambria', 18), bg="#009ACD", width=800)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=600)
    MidLoginForm.pack(side=TOP, pady=20)
    lbl_username = Label(MidLoginForm, text="Username:", font=('Cambria', 16), bd=12)
    lbl_username.grid(row=0, column=0, pady=10)
    lbl_password = Label(MidLoginForm, text="Password:", font=('Cambria', 16), bd=12)
    lbl_password.grid(row=1, column=0, pady=10)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('Cambria', 16), width=12)
    username.grid(row=0, column=1, pady=10)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('Cambria', 16), width=12, show="*")
    password.grid(row=1, column=1, pady=10)
    btn_login = Button(MidLoginForm, text="Login", font=('Cambria', 16), width=10, bg="#009ACD", command=Login)
    btn_login.grid(row=2, column=0, padx=20, pady=30)
    btn_login.bind('<Return>', Login)
    btn_clear = Button(MidLoginForm, text="Clear", font=('Cambria', 16), width=10, bg="#009ACD", command=canceldata)
    btn_clear.grid(row=2, column=1, padx=20,  pady=30)
    btn_close = Button(MidLoginForm, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=exitloginform)
    btn_close.grid(row=2,column=2, padx=20, pady=30)
    loginform.protocol("WM_DELETE_WINDOW", exitloginform)
    
def exitloginform():
    textto = loginform
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
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
    nu_cleardata()
    global adduserform
    adduserform = Toplevel()
    adduserform.title("Smart Inventory System/Add New User")
    width = 675
    height = 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    adduserform.resizable(0, 0)
    adduserform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    AddUserForm()

def AddUserForm():
    TopAddUser = Frame(adduserform, width=600, height=100, bd=1, relief=SOLID)
    TopAddUser.pack(side=TOP, pady=10)
    lbl_text = Label(TopAddUser, text="NEW USER", font=('Cambria', 18), bg="#009ACD", width=600)
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
    empname = Entry(MidAddUser, textvariable=EMP_NAME, font=('Cambria', 15), width=20)
    empname.grid(row=0, column=1)
    empid = Entry(MidAddUser, textvariable=EMP_ID, font=('Cambria', 15), width=20)
    empid.grid(row=1, column=1)
    username = Entry(MidAddUser, textvariable=EMP_USER_NAME, font=('Cambria', 15), width=20)
    username.grid(row=2, column=1)
    choices = {'Manager', 'Employee'}
    PRIVILAGE.set('Select privilage')
    popupMenu = OptionMenu(MidAddUser, PRIVILAGE, *choices)
    popupMenu.grid(row=3, column=1)
    popupMenu.config(font=('Cambria', 8), width=35)

    choices = {'Year of joining the current company?',
               'What is your pet name?',
               'What is your higher secondary school name?',
               'What is your mother’s maiden name?',
               'What was your favorite food as child?'}
    SECRET_QUESTION.set('Select Question')
    popupMenu = OptionMenu(MidAddUser, SECRET_QUESTION, *choices)
    popupMenu.grid(row=4, column=1)
    popupMenu.config(font=('Cambria', 8), width=35)    
    secretanswer = Entry(MidAddUser, textvariable=SECRET_ANSWER, font=('Cambria', 15), width=20)
    secretanswer.grid(row=5, column=1)    
    password = Entry(MidAddUser, textvariable=EMP_PASSWORD, show="*", font=('Cambria', 15), width=20)
    password.grid(row=6, column=1)    
    confirmpassword = Entry(MidAddUser, textvariable=EMP_CONFIRM_PASSWORD, show="*", font=('Cambria', 15), width=20)
    confirmpassword.grid(row=7, column=1)    
    btn_add = Button(MidAddUser, text="Add", font=('Cambria', 16), width=12, bg="#009ACD", command=AddUser)
    btn_add.grid(row=8, column=0, pady=30)    
    btn_clear = Button(MidAddUser, text="Clear", font=('Cambria', 16), width=12, bg="#009ACD", command=nu_cleardata)
    btn_clear.grid(row=8, column=1, pady=30)
    btn_cancel = Button(MidAddUser, text="Close", font=('Cambria', 16), width=12, bg="#009ACD", command=exitadduserform)
    btn_cancel.grid(row=8, column=2, pady=30)
    adduserform.protocol("WM_DELETE_WINDOW", exitadduserform)
    
def exitadduserform():
    textto = adduserform
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
        adduserform.withdraw()
        root.deiconify()

def AddUser():
    global DATA, strftime
    textto = adduserform
    Database()
    DATA = cursor.execute("select * from new_user")
    userinfo = DATA.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    emp_name = EMP_NAME.get()
    user_name = EMP_USER_NAME.get()
    privilege = PRIVILAGE.get()
    secret_question = SECRET_QUESTION.get()
    secret_answer = SECRET_ANSWER.get()
    password = EMP_PASSWORD.get()
    confirm_password = EMP_CONFIRM_PASSWORD.get()
    now = datetime.now()
    change_password_date = now.strftime("%Y-%m-%d %H:%M:%S")
    special_sym = ['$', '@', '#', '%']
    res = user_name in chain(*userinfo)
   
    if emp_name == "" or user_name == "" or privilege == 'Select privilage':
        tkMessageBox.showinfo("New User", " All fields should be mandatory!", parent=textto)
        return
    elif secret_question == 'Select Question' or secret_answer == "":
        tkMessageBox.showinfo("New User", " All fields should be mandatory!", parent=textto)
        return
    elif password == "" or confirm_password == "":
        tkMessageBox.showinfo("New User", "All fields should be mandatory!", parent=textto)
        return
    else:
        try:
            emp_id = EMP_ID.get()
        except FloatingPointError:
            tkMessageBox.showinfo("New User", "Please Enter Correct Employee ID!", parent=textto)
            return
        except ValueError:
            tkMessageBox.showinfo("New User", "Please Enter Correct Employee ID!", parent=textto)
            return
        except TclError:
            tkMessageBox.showinfo("New User", "Please Enter Correct Employee ID!", parent=textto)
            return

    res1 = emp_id in chain(*userinfo)
    for i in range(len(userinfo)):
        if res == True and user_name != "":
            tkMessageBox.showinfo('New User', "Username already exist!", parent=textto)
            break
        elif  res1 == True  and emp_id != "":
            tkMessageBox.showinfo('New User', "Employee Id already exist!", parent=textto)
            break
        elif any(char.isdigit() for char in emp_name):
            tkMessageBox.showinfo('New User', "Please Enter Correct Employee Name!", parent=textto)
            break
        elif any(char.isdigit() for char in user_name):
            tkMessageBox.showinfo('New User',
                                "Please Enter Correct Employee Username\n(Accept only Characters!)", parent=textto)
            break
        elif any(char.isalpha() for char in str(emp_id)):
            tkMessageBox.showinfo('New User', "Please Enter Correct Employee ID!", parent=textto)
            break
        elif secret_question == 'Year of joining the current company?' and any(char.isalpha() for char in secret_answer):
            tkMessageBox.showinfo('New User', "Enter the Correct Answer \n in 'YYYY' format!", parent=textto)
            break
        elif secret_question != 'Year of joining the current company?'and any(char.isdigit() for char in secret_answer):
            tkMessageBox.showinfo('New User', "Enter the Correct Answer in string format!", parent=textto)
            break
        elif secret_question == 'Year of joining the current company?'and len(str(secret_answer)) != 4:
            tkMessageBox.showinfo('New User',
                                "Enter the Correct secret Answer \n in 'YYYY' format!", parent=textto)
            break
        elif len(str(emp_id)) >= 8:
            tkMessageBox.showinfo('New User', "EmpID is restricted \n to 8 charcters!", parent=textto)
            break
        elif len(password) < 8:
            tkMessageBox.showinfo("New User", "Password length should be \n at least 8!", parent=textto)
            break
        elif len(password) > 20:
            tkMessageBox.showinfo("New User", "Password length should not \n be greater than 20!", parent=textto)
            break
        elif not any(char.isdigit() for char in password):
            tkMessageBox.showinfo("New User", "Password should have at \n least one numeral!", parent=textto)
            break
        elif not any(char.isupper() for char in password):
            tkMessageBox.showinfo("New User", "Password should have at least \n one uppercase letter!", parent=textto)
            break
        elif not any(char.islower() for char in password):
            tkMessageBox.showinfo("New User", "Password should have at least \n one lowercase letter!", parent=textto)
            break
        elif not any(char in special_sym for char in password):
            tkMessageBox.showinfo("New User",
                                "Password should have at \n least one of the symbols \n $ @ # %!", parent=textto)
            break
        elif  password != confirm_password:
            tkMessageBox.showinfo("New User", "Password and Confirm Password \n did not match!",parent=textto)
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
            #lbl_result.config(text="Added Successfully \n Add new user or Press Cancel to exit", fg="red")
            tkMessageBox.showinfo("New User", "Added Successfully ", parent=textto)
            nu_cleardata()

def fp_cleardata():
    FP_EMP_ID.set("")
    FP_EMP_USER_NAME.set("")
    FP_SECRET_QUESTION.set('Select Question')
    FP_SECRET_ANSWER.set("")
    FP_EMP_PASSWORD.set("")
    FP_EMP_CONFIRM_PASSWORD.set("")

def ShowForgetPassword():
    fp_cleardata()
    global forgetpasswordform
    forgetpasswordform = Toplevel()
    forgetpasswordform.title("Smart Inventory System/Forget Password Page")
    width = 625
    height = 475
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
    lbl_text = Label(TopForgetPassword, text="FORGET PASSWORD", font=('Cambria', 15), bg="#009ACD", width=600)
    lbl_text.pack(fill=X)
    MidForgetPassword = Frame(forgetpasswordform, width=600)
    MidForgetPassword.pack(side=TOP, pady=20)    
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
    empid = Entry(MidForgetPassword, textvariable=FP_EMP_ID, font=('Cambria', 15), width=20)
    empid.grid(row=0, column=1)
    username = Entry(MidForgetPassword, textvariable=FP_EMP_USER_NAME, font=('Cambria', 15), width=20)
    username.grid(row=1, column=1)
    choices = {'Year of joining the current company?',
               'What is your pet name?',
               'What is your higher secondary school name?',
               'What is your mother’s maiden name?',
               'What was your favorite food as child?'}
    FP_SECRET_QUESTION.set('Select Question')
    popupMenu = OptionMenu(MidForgetPassword, FP_SECRET_QUESTION, *choices)
    popupMenu.grid(row=2, column=1)
    popupMenu.config(font=('Cambria', 8), width=35)
    secretanswer = Entry(MidForgetPassword, textvariable=FP_SECRET_ANSWER, font=('Cambria', 15), width=20)
    secretanswer.grid(row=3, column=1)    
    password = Entry(MidForgetPassword, textvariable=FP_EMP_PASSWORD, show="*", font=('Cambria', 15), width=20)
    password.grid(row=4, column=1)    
    confirmpassword = Entry(MidForgetPassword, textvariable=FP_EMP_CONFIRM_PASSWORD, show="*", font=('Cambria', 15), width=20)
    confirmpassword.grid(row=5, column=1)    
    btn_update = Button(MidForgetPassword, text="Update", font=('Cambria', 15), width=12, bg="#009ACD", command=ForgetPassword)
    btn_update.grid(row=6, column=0, pady=30)    
    btn_clear = Button(MidForgetPassword, text="Clear", font=('Cambria', 15), width=12, bg="#009ACD", command=fp_cleardata)
    btn_clear.grid(row=6, column=1, pady=30)
    btn_close = Button(MidForgetPassword, text="Close", font=('Cambria', 15), width=12, bg="#009ACD", command=exitforgetpasswordform)
    btn_close.grid(row=6, column=2, pady=30)
    forgetpasswordform.protocol("WM_DELETE_WINDOW", exitforgetpasswordform)
    
def exitforgetpasswordform():
    textto = forgetpasswordform
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
        forgetpasswordform.withdraw()
        root.deiconify()

def ForgetPassword():
    textto = forgetpasswordform
    Database()
    DATA1 = cursor.execute("select * from new_user")
    userinfofp = DATA1.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    user_name = FP_EMP_USER_NAME.get()
    secret_question = FP_SECRET_QUESTION.get()
    secret_answer = FP_SECRET_ANSWER.get()
    password = FP_EMP_PASSWORD.get()
    confirm_password = FP_EMP_CONFIRM_PASSWORD.get()
    now = datetime.now()
    change_password_date = now.strftime("%Y-%m-%d %H:%M:%S")
    special_sym = ['$', '@', '#', '%']
    res = user_name in chain(*userinfofp)
    res2 = secret_question in chain(*userinfofp)
    res3 = secret_answer in chain(*userinfofp)
  
    if user_name == "":
        tkMessageBox.showinfo("Forget Password", " All fields should be mandatory!", parent=textto)
        return
    elif secret_question == 'Select Question' or secret_answer == "":
         tkMessageBox.showinfo("Forget Password", " All fields should be mandatory!", parent=textto)
         return
    elif password == "" or confirm_password == "":
        tkMessageBox.showinfo("Forget Password", " All fields should be mandatory!", parent=textto)
        return
    else:
        try:
            emp_id = FP_EMP_ID.get()
        except FloatingPointError:
            tkMessageBox.showinfo("Forget Password", "Please Enter Correct Employee ID", parent=textto)
            return
        except ValueError:
            tkMessageBox.showinfo("Forget Password", "Please Enter Correct Employee ID", parent=textto)
            return
        except TclError:
             tkMessageBox.showinfo("Forget Password", "Please Enter Correct Employee ID", parent=textto)
             return

    res1 = emp_id in chain(*userinfofp)
    for i in range(len(userinfofp)):
        if  res != True and user_name != "":
            tkMessageBox.showinfo('Forget Password', "Invalid Username", parent=textto)
            break
        elif res1 != True and emp_id != "":
            tkMessageBox.showinfo('Forget Password', "Invalid Employee Id", parent=textto)
            break
        elif res2 != True and secret_question != "":
            tkMessageBox.showinfo('Forget Password', "Invalid Secret Question", parent=textto)
            break
        elif res3 != True and secret_answer != "":
            tkMessageBox.showinfo('Forget Password', "Invalid Secret Answer", parent=textto)
            break
        elif len(str(emp_id)) >= 8:
            tkMessageBox.showinfo('Forget Password', "EmpID is restricted \n to 8 charcters", parent=textto)
            break
        elif len(password) < 8:
            tkMessageBox.showinfo("Forget Password", "Password length should be \n at least 8", parent=textto)
            break
        elif len(password) > 20:
            tkMessageBox.showinfo("Forget Password", "Password length should not \n be greater than 20", parent=textto)
            break
        elif not any(char.isdigit() for char in password):
            tkMessageBox.showinfo("Forget Password", "Password should have at \n least one numeral", parent=textto)
            break
        elif not any(char.isupper() for char in password):
            tkMessageBox.showinfo("Forget_Password", "Password should have at least \n one uppercase letter", parent=textto)
            break
        elif not any(char.islower() for char in password):
            tkMessageBox.showinfo("Forget Password", "Password should have at least \n one lowercase letter", parent=textto)
            break
        elif not any(char in special_sym for char in password):
            tkMessageBox.showinfo("Forget Password",
                                "Password should have at \n least one of the symbols \n $ @ # %", parent=textto)
            break
        elif  password != confirm_password:
            tkMessageBox.showinfo("Forget Password", "Password and Confirm Password \n did not match", parent=textto)
            break
        elif str(emp_id) in str(userinfofp[i][1]) and user_name not in userinfofp[i][3]:
            print(emp_id,userinfofp[i][1])
            tkMessageBox.showinfo('Forget Password', 'Invalid User Name', parent=textto)
            break
        elif str(emp_id) in str(userinfofp[i][1]) and secret_question not in userinfofp[i][5]:
            tkMessageBox.showinfo('Forget Password', 'Invalid Secret Question', parent=textto)
            break
        elif str(emp_id) in str(userinfofp[i][1]) and secret_answer not in userinfofp[i][6]:
            tkMessageBox.showinfo('Forget Password', 'Invalid Secret Answer', parent=textto)
            break
        elif str(emp_id) in str(userinfofp[i][1]) and password in userinfofp[i][7]:
            tkMessageBox.showinfo('Forget Password',
                               'New Password Cannot Be The Same As \n The Last Three Passwords', parent=textto)
            break
        elif i == (len(userinfofp)-1):
            Database()
            cursor.execute("Update new_user Set password=?, change_password_date=? Where emp_id=?",(password, change_password_date, emp_id))
            conn.commit()
            cursor.close()
            conn.close()
            tkMessageBox.showinfo("Forget Password", "Password Updated Successfully", parent=textto)
            fp_cleardata()

def home():
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
    lbl_display = Label(Title, text="Smart Inventory System", font=('Cambria', 45), bg="#009ACD")
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
    #windows.append(Home)
    Home.protocol("WM_DELETE_WINDOW", exitHome)

def exitHome():
    textto = Home
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
        Home.withdraw()
        root.deiconify()
        
def ShowStock():
    Clear()
    global getstockform
    getstockform = Toplevel()
    getstockform.title("Smart Inventory System/Stock Inventory")
    width = 700
    height = 600
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    getstockform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    getstockform.resizable(0, 0)
    windows.append(getstockform)
    GetStockForm()

def GetStockForm():
    TopGetStock = Frame(getstockform, width=600, height=100, bd=1, relief=SOLID)
    TopGetStock.pack(side=TOP, pady=10)
    lbl_text = Label(TopGetStock, text="Stock Inventory", font=('Cambria', 18), bg="#009ACD", width=600)
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
    totalqty = Entry(MidStock, textvariable=TOTAL_QTY, font=('Cambria', 18), width=20)
    totalqty.grid(row=3, column=1)
    totalqty.config(state='disabled')
    enddate = Entry(MidStock, textvariable=CALIBRATION_ENDDATE, font=('Cambria', 18), width=20)
    enddate.grid(row=4, column=1)
    enddate.config(state='disabled')
    priceperpiece = Entry(MidStock, textvariable=PRICE_PER_PIECE, font=('Cambria', 18), width=20)
    priceperpiece.grid(row=5, column=1)
    priceperpiece.config(state='disabled')
    priceinbulk = Entry(MidStock, textvariable=PRICE_IN_BULK, font=('Cambria', 18), width=20)
    priceinbulk.grid(row=6, column=1)
    priceinbulk.config(state='disabled')    
    requiredqty = Entry(MidStock, textvariable=REQUIRED_QTY, font=('Cambria', 18), width=20)
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
    btn_close = Button(MidStock, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=exitgetstockform)
    btn_close.grid(row=9, column=2, pady=30)

    getstockform.protocol("WM_DELETE_WINDOW", exitgetstockform)
    
def exitgetstockform():
    textto = getstockform
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
        getstockform.withdraw()
        Home.deiconify()

def GetStock(event=None):
    textto = getstockform
    itemno = PART_NO.get()
    if itemno != 'Select Item Number':
        itemno = eval(itemno)
        itemno = (itemno[0])
    partdescrip = PART_DESARIPTION.get()
    partmanufacturer = PART_MANUFACTURER.get()
    date = CALIBRATION_ENDDATE.get()
    purpose = PURPOSE.get()

    if itemno == 'Select Item Number' or purpose == 'Select Purpose':
        tkMessageBox.showinfo('Stock Inventory', "All fields should be mandatory!", parent=textto)
        return
    else:
        try:
            tlqty = TOTAL_QTY.get()
            pricepiece = PRICE_PER_PIECE.get()
            bulk = PRICE_IN_BULK.get()
        except FloatingPointError:
            tkMessageBox.showinfo('Stock Inventory', "All fields should be mandatory!", parent=textto)
            return
        except ValueError:
            tkMessageBox.showinfo('Stock Inventory', "All fields should be mandatory!", parent=textto)
            return
        except TclError:
            tkMessageBox.showinfo('Stock Inventory', "All fields should be mandatory!", parent=textto)
            return    
        try:
            reqdqty = REQUIRED_QTY.get()
        except FloatingPointError:
            tkMessageBox.showinfo('Stock Inventory', "InValid Required Quantity!", parent=textto)
            return
        except ValueError:
            tkMessageBox.showinfo('Stock Inventory', "InValid Required Quantity!", parent=textto)
            return
        except TclError:
            tkMessageBox.showinfo('Stock Inventory', "InValid Required Quantity!", parent=textto)
            return 

    if reqdqty > tlqty:
        result = tkMessageBox.askquestion('Stock Inventory',"Inventory stock for selected part number is low Would you like to order!", parent=textto)
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
        tkMessageBox.showinfo('Stock Inventory', "Stock updated successfully!", parent=textto)
        Clear()

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
    TOTAL_QTY.set("")
    CALIBRATION_ENDDATE.set("")
    PRICE_PER_PIECE.set("")
    PRICE_IN_BULK.set("")
    REQUIRED_QTY.set("")
    PURPOSE.set("Select Purpose")

def ShowOrder():
    Cancel()
    global orderform
    orderform = Toplevel()
    orderform.title("Smart Inventory System/Stock Inventory")
    width = 700
    height = 350
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    orderform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    orderform.resizable(0, 0)
    windows.append(orderform)
    windows.append(orderform)
    OrderForm()
    
def OrderForm():
    TopOrder = Frame(orderform, width=600, height=100, bd=1, relief=SOLID)
    TopOrder.pack(side=TOP, pady=10)
    lbl_text = Label(TopOrder, text="Stock Inventory", font=('Cambria', 18),bg="#009ACD", width=600)
    lbl_text.pack(fill=X)
    MidOrder = Frame(orderform, width=700)
    MidOrder.pack(side=TOP, pady=50)    
    lbl_partno = Label(MidOrder, text="Item Part Number:", font=('Cambria', 18), bd=10)
    lbl_partno.grid(row=1, sticky=W)
    
    #lbl_manufact = Label(MidOrder, text="Manufacturer:", font=('Cambria', 18), bd=10)
    #lbl_manufact.grid(row=2, sticky=W)
    
    lbl_quantity = Label(MidOrder, text="Required Quantity:", font=('Cambria', 18), bd=10)
    lbl_quantity.grid(row=3, sticky=W)
    itempartno = PART_NO.get()
    itempartno = eval(itempartno)
    itempartno = (itempartno[0])
    PART_NUMBER.set(itempartno)
    partnumber = Entry(MidOrder, textvariable=PART_NUMBER, font=('Cambria', 18), width=19)
    partnumber.grid(row=1, column=1)
    partnumber.config(state='disabled')
    
    #choices = {'Digi key', 'Mouser Electronic', 'Elements 14', 'Arrow Electronic', 'Verical', 'Quest Electronic', 'Avnet'}
    #MANUFACTURER.set('Select Manufacturer')
    #popupMenu = OptionMenu(MidOrder, MANUFACTURER, *choices)
    #popupMenu.grid(row=2, column=1)
    #popupMenu.config(font=('Cambria', 16), width=18)
    
    requiredqty = Entry(MidOrder, textvariable=REQUIRED_QUANTITY, font=('Cambria', 18), width=19)
    requiredqty.grid(row=3, column=1)   
    btn_search = Button(MidOrder, text="Search", font=('Cambria', 16), width=10, bg="#009ACD", command=StockSearch)
    btn_search.grid(row=4,column=0, pady=30)
    btn_search.bind('<Return>', StockSearch)
    btn_clear = Button(MidOrder, text="Clear", font=('Cambria', 16), width=10, bg="#009ACD", command=Cancel)
    btn_clear.grid(row=4, column=1, pady=30)
    btn_close = Button(MidOrder, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=exitorderform)
    btn_close.grid(row=4, column=2, pady=30)

    orderform.protocol("WM_DELETE_WINDOW", exitorderform)
    
def exitorderform():
    textto = orderform
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
        orderform.withdraw()
        Home.deiconify()

def Cancel():
    REQUIRED_QUANTITY.set("")
    #MANUFACTURER.set('Select Manufacturer')

def StockSearch(event=None):
    textto = orderform
    global itemno, manufact, reqty, listlinks
    itemno = PART_NUMBER.get()
    #manufact = MANUFACTURER.get()

    if itemno == "":
        tkMessageBox.showinfo("Smart Inventory System", "All fields should be mandatory!", parent=textto)
        return
    else:
        try:
            reqty = REQUIRED_QUANTITY.get()
        except FloatingPointError:
            tkMessageBox.showinfo('Smart Inventory System', "InValid Required Quantity!", parent=textto)
            return
        except ValueError:
            tkMessageBox.showinfo('Smart Inventory System', "InValid Required Quantity!", parent=textto)
            return
        except TclError:
            tkMessageBox.showinfo('Smart Inventory System', "InValid Required Quantity!", parent=textto)
            return
    try:
        from googlesearch import search 
    except ImportError:
        print("No module named 'google' found")
    listlinks = []
    query = itemno
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        #Create and write to txt file
        listlinks.append(j)
    print(listlinks)   
    matching = [s for s in listlinks if "www.youtube.com" in s]
    print(matching)
    if matching != []:
        for i in range(len(matching)):
            listlinks.remove(matching[i])
    with open("links.txt",'w',encoding = 'utf-8') as f:
        for i in listlinks:
            f.write(i + "\n")
    if  listlinks == []:
        tkMessageBox.showinfo("Link", " Manufecturer link not found - please make sure partno. is correct!", parent=textto)
        return
    else:    
        result = tkMessageBox.askquestion('Email Notification', 'Would you like to Send Email to Procurment team?', icon="warning", parent=textto)
        if result == 'yes': 
            SearchForm()
        else:
            return
	
def SearchForm():
    # Function to read the contacts from a given contact file and return a
    # list of names and email addresses
    global itemno, manufact, reqty, listlinks
    subject = "Procurment Notification..."
    body = "Hi All,\n Please find the attached text file with links for the  procurement of the below mentioned item : \n Part NO. -  ", itemno,\
    "\n Required Quntity - ", reqty, "\n \n Note : This is an automatically generate email.\n Please do not reply to it." \
    "if you have any queries regarding your order please email 'ankit.shukla@altran.com'. "
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
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    tkMessageBox.showinfo('Email notification', "Email Sent to Procurment team!")

def UpdateStock():
    UpdateClear()
    global updateform
    updateform = Toplevel()
    updateform.title("Smart Inventory System/Update Inventory stock")
    width = 700
    height = 600
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    updateform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateform.resizable(0, 0)
    windows.append(updateform)
    UpdateStockForm()

def UpdateStockForm():
    TopUpdate = Frame(updateform, width=600, height=100, bd=1, relief=SOLID)
    TopUpdate.pack(side=TOP, pady=10)
    lbl_text = Label(TopUpdate, text="Update Inventory Stock", font=('Cambria', 18), bg="#009ACD", width=600)
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
    totalqty = Entry(MidUpdate, textvariable=Total_Quantity, font=('Cambria', 18), width=18)
    totalqty.grid(row=3, column=1)
    enddate = DateEntry(MidUpdate, locale='en_US', date_pattern='MM/dd/yyyy', textvariable=Calib_EndDate)
    enddate.grid(row=4, column=1)
    enddate.config(width=35)
    priceperpiece = Entry(MidUpdate, textvariable=Price_Piece, font=('Cambria', 18), width=18)
    priceperpiece.grid(row=5, column=1)
    priceinbulk = Entry(MidUpdate, textvariable=Price_Bulk, font=('Cambria', 18), width=18)
    priceinbulk.grid(row=6, column=1)    
    remarks = Entry(MidUpdate, textvariable=Re_Marks, font=('Cambria', 18), width=18)
    remarks.grid(row=7, column=1)    
    btn_update = Button(MidUpdate, text="Update", font=('Cambria', 16), width=10, bg="#009ACD", command=Update)
    btn_update.grid(row=9,column=0, pady=30)
    btn_update.bind('<Return>', Update)
    btn_clear = Button(MidUpdate, text="Clear", font=('Cambria', 16), width=10, bg="#009ACD", command=UpdateClear)
    btn_clear.grid(row=9, column=1, pady=30)
    btn_close = Button(MidUpdate, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=exitupdateform)
    btn_close.grid(row=9, column=2, pady=30)

    updateform.protocol("WM_DELETE_WINDOW", exitupdateform)
    
def exitupdateform():
    textto = updateform
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
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
    Total_Quantity.set("")
    Price_Piece.set("")
    Price_Bulk.set("")
    Re_Marks.set("")

def Update():
    textto = updateform
    partno = Item_Number.get()
    if partno != 'Select Part Number':
        partno = eval(partno)
        partno = (partno[0])

    manufacturer = Item_Manufacturer.get()
    description = Product_Description.get()
    enddate = Calib_EndDate.get()
    remarks = Re_Marks.get()    
    Database()
    cursor.execute("select * from Master")
    stockdetails = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    
    if partno == 'Select Part Number' or manufacturer == "" or description == "" or remarks == "":
            tkMessageBox.showinfo("Update Inventory Stock", "All fields should be mandatory!", parent=textto)
            return
    else:
        try:
            quantity = Total_Quantity.get()
            price = Price_Piece.get()
            bulk = Price_Bulk.get()
        except FloatingPointError:
            tkMessageBox.showinfo('Update Inventory Stock', "InValid Total Quantity/Price Per Piece/Price In Bulk!", parent=textto)
            return
        except ValueError:
            tkMessageBox.showinfo('Update Inventory Stock', "InValid Total Quantity/Price Per Piece/Price In Bulk!", parent=textto)
            return
        except TclError:
            tkMessageBox.showinfo('Update Inventory Stock', "InValid Total Quantity/Price Per Piece/Price In Bulk!", parent=textto)
            return

    for i in range(len(stockdetails)):
        if i == (len(stockdetails)-1):
            Database()
            cursor.execute("Update Master Set Part_Manufacturer=?, Part_Description=?, Total_Qty=?, Calibration_EndDate=?, price_of_per_pice=?, Price_of_Bulk=?,\
                           Remarks=? Where Manufacturer_Partno=?",(manufacturer , description, quantity, enddate, price, bulk, remarks, partno,))
            conn.commit()
            cursor.close()
            conn.close()
            tkMessageBox.showinfo("Update Inventory Stock", "Successfully updated stock details", parent=textto)
            UpdateClear()

def ShowAddNew():
    AddClear()
    global addnewform
    addnewform = Toplevel()
    addnewform.title("Smart Inventory System/Add new")
    width = 750
    height = 600
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    windows.append(addnewform)
    AddNewForm()

def AddNewForm():
    TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text="Add New Product", font=('Cambria', 18), bg="#009ACD", width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=600)
    MidAddNew.pack(side=TOP, pady=10)
    
    lbl_partnumber = Label(MidAddNew, text="Manufacturer Part number:", font=('Cambria', 18), bd=10)
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

    partnumber = Entry(MidAddNew, textvariable=Part_Number, font=('Cambria', 18), width=20)
    partnumber.grid(row=0, column=1)
    partmanu = Entry(MidAddNew, textvariable=Part_Manufecturer, font=('Cambria', 18), width=20)
    partmanu.grid(row=1, column=1)
    partdesc = Entry(MidAddNew, textvariable=Part_Description, font=('Cambria', 18), width=20)
    partdesc.grid(row=2, column=1)
    Totalqty = Entry(MidAddNew, textvariable=Total_Qty, font=('Cambria', 18), width=20)
    Totalqty.grid(row=3, column=1)    
    Calibenddate = DateEntry(MidAddNew, locale='en_US', date_pattern='MM/dd/yyyy', textvariable=Calibration_EndDate)
    Calibenddate.grid(row=4, column=1)
    Calibenddate.config(width=40, state='enabled')    
    priceperpice = Entry(MidAddNew, textvariable=Price_Per_Piece, font=('Cambria', 18), width=20)
    priceperpice.grid(row=5, column=1)
    priceinbulk = Entry(MidAddNew, textvariable=Price_In_Bulk, font=('Cambria', 18), width=20)
    priceinbulk.grid(row=6, column=1)
    remarks = Entry(MidAddNew, textvariable=Remarks, font=('Cambria', 18), width=20)
    remarks.grid(row=7, column=1)    
    btn_add = Button(MidAddNew, text="Save", font=('Cambria', 16), width=10, bg="#009ACD", command=AddNew)
    btn_add.grid(row=8, column=0, pady=30)
    btn_clear = Button(MidAddNew, text="Clear", font=('Cambria', 16), width=10, bg="#009ACD", command=AddClear)
    btn_clear.grid(row=8, column=1, pady=30)
    btn_close = Button(MidAddNew, text="Close", font=('Cambria', 16), width=10, bg="#009ACD", command=exitaddnewform)
    btn_close.grid(row=8, column=2, pady=30)

    addnewform.protocol("WM_DELETE_WINDOW", exitaddnewform)
    
def exitaddnewform():
    textto = addnewform
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
        addnewform.withdraw()
        Home.deiconify()

def AddClear():
    Part_Number.set("")
    Part_Manufecturer.set("")
    Part_Description.set("")
    Total_Qty.set("")
    Price_Per_Piece.set("")
    Price_In_Bulk.set("")
    Remarks.set("")
    
def AddNew():
    textto = addnewform
    Database()
    cursor.execute("select * from Master")
    adddetails = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    for i in range(len(adddetails)):
        if Part_Number.get() == "" or Part_Manufecturer.get() == "" or Part_Description.get() == ""  or Calibration_EndDate.get() == "" or Remarks.get() == "":
            tkMessageBox.showinfo('Add Inventory Data', "All fields should be mandatory!", parent=textto)
            return
        else:
            try:
                tquantity = Total_Qty.get()
                pprice = Price_Per_Piece.get()
                pbulk = Price_In_Bulk.get()
            except FloatingPointError:
                tkMessageBox.showinfo('Add Inventory Data', "InValid Total Quantity/Price Per Piece/Price In Bulk!", parent=textto)
                return
            except ValueError:
                tkMessageBox.showinfo('Add Inventory Data', "InValid Total Quantity/Price Per Piece/Price In Bulk!", parent=textto)
                return
            except TclError:
                tkMessageBox.showinfo('Add Inventory Data', "InValid Total Quantity/Price Per Piece/Price In Bulk!", parent=textto)
                return    
        #for i in range(len(adddetails)):
            if i == (len(adddetails)-1):
                Database()
                cursor.execute("INSERT INTO `Master` (Manufacturer_Partno, Part_Manufacturer, Part_Description, Total_Qty, Calibration_EndDate, price_of_per_pice,\
                               Price_of_Bulk, Remarks) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (str(Part_Number.get()), str(Part_Manufecturer.get()), str(Part_Description.get()), int(Total_Qty.get()), str(Calibration_EndDate.get()), int(Price_Per_Piece.get()), int(Price_In_Bulk.get()), str(Remarks.get())))
                conn.commit()
                tkMessageBox.showinfo('Add Inventory Data', "Record Added successfully!", parent=textto)
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
    lbl_text = Label(TopViewForm, text="View Products", font=('Cambria', 18), bg="#009ACD", width=600)
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
    btn_bom = Button(LeftViewForm, text="Generate BOM", command=Bom)
    btn_bom.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_close = Button(LeftViewForm, text="Close", command=exitviewform)
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
    textto = viewform
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?", parent=textto):
        viewform.withdraw()
        Home.deiconify()
        
def DisplayData():
    textto = viewform
    Database()
    cursor.execute("SELECT * FROM `Master`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    
def Bom():
    textto = viewform
    curItems = tree.selection()
    if not tree.selection():
        tkMessageBox.showinfo('Smart Inventory System', "Please select the row!", parent=textto)
    else:
        bom_lists=([list(tree.item(i)['values']) for i in curItems])
        print(bom_lists)
        df = DataFrame (bom_lists)
        now = datetime.now()
        Bom_Creat_date = now.strftime("%Y-%m-%d_%H-%M-%S") 
        input_filename = "Bom" + str(Bom_Creat_date) + ".xlsx"
        path = "Automated_Bom" + "/" + input_filename
        if os.path.isfile(path):
            writer = pd.ExcelWriter(path, engine='openpyxl')
            # try to open an existing workbook
            writer.book = load_workbook(path)
            # copy existing sheets
            writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
            # read existing file
            reader = pd.read_excel(path)
            # write out the new sheet
            df.to_excel(writer,sheet_name='BOM',index=False,header=False,startrow=len(reader)+1)
            writer.close()
            Reset()
        else:
            df.columns = ['part_id','Manufacturer_Partno','Part_Manufacturer','Part_Description','Total_Qty','Calibration_EndDate','price_of_per_pice','Price_of_Bulk','Remarks']
            #print (df)
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='BOM')
            writer.save()
            tkMessageBox.showinfo("BOM File", "Please navigate to Automated_Bom folder from current directory to find the generated BOM!", parent=textto)
            Reset()    
        
def Search():
    textto = viewform
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())

        Database()
        cursor.execute("SELECT * FROM `Master` WHERE `Manufacturer_Partno` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetchno = cursor.fetchall()

        cursor.execute("SELECT * FROM `Master` WHERE `Part_Description` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetchmanu = cursor.fetchall()
        
        res_list = []
        for i in fetchno:
            if i not in fetchmanu:
                res_list.append(i) 
        for i in fetchmanu:
            if i not in fetchno:
                res_list.append(i)
        #print(res_list)
        for i in fetchno:
            if i in fetchmanu:
                res_list.append(i) 
        #print(res_list)
        
        for data in res_list:
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
    textto = viewform
    if not tree.selection():
        tkMessageBox.showinfo('Smart Inventory System', "Please select the row to delete the record!",parent=textto)
        return
    else:
        result = tkMessageBox.askquestion('Smart Inventory System', 'Are you sure you want to delete this record?', icon="warning", parent=textto)
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
    windows.append(viewform)
    ViewForm()

def Logout():
    result = tkMessageBox.askquestion('Smart Inventory System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home.destroy()
        for window in range(len(windows)):         
            windows[window].destroy()
              
      
  
def Login(event=None):
    global admin_id
    textto = loginform
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        tkMessageBox.showinfo('Account Login', " Please complete the required field!", parent=textto)
    else:
        cursor.execute("SELECT * FROM `new_user` WHERE `user_name` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `new_user` WHERE `user_name` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            ShowHome()            
        else:
            tkMessageBox.showinfo('Account Login', " Invalid username or password!", parent=textto)
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 
    
def ShowHome():
    global Home
    root.withdraw()
    loginform.destroy()
    home()

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
#========================================FRAME============================================
Title = Frame(root, bd=1, relief=SOLID)
Title.pack(pady=10)
#========================================LABEL WIDGET=====================================
lbl_display = Label(Title, text="Smart Inventory System", font=('Cambria', 40))
lbl_display.pack()
#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
