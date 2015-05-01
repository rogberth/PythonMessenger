# -*- coding: utf-8 -*-

from Tkinter import *
import socket
import threading

def bPressed():
	global STATE
	global t
	if not STATE:
		STATE = True
		labelONOFF.configure(text="Server ON", bg = "green")
		t = threading.Thread(target=serverThread)
		writeInBox("Server ON")
		t.start()
	else:
		STATE = False
		labelONOFF.configure(text="Server OFF", bg = "red")
		closeConn()
		writeInBox("Server SHUTDOWN")
		return

def closeConn():
	for cx in conn:
		cx.close()
		s.shutdown(socket.SHUT_RDWD)
		s.close()
	return

def serverThread():
	global s
	global PORT
	global conn
	try:
		s.bind((entryIP.get(), PORT))
	except: pass
	s.listen(3)

	writeInBox("Server awaiting first user")
	
	s.setblocking(0)


	#Supuestamente hace que no sea bloqueante y se hace después del 1º
	

	while STATE:
		for rcx in conn:
			data = None
			try:
				data = rcx.recv(STREAMSIZE)
				text = data.split(SEP)
				writeInBox("\n"+str(text[0])+" says:\n"+str(text[1]))
			except: pass
			if data != None:
				for cx in conn:
					cx.sendall(data)
		try:
			addr = s.accept()
			conn.append(addr[0])
			writeInBox('New user : '+ str(addr[1]))
		except: pass




def writeInBox(cadena):
	textBox.config(state=NORMAL)
	textBox.insert(END,cadena+"\n")
	textBox.see(END)
	textBox.config(state=DISABLED)
	return

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#SERVER VARIABLES
SEP ="|"
NICK = "SERVER"
HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
STREAMSIZE = 1024
STATE = False
#t = server thread
#connections list
conn = []
#socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


master = Tk()
# width x height + x_offset + y_offset:
#master.geometry("800x500+100+100") 
master.wm_title("SERVER")
master.resizable(width=FALSE, height=FALSE)

blockup = Frame()
blockup.pack(side = TOP)

entryIP = Entry(master)
entryIP.config()
entryIP.pack(side=TOP,pady=10)
entryIP.insert(0,HOST)


labelONOFF = Label(master, text="Server OFF", bg = "red")
labelONOFF.pack(side = RIGHT)

bONOFF = Button(master, text="Start/Stop", command=bPressed)
bONOFF.pack(side = RIGHT)

scrollbar = Scrollbar(blockup)
scrollbar.pack(side = RIGHT,fill = Y)

textBox = Text(blockup, height=20, width=100,yscrollcommand=scrollbar.set)
textBox.pack(side = LEFT,fill = Y)
#Desable editing the text box
textBox.config(state=DISABLED)

scrollbar.config(command=textBox.yview)

mainloop()



#-----------------
