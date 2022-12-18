from tkinter import *
import tkinter as tk
from tkinter import ttk
import csv
import pandas as pd
import mysql.connector
# from sqlalchemy import create_engine

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Gonzalez#1222",
    db="pharm_db")
cursor = mydb.cursor()

app = tk.Tk()
app.title('Test')
app.geometry('800x500')
app.resizable(0, 0)
font1 = ['Times', 14, 'normal']
textbox = tk.Text(app, height=2, width=60, bg="light grey", font=font1)
textbox.grid(row=0, column=0, padx=5, pady=10)
button1 = tk.Button(app, text='Search', font=18,
                    command=lambda: my_query(textbox.get('1.0', 'end')))
button1.grid(row=0, column=1)


def my_query(query):
    for w in app.grid_slaves(1):
        w.grid_forget()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        numberofFields = len(cursor.description)
        fieldNames = [i[0] for i in cursor.description]

    except:
        print("Error")
    else:  # No errors will display a TreeView
        trv = ttk.Treeview(app, selectmode='browse',
                           columns=fieldNames, show='headings', height=10)

        trv.place(relx=0.01, rely=0.128, width=640, height=410)

        for i in fieldNames:  # Listof columns collects from Database
            trv.column(i, width=200, stretch=True)
            trv.heading(i, text=i, anchor=W)

        row = 0
        for data in rows:  # adding records
            trv.insert('', 'end', iid=row, text=data[0], values=list(data))
            row += 1


app.mainloop()
