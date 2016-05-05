import re

#TRACK (STREAM) FROM AVCONV OUTPUT

class Track ( object ) :
    trackInfo = "" #RAW STRING FROM AVCONV OUTPUT
    trackType = "" #TRACK TYPE (AUDIO, VIDEO, SUBTITLES ...)
    trackSpec = [] #LIST SPLITED FROM STRING
    trackLang = "" #STREAM LANGUAGE

    def __init__ ( self, trackInfo ) :
        self.trackInfo = trackInfo
        self.trackType = self.scrapTrackType()
        self.trackSpec = self.scrapTrackSpec()
        self.trackLang = self.scrapTrackLang()

    #GETTER
    def getTrackInfo ( self ) :
        return self.trackInfo
    def getTrackType ( self ) :
        return self.trackType
    def getTrackSpec ( self ) :
        return self.trackSpec
    def getTrackLang ( self ) :
        return self.trackLang

    #SETTER
    def setTrackInfo ( self, trackInfo ) :
        self.trackInfo = trackInfo
    def setTrackType ( self, trackType ) :
        self.trackType = trackType
    def setTrackSpec ( self, trackSpec ) :
        self.trackSpec = trackSpec
    def setTrackLang ( self, trackLang ) :
        self.trackLang = trackLang

    def scrapTrackType ( self ) :
        result = self.trackInfo.split(":")
        return result[1].strip()

    def scrapTrackSpec ( self ) :
        result = self.trackInfo.split(": ")
        return result[2].strip().split(", ")

    def scrapTrackLang ( self ) :
        result = re.match(r"^\s+Stream\s#[0-9.]+\(([a-z]+)\)", self.trackInfo)
        if result is not None : 
            return result.group(1)

    def showInfo ( self ) :
        print "TRACK : ", self.trackInfo
        print "TYPE : ", self.trackType
        print "SPEC : ", self.trackSpec

