import unittest
import ds_protocol as dsp
DSUSERVER = "168.235.86.101"
PORT = 3021
USERNAME = "strawberry"
PASSWORD = "banana"

class test_directmessage(unittest.TestCase):
    def test_normally(self):
        results = dsp.directmessage("Hello world", "teatime", DSUSERVER, USERNAME, PASSWORD)
        assert results[0] == "Direct message successfully sent"
        assert results[1] == "61131fe2-33e4-41c7-929c-d73dedfd27be"

    def test_json_extraction(self):
        json_msg = '{"response": {"type": "ok", "token": "usertoken", "message": "hello world"}}'
        result = dsp.extract_json(json_msg)
        assert result == ("ok", "hello world", "usertoken")
    
    def testing_json_errors(self):
        msg =  '{"response": {"type": "error"}}'
        result = dsp.extract_json(msg)
        assert result == ("error", "", "")

    def test_dm_errors(self):
        wrong_server = dsp.directmessage("Hello world", "teatime", "notadsuserverlol", USERNAME, PASSWORD)
        assert wrong_server == "Error with sending direct message."