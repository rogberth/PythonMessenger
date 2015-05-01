# -*- coding: utf-8 -*-


from Tkinter import *
import socket
import threading

def insertChat(event):
	global NICK
	global SEP
	
 	data = NICK+SEP+entry.get()+SEP
	s.send(data)
 	entry.delete(0, END)
 	
 	return

def insertName(event):
	global HOST
	global PORT
	global NICK

	HOST = entryIP.get()

	try:
		s.connect((HOST, PORT))
		s.setblocking(0)

		NICK = entryNick.get()
		block1.pack_forget()
		blockup.pack(side = TOP)
		scrollbar.pack(side = RIGHT,fill = Y)
		textBox.pack(side = LEFT,fill = Y)
		entry.pack(side=BOTTOM,pady=10)


		t = threading.Thread(target=listenThread)
		t.start()

	except:
		labelError.pack(side = TOP, pady = 20)
		pass
 	return

def listenThread():
	global s
	while 1:
		text = []
		try:
			rdata = s.recv(1024)
			text = rdata.split(SEP)
		except: pass
		cont = 0
		if len(text) >1:
			for x in range(len(text)/2):
				rtext = "\n"+str(text[x+cont])+" says:\n"+str(text[x+cont+1])
				writeInBox(rtext)
				cont += 2
	return

def writeInBox(cadena):
	textBox.config(state=NORMAL)
	textBox.insert(END,cadena+"\n")
	textBox.see(END)
	textBox.config(state=DISABLED)
	return


SEP ="|"
NICK = ""

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


master = Tk()
master.resizable(width=FALSE, height=FALSE)
# width x height + x_offset + y_offset:
#master.geometry("800x500+100+100") 
master.wm_title("PythonChat")

block1 = Frame(width=200, height=100)
block1.pack()

labelError = Label(block1, text="Server not available", fg = "red") 
label1 = Label(block1, text="Login nickname:")
label1.pack(side = TOP)


entryNick = Entry(block1)
entryNick.config(width=15)
entryNick.pack(side=TOP,pady=10)

entryIP = Entry(block1)
entryIP.config()
entryIP.pack(side=TOP,pady=10)
entryIP.insert(0,HOST)

blockup = Frame(width=600, height=500)


scrollbar = Scrollbar(blockup)


textBox = Text(blockup, height=20, width=100)

#Desable editing the text box
textBox.config(state=DISABLED)

textBox.config(yscrollcommand=scrollbar.set)

entry = Entry(master)
entry.config(width=50)



entryNick.bind("<Return>", insertName) 

entry.bind("<Return>", insertChat) 
mainloop()

