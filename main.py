from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Gonzalez#1222",
    db="pharm_db")
cursor = mydb.cursor()

app = tk.Tk()
app.title('Test')
app.geometry('800x700')
app.resizable(0, 0)

query_frame = Frame(app)
font1 = ['Times', 14, 'normal']
var1 = StringVar()
var1.set("Enter query: ")
label1 = tk.Label(app, textvariable=var1)
textbox = tk.Text(query_frame, height=2, width=60, bg="light grey", font=font1)
button1 = tk.Button(query_frame, text='Search', font=18, padx=25,
                    command=lambda: my_query(textbox.get('1.0', 'end')))
textbox.pack(side=LEFT)
button1.pack(side=LEFT, padx=10)

var2 = StringVar()
label2 = tk.Label(app, textvariable=var2)
var2.set("Enter Drug Name: ")
name_frame = Frame(app)
textbox2 = tk.Text(name_frame, height=1, width=30, bg="light grey", font=font1)
button2 = tk.Button(name_frame, text='Find', font=18, padx=25,
                    command=lambda: get_by_drug_name())

var3 = StringVar()
label3 = tk.Label(app, textvariable=var3)
var3.set("Search for Predicted Properties (Water Solubility, logP, logS, ect.):")
pro_frame1 = Frame(app, pady=10)
textbox3 = tk.Text(pro_frame1, height=1, width=30, bg="light grey", font=font1)
button3 = tk.Button(pro_frame1, text='Find', font=18, padx=25,
                    command=lambda: get_by_pred_prop())

var4 = StringVar()
label4 = tk.Label(app, textvariable=var4)
var4.set("Search for Experimental Properties (melting point, boiling point, pKa, ect.): ")
pro_frame2 = Frame(app)
textbox4 = tk.Text(pro_frame2, height=1, width=30, bg="light grey", font=font1)
button4 = tk.Button(pro_frame2, text='Find', font=18, padx=25,
                    command=lambda: get_by_ex_prop())

textbox2.pack(side=LEFT)
button2.pack(side=LEFT, padx=10)
label1.grid(row=0, column=0, sticky=W)
query_frame.grid(row=1, column=0)
label2.grid(row=2, column=0, sticky=W)
name_frame.grid(row=3,  column=0, sticky=W)

textbox3.pack(side=LEFT)
button3.pack(side=LEFT, padx=10)
label3.grid(row=4, column=0, sticky=W)
pro_frame1.grid(row=5, column=0, sticky=W)


textbox4.pack(side=LEFT)
button4.pack(side=LEFT, padx=10)
label4.grid(row=6, column=0, sticky=W)
pro_frame2.grid(row=7, column=0, sticky=W)


def my_query(query):
    for w in app.place_slaves():
        w.place_forget()

    if "Delete" in query or "Drop" in query:
        messagebox.showerror("Error", "Cannot drop or delete data")

    else:
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            no_result()
            print(cursor.rowcount)
            numberofFields = len(cursor.description)
            fieldNames = [i[0] for i in cursor.description]

        except:
            error_handle()
        else:  # No errors will display a TreeView
            trv = ttk.Treeview(app, selectmode='browse',
                               columns=fieldNames, show='headings', height=10)

            trv.place(relx=0.01, rely=0.380, width=640, height=410)

            for i in fieldNames:  # Listof columns collects from Database
                trv.column(i, width=200, stretch=True)
                trv.heading(i, text=i, anchor=W)

            row = 0
            for data in rows:  # adding records
                trv.insert('', 'end', iid=row, text=data[0], values=list(data))
                row += 1


def get_by_drug_name():
    for w in app.place_slaves():
        w.place_forget()
    try:
        inp = textbox2.get(1.0, "end")
        query = "Select * from DailymedDrug where drugName like \'%" + \
            str(inp.rstrip()) + "%\'"
        cursor.execute(query)
        rows = cursor.fetchall()
        no_result()
        numberofFields = len(cursor.description)
        fieldNames = [i[0] for i in cursor.description]
    except:
        error_handle()
    else:  # No errors will display a TreeView
        trv = ttk.Treeview(app, selectmode='browse',
                           columns=fieldNames, show='headings', height=10)

        trv.place(relx=0.01, rely=0.380, width=640, height=410)

        for i in fieldNames:  # Listof columns collects from Database
            trv.column(i, width=200, stretch=True)
            trv.heading(i, text=i, anchor=W)

        row = 0
        for data in rows:  # adding records
            trv.insert('', 'end', iid=row, text=data[0], values=list(data))
            row += 1


def get_by_pred_prop():
    for w in app.place_slaves():
        w.place_forget()
    try:
        inp = textbox3.get(1.0, "end")
        query = "Select d.drugName, p.predPropertyNo, p.propertyName, p.propertyValue from DailymedDrug as d Natural Join " + \
            "PredictedProperties as p where propertyName like \'%" + \
            str(inp.rstrip()) + "%\'"
        no_result()
        cursor.execute(query)
        rows = cursor.fetchall()
        # no_result()
        numberofFields = len(cursor.description)
        fieldNames = [i[0] for i in cursor.description]
    except:
        error_handle()
    else:  # No errors will display a TreeView
        trv = ttk.Treeview(app, selectmode='browse',
                           columns=fieldNames, show='headings', height=10)

        trv.place(relx=0.01, rely=0.380, width=640, height=410)

        for i in fieldNames:  # Listof columns collects from Database
            trv.column(i, width=200, stretch=True)
            trv.heading(i, text=i, anchor=W)

        row = 0
        for data in rows:  # adding records
            trv.insert('', 'end', iid=row, text=data[0], values=list(data))
            row += 1


def get_by_ex_prop():
    for w in app.place_slaves():
        w.place_forget()
    try:
        inp = textbox4.get(1.0, "end")
        query = "Select d.drugName, e.expPropertyNo, e.propertyName, e.propertyValue from DailymedDrug as d Natural Join " + \
            "ExperimentalProperties as e where propertyName like \'%" + \
            str(inp.rstrip()) + "%\'"
        cursor.execute(query)
        rows = cursor.fetchall()
        no_result()
        numberofFields = len(cursor.description)
        fieldNames = [i[0] for i in cursor.description]
    except:
        error_handle()
    else:  # No errors will display a TreeView
        trv = ttk.Treeview(app, selectmode='browse',
                           columns=fieldNames, show='headings', height=10)

        trv.place(relx=0.01, rely=0.380, width=640, height=410)

        for i in fieldNames:  # Listof columns collects from Database
            trv.column(i, width=200, stretch=True)
            trv.heading(i, text=i, anchor=W)

        row = 0
        for data in rows:  # adding records
            trv.insert('', 'end', iid=row, text=data[0], values=list(data))
            row += 1


def no_result():
    if cursor.rowcount <= 0:
        messagebox.showinfo("Information", "No results could be found.")


def error_handle():
    messagebox.showerror("Error", "Request could not be completed.")


app.mainloop()
