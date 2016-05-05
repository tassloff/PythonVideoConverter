import re
import subprocess

from track import *

#READ AUDIO STREAM DATA FROM AVCONV OUTPUT
#EXAMPLE :
#Stream #0.1[0x1c0]: Audio: mp2, 44100 Hz, stereo, s16p, 128 kb/s
#CODEC, FREQUENCE, CHANNEL, SAMPLEFORMAT, BITRATE

class AudioTrack ( Track ) :
    trackCodec = ""
    trackFrequence = ""
    trackChannel = ""
    trackSampleFormat = ""
    trackBitRate = ""

    def __init__ ( self, trackInfo ) :
        Track.__init__(self, trackInfo)
        self.trackCodec = self.scrapCodec()
        self.trackFrequence = self.scrapFrequence()
        self.trackChannel = self.scrapChannel()
        self.trackSampleFormat = self.scrapSampleFormat()
        self.trackBitRate = self.scrapBitRate()

    #GETTER
    def getTrackCodec ( self ) :
        return self.trackCodec
    def getTrackFrequence ( self ) :
        return self.trackFrequence
    def getTrackChannel ( self ) :
        return self.trackChannel
    def getTrackSampleFormat ( self ) :
        return self.trackSampleFormat
    def getTrackBitRate ( self ) :
        return self.trackBitRate

    #SETTER
    def setTrackCodec ( self, trackCodec ) :
        self.trackCodec = trackCodec
    def setTrackFrequence ( self, trackFrequence ) :
        self.trackFrequence = trackFrequence
    def setTrackChannel ( self, trackChannel ) :
        self.trackChannel = trackChannel
    def setTrackSampleFormat ( self, trackSampleFormat ) :
        self.trackSampleFormat = trackSampleFormat
    def setTrackBitRate ( self, trackBitRate ) :
        self.trackBitRate = trackBitRate


    def scrapCodec ( self ) :
        return self.trackSpec[0]

    def scrapFrequence ( self ) :
        return self.trackSpec[1]

    def scrapChannel ( self ) :
        return self.trackSpec[2]

    def scrapSampleFormat ( self ) :
        return self.trackSpec[3]

    def scrapBitRate ( self ) :
        for i in self.trackSpec :
            result = re.match(r"([0-9]+)\skb\/s", i)
            if result is not None : 
                return result.group(1)

    def extractTrack ( self, filename, fileinfo, trackNb ) :
        if fileinfo.startswith('matroska') :
            cmd = "mkvextract tracks " + filename + " " + str(trackNb) + ":audio" + str(trackNb) + ".aac"
        else :
            cmd = "avconv -i " + filename + " -vn -acodec copy audio." + self.trackCodec + " 2>&1"
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
        print "AUDIO CODEC : ", self.trackCodec
        print "AUDIO FREQUENCE : ", self.trackFrequence
        print "AUDIO CHANNEL : ", self.trackChannel
        print "AUDIO SAMPLE FORMAT : ", self.trackSampleFormat
        print "AUDIO BITRATE : ", self.trackBitRate

