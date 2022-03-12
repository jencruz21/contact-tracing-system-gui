from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import sqlite3

window = Tk()
db = "contact_tracing_system.db"
school_logo = PhotoImage(file="school-logo.png")
window.geometry("1100x600")
window.title("Contact Tracing System")
window.resizable(False, False)
window.iconphoto(True, school_logo)
index = 0
x = IntVar()
entry_name = StringVar()
entry_address = StringVar()
entry_contact_no = StringVar()
entry_temp = StringVar()

# We are establishing a connection to the sqlite database
conn = sqlite3.connect(db)

# Creating a cursor object
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS person_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        whole_name TEXT DEFAULT "N/A",
        address TEXT DEFAULT "N/A",
        contact_no INTEGER DEFAULT "N/A",
        vaccination_status TEXT,
        date_visited TEXT,
        temperature TEXT)
""")

# Button Actions, Adds the user data to the table, Edits the data of the user, Deletes the user completely


# This is the callback function to add a person to the table
def add_person():
    current_date = datetime.datetime.today()
    formatted_date = datetime.datetime.strftime(current_date, "%m/%d/%Y")

    name = name_entry.get()
    address = address_entry.get()
    contact_no = str("0" + contact_no_entry.get())
    temperature = str(temperature_entry.get())

    global index
    index += 1

    if name != "" and address != "" and contact_no != "" and temperature != "":
        conn8 = sqlite3.connect(db)
        cursor8 = conn8.cursor()

        # This is where we check all the data to see if a specific person is registered or vaccinated so the data will not double
        is_registered = False
        cursor8.execute("SELECT * FROM person_data")
        result_set_check = cursor8.fetchall()
        length = len(result_set_check)

        for data in result_set_check:
            is_registered = True if data[1] == name and data[2] == address and data[3] == contact_no and data[4] == "Vaccinated" and data[6] == temperature else False

        conn8.commit()
        conn8.close()

        if is_registered:
            messagebox.showwarning(title="Registered and Vaccinated", message="This person is registered and vaccinated")
        else:
            if x.get() == 1:
                data_table.insert(parent="", index="end", text=index,
                                  values=(
                                  length + 1, name, address, contact_no, "Vaccinated", formatted_date, temperature))

                # We are establishing a connection to the sqlite database
                conn1 = sqlite3.connect(db)

                # Creating a cursor object
                cursor1 = conn1.cursor()

                # this is where we add the person data in the database
                cursor1.execute(
                    "INSERT INTO person_data (whole_name, address, contact_no, vaccination_status, date_visited, temperature) VALUES(?, ?, ?, ?, ?, ?)",
                    (name, address, contact_no, "Vaccinated", formatted_date, temperature))

                # committing the changes and closing the connection
                conn1.commit()
                conn1.close()

                name_entry.delete(0, END)
                address_entry.delete(0, END)
                contact_no_entry.delete(0, END)
                temperature_entry.delete(0, END)
            else :
                data_table.insert(parent="", index="end", text=index,
                                  values=(
                                  length + 1, name, address, contact_no, "Not Vaccinated", formatted_date, temperature))

                # We are establishing a connection to the sqlite database
                conn2 = sqlite3.connect(db)

                # Creating a cursor object
                cursor2 = conn2.cursor()

                # this is where we add the person in the database
                cursor2.execute(
                    "INSERT INTO person_data (whole_name, address, contact_no, vaccination_status, date_visited, temperature) VALUES(?, ?, ?, ?, ?, ?)",
                    (name, address, contact_no, "Not Vaccinated", formatted_date, temperature))

                # committing the changes and closing the connection
                conn2.commit()
                conn2.close()

                name_entry.delete(0, END)
                address_entry.delete(0, END)
                contact_no_entry.delete(0, END)
                temperature_entry.delete(0, END)
    else:
        messagebox.showerror(title="Error", message="Please enter the necessary credentials")


# Edits the selected person in the table and also updates the selected id in the database
def edit_person():
    current_date = datetime.datetime.today()
    formatted_date = datetime.datetime.strftime(current_date, "%m/%d/%Y")
    current_item = data_table.selection()[0]

    uid = data_table.item(current_item)["values"][0]
    name = name_entry.get()
    address = address_entry.get()
    contact_no = str(contact_no_entry.get())
    temperature = str(temperature_entry.get())

    if name != "" and address != "" and contact_no != "" and temperature != "":
        if x.get() == 1:
            conn3 = sqlite3.connect(db)

            cursor3 = conn3.cursor()

            data_table.set(current_item, "#1", uid)
            data_table.set(current_item, "#2", name)
            data_table.set(current_item, "#3", address)
            data_table.set(current_item, "#4", contact_no)
            data_table.set(current_item, "#5", "Vaccinated")
            data_table.set(current_item, "#6", formatted_date)
            data_table.set(current_item, "#7", temperature)

            # This is where we update the data in the database
            cursor3.execute("""
                UPDATE person_data 
                SET whole_name = ?,
                    address = ?,
                    contact_no = ?,
                    vaccination_status = ?,
                    date_visited = ?,
                    temperature = ?
                WHERE id = ?
            """, (name, address, contact_no, "Vaccinated", formatted_date, temperature, uid))

            name_entry.delete(0, END)
            address_entry.delete(0, END)
            contact_no_entry.delete(0, END)
            temperature_entry.delete(0, END)

            # committing the changes and closing the connection5
            conn3.commit()
            conn3.close()

        else:
            conn4 = sqlite3.connect(db)
            cursor4 = conn4.cursor()

            data_table.set(current_item, "#1", uid)
            data_table.set(current_item, "#2", name)
            data_table.set(current_item, "#3", address)
            data_table.set(current_item, "#4", contact_no)
            data_table.set(current_item, "#5", "Not Vaccinated")
            data_table.set(current_item, "#6", formatted_date)
            data_table.set(current_item, "#7", temperature)

            # This is where we update the data in the database
            cursor4.execute("""
                       UPDATE person_data 
                       SET whole_name = ?,
                           address = ?,
                           contact_no = ?,
                           vaccination_status = ?,
                           date_visited = ?,
                           temperature = ?
                       WHERE id = ?
                   """, (name, address, contact_no, "Not Vaccinated", formatted_date, temperature, uid))

            name_entry.delete(0, END)
            address_entry.delete(0, END)
            contact_no_entry.delete(0, END)
            temperature_entry.delete(0, END)

            # committing the changes and closing the connection
            conn4.commit()
            conn4.close()
    else:
        messagebox.showerror(title="Error", message="Please enter the necessary credentials")


# Deletes the selected person in the table and deletes the selected person id in the database
def delete_person():
    conn5 = sqlite3.connect(db)
    cursor5 = conn5.cursor()

    deleted_item = data_table.selection()[0]

    uid = data_table.item(deleted_item)["values"][0]

    # this is where we delete the specific person id in the database
    cursor5.execute("DELETE FROM person_data WHERE id = ?", (uid,))

    data_table.delete(deleted_item)

    # committing the changes and closing the connection
    conn5.commit()
    conn5.close()


# End of Button Actions

# Select the item the tree view
# Don't mind this Chaos Engineering Abomination over here this was supposed to put the current data in the table to the text boxes(for aesthetic purposes)
# This is an ongoing bug nothing destructive here. The selected data just won't appear in the text boxes probably the library bug just move on
def selected_item(event):
    curt_item = data_table.selection()[0]
    tree_item = data_table.item(curt_item)
    print(tree_item)

    person_name = tree_item['values'][1]
    person_address = tree_item['values'][2]
    person_contact_no = "0" + str(tree_item['values'][3])
    person_temperature = tree_item['values'][6]

    entry_name.set(person_name)
    entry_address.set(person_address)
    entry_contact_no.set(person_contact_no)
    entry_temp.set(person_temperature)


# Shows and filter vaccinated people in the new vaccinated table
def show_vaccinated():
    vaccinated_window = Tk()
    vaccinated_window.title("Vaccinated")
    vaccinated_window.geometry("630x600")
    vaccinated_window.resizable(False, False)

    vaccinated_table = ttk.Treeview(vaccinated_window, height=600)

    vaccinated_table["columns"] = ("Name", "Address", "Contact No.", "Vaccination Status", "Date Visited", "Temp")
    vaccinated_table.column("#0", width=0, minwidth=0)
    vaccinated_table.column("Name", anchor=W, width=120, minwidth=120)
    vaccinated_table.column("Address", anchor=W, width=120, minwidth=120)
    vaccinated_table.column("Contact No.", anchor=W, width=110, minwidth=110)
    vaccinated_table.column("Vaccination Status", anchor=W, width=120, minwidth=120)
    vaccinated_table.column("Date Visited", anchor=W, width=110, minwidth=60)
    vaccinated_table.column("Temp", anchor=W, width=50, minwidth=35)

    vaccinated_table.heading("Name", text="Name", anchor=W)
    vaccinated_table.heading("Address", text="Address", anchor=W)
    vaccinated_table.heading("Contact No.", text="Contact No.", anchor=W)
    vaccinated_table.heading("Vaccination Status", text="Vaccination Status", anchor=W)
    vaccinated_table.heading("Date Visited", text="Date Visited", anchor=W)
    vaccinated_table.heading("Temp", text="Temp.", anchor=W)

    vaccinated_table.pack()

    conn6 = sqlite3.connect(db)
    cursor6 = conn6.cursor()

    # Getting all data also filtering the data where all people are vaccinated
    cursor6.execute("""
            SELECT * FROM person_data
            WHERE vaccination_status = "Vaccinated"
        """)

    result_set3 = cursor6.fetchall()
    for data in result_set3:
        vaccinated_table.insert(parent="", index="end", iid=data[0], values=(data[1], data[2], data[3], data[4], data[5], data[6]))

    # committing the changes and closing the connection
    conn6.commit()
    conn6.close()


# Shows and filter not vaccinated people in the not vaccinated table
def show_not_vaccinated():
    not_vaccinated_window = Tk()
    not_vaccinated_window.title("Not Vaccinated")
    not_vaccinated_window.geometry("630x600")
    not_vaccinated_window.resizable(False, False)

    not_vaccinated_table = ttk.Treeview(not_vaccinated_window, height=600)

    not_vaccinated_table["columns"] = ("Name", "Address", "Contact No.", "Vaccination Status", "Date Visited", "Temp")
    not_vaccinated_table.column("#0", width=0, minwidth=0)
    not_vaccinated_table.column("Name", anchor=W, width=120, minwidth=120)
    not_vaccinated_table.column("Address", anchor=W, width=120, minwidth=120)
    not_vaccinated_table.column("Contact No.", anchor=W, width=110, minwidth=110)
    not_vaccinated_table.column("Vaccination Status", anchor=W, width=120, minwidth=120)
    not_vaccinated_table.column("Date Visited", anchor=W, width=110, minwidth=60)
    not_vaccinated_table.column("Temp", anchor=W, width=50, minwidth=35)

    not_vaccinated_table.heading("Name", text="Name", anchor=W)
    not_vaccinated_table.heading("Address", text="Address", anchor=W)
    not_vaccinated_table.heading("Contact No.", text="Contact No.", anchor=W)
    not_vaccinated_table.heading("Vaccination Status", text="Vaccination Status", anchor=W)
    not_vaccinated_table.heading("Date Visited", text="Date Visited", anchor=W)
    not_vaccinated_table.heading("Temp", text="Temp.", anchor=W)

    not_vaccinated_table.pack()

    conn7 = sqlite3.connect(db)
    cursor7 = conn7.cursor()

    # This is where we fetch all data and filter the not vaccinated people
    cursor7.execute("""
        SELECT * FROM person_data
        WHERE vaccination_status = "Not Vaccinated"
    """)

    result_set3 = cursor7.fetchall()
    for data in result_set3:
        not_vaccinated_table.insert(parent="", index="end", iid=data[0], values=(data[1], data[2], data[3], data[4], data[5], data[6]))

    # committing the changes and closing the connection
    conn7.commit()
    conn7.close()


# public class Main {
#
#     public static void main(String[] args) {
#         System.out.println("Displays the group number and the names of the members");
#     }
# }
def group_one():
    messagebox.showinfo(title="Members", message="Alfredo Sedol Jr.,\nJethro Aurelio,\nRichmond John Genabe(Pogi)")

# Widgets
# This is the components of the application eg. Buttons, Labels, Entry, etc.


# Logos
add_logo = PhotoImage(file="add.png")
add_logo = add_logo.subsample(10, 10)

delete_logo = PhotoImage(file="delete.png")
delete_logo = delete_logo.subsample(10, 10)

edit_logo = PhotoImage(file="change.png")
edit_logo = edit_logo.subsample(10, 10)

# Frame for the buttons and the tree view
frame1 = Frame(window, width=675, height=600)
frame2 = Frame(window, width=425, height=600)

frame1.place(x=0, y=0)
frame2.place(x=685, y=0)

# TreeView Widget this is where we display all data
data_table = ttk.Treeview(frame1, height=600)

data_table["columns"] = ("ID", "Name", "Address", "Contact No.", "Vaccination Status", "Date Visited", "Temp")
data_table.column("#0", width=0, minwidth=0)
data_table.column("ID", anchor=CENTER, width=45, minwidth=35)
data_table.column("Name", anchor=W, width=120, minwidth=120)
data_table.column("Address", anchor=W, width=120, minwidth=120)
data_table.column("Contact No.", anchor=W, width=110, minwidth=110)
data_table.column("Vaccination Status", anchor=W, width=120, minwidth=120)
data_table.column("Date Visited", anchor=W, width=110, minwidth=60)
data_table.column("Temp", anchor=W, width=50, minwidth=35)

data_table.heading("ID", text="ID", anchor=W)
data_table.heading("Name", text="Name", anchor=W)
data_table.heading("Address", text="Address", anchor=W)
data_table.heading("Contact No.", text="Contact No.", anchor=W)
data_table.heading("Vaccination Status", text="Vaccination Status", anchor=W)
data_table.heading("Date Visited", text="Date Visited", anchor=W)
data_table.heading("Temp", text="Temp.", anchor=W)

# Fetching all the data from the database
cursor.execute("SELECT * FROM person_data")
result_set = cursor.fetchall()
for data in result_set:
    data_table.insert(parent="", index="end", iid=data[0], values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
data_table.pack(side=LEFT)

# ENTRIES
name_entry = Entry(frame2, font=("Comic Sans", 12), textvariable=entry_name)
address_entry = Entry(frame2, font=("Comic Sans", 12), textvariable=entry_address)
contact_no_entry = Entry(frame2, font=("Comic Sans", 12), textvariable=entry_contact_no)
temperature_entry = Entry(frame2, font=("Comic Sans", 12), textvariable=entry_temp)
vaccinated_entry = Checkbutton(frame2, text="Vaccinated", onvalue=1, offvalue=0, variable=x)

name_entry.place(x=150, y=300)
address_entry.place(x=150, y=330)
contact_no_entry.place(x=150, y=360)
temperature_entry.place(x=150, y=390)
vaccinated_entry.place(x=150, y=420)

# LABELS
name_label = Label(frame2, text="Name: ", font=("Comic Sans", 12, "bold"))
address_label = Label(frame2, text="Address: ", font=("Comic Sans", 12, "bold"))
contact_no_label = Label(frame2, text="Contact no.: ", font=("Comic Sans", 12, "bold"))
temperature_label = Label(frame2, text="Temperature: ", font=("Comic Sans", 12, "bold"))
vaccination = Label(frame2, text="V. Status: ", font=("Comic Sans", 12, "bold"))

name_label.place(x=30, y=300)
address_label.place(x=30, y=330)
contact_no_label.place(x=30, y=360)
temperature_label.place(x=30, y=390)
vaccination.place(x=30, y=420)

# Add Button
addButton = Button(frame2,
                   text="Add Person",
                   command=add_person,
                   image=add_logo,
                   activebackground="white smoke",
                   compound="left")

# Edit Button
editButton = Button(frame2,
                    text="Edit Person",
                    command=edit_person,
                    image=edit_logo,
                    activebackground="white smoke",
                    compound="left")

# Delete Button
deleteButton = Button(frame2,
                      text="Delete Person",
                      command=delete_person,
                      image=delete_logo,
                      activebackground="white smoke",
                      compound="left")

# vaccinated button
vaccinated_button = Button(frame2,
                           text="Show Vaccinated",
                           command=show_vaccinated,
                           activebackground="white smoke")

# not vaccinated button
not_vaccinated_button = Button(frame2,
                               text="Show Not Vaccinated",
                               command=show_not_vaccinated,
                               activebackground="white smoke")

# group_one_button
group_one_btn = Button(frame2,
                       text="Group 1",
                       command=group_one)


addButton.place(x=40, y=550)
editButton.place(x=135, y=550)
deleteButton.place(x=230, y=550)
vaccinated_button.place(x=40, y=510)
not_vaccinated_button.place(x=145, y=510)
group_one_btn.place(x=273, y=510)

# School logo
school_logo_label = Label(frame2,
                          text="Contact Tracing System",
                          font=("Comic Sans", 0, "bold"),
                          image=school_logo,
                          compound="top")

school_logo_label.place(x=70, y=0)
# End of widgets

# Committing all the changes that happened in the databases
conn.commit()

# Closing the connection of the database == Tapos na ang changes at para maiwasan ang memory leaks
conn.close()

window.mainloop()
