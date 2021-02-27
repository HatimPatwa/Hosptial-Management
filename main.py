from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from threading import Thread
from time import sleep
import random

root = Tk()  # making root window
root.geometry("700x320")
root.maxsize(width=700, height=400)
root.minsize(width=550, height=370)
root.iconbitmap("photos/hospital.ico")
root.title("RED CROSS HOSPITAL")

# Variables
mysql_connection = False


# connection with mysql


# miscellaneous defs


def new_win():
    new = Toplevel(root)
    new.geometry("250x280")
    new.iconbitmap("photos/hospital.ico")

    lbl_Fname = ttk.Label(new, text=" FIRST NAME : ")
    lbl_Fname.grid(row=0, column=0, pady=20, padx=10)

    en_Fname = ttk.Entry(new)
    en_Fname.grid(row=0, column=1)

    lbl_Lname = ttk.Label(new, text=" LAST NAME : ")
    lbl_Lname.grid(row=1, column=0, pady=20, padx=10)

    en_Lname = ttk.Entry(new)
    en_Lname.grid(row=1, column=1)

    lbl_Room = ttk.Label(new, text="Room Alotted : ")
    lbl_Room.grid(row=2, column=0, padx=10)

    options = [
        "Casualty",
        "Day Room",
        "Emergency Room",
        "High Dependency unit",
        "ICU",
        "Delivery Room",
        "Operation Theatre",
        "Ward",
        "Nursery Room",
    ]

    variable = StringVar(root)
    variable.set(options[0])

    opt_box = ttk.OptionMenu(new, variable, *options)
    opt_box.grid(row=2, column=1)

    bed_no = Label(new, text=" Bed no. : ")
    bed_no.grid(row=3, column=0, pady=20)

    en_bed = Entry(new)
    en_bed.grid(row=3, column=1)

    status_bar_2 = Label(
        new, text="...", relief=GROOVE, anchor=W, font="comicsansMS 8 italic", bd=0
    )
    status_bar_2.grid(row=5, column=0, columnspan=2, sticky=W)

    btn_submit = ttk.Button(
        new, text="Submit", command=lambda: submit(en_Fname, en_Lname, en_bed, variable, new)
    )
    btn_submit.grid(row=4, column=0, columnspan=2, pady=10)

    return en_Fname, en_Lname, en_bed, variable,


def about_us():
    messagebox._show("Red Cross Hospital", "Hey welcome to Hospital Management System"
                                           "\n Copyright © 2021 Hatim Studios, Inc.")


def submit(
        en_Fname,
        en_Lname,
        en_bed,
        variable,
        new
):
    try:
        Fname = en_Fname.get().strip()
        Lname = en_Lname.get().strip()
        bed = en_bed.get()
        bed = int(bed)
        room = variable.get()
        print(Fname, type(Fname))
        print(Lname, type(Lname))
        print(bed, type(bed))
        print(room, type(room))

        query1 = "INSERT INTO `hatim_data`.`hospital_pt` (`F_name`, `L_name`, `Room`, `Bed_no`) VALUES (%s,%s,%s,%s);"

        mycursor.execute(query1, (Fname, Lname, room, bed))

        if messagebox.askyesno("hospital management", "confirm insertion of data"):
            mydb.commit()
            new.destroy()
    except ValueError as error:
        messagebox.showerror("Error", "Invalid entry !! possible cause : string used instead of int")


def search(entry_sch):
    list_box.delete(0, 10)
    name = entry_sch.get().strip()
    if " " in name:
        name = name.split()
    else:
        name = [name, " "]
    print(name)
    entry_sch.delete(0, END)
    squery = "select * from hospital_pt where F_name = '{}' || L_name = '{}' ;".format(name[0], name[1])
    mycursor.execute(squery)
    row = 0
    for x in range(10):
        try:
            a = mycursor.fetchone()
            row += 1
            data = "{}|      Patient's name = {} {}           Room = {}    BED Alotted = {} ".format(row, a[1], a[2],
                                                                                                     a[3],
                                                                                                     a[4])
            print(data)
            list_box.insert(x, data)
        except TypeError:
            row -= 1
            break
    print(row)
    if row == 0:
        list_box.insert(0, "NO patients found")
    lbl_resuts_no["text"] = "Results ={}".format(row)


