import sys
import os
from os import walk

from videoFile import *



test = VideoFile(sys.argv[1])
#(_, _, allFiles) = walk(sys.argv[1]).next()
#for onefile in allFiles :
#    filename, file_extension = os.path.splitext(onefile)
