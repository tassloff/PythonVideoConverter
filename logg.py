import datetime
import time

class logg ( object ) :
    logPath = ""
    logFile = ""

    #CREATOR
    def __init__ ( self, path="./" ) :
        self.logFile = datetime.datetime.now().strftime("%Y-%m-%d_converter.log")
        self.logPath = path
