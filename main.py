from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as thk
import mysql.connector
from time import sleep
from threading import Thread

root = Tk()
#root.get_themes()
#root.set_theme("radiance")
root.geometry("700x320")
root.maxsize(width=700, height=350)
root.minsize(width=550, height=300)
root.iconbitmap("")
root.title("RED CROSS HOSPITAL")

#Variables
mysql_connection = False

# connection with mysql


def mysql_connect():
    global mysql_connection
    if mysql_connection == True :
        status_bar['text'] = "Already connected!"
    else:
        btn_connect['state'] = DISABLED
        status_bar['text'] = "connecting to database"
        mydb = mysql.connector.connect(host="db4free.net",
                                        user="host_root",
                                        passwd="hatim1603",
                                        database="hatim_data")
                
        mycursor = mydb.cursor()
        mysql_connection = True
        status_bar['text'] = "Connection successful!!"
        btn_connect['state'] = ACTIVE

def t1start():
    t1 = Thread(target=mysql_connect)
    t1.start()


# miscellaneous defs

def new_win():
    new = Toplevel(root)
    new.geometry("250x260")

    lbl_Fname = Label(new,text = " FIRST NAME : ")
    lbl_Fname.grid(row = 0 , column = 0, pady = 20 , padx =10 )

    en_Fname  = Entry(new)
    en_Fname.grid(row = 0 , column = 1)

    lbl_Lname = Label(new,text = " LAST NAME : ")
    lbl_Lname.grid(row = 1 , column = 0, pady = 20 , padx =10 )

    en_Lname  = Entry(new)
    en_Lname.grid(row = 1 , column = 1)

    lbl_Room = Label(new, text = "Room Alotted : ")
    lbl_Room.grid(row = 2 , column = 0, padx = 10)

    options = [
        "Casualty" ,
        "Day Room" , 
        "Consulting Room" , 
        "Emergency Room" , 
        "High Dependency unit" ,
        "ICU",
        "Delivery Room",
        "Operation Theatre",
        "Ward",
        "Nursery Room"]

    variable = StringVar(root)
    variable.set(options[0])

    opt_box = OptionMenu(new,variable,*options)
    opt_box.grid(row = 2 , column = 1 )

    bed_no = Label(new, text = " Bed no. : ")
    bed_no.grid(row = 3 , column = 0 , pady = 20)

    en_bed = Entry(new)
    en_bed.grid(row = 3 , column = 1)

    btn_submit = Button(new, text = "Submit" , command = lambda: submit(en_Fname , en_Lname , en_bed , variable) )
    btn_submit.grid(row = 4 , column = 0 , columnspan = 2 , pady = 10)

    return en_Fname , en_Lname , en_bed , variable

def submit(en_Fname , en_Lname , en_bed , variable):
    Fname = en_Fname.get()
    Lname = en_Lname.get()
    bed = en_bed.get()
    bed = int(bed)
    room = variable.get()
    print(Fname,type(Fname))
    print(bed,type(bed))
    print(room,type(room))

    values  = [Fname , Lname , room,bed]
    query1 = "NSERT INTO `hatim_data`.`hospital_pt` (`F_name`, `L_name`, `Room`, `Bed_no`) VALUES ({}, {}, {},{});".format(values)

# Frames

left_frame = Frame(root)
left_frame.pack()

right_frame = Frame(root)
right_frame.pack()

top_frame = Frame(right_frame)
top_frame.pack()


# Label 1


btn_connect = Button(left_frame,text="Connect to database" , command = t1start)
btn_connect.grid(row = 0, column = 0 )

btn_add = Button(left_frame,text = "ADD NEW ENTRY",command = new_win, state = ACTIVE )
btn_add.grid(row = 1 , column = 0 , pady = 10 )







status_bar = ttk.Label(root, text="WELCOME to Hotel Management section", relief=GROOVE, anchor=W, font='comicsansMS 8 italic')
status_bar.pack(side = BOTTOM , fill = X )




#Bottom Frame









root.mainloop()
