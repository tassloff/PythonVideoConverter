import re
import subprocess

from track import *

#READ VIDEO STREAM DATA FROM AVCONV OUTPUT
#EXAMPLE :
#Stream #0.0[0x1e0]: Video: mpeg1video, yuv420p, 352x240 [PAR 49:33 DAR 98:45], 1638 kb/s, 25 fps, 90k tbn, 25 tbc
#CODEC, PIXELFORMAT, RESOLUTION, BITRATE, FRAMERATE, TBR, TBN, TBC

class VideoTrack ( Track ) :
    trackCodec = ""
    trackPixelFormat = ""
    trackResolution = ""
    trackBitRate = ""
    trackFrameRate = ""
    tracktbr = ""
    tracktbn = ""
    tracktbc = ""

    def __init__ ( self, trackInfo ) :
        Track.__init__(self, trackInfo)
        self.trackCodec = self.scrapCodec()
        self.trackPixelFormat = self.scrapPixelFormat()
        self.trackResolution = self.scrapResolution()
        self.trackBitRate = self.scrapBitRate()
        self.trackFrameRate = self.scrapFrameRate()
        self.tracktbr = self.scraptbr()
        self.tracktbn = self.scraptbn()
        self.tracktbc = self.scraptbc()

    #GETTER
    def getTrackCodec ( self ) :
        return self.trackCodec
    def getTrackPixelFormat ( self ) :
        return self.trackPixelFormat
    def getTrackResolution ( self ) :
        return self.trackResolution
    def getTrackBitRate ( self ) :
        return self.trackBitRate
    def getTrackFrameRate ( self ) :
        return self.trackFrameRate
    def getTracktbr ( self ) :
        return self.tracktbr
    def getTracktbn ( self ) :
        return self.tracktbn
    def getTracktbc ( self ) :
        return self.tracktbc

    #SETTER
    def setTrackCodec ( self, trackCodec ) :
        self.trackCodec = trackCodec
    def setTrackPixelFormat ( self, trackPixelFormat ) :
        self.trackPixelFormat = trackPixelFormat
    def setTrackResolution ( self, trackResolution ) :
        self.trackResolution = trackResolution
    def setTrackBitRate ( self, trackBitRate ) :
        self.trackBitRate = trackBitRate
    def setTrackFrameRate ( self, trackFrameRate ) :
        self.trackFrameRate = trackFrameRate
    def setTracktbr ( self, tracktbr ) :
        self.tracktbr = tracktbr
    def setTracktbn ( self, tracktbn ) :
        self.tracktbn = tracktbn
    def setTracktbc ( self, tracktbc ) :
        self.tracktbc = tracktbc

    def scrapCodec ( self ) :
        return self.trackSpec[0]

    def scrapPixelFormat ( self ) :
        return self.trackSpec[1]

    def scrapResolution ( self ) :
        return self.trackSpec[2]

    def scrapBitRate ( self ) :
        for i in self.trackSpec :
            result = re.match(r"([0-9]+)\skb\/s", i)
            if result is not None : 
                return result.group(1)

    def scrapFrameRate ( self ) :
        for i in self.trackSpec :
            result = re.match(r"([0-9.]+)\sfps", i)
            if result is not None : 
                return result.group(1)

    def scraptbr ( self ) :
        for i in self.trackSpec :
            result = re.match(r"([0-9.]+)\stbr", i)
            if result is not None : 
                return result.group(1)

    def scraptbn ( self ) :
        for i in self.trackSpec :
            result = re.match(r"([0-9k]+)\stbn", i)
            if result is not None : 
                return result.group(1)

    def scraptbc ( self ) :
        for i in self.trackSpec :
            result = re.match(r"([0-9k.]+)\stbc", i)
            if result is not None : 
                return result.group(1)

    def extractTrack ( self, filename, fileinfo, trackNb ) :
        if fileinfo.startswith('matroska') :
            cmd = "mkvextract tracks " + filename + " " + str(trackNb) + ":video" + str(trackNb) + ".h264"
        else :
            cmd = "avconv -i " + filename + " -an -vcodec copy video." + self.trackCodec + " 2>&1"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = p.communicate()
        if p.returncode < 2 :
            #print stdout_data
            return 1
        else :
            #print "ERROR : " + stdout_data + "(" + str(p.returncode) + ")"
            return "ERROR : " + stdout_data + "(" + str(p.returncode) + ")"

    def showInfo ( self ) :
        Track.showInfo(self)
        print "VIDEO CODEC : ", self.trackCodec
        print "VIDEO PIXEL FORMAT : ", self.trackPixelFormat
        print "VIDEO RESOLUTION : ", self.trackResolution
        print "VIDEO BITRATE : ", self.trackBitRate
        print "VIDEO FRAMERATE : ", self.trackFrameRate
        print "VIDEO TBR : ", self.tracktbr
        print "VIDEO TBN : ", self.tracktbn
        print "VIDEO TBC : ", self.tracktbc

