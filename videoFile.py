import subprocess
import re
import sys
import os.path
from cStringIO import StringIO

from track import *
from videoTrack import *
from audioTrack import *

class VideoFile ( object ) :
    #VIDEO FILE NAME
    fileName = ""
    #VIDEO BASE NAME
    fileBaseName = ""
    #VIDEO EXTENSION
    fileExtension = ""
    #VIDEO FILE INFO
    fileInfo = ""
    #VIDEO INFORMATIONS (AVCONV -I OUTPUT)
    tracksInfo = ""
    #NUMBER OF TRACKS(VIDEO, AUDIO, SUB...)
    tracksNumber = 0
    #ARRAY FOR TRACKS INFORMATIONS
    tracks = []

    #CREATOR
    def __init__ ( self, fileName ) :
        self.fileName = fileName
        self.fileBaseName, self.fileExtension = os.path.splitext(self.fileName)
        self.tracksInfo = self.scrapTracksInfo()
        self.tracksNumber = self.processTracks()
        self.fileInfo = self.processFile()
        #self.showFileInfo()
        self.extractTracks()
        self.joinTracks()

    #GETTER
    def getFileName ( self ) :
        return self.fileName
    def getFileBaseName ( self ) :
        return self.fileBaseName
    def getFileExtension ( self ) :
        return self.fileExtension
    def getFileInfo ( self ) :
        return self.fileInfo
    def getTracksInfo ( self ) :
        return self.tracksInfo
    def getTracksNumber ( self ) :
        return self.tracksNumber
    def getTracks ( self ) :
        return self.tracks

    #SETTER
    def setFileName ( self, fileName ) :
        self.fileName = fileName
    def setFileBaseName ( self, fileBaseName ) :
        self.fileBaseName = fileBaseName
    def setFileExtension ( self, fileExtension ) :
        self.fileExtension = fileExtension
    def setFileInfo ( self, fileInfo ) :
        self.fileInfo = fileInfo
    def setTracksInfo ( self, tracksInfo ) :
        self.tracksInfo = tracksInfo
    def setTracksNumber ( self, tracksNumber ) :
        self.tracksNumber = tracksNumber
    def setTracks ( self, tracks ) :
        self.tracks = tracks

    #GET AVCONV OUTPUT AS RAW STRING
    def scrapTracksInfo ( self ) :
        cmd = "avconv -i " + self.fileName + " 2>&1"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = p.communicate()
        #ERROR CHECK
        if p.returncode == 1 :
            return stdout_data
        else :
            return "ERROR : " + stdout_data + "(" + str(p.returncode) + ")"

    #READ RAW STRING FILE INFO
    def processFile ( self ) :
        for item in self.tracksInfo.split("\n") :
            result = re.match(r"^Input\s#", item)
            if result :
                endPos = item.find(" from ")
                endPos = endPos - 1
                if ( endPos != -1 ) :
                    return item[10:endPos]
    #SPLIT RAW STRING AS TRACK (STREAM)
    def processTracks ( self ) :
        #NUMBER OF TRACKS
        i = 0
        #EACH LINE, STREAM => ONE TRACK
        for item in self.tracksInfo.split("\n") :
            result = re.match(r"^\s+Stream.*", item)
            if result :
                oneTrack = Track(item)
                #VIDEO
                if oneTrack.getTrackType() == "Video" :
                    self.tracks.append(VideoTrack(item))
                #AUDIO
                elif oneTrack.getTrackType() == "Audio" :
                    self.tracks.append(AudioTrack(item))
                #OTHER
                else :
                    self.tracks.append(oneTrack)
                i = i + 1
        return i

    def showFileInfo ( self, log=False ) :

        #LOG INSTEAD OF DISPLAY
        if log :
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()

        print "FILE NAME : ", self.fileName
        print "FILE BASENAME : ", self.fileBaseName
        print "FILE EXTENSION : ", self.fileExtension
        print "FILE INFO : ", self.fileInfo
        if self.fileInfo.startswith('matroska') :
            print 'MATROSKA FILE'
        print "TRACKS NUMBER : ", self.tracksNumber
        i = 1
        for track in self.tracks :
            print "TRACK NUMERO : ", i
            track.showInfo()
            i = i + 1

        if log :
            sys.stdout = old_stdout
            #examine mystdout.getvalue()

    #EXTRACT TRACKS (STREAM)
    def extractTracks ( self ) :
        i = 0
        for track in self.tracks :
            #AUDIO EXTRACT TRACK
            if track.getTrackType() == "Audio" :
                audioExtracted = track.extractTrack( self.fileName, self.fileInfo, i )
                if audioExtracted == 1 :
                    print "AUDIO EXTRACTED CORRECLY"
                else :
                    print audioExtracted

            #VIDEO EXTRACT TRACK
            if track.getTrackType() == "Video" :
                videoExtracted = track.extractTrack( self.fileName, self.fileInfo, i )
                if videoExtracted == 1 :
                    print "VIDEO EXTRACTED CORRECLY"
                else :
                    print videoExtracted
            i = i + 1

    #JOIN TRACKS (STREAM)
    def joinTracks ( self ) :
        if self.fileInfo.startswith('matroska') :
            cmd = "MP4Box "
        else :
            cmd = "avconv -i " + filename + " -an -vcodec copy video." + self.trackCodec + " 2>&1"
        i = 0
        for track in self.tracks :
            if i > 1 :
                continue
            if track.getTrackType() == "Audio" :
                cmd = cmd + "-add audio" + str(i) + ".aac:lang=" + track.getTrackLang() + " "
            if track.getTrackType() == "Video" :
                cmd = cmd + "-add video" + str(i) + ".h264:fps=" + track.getTrackFrameRate() + " "
                #cmd = cmd + "video" + str(i) + ".mp4 "
            i = i + 1
        cmd = cmd + self.fileBaseName + ".mp4"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = p.communicate()
        if p.returncode == 0 :
            print "here"
            print stdout_data
        else :
            print "ERROR : " + stdout_data + "(" + str(p.returncode) + ")"
