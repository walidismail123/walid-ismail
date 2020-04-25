#imported modules
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
import time
import datetime
import smtplib
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MT1
import requests
import matplotlib.pyplot as plt

import os#usernames and password are saved in a txt file 





def get_data(country_code=''):#function that gets the country/global data 
    if country_code=='':
        url='https://api.thevirustracker.com/free-api?global=stats'
        page=requests.get(url)
        data=page.json()
        results={}
        for elt in data['results'][0].keys():
            if elt!='source':
                temp={'title':'World','code':''}
                temp[elt]=data['results'][0][elt]
                results.update(temp)
        return results
    

    url='https://api.thevirustracker.com/free-api?countryTotal='+country_code
    page=requests.get(url)
    data=page.json()
    country_name=country_code.lower()
    results={}

    for elt in data['countrydata'][0]['info'].keys():
        if elt == 'title' or elt == 'code':
            results[elt]=data['countrydata'][0]['info'][elt]

    for elt in data['countrydata'][0].keys():
        if elt!='info':
            temp={}
            temp[elt]=data['countrydata'][0][elt]
            results.update(temp)


    return results




def get_countries(): #function that returns a dictionnary with country names as keys and country codes as values
    url='https://api.thevirustracker.com/free-api?countryTotals=ALL'
    page=requests.get(url)
    data=page.json()
    database={'World':''}
    temp={}

    for i in range(1,len(data['countryitems'][0])):
        for j in data['countryitems'][0][str(i)].keys():
            if j =='title':
                name=data['countryitems'][0][str(i)][j]
            if j=='code':
                temp[name]=data['countryitems'][0][str(i)][j]
            database.update(temp)

    return database


    

def get_country_code(name):#function that transforms an inputted country name into it's respective country code
    database=get_countries()
    for i in database.keys():
        if name.lower()==i.lower():
            return database[i]



def print_(country_data):#function that print the dictionnary data prior to the function get_data()(returns a string)
    res=''
    for i in country_data.keys():
        res=res+(' ').join(i.split('_'))+' : '+str(country_data[i])+'\n'
    return res


def user_registration():#this function will create a database file for each user containing their private information(email,password,username...)
    UserNameliste=[]
    NAME=Name.get()
    UserName=Username.get()
    emailid=EmailId.get()
    password=Password.get()
    userfile=open(UserName,"w")
    userfile.write(NAME+"\n")
    userfile.write(UserName+"\n")
    userfile.write(emailid+"\n")
    userfile.write(password+"\n")
    userfile.close()
    
    if NAME!='' and UserName!='' and emailid!='' and password!='':#this is to verify that every entry is filled
        messagebox.showinfo("Succes!", "Registration Success!")
    else:
        messagebox.showerror("Error!", "Registration Failed!")  
    
def register():#creating the register GUI
    global ScreenRegi,UserNameliste,Name,Username,EmailId,Password,user_verify,pass_verify

    ScreenRegi=Toplevel(RegiAndLogin)
    ScreenRegi.title("registration form")
    ScreenRegi.geometry("400x400")

    Name=StringVar()
    Username=StringVar()
    EmailId=StringVar()
    Password=StringVar()
    NameLabel=Label(ScreenRegi,text="  Name  ").pack()
    NameEntry=Entry(ScreenRegi,textvariable=Name,width=50).pack()
    UsernameLabel=Label(ScreenRegi,text="   Username   ").pack()
    UsernameEntry=Entry(ScreenRegi,textvariable=Username,width=50).pack()
    EmailIdLabel=Label(ScreenRegi,text="   Email   ").pack()
    EmailIdLabel=Entry(ScreenRegi,textvariable=EmailId,width=50).pack()
    PasswordLabel=Label(ScreenRegi,text="   Password   ").pack()
    PasswordEntry=Entry(ScreenRegi,textvariable=Password,show="*",width=50).pack()
    blank=Label(ScreenRegi,text="  ").pack()
    RegistrationButton=Button(ScreenRegi,text="register",command=user_registration).pack()
 #pack is used here to allign the widgets quickly since not too much is going on 



def login():#creating the login GUI
    global ScreenLogIn,olduser,oldpass,Name,Username,EmailId,Password

    olduser=StringVar()
    oldpass=StringVar()
    ScreenLogIn=Toplevel(RegiAndLogin)
    ScreenLogIn.title("log in")
    ScreenLogIn.geometry("400x400")
    loginuser=Label(ScreenLogIn,text="Username").pack()
    login_user_entry=Entry(ScreenLogIn,textvariable=olduser,width=50).pack()
    loginpass=Label(ScreenLogIn,text="Password").pack()
    login_pass_entry=Entry(ScreenLogIn,textvariable=oldpass,show="*",width=50).pack()
    login_Button=Button(ScreenLogIn,text="Login",command=button_login).pack()


    

