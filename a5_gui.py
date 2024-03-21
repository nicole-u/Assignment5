import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from typing import Text
from ds_messenger import DirectMessenger
from Profile import Profile


class Body(tk.Frame):
    """
    The class that's responsible for drawing the main body
    of the GUI.
    """
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        """
        Function to help with node selection
        """
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """
        Function that takes care of inserting a contact
        into the GUI
        """
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        """
        Function that inserts the contact tree
        """
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        """
        Function that inserts the user message into the box
        """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """
        Function that inserts the contact message into the box
        """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """
        Function that gets the message from the editor
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """
        Function that sets the text entry back to empty
        """
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def empty_editor(self):
        self.entry_editor.delete(1.0, tk.END)

    def _draw(self):
        """
        Function that draws all the things to tkinter
        """
        posts_frame = tk.Frame(master=self, width=250, background="#3ba39e")
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        style = ttk.Style()
        style.configure("Treeview", background="#cbf2ee", fieldbackground="#b0d6d4", font="bahnschrift 12")
        self.posts_tree = ttk.Treeview(posts_frame, style="Treeview")
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="#3ba39e")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="#3ba39e")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="#3ba39e", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="#3ba39e")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5, bg="#cbf2ee", blockcursor=True, font="bahnschrift 12")
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5, bg="#b0d6d4", font="bahnschrift 12")
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview, bg="#3ba39e")
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    Class that instantiates the footer.
    """
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """
        Function that calls back when the button is pushed.
        """
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """
        Function that draws in the footer.
        """
        save_button = tk.Button(master=self, text="Send", width=12, bg="#195e5b", fg="white", font="bahnschrift 10", command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, bg="#cbf2ee", text="Ready.", font="bahnschrift 10")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """
    Class that creates a dialog when adding a contact.
    """
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """
        Class that takes care of the configuration
        """
        self.server_label = tk.Label(frame, width=30, text="DS Server Address", bg="#b0d6d4")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username", bg="#b0d6d4")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password", bg="#b0d6d4")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = "*"
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        """
        Takes the username, password, and server from the entries
        """
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """
    Class that handles main work
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = "168.235.86.101"
        self.recipient = None
        self._get_profile()
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
        self._draw()
        profile.load_profile(self.filepath)
        for contact in self.contacts:
            self.body.insert_contact(contact)
        self.body.insert_contact("studentexw23")  # adding one example student.

    def send_message(self):
        """
        Function responsible for sending messages.
        """
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
        message = self.body.get_text_entry()
        # print(message)
        self.direct_messenger.send(message, self.recipient)
        self.body.insert_user_message(message)
        self.body.set_text_entry("")
        self.profile.load_profile(self.filepath)
        self.profile.contact_messages.append(message)
        self.profile.save_profile(self.filepath)

    def add_contact(self):
        """
        Function responsible for adding contacts.
        """
        global profile
        new_contact = simpledialog.askstring("New contact:", "Please enter the new contact's name")
        self.body.insert_contact(new_contact)
        self.profile.load_profile(self.filepath)
        profile.contacts.append(new_contact)
        self.profile.save_profile(self.filepath)
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list

    def recipient_selected(self, recipient):
        """
        Function responsible for getting messages when clicked.
        """
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
        self.recipient = recipient
        if self.recipient not in profile.contacts:
            Body.empty_editor()
            profile.contacts.append(self.recipient)
        else:
            message_list = self.direct_messenger.retrieve_all()
            for message in message_list:
                self.body.insert_contact_message(message.message)
                self.profile.contact_messages.append(message.message)
                profile.save_profile(self.filepath)

    def configure_server(self):
        """
        Function responsible for configuring server.
        """
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)

    def publish(self, message: str):
        """
        Function responsible for publishing.
        """
        self.direct_messenger.send(message, self.recipient)

    def check_new(self):
        """
        Function responsible for checking for new messages.
        """
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
        self.after(2500, self.direct_messenger.retrieve_new())
        msg_list = self.direct_messenger.retrieve_new()
        if msg_list:
            for message_obj in msg_list:
                if message_obj.recipient not in self.body._contacts:
                    self.body.insert_contact(message_obj.recipient)
                elif message_obj.recipient == self.recipient:
                    self.body.insert_contact_message(message_obj.message)
                self.profile.contacts.append({"contact": message_obj.recipient})
                self.profile.contact_messages.append({self.recipient: {"message": message_obj.message, "timestamp": message_obj.timestamp}})
                self.profile.save_profile(self.filepath)

    def _get_profile(self):
        """
        Function to get profile info.
        """
        profile_to_load = filedialog.askopenfile()
        filepath = str(profile_to_load.name)
        global profile
        profile = Profile()
        profile.load_profile(filepath)
        self.filepath = filepath
        self.profile = profile
        server_from_profile = profile.dsuserver
        username_from_profile = profile.username
        password_from_profile = profile.password
        self.contacts = profile.contacts
        self.server = server_from_profile
        self.username = username_from_profile
        self.password = password_from_profile

    def _new_profile(self):
        """
        Function to create new profile in GUI
        """
        folder_to_load = filedialog.askdirectory()
        terminal_time = tk.Label(master=self, text="Please check the terminal to create your profile.")
        terminal_time.pack()
        file_name = input("Please input a filename.")
        filepath = f"{folder_to_load}" + f"\\{file_name}.dsu"
        profile = Profile()
        new_user = input("Please enter a username for this file.\n")
        while " " in new_user:
            new_user = input("Username cannot have whitespace. Please try again.")
        profile.username = new_user
        psswd = input("Please enter a password for this file.\n")
        while " " in psswd:
            psswd = input("Password cannot have whitespace. Please try again.")
        profile.password = psswd
        new_bio = input("Please type a short bio for this file.\n")
        profile.bio = new_bio
        profile.dsuserver = str(input("What server would you like to save to?\n"))
        profile.save_profile(filepath)
        self.server = profile.dsuserver
        self.username = profile.username
        self.password = profile.password
        print(f"{filepath} created.\n")

    def _draw(self):
        """
        Function that builds the menu
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File', background="black")
        menu_file.add_command(label='New', background="#b0d6d4", font="bahnschrift 10", activebackground="#195e5b", command=self._new_profile)
        menu_file.add_command(label='Open...', background="#b0d6d4", font="bahnschrift 10", activebackground="#195e5b", command=self._get_profile)
        menu_file.add_command(label='Close', background="#b0d6d4", font="bahnschrift 10", activebackground="#195e5b", command=quit)

        settings_file = tk.Menu(menu_bar, background="black")
        menu_bar.add_cascade(menu=settings_file, label='Settings', background="black")
        settings_file.add_command(label='Add Contact', background="#b0d6d4", font="bahnschrift 10", activebackground="#195e5b",
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server', background="#b0d6d4", font="bahnschrift 10", activebackground="#195e5b",
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


def main():
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 DSU Chat Room")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("800x360")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()


if __name__ == "__main__":
    main()
