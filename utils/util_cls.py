import json
import threading
import sys
import datetime as dt
from bson import ObjectId


class KThread(threading.Thread):

    def __init__(self, *args, **kwargs):

        threading.Thread.__init__(self, *args, **kwargs)

        self.killed = False

    def start(self):

        """Start the thread."""

        self.__run_backup = self.run

        self.run = self.__run  # Force the Thread to install our trace.

        threading.Thread.start(self)

    def __run(self):

        """Hacked run function, which installs the

        trace."""

        sys.settrace(self.globaltrace)

        self.__run_backup()

        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):

        if why == 'call':

            return self.localtrace

        else:

            return None

    def localtrace(self, frame, why, arg):

        if self.killed:

            if why == 'line':
                raise SystemExit()

        return self.localtrace

    def kill(self):

        self.killed = True


class Timeout(Exception):
    """function run timeout"""


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, dt.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
