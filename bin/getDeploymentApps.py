from splunk.persistconn.application import PersistentServerConnectionApplication
import os
import json
import logging
import sys

if sys.platform == "win32":
    import msvcrt
    # Binary mode is required for persistent mode on Windows.
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stderr.fileno(), os.O_BINARY)

class GetDeploymentApps(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        super(PersistentServerConnectionApplication, self).__init__()

    # Handle a syncronous from splunkd.
    def handle(self, in_string):

        dc = {}
        isRoot = True
        root = "/opt/splunk/etc/deployment-apps" if os.environ.get('SPLUNK_HOME')==None else os.path.join(os.environ.get('SPLUNK_HOME'), 'etc/deployment-apps')

        for path, dirs, files in os.walk(root):
            dirs.sort()
            files.sort()
            if isRoot:
                dc[path] = {'path': path, 'type': 'folder', 'isRoot':isRoot, 'children' : [path + "/" + leaf for leaf in dirs+files]}
                isRoot = False
            else:
                dc[path] = {'path': path, 'type': 'folder', 'children' : [path + "/" + leaf for leaf in dirs+files]}
            for file in files:
                dc[path+"/"+file] = {'path':path+"/"+file, 'type':'file' }
        return {'payload': dc, 'status': 200}

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
