import unittest
from ds_messenger import DirectMessenger, DirectMessage

messenger = DirectMessenger(dsuserver='168.235.86.101', username='strawberry', password='banana')

class test_messenger(unittest.TestCase):
    def test_send(self):
        recipient = "teatime"
        message = "This is a test"
        test = messenger.send(message, recipient)
        assert test == True

    def test_send_errors(self):
        wrong_messenger = DirectMessenger(dsuserver='notadsuserver', username='strawberry', password='wrongpassword')
        recipient = "teatime"
        message = "This is a test"
        test2 = wrong_messenger.send(message, recipient)
        assert test2 == False

    def test_retrieve_all(self):
        messenger.send("Hello world", "teatime")
        messenger.send("Hello world!!", "teatime")
        retrieveall_msger = DirectMessenger(dsuserver='168.235.86.101', username='teatime', password='iceecream')
        all_msgs = retrieveall_msger.retrieve_all()
        first_msg = all_msgs[0]
        assert type(first_msg.message) == str

    def test_retrieve_new(self):
        messenger.send("Hello again", "teatime")
        retrievenew_msger = DirectMessenger(dsuserver='168.235.86.101', username='teatime', password='iceecream')
        new_msgs = retrievenew_msger.retrieve_new()
        assert type(new_msgs[0].message) == str
