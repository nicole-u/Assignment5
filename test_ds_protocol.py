import tkinter
from tkinter import simpledialog

def add_contact():
    new_contact = simpledialog.askstring("New contact:", "Please enter the new contact's name")
    print(new_contact)

add_contact()