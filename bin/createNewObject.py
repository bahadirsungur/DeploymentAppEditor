from splunk.persistconn.application import PersistentServerConnectionApplication
import os
import json
import platform
import logging
import sys

if sys.platform == "win32":
    import msvcrt
    # Binary mode is required for persistent mode on Windows.
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stderr.fileno(), os.O_BINARY)

class CreateNewObject(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        super(PersistentServerConnectionApplication, self).__init__()

    # Handle a syncronous from splunkd.
    def handle(self, in_string):
        try:
            payload = json.loads(json.loads(in_string)['payload']) 
            obj = payload['obj']
            objType = payload['objType']
            os.mkdir(obj) if objType!='file' else open(obj, 'a').close()
            status = f"{obj} {objType} created successfully."
        except Exception as e:
            status = str(e)
            obj = "See exception on browser console." 
            objType = "See exception on browser console."
        payload = {
            "obj" : obj,
            "objType" : objType,
            "status": status
        }
        return {'payload': payload, 'status': 200}

    def handleStream(self, handle, in_string):
        """
        For future use
        """
        raise NotImplementedError(
            "PersistentServerConnectionApplication.handleStream")

    def done(self):
        """
        Virtual method which can be optionally overridden to receive a
        callback after the request completes.
        """
        pass
