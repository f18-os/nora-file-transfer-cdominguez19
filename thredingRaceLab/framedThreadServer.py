#! /usr/bin/env python3
import sys, os, socket, params, time
import threading#from threading import Thread
from framedSock import FramedStreamSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

counter = 0
lock = threading.Lock()

class ServerThread(threading.Thread):
    requestCount = 0            # one instance / class
    def __init__(self, sock, debug):
        threading.Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
    def run(self):
#lock before while
        fileName = "test.txt"#input("Save file as: ")
        with lock:
            files = [f for f in os.listdir('.') if os.path.isfile(f)]#determine if file exists for sending
            for f in files:
                if f == fileName:
                    global counter
                    counter += 1
                    fileName = str(counter) + fileName
                    print("file name taken renaming to: %s" % fileName)
                    self.fsock.receivemsg(fileName)
                    break
            else:
                self.fsock.receivemsg(fileName)
                print("file saved")#if file not found exit
                sys.exit(0)

        #while True:
            #with lock:
                #msg = self.fsock.receivemsg()
                #if not msg:
                    #if self.debug: print(self.fsock, "server thread done")
                    #return
                #requestNum = ServerThread.requestCount
                #time.sleep(0.001)
                #ServerThread.requestCount = requestNum + 1
                #msg = ("%s! (%d)" % (msg, requestNum)).encode()
                #self.fsock.sendmsg(msg)


while True:
    sock, addr = lsock.accept()
    ServerThread(sock, debug)
