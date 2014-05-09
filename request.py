import os
import urllib2
import urllib
class EnhancedFile(file):
    def __init__(self, *args, **keyws):
        file.__init__(self, *args, **keyws)

    def __len__(self):
        return int(os.fstat(self.fileno())[6])


theUrl = "file:///home/ubuntu/Desktop/repositorio/tesis_juego/request/inva.html"

theHeaders= {'Content-Type':'text/html'}

theFile = EnhancedFile('highscores.txt', 'r')

#for line in theFile:
#  print line

values ={'name':'MARLEN','password':'100'}

theData = urllib.urlencode(values)

theRequest = urllib2.Request(theUrl, theData)

response = urllib2.urlopen(theRequest)

theFile.close()
