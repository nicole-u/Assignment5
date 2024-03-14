# a4.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Nicole Utama
# nutama@uci.edu
# 20267081

from Profile import *
import ui

ACCEPTED_P_OPTIONS = ["-usr", "-pwd", "-bio", "-posts", "-post", "-all", "done"]
ACCEPTED_E_OPTIONS = ["-usr", "-pwd", "-bio", "-addpost", "-delpost", "done"]


def welcome():
    """
    The main menu welcome function. This function
    runs first, and guides the user through opening
    or creating a new DSU file to which everything
    will be saved.
    """
    print("Welcome to PyJournal! Type 'Q' at any time to quit.")
    user_action = input("Would you like to create a DSU file(C) or open a DSU file (O)?\n")
    user_action = user_action.upper()
    while user_action != "Q":
        if user_action == "C":
            path = input("Please enter the path where you want to create the file.\n")
            filename = input("What would you like to name this file?\n")
            if path == "Q" or filename == "Q":
                quit()
            else:
                ui.c_command(path, filename)
        elif user_action == "O":
            path = input("Please enter the path of the file you want to open.\n")
            filename = input("Please enter the file name you want to open. (Do not include .dsu)\n")
            if path == "Q" or filename == "Q":
                quit()
            else:
                ui.o_command(path, filename)
        else:
            user_action = input("Invalid action. Please try again.\n")
            user_action = user_action.upper()
            continue
        print_and_edit(path, filename)
    quit()


def print_and_edit(filepath, filename):
    """
    A submenu of the welcome function. After
    creating a file, this function runs in a
    loop that lets the user print and edit
    their DSU file properties.
    """
    user_action = input("Would you like to print (P) or edit (E)? Type 'out' to exit.\n")
    user_action = user_action.upper()
    while user_action != "OUT":
        if user_action == "P":
            print("Accepted options:")
            for option in ACCEPTED_P_OPTIONS:
                print(option)
            input_options = input("What would you like to print? Type 'done' when done.\n")
            while input_options != "done":
                if input_options not in ACCEPTED_P_OPTIONS:
                    input_options = input("Invalid. Please try again.\n")
                ui.p_command(input_options, filepath, filename)
                input_options = input("What would you like to print? Type 'done' when done.\n")
            user_action = input("Would you like to print (P) or edit (E)? Type 'out' to exit.\n")
            user_action = user_action.upper()
        elif user_action == "E":
            print("Accepted options:")
            for option in ACCEPTED_E_OPTIONS:
                print(option)
            input_options = input("What would you like to edit? Type 'done' when done.\n")
            while input_options != "done":
                if input_options not in ACCEPTED_E_OPTIONS:
                    input_options = input("Invalid. Please try again.\n")
                ui.e_command(input_options, filepath, filename)
                input_options = input("What would you like to edit? Type 'done' when done.\n")
            user_action = input("Would you like to print (P) or edit (E)? Type 'out' to exit.\n")
            user_action = user_action.upper()
        else:
            user_action = input("Invalid action. Please retype.\n")
            user_action = user_action.upper()
    welcome()


if __name__ == "__main__":
    welcome()
