#!/usr/bin/evn python3
# -*- coding: utf-8 -*-

""" task7 will focus on GUI interface"""

import tkinter as tk
from tkinter import *
from Task2 import t2
from Task3 import t3
from Task4 import t4
from Task5 import t5
import threading

button_row_number = 8

def countryButton():
    """function activates on button click, performs task 2a"""
    show_tb1.delete(0.0, END)
    #textfield input criteria check
    if not tb1.get():
        show_tb1.insert(END, "No filename entered\n")
    if not tb2.get():
        show_tb1.insert(END, "No doc ID entered\n")
    #perform task if input criteria have being met
    if tb1.get() and tb2.get():
        t2.country_input(tb2.get(), tb1.get())

def continentButton():
    """function activates on button click, performs task 2b"""
    show_tb1.delete(0.0, END)
    # textfield input criteria check
    if not tb1.get():
        show_tb1.insert(END, "No filename entered\n")
    if not tb2.get():
        show_tb1.insert(END, "No doc ID entered\n")
    # perform task if input criteria have being met
    if tb1.get() and tb2.get():
        t2.continent_input(tb2.get(), tb1.get())


def browserButton():
    """function activates on button click, performs task 3a"""
    show_tb1.delete(0.0, END)
    # textfield input criteria check
    if not tb1.get():
        show_tb1.insert(END, "No filename entered\n")
    # perform task if input criteria have being met
    else:
        t3.input_total_browser(tb1.get())


def mainBrowserButton():
    """function activates on button click, performs task 3b"""
    show_tb1.delete(0.0, END)
    # textfield input criteria check
    if not tb1.get():
        show_tb1.insert(END, "No filename entered\n")
    # perform task if input criteria have being met
    else:
        t3.input_browser(tb1.get())


def top10button():
    """function activates on button click, performs task 4 with new thread"""
    show_tb1.delete(0.0, END)
    # textfield input criteria check
    if not tb1.get():
        show_tb1.insert(END, "No filename entered\n")
    # perform task if input criteria have being met
    else:
        message_processing()
        temp = threading.Thread(target=show_top10button, args=[tb1.get()])
        temp.start()

def show_top10button(filename):
    """returns task 4 to output textbox"""
    display(t4.reader_list(filename))



def alsoLikesButton():
    """function activates on button click, performs task 5d with new thread"""
    show_tb1.delete(0.0, END)
    # textfield input criteria check
    if not tb1.get():
        show_tb1.insert(END, "No filename entered\n")
    if not tb2.get():
        show_tb1.insert(END, "No doc ID entered\n")
    # perform task if input criteria have being met(with user ID)
    if tb1.get() and tb2.get() and input_textbox3.get():
        message_processing()
        temp = threading.Thread(target=show_alsoLikes,
                                args=[input_textbox3.get(), tb2.get(), tb1.get()])
        temp.start()
    # perform task if input criteria have being met(without user ID)
    elif tb1.get() and tb2.get():
        message_processing()
        temp = threading.Thread(target=show_alsoLikes, args=["0", tb2.get(), tb1.get()])
        temp.start()


def graphButton():
    """function activates on button click, performs ta6 5d with new thread"""
    show_tb1.delete(0.0, END)
    # textfield input criteria check
    if not tb1.get():
        show_tb1.insert(END, "No filename entered\n")
    if not tb2.get():
        show_tb1.insert(END, "No doc ID entered\n")
    # perform task if input criteria have being met(with user ID)
    if tb1.get() and tb2.get() and input_textbox3.get():
        message_processing()
        temp = threading.Thread(target=t5.show_graph,
                                args=(input_textbox3.get(), tb2.get(), tb1.get()))
        temp.start()
    # perform task if input criteria have being met(without user ID)
    elif tb1.get() and tb2.get():
        message_processing()
        temp = threading.Thread(target=t5.show_graph, args=("0", tb2.get(), tb1.get()))
        temp.start()

def show_alsoLikes(userID, docID, filename):
    """returns task 5d and 6 and to output textbox"""
    display(t5.alsolikes_sorted(userID, docID, filename))


def display(result):
    """returns input in the output textbox"""
    show_tb1.insert(END, result)