def discharge():
    select = list_box.curselection()
    value = list_box.get(select)
    value = value[25:50]
    print(value)
    value = value.split()
    print(value)
    if messagebox.askyesno("hospital management",
                           "confirm discharge of {} {} \n This can't be undone !!".format(value[0], value[1])):
        query = "DELETE from hospital_pt where F_name = '{}' and L_name = '{}';".format(value[0], value[1])
        mycursor.execute(query)

        list_box.delete(select)
    mydb.commit()


def close():  # properly closes the root window
    mydb.commit()
    mydb.close()
    prog_bar.destroy()
    root.destroy()


def new_win_ambu():  # new window for destination entry
    new = Toplevel(root)
    new.geometry("350x100")
    new.iconbitmap("photos/hospital.ico")

    lbl_dest = ttk.Label(new, text="Enter destination")
    lbl_dest.grid(row=0, column=0, padx=10, pady=10)

    entry_dest = ttk.Entry(new, width=30)
    entry_dest.grid(row=0, column=1)

    btn_dest = ttk.Button(new, text="dispatch", width=15, command=lambda: t(new))
    btn_dest.grid(row=1, column=1, sticky=W)


def progress():
    prog_bar.stop()
    time_taken = random.randint(1, 5)
    print(time_taken)
    time_left = 100 / time_taken
    time_left = time_left.__round__(2)
    time_left = int(time_left)
    lbl_time_left['text'] = "Ambulance will reach it's destination in {} Mins".format(time_left)
    while prog_bar['value'] <= 100:
        prog_bar['value'] += time_taken
        root.update_idletasks()
        sleep(1)
    lbl_time_left['text'] = "The ambulance has reached its Destination"


def t(new):
    t1 = Thread(target=progress)
    new.destroy()
    t1.start()


# Defs End

status_bar = Label(
    root,
    text="WELCOME to Hotel Management section",
    relief=GROOVE,
    anchor=W,
    font="comicsansMS 8 italic",
)
status_bar.pack(side=BOTTOM, fill=X)

# menu
menubar = Menu(root)
root.config(menu=menubar)

# submenu
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Commands", menu=submenu)
submenu.add_command(label="ADD     ctrl+a", command=new_win)
submenu.add_command(label="exit", command=close)

# submenu 2
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="about us", command=about_us)

# Frames

left_frame = Frame(root)
left_frame.pack(anchor=N)

right_frame = Frame(root)
right_frame.pack()

# Label 1

btn_add = ttk.Button(left_frame, text="ADD NEW ENTRY", command=new_win, state=ACTIVE, cursor="plus")
btn_add.grid(row=0, column=1, pady=10)

entry_sch = ttk.Entry(left_frame)
entry_sch.insert(0, "enter patient's name ")
entry_sch.grid(row=0, column=2)

btn_sch = ttk.Button(left_frame, text="search", command=lambda: search(entry_sch), width=20)
btn_sch.grid(row=0, column=3)

lbl_resuts = ttk.Label(left_frame, text="DATA")
lbl_resuts.grid(row=2, column=0, sticky=W, padx=20)

lbl_resuts_no = ttk.Label(left_frame, text="Results = ")
lbl_resuts_no.grid(row=2, column=4)

list_box = Listbox(left_frame, width=110)
list_box.grid(row=3, column=0, pady=10, padx=10, columnspan=5)

btn_discharge = ttk.Button(left_frame, text="Discharge patient", width=20, command=discharge)
btn_discharge.grid(row=4, column=4, pady=5)

prog_bar = ttk.Progressbar(left_frame, value=0, length=300, mode="determinate", maximum=100)
prog_bar.grid(row=5, column=1, columnspan=2)

btn_ambu = ttk.Button(left_frame, text="Emergency Ambulance", width=22, command=new_win_ambu)
btn_ambu.grid(row=5, column=4, pady=5)

lbl_time_left = ttk.Label(left_frame, text="")
lbl_time_left.grid(row=6, column=1, columnspan=2)

# mysql connection

try:
    if mysql_connection:
        status_bar["text"] = "Already connected!"
    else:

        status_bar["text"] = "connecting to database"
        mydb = mysql.connector.connect(
            host="db4free.net",
            user="host_root",
            passwd="hatim1603",
            database="hatim_data",
            port=3306
        )

        mycursor = mydb.cursor()
        mysql_connection = True
        status_bar["text"] = "Connection successful!!"

except Exception as ex:
    status_bar['text'] = "check your internet connection or service", ex


def cleartext(event):
    entry_sch.delete(0, END)


entry_sch.bind("<Button - 1>", cleartext)
# Bottom Frame


root.mainloop()