def button_login():#define the command of the login button
    global olduser
    user_verify=olduser.get()
    pass_verify=oldpass.get()
    #to verify the username and the password
    list_of_files=os.listdir()
    if user_verify in list_of_files:
        userfile=open(user_verify,"r")
        verify=userfile.read().splitlines()#we are veryfying the information inputed through the data base file created prior to the registry process
        if pass_verify in verify:
            messagebox.showinfo("Succes!", "Login success")
            ScreenLogIn.withdraw()
            RegiAndLogin.destroy()
            
            
        else:
            messagebox.showerror("Error!", "Password doesn't match!")
    else:
        messagebox.showerror("Error!", "User not found")
        
        

def registerAndLogin():#creating the "Welcome" interface

    global RegiAndLogin

    RegiAndLogin=Tk()
    RegiAndLogin.geometry("626x391")
    RegiAndLogin.title("Corona Virus Data Tracker")
    RegiAndLogin.resizable(0,0)
    RegiAndLogin.overrideredirect(True)

    canvas=Canvas(RegiAndLogin,height=626,width=391).pack(fill=BOTH)#this allows us to create a canvas for a background image
    image=ImageTk.PhotoImage(file='application background.jpg')
    background_label=ttk.Label(image=image)
    background_label.image=image
    background_label.place(x=0,y=0,relwidth=1,relheight=1)



    regi_button=Button(RegiAndLogin,text="Register",command=register)
    login_button=Button(RegiAndLogin,text="Login",command=login)
    welcome_label=ttk.Label(RegiAndLogin,text="Welcome to the Corona Virus Data Tracker!",anchor=CENTER)
    login_label=ttk.Label(RegiAndLogin,text='Login if you have an account:',anchor=CENTER)
    Register_label=ttk.Label(RegiAndLogin,text="Don't have an account Register:",anchor=CENTER)


    welcome_label.place(x=100,y=10,width=400)
    login_label.place(x=180,y=100,width =200)
    Register_label.place(x=180,y=180,width=200)
    regi_button.place(x=240,y=220,width=100)
    login_button.place(x=240,y=140,width=100)


    RegiAndLogin.mainloop()





def get_country_name_list(): #this function returns a list with all the country names gathered from the API to be used for the combobox later
    country_dict=get_countries()
    country_list=[]
    for i in country_dict.keys():
        country_list.append(i)
    return country_list
    

def country_selector(evt): #this function allows an action to trigger in the events of someone clicking an item in the combobox
    country_dict=get_countries()
    country_code.set(country_dict[country_box.get()])
    print_data(get_data(country_code.get()))
    

def print_data(country_data):#displays the country data in form of labels
    global country_result_LBL,widget
    widget=[]
    for i in country_data.keys():
            country_result_LBL=ttk.Label(main_window,text=(' ').join(i.split('_'))+' : '+str(country_data[i]),background='white',width=25)
            widget.append(country_result_LBL)
            gridding_results()
            
    country_box['state']='disabled'

def gridding_results():#this function is gridding the labels created by the function print_data
    global widget
    for i in range(len(widget)):
        country_result_LBL.place(x=400,y=(i+4)*20)

        


def clear():# this function will clear the displayed data in order for it to be replaced when the function print_data is called again
    global widget
    for i in widget:
        i.destroy()
    country_box['state']='readonly'
    

def tick(): #this function helps refresh the clock every 200 ticks( every second)
    global time
    current_time=time.strftime('%H:%M:%S')#local time from pc
    if current_time != time:#update time if it changes
        time1 = current_time
        clock.config(text=current_time)
    clock.after(200, tick)#refreshes after 200 ticks
    