def message_processing():
    """displays processing message in the output textbox"""
    show_tb1.insert(END, "Processing request...\n\n")


def full_message():
    """displays complete message in the output textbox"""
    show_tb1.insert(END, "Request complete\n\n")


def msg():
    """displays help message in the output textbox"""
    show_tb1.delete(0.0, END)
    msg = "To use the document tracker: \n1. Enter the the JSON file path, document ID and use ID (if applicable) " \
          "in the text boxes above. \n2. Then select an search option to process."
    show_tb1.insert(END, msg)


def closeButton():
    """closes window"""
    window.destroy()
    exit()


def GUI(fileID, userID, docID):
    """
    function called in main to initialise GUI
    reads in file name, user Id and document ID from terminal input
    """

    # create GUI window
    global window
    window = tk.Tk()
    window.title("Document Analysis")
    window.configure(bg="grey")
    window.geometry("800x500")
   

    # create 3 text fields amd their lables (filename, document ID and user ID)
    Label(window, text="Enter File Path:", bg="black", fg="white", font=('Times New Roman',12, 'bold')).grid(row=1, column=0,
                                                                                                  columnspan=2,sticky=W)
    global tb1
    tb1 = Entry(window, width=50, bg="white")
    tb1.grid(row=2, column=0, columnspan=3, sticky=W)
    tb1.insert(0, fileID)

    Label(window, text="Document ID:", bg="black", fg="white", font=('Times New Roman',12, 'bold')).grid(row=3, column=0,
                                                                                               columnspan=2, sticky=W)
    global tb2
    tb2 = Entry(window, width=50, bg="white")
    tb2.grid(row=4, columnspan=3, sticky=W)
    tb2.insert(0, docID)

    Label(window, text="User ID:", bg="black", fg="white", font=('Times New Roman',12, 'bold')).grid(row=5, column=0,
                                                                                           columnspan=2, sticky=W)
    global input_textbox3
    input_textbox3 = Entry(window, width=50, bg="white")
    input_textbox3.grid(row=6, columnspan=3, sticky=W)
    input_textbox3.insert(0, userID)

    # label for search buttons
    Label(window, text="Select option:", bg="black", fg="white", font=('Times New Roman',12, 'bold')).place(x=530,y=0)

    # create search/task buttons for tasks 2a, 2b, 3a, 3b, 4, 5d and 6
    # each button's command links to a perform task function of the same task
    Button(window, text="View By Country", width=15, command=countryButton,font=('Times New Roman',12, 'bold')).place(x=450,y=30)
    Button(window, text="View By Continent", width=15, command=continentButton, font=('Times New Roman',12, 'bold')).place(x=450,y=70)
    Button(window, text="All Browsers", width=14, command=browserButton, font=('Times New Roman',12, 'bold')).place(x=530,y=150)
    Button(window, text="Top 5 Browsers", width=14, command=mainBrowserButton, font=('Times New Roman',12, 'bold')).place(x=615,y=30)
    Button(window, text="Top 10 Readers", width=14, command=top10button, font=('Times New Roman',12, 'bold')).place(x=615,y=70)
    Button(window, text="Also Likes", width=14, command=alsoLikesButton, font=('Times New Roman',12, 'bold')).place(x=615,y=110)
    Button(window, text="Also Likes Graph", width=14, command=graphButton, font=('Times New Roman',12, 'bold')).place(x=450,y=110)
    

    # create help and exit button with their commands linked to functions for help and close window.
    Button(window, text="Help", width=14, command=msg, font=('Times New Roman',12, 'bold')).place(x=10,y=490)
    Button(window, text="Exit", width=14, command=closeButton,font=('Times New Roman',12, 'bold')).place(x=175,y=490)

    # crate a output textbox
    global show_tb1
    show_tb1 = Text(window, width=99, height=15, wrap=WORD, bg="white")
    show_tb1.place(x=0,y=200)

    # perform task 6 on startup of the GUI
    graphButton()

    # output message on startup
    msg()

    # loop GUI window
    window.mainloop()


if __name__ == "__main__":
    GUI(r"/home/salman/Documents/IP/sample_3m_lines.json","0",
        "0")
