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

class RenameObject(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        super(PersistentServerConnectionApplication, self).__init__()

    # Handle a syncronous from splunkd.
    def handle(self, in_string):
        try:
            payload = json.loads(json.loads(in_string)['payload']) 
            obj = payload['obj']
            newObj = payload['newObj']
            os.rename(obj, newObj)
            status = f"{obj} renamed to {newObj} successfully."
        except Exception as e:
            status = str(e)
            obj = "See exception on browser console." 
            newObj = "See exception on browser console."
        payload = {
            "obj" : obj,
            "newObj" : newObj,
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