def Share(): #creating the interface that will allow the user to share the data that he/she requested
    global email,password,receiver,Subject,message,share_window
    
    share_window=Toplevel(main_window)
    share_window.geometry('626x391')
    share_window.title('Sharing')

    email=StringVar()
    password=StringVar()
    receiver=StringVar()
    Subject=StringVar()
    message=StringVar()

    

    from_Label=ttk.Label(share_window,text='Sender email').pack()
    from_Entry=ttk.Entry(share_window,textvariable=email,width=50).pack()
    
    pass_Label=ttk.Label(share_window,text='Password').pack()
    pass_Entry=ttk.Entry(share_window,textvariable=password,show="*",width=50).pack()

    To_Label=ttk.Label(share_window,text='Recipient email').pack()
    To_Entry=ttk.Entry(share_window,textvariable=receiver,width=50).pack()

    Sub_Label=ttk.Label(share_window,text='Subject').pack()
    subject_Entry=ttk.Entry(share_window,textvariable=Subject,width=50).pack()

    Msg_Label=ttk.Label(share_window,text='Message').pack()
    message_Entry=ttk.Entry(share_window,textvariable=message,width=100).pack(ipady=50)


    
    
    Send_button=ttk.Button(share_window,command=mail,text='send').pack()



    if country_name.get()=='' or country_name.get()=='World':
        Subject.set('Global Corona Statistics')
    else:
        Subject.set('Corona Statistics for '+country_name.get())
        
    

    data=get_data(country_code.get())
    
    message.set('Here are the statistics of covid-19 recorded on '+str(date.strftime('%A'))+' '+str(date.strftime('%B'))+' '+str(date.strftime('%d'))+' '+str(date.strftime('%Y'))+' in '+country_name.get()+' at '+str(time.strftime('%H:%M:%S'))+':\n'+print_(get_data(country_code.get())))

def mail(): # this function is responsible of sending an email via the messaging server (gmail only)
    email_user=email.get()
    password_user=password.get()
    send_to=receiver.get()
    subject = Subject.get()
    message_content= message.get()

    msg=MT1()
    msg['From']=email_user
    msg['To']=send_to
    msg['Subject']=subject

    msg.attach(MT(message_content, 'plain'))

    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_user,password_user)
    text=msg.as_string()
    server.sendmail(email_user, send_to,text)
    server.quit()

    messagebox.showinfo('Succes!','The data you requested was sent succesfully')
    share_window.withdraw()

        
        


def plot():
    plt.bar(x,y,color='red')
    plt.title('Requested chart for '+country_name.get(),fontsize=16)
    plt.ylabel('Values',fontsize=14)
    plt.xlabel('Critieria',fontsize=14)
    plt.show()
    
    



x=[]
y=[]
def createaxis0():
        temp=stat0.get()
        x.append(temp)
        y.append(data[temp])
        stat0_check_button['state']=DISABLED
def createaxis1():
        temp=stat1.get()
        x.append(temp)
        y.append(data[temp])
        stat1_check_button.config(state=DISABLED)
def createaxis2():
        temp=stat2.get()
        x.append(temp)
        y.append(data[temp])
        stat2_check_button.config(state=DISABLED)

def createaxis3():
        temp=stat3.get()
        x.append(temp)
        y.append(data[temp])
        stat3_check_button.config(state=DISABLED)
def createaxis4():
        temp=stat4.get()
        x.append(temp)
        y.append(data[temp])
        stat4_check_button.config(state=DISABLED)

def createaxis5():
        temp=stat5.get()
        x.append(temp)
        y.append(data[temp])
        stat5_check_button.config(state=DISABLED)
def createaxis6():
        temp=stat6.get()
        x.append(temp)
        y.append(data[temp])
        stat6_check_button.config(state=DISABLED)
def createaxis7():
        temp=stat7.get()
        x.append(temp)
        y.append(data[temp])
        stat7_check_button.config(state=DISABLED)
def clearaxis():
    global x,y
    x=[]
    y=[]
    stat0.set('')
    stat1.set('')
    stat2.set('')
    stat3.set('')
    stat4.set('')
    stat5.set('')
    stat6.set('')
    stat7.set('')
    
    stat0_check_button.config(state=NORMAL)
    stat1_check_button.config(state=NORMAL)
    stat2_check_button.config(state=NORMAL)
    stat3_check_button.config(state=NORMAL)
    stat4_check_button.config(state=NORMAL)
    stat5_check_button.config(state=NORMAL)
    stat6_check_button.config(state=NORMAL)
    stat7_check_button.config(state=NORMAL)
    if country_name.get()=='World' or country_name.get()=="":
        stat7_check_button.config(state=DISABLED) 


    

        
