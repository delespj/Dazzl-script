#!/usr/bin/env python
# coding: utf8

import os, time

class TreatNfo:
    """Get and treat .nfo file"""

    def __init__(self, FilePath, FileName, Execution):
        self.FilePath = FilePath
        self.header = ""
        self.name = ""
        self.date = ""
        self.audio = ""
        self.video = ""
        if Execution == "clean":
            if os.path.exists(FilePath):
                self.ParsNfo()
            else:
                self.CreateNfo(FileName)
                self.ParsNfo()
        elif Execution == "mux":
            self.ParsNfo()
    
    def ParsNfo(self):
        if (os.path.exists(self.FilePath)):
            f = open(self.FilePath, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                field = line.split(" = ")
                if line[0] == "[":
                    self.header = line
                elif field[0] == "name":
                    self.name = field[1]
                elif field[0] == "date":
                    self.CheckDate(field[1])
                elif field[0] == "audio":
                    self.audio = field[1]
                elif field[0] == "video":
                    self.video = field[1]
                else:
                    # to treat further
                    continue
        else:
            print "File does not exist"

    def CheckDate(self, field):
        for letter in field:
            if ((letter >= '0' and letter <= '9') or letter == ':'
                or letter == ' ' or letter == '-' or letter == '\r' or letter == '\n'):
                continue
            else:
                time.ctime(os.path.getctime(self.FilePath))
                self.date = time.strftime("%Y-%m-%d %H:%M:%S") + '\r\n'
                return
        self.date = field

    def CreateCleanedNfo(self):
        with open(self.FilePath + ".clean", "w") as f:
            f.write(self.header)
            f.write("name = " + self.name)
            f.write("date = " + self.date)
            f.write("audio = " + self.audio)
            f.write("video = " + self.video)

    def DeleteNfo(self):
        os.system("rm -f " + self.FilePath)

    def CreateNfo(self, FileName):
        with open(self.FilePath, "w") as f:
            f.write("[" + FileName + "]" + '\r\n')
            f.write("name = Videocast " + FileName + '\r\n')
            time.ctime(os.path.getctime(self.FilePath))
            f.write("date = " + time.strftime("%Y-%m-%d %H:%M:%S") + '\r\n')
            f.write("audio = rec-" + FileName + "-audio.mjr" + '\r\n')
            f.write("video = rec-" + FileName + "-video.mjr" + '\r\n')

    def CreateMuxedNfo(self, audio, video, mux):
        with open(self.FilePath + ".muxed", "w") as f:
            f.write(self.header)
            f.write("name = " + self.name)
            f.write("date = " + self.date)
            f.write("audio = " + self.audio)
            f.write("video = " + self.video)
            f.write("audio.opus = " + audio)
            f.write("video.webm = " + video)
            f.write("mux.webm = " + mux)

    def GetDay(self):
        time = self.date.split(" ")
        return time[0]

    def GetHour(self):
        time = self.date.split(" ")
        hour = time.split(":")
        return hour[0]
