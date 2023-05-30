import mysql.connector
from datetime import datetime  # I had to import datetime to convert the string to date type in mysql
import tkinter as tk
from tkinter import messagebox

dataBase = mysql.connector.connect(
    host="localhost",

    user="root",

    passwd="1234"
)

cursorObject = dataBase.cursor()

cursorObject.execute("DROP DATABASE IF EXISTS Marvel")

cursorObject.execute("CREATE DATABASE IF NOT EXISTS Marvel")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    database="Marvel",
    passwd="1234"
)

cursorObject = connection.cursor()

table_Query = """
CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY NOT NULL,
    movie VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    mcu_phase LONGTEXT NOT NULL
)
"""

cursorObject.execute(table_Query)

with open('Marvel.txt', 'r') as file:
    for line in file:
        words = line.strip().split()
        id = int(words[0])
        movie = words[1]
        date = words[2]
        mcu_phase = words[3]
        if date == "War":  # There is a space on Infinity War, so I had to reassign the variables only for that movie
            movie = movie + "War"
            date = words[3]
            mcu_phase = words[4]
        date = datetime.strptime(date, "%B%d,%Y").date()
        insert_Query = """
                 INSERT INTO movies (id, movie, date, mcu_phase)
                 VALUES (%s, %s, %s, %s)
                 """
        cursorObject.execute(insert_Query, (id, movie, date, mcu_phase))

connection.commit()


def add_data():
    add_window = tk.Toplevel(movieGui)


    entry = tk.Entry(add_window)
    entry.pack()

    def ok_click():
        movie_data = entry.get()
        try:
            id, movie, date_str, mcu_phase = movie_data.split()
            date = datetime.strptime(date_str, "%B%d,%Y").date()

            insert_query = """
                INSERT INTO movies (id, movie, date, mcu_phase)
                VALUES (%s, %s, %s, %s)
            """
            cursorObject.execute(insert_query, (id, movie, date, mcu_phase))
            dataBase.commit()

            messagebox.showinfo("Success", "Data added successfully!")
            refresh_dropdown()
            text_box.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        add_window.destroy()

    def cancel_click():
        add_window.destroy()

    ok_button = tk.Button(add_window, text="Ok", command=ok_click)
    ok_button.pack(side=tk.LEFT)

    cancel_button = tk.Button(add_window, text="Cancel", command=cancel_click)
    cancel_button.pack(side=tk.RIGHT)


def refresh_dropdown():
    cursorObject.execute("SELECT id FROM movies")
    ids = cursorObject.fetchall()
    options = [str(id[0]) for id in ids]
    menu = dropdown["menu"]
    menu.delete(0, tk.END)
    selected_id.set("Select Movie ID")
    for option in options:
        menu.add_command(label=option, command=lambda value=option: show_selected_movie(value))

def list_all():
    selected_id.set("Select Movie ID")
    text_box.delete("1.0", tk.END)

    select_query = "SELECT * FROM movies"
    cursorObject.execute(select_query)
    rows = cursorObject.fetchall()

    for row in rows:
        text_box.insert(tk.END, f"ID: {row[0]}\n")
        text_box.insert(tk.END, f"Movie: {row[1]}\n")
        text_box.insert(tk.END, f"Date: {row[2]}\n")
        text_box.insert(tk.END, f"MCU Phase: {row[3]}\n")
        text_box.insert(tk.END, "-" * 20 + "\n")

def show_selected_movie(movieID):
    text_box.delete("1.0", tk.END)

    movieID = int(movieID)

    select_query = "SELECT * FROM movies WHERE id = %s"
    cursorObject.execute(select_query, (movieID,))
    rows = cursorObject.fetchall()

    for row in rows:
        text_box.insert(tk.END, f"ID: {row[0]}\n")
        text_box.insert(tk.END, f"Movie: {row[1]}\n")
        text_box.insert(tk.END, f"Date: {row[2]}\n")
        text_box.insert(tk.END, f"MCU Phase: {row[3]}\n")
        text_box.insert(tk.END, "-" * 20 + "\n")




movieGui = tk.Tk()
movieGui.title("MovieGUI")

mainFrame = tk.Frame(movieGui)
mainFrame.pack()

cursorObject.execute("SELECT id FROM movies")
ids = cursorObject.fetchall()
options = [str(id[0]) for id in ids]

selected_id = tk.StringVar()
selected_id.set("Select Movie ID")
dropdown = tk.OptionMenu(mainFrame, selected_id, *options, command=show_selected_movie)
dropdown.config(width=10)
dropdown.pack()


text_box = tk.Text(mainFrame, height=10, width=30)
text_box.pack()

add_button = tk.Button(mainFrame, text="Add", command=add_data)
add_button.pack(side=tk.LEFT)


list_all_button = tk.Button(mainFrame, text="List All", command=list_all)
list_all_button.pack(side=tk.RIGHT)



movieGui.mainloop()