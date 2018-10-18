#! /usr/bin/env python3

# Echo client program
import socket, sys, os, re
import params
from framedSock import FramedStreamSock
from threading import Thread
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, fileName, debug):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.fileName, self.debug = serverHost, serverPort, fileName, debug
        self.start()
    def run(self):
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(af, socktype, proto)
           except socket.error as msg:
               print(" error: %s" % msg)
               s = None
               continue
           try:
               print(" attempting to connect to %s" % repr(sa))
               s.connect(sa)
           except socket.error as msg:
               print(" error: %s" % msg)
               s.close()
               s = None
               continue
           break

       if s is None:
           print('could not open socket')
           sys.exit(1)

       fs = FramedStreamSock(s, debug=debug)


       fname = self.fileName#input("please enter name of file to send to server: ")
       files = [f for f in os.listdir('.') if os.path.isfile(f)]#determine if file exists for sending
       for f in files:
           if f == fname:
               #sendName(fname)
               break
       else:
           print("file for sending not found exiting")#if file not found exit
           sys.exit(0)

       print("sending file")
       fs.sendmsg(fname)#otherwise send file to server

       #print("sending hello world")
       #fs.sendmsg(b"hello world")
       #print("received:", fs.receivemsg())

       #fs.sendmsg(b"hello world")
       #print("received:", fs.receivemsg())
fileName1 = "fsend.txt"
fileName2 = "dog.txt"
for i in range(5):
    ClientThread(serverHost, serverPort, fileName1, debug)
    ClientThread(serverHost, serverPort, fileName2, debug)