def Analyse():

    global stat0,stat1,stat2,stat3,stat4,stat5,stat6,stat7,data,analyse_window
    global stat0_check_button,stat1_check_button,stat2_check_button,stat3_check_button,stat4_check_button,stat5_check_button,stat6_check_button,stat7_check_button
    data=get_data(country_code.get())
    analyse_window=Toplevel(main_window)
    
    stat0=StringVar()
    stat1=StringVar()
    stat2=StringVar()
    stat3=StringVar()
    stat4=StringVar()
    stat5=StringVar()
    stat6=StringVar()
    stat7=StringVar()
    

   
    stat0_check_button=ttk.Checkbutton(analyse_window,text='total cases',onvalue='total_cases',variable=stat0,command=createaxis0)
    stat0_check_button.grid()
    stat1_check_button=ttk.Checkbutton(analyse_window,text='total recovered',onvalue='total_recovered',variable=stat1,command=createaxis1)
    stat1_check_button.grid()
    stat2_check_button=ttk.Checkbutton(analyse_window,text='total unresolved',onvalue='total_unresolved',variable=stat2,command=createaxis2)
    stat2_check_button.grid()
    stat3_check_button=ttk.Checkbutton(analyse_window,text='total deaths',onvalue='total_deaths',variable=stat3,command=createaxis3)
    stat3_check_button.grid()
    stat4_check_button=ttk.Checkbutton(analyse_window,text='total new cases today',onvalue='total_new_cases_today',variable=stat4,command=createaxis4)
    stat4_check_button.grid()
    stat5_check_button=ttk.Checkbutton(analyse_window,text='total active cases',onvalue='total_active_cases',variable=stat5,command=createaxis5)
    stat5_check_button.grid()
    stat6_check_button=ttk.Checkbutton(analyse_window,text='total serious cases',onvalue='total_serious_cases',variable=stat6,command=createaxis6)
    stat6_check_button.grid()
    stat7_check_button=ttk.Checkbutton(analyse_window,text='total danger rank',onvalue='total_danger_rank',variable=stat7,command=createaxis7)
    stat7_check_button.grid()

    if country_name.get()=='World' or country_name.get()=="":
        stat7_check_button.config(state=DISABLED)      
        
         

    plot_button=ttk.Button(analyse_window,text='Plot',command=plot).grid()
    clearBTN=ttk.Button(analyse_window,text='clear',command=clearaxis).grid()
            
    
    
        
        
    


    
    


        
######################################MAIN INTERFACE##################################################:


def datapage():#creating the GUI that will display the data requested
    global country_box,country_code,country_name,country_results,main_window,result_frame,clock,date,calendar
    
    
    
    
    main_window=Tk()
    main_window.geometry('626x391')
    main_window.title('Corona Virus Data Tracker')
    main_window.resizable(0,0)
    canvas=Canvas(main_window,height=626,width=391)
    image=ImageTk.PhotoImage(file='application background title.jpg')
    background_label=ttk.Label(image=image)
    background_label.image=image
    background_label.place(x=0,y=0,relwidth=1,relheight=1)

    clear_button=ttk.Button(text='Clear',command=clear,width=24)
    

    country_list=get_country_name_list()
    country_list.sort()

    country_code=StringVar()
    country_name=StringVar()
    
    
    
    country_name_LBL=ttk.Label(main_window,text='Country Name',background='white',width=20,anchor=CENTER)
    country_code_LBL=ttk.Label(main_window,text='Country Code',background='white',width=20,anchor=CENTER)
    country__code_Show_LBL=ttk.Label(main_window,background='white',textvariable=country_code)
    


    country_box=ttk.Combobox(main_window,textvariable=country_name,values=country_list,state='readonly')
    country_box.bind('<<ComboboxSelected>>',country_selector)
   
    clear_button.place(x=400,y=300)
    country_box.place(x=130,y=149)
    country_name_LBL.place(x=0,y=150)
    country_code_LBL.place(x=0,y=200)
    country__code_Show_LBL.place(x=200,y=201)



#create a clock and a calendar:
    time=''
    clock=ttk.Label(main_window,background='white')
    clock.place(x=230,y=100)
    tick()

    date=datetime.datetime.now()
    calendar=ttk.Label(main_window,background='white',text=str(date.strftime('%A'))+' '+str(date.strftime('%B'))+' '+str(date.strftime('%d'))+' '+str(date.strftime('%Y')))
    calendar.place(x=100,y=100)


    button_share=ttk.Button(text='Share',command=Share,width=25)
    button_share.place(x=0,y=300)


    button_analyze=ttk.Button(text='Analyse',command=Analyse,width=27).place(x=200,y=300)
    
    
    main_window.mainloop()
    





##############################Main Program#################################################################################################################################################
registerAndLogin()
datapage()







