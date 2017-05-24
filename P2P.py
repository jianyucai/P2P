#coding=utf-8
import socket
import sys
import traceback
import os
import struct
import re
import math
import platform
import signal

BUFSIZE = 1024

'''
showing the progress of file transmission
@:param cur current percent
@:param total percent
'''
def progressbar(cur, total):
    percent = '{:.2%}'.format(float(cur) / float(total))

    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %s' % ( '=' * int(math.floor(cur * 50 /total)), percent))
    sys.stdout.flush()

    if cur == total:
        sys.stdout.write('\n')




def sender():
    # initialize socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initialize the socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    isConnected = False
    # get valid receiver IP address
    while True:
        try:
            receiver_ip = raw_input("\n>>input the IP of receiver: ")  # input the receiver ip
            s.connect((receiver_ip, 12345)) # socket connection
            isConnected = True
        except:
            print "\n>>connection failed!"
            exit()
        if isConnected == True:
            break

    # get valid file path
    isValidFile = False
    while True:
        try:
            filename = raw_input("\n>>input the file path: ")  # input the filename
            fp = open(filename, 'rb')
            isValidFile = True
        except:
            print "\n>>no such file!"
            exit()
        if isValidFile == True:
            break


    # head of file 
    fhead = struct.pack('128s11I', filename, 0, 0, 0, 0, 0, 0, 0, 0, os.stat(filename).st_size, 0, 0)
    s.send(fhead) # send the file header


    # send the file data
    while 1:
        filedata = fp.read(BUFSIZE)
        if not filedata:
            break
        s.sendall(filedata)
    fp.close()


    print "\n>>file fetch complete!"

    # receive message from sender
    while 1:
        buf = s.recv(1024)
        break
    if buf == "succeed":
        print "\n>>file transmission complete!"
    else:
        print "\n>>file transmission failed!"
    return





def receiver():
    # get hostname and initialize port
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = 12345

    if "Linux" in platform.system(): # Linux System requires this method to obtain ip (weird linux)
        host = os.popen(
            "ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()


    print "\n>>host ip:", host

    # initialize socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)

    print "\n>>waiting for sender connection..."

    while 1:
        try:
            clientSock, clientAddr = s.accept()
        except:
            traceback.print_exc()
            continue
        try:
            print "\n>>connection from", "ip:", clientSock.getpeername()[0], "port:", clientSock.getpeername()[1]

            FILEINFO_SIZE = struct.calcsize('128s32sI8s')

            fhead = clientSock.recv(FILEINFO_SIZE)
            filepath, temp1, filesize, temp2 = struct.unpack('128s32sI8s', fhead)

            m = re.match(r'.*/(.*)$', filepath)
            filename = m.group(1)

            # print file name and size
            if filesize < 1024:
                print "\n>>receiving file " + filename + " " + str(filesize) + "B"
            elif filesize < 1024 * 1024:
                print "\n>>receiving file " + filename + " " + str(filesize / 1024 ) + "KB"
            elif filesize < 1024 * 1024 * 1024:
                print "\n>>receiving file " + filename + " " + str(filesize / 1024 / 1024 ) + "MB"
            else:
                print "\n>>receiving file " + filename + " " + str(filesize / 1024 / 1024 / 1024) + "MB"

            savedFilename = filename.strip('\0')
            fp = open(sys.path[0]+"/"+savedFilename, 'wb')

            remain_size = filesize
            while remain_size > 0:
                filedata = clientSock.recv(BUFSIZE)
                if remain_size <= 1024:
                    progressbar(filesize , filesize)
                    break
                else:
                    current_size = filesize - remain_size
                    progressbar(current_size, filesize)
                    remain_size -= 1024
                    fp.write(filedata)

            fp.close()

            print "\n>>file receiced!"
            print "\n>>\"" + savedFilename + "\" is saved in \""+ sys.path[0] + "\""

            clientSock.send("succeed")


        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()

        try:
            clientSock.close()
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()
        return


if __name__=="__main__":

    if len(sys.argv) == 1:
        print "  This is a P2P file transmission script, allowing file transmission between hosts in LAN, requring python 2.7"
        print "  -s:  run as server mode, for recerving files "
        print "  -c:  run as client mode, for sending files"
        exit()

    arg = sys.argv[1]

    if arg == "-c":
        sender()
    elif arg == "-s":
        receiver()
    else:
        print ">>argument fault!\n"
