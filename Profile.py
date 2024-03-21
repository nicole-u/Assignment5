# Profile.py
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ THE JSON ASPECTS OF THIS CODE
# NOW, though can you certainly take a look at it if you are curious since we
# already covered a bit of the JSON format in class.
#

"""
This file has all the essential methods for profiles in a3.py and ui.py.
"""

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """
DsuFileError is a custom exception handler that you catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.
    """
    pass


class DsuProfileError(Exception):
    """
DsuProfileError is a exception handler that you catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.
    """
    pass


class Post(dict):
    """
    Post class is responsible for working with user posts. It currently
    supports two features: A timestamp property set upon instantiation and
    when entry object is set and an entry property that stores post message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """
        A function that sets the entry.
        """
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        """
        A function that gets the entry.
        """
        return self._entry

    def set_time(self, timestamp: float):
        """
        Sets the timestamp for the post.
        """
        self._timestamp = timestamp
        dict.__setitem__(self, 'timestamp', timestamp)

    def get_time(self):
        """
        Gets the timestamp from the post.
        """
        return self._timestamp

    entry = property(get_entry, set_entry)
    """
    The property method is used to support get and set capability for entry and
    time values. When the value is changed or set, the timestamp field is
    updated to the current time.
    """
    timestamp = property(get_time, set_time)


class Profile:
    """
    The class exposes properties required to join an ICS 32 DSU server. You
    need to use this class to manage the information provided by each user
    created within your program for a2. Pay close attention to properties and
    functions in this class as you need to make use of them.

    When creating program you need to collect user input for the properties
    exposed by the class. Profile class should ensure that a username and psswd
    are set, but contains no conventions to do so. Make sure that your code
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''            # OPTIONAL
        self._posts = []         # OPTIONAL
        self._contacts = []

    def add_post(self, post: Post) -> None:
        """
        add_post accepts a Post object and appends it to the posts list. Posts
        are stored in a list in the order they are added. So if Post objects
        are made, but added to Profile in a different order, it is possible
        for the list to not be sorted by Post.timestamp. So take caution
        as to how you implement your add_post code.
        """
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """
    del_post removes a Post at a given index. returns True or False if
    an invalid index was supplied.

    To find which post to delete you must make your own search operation on
    the posts returned from the get_posts function to find the correct index.
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """
    get_posts returns list object containing posts that have been added to the
    Profile object
    """
        return self._posts

    def save_profile(self, path: str) -> None:
        """
    save_profile accepts an existing dsu file to save the instance of Profile
    to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while processing the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the instance of Profile
        with data stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
