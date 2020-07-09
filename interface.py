from tkinter import Tk, Frame, BOTH, X, Y, NONE, LEFT, Label, Entry, Text, W, scrolledtext
import tkinter as tk




'''ip_addr = "127.0.0.1" 
sv_port = "80" 
cl_port = "52352" 
stt = "Connected" 
log = "ABCDEF"
'''

class Inerface(Frame):
    def __init__(self, parent):
        #khung giao dien chinh
        Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        self.initUI()
  
    def initUI(self):
        #cai dat thong tin: ten, khoi tao de ve len khung giao dien
        self.parent.title("[MMT_18_5]209_214_215")
        self.pack(fill=BOTH, expand=1)
        #frame IP Address - Port Server
        self.frame1 = Frame(self)
        self.frame1.pack(fill= X)
 
        self.addr_lb = Label(self.frame1, text="IP Address:", width=10, anchor=W)
        self.addr_lb.pack(side=LEFT, padx=5, pady=5)           
 
        self.addr_entry = Text(self.frame1, width=12, height=1)
        self.addr_entry.pack(side=LEFT,fill=NONE, padx=5, pady=5, expand=0)
        #self.addr_entry.insert(tk.END, ip_addr)

        #Server Port
        self.port_sv_lb = Label(self.frame1, text="Server Port:")
        self.port_sv_lb.pack(side=LEFT, padx=30, pady=5)           
 
        self.port_sv_entry = Text(self.frame1, width=7, height=1)
        self.port_sv_entry.pack(side=LEFT,fill=NONE, padx=5, pady=5, expand=0)
        #self.port_sv_entry.insert(tk.END, sv_port)

        #frame Status
        self.frame2 = Frame(self)
        self.frame2.pack(fill= X)
 
        self.stt_lb = Label(self.frame2, text="Status:", width=10, anchor=W)
        self.stt_lb.pack(side=LEFT, padx=5, pady=5)           
 
        self.stt_entry = Text(self.frame2, width=12, height=1)
        self.stt_entry.pack(side=LEFT,fill=NONE, padx=5, pady=5, expand=0)
        #self.stt_entry.insert(tk.END, stt)

        #Client Port
        self.port_cl_lb = Label(self.frame2, text="Client Port:")
        self.port_cl_lb.pack(side=LEFT, padx=30, pady=5)           
 
        self.port_cl_entry =  Text(self.frame2, width=7, height=1)
        self.port_cl_entry.pack(side=LEFT,fill=NONE, padx=5, pady=5, expand=0)
        #self.port_cl_entry.insert(tk.END, cl_port)

        #frame Log
        self.frame3 = Frame(self)
        self.frame3.pack(fill= BOTH, expand=True)
 
        self.log_lb = Label(self.frame3, text="Logging:", width=10, anchor=W)
        self.log_lb.pack(side=LEFT, padx=5, pady=5)           
 
        self.log_entry = scrolledtext.ScrolledText(self.frame3, width=47, height=12)
        self.log_entry.pack(side=LEFT, fill=NONE, padx=5, pady=5, expand=0)
        #self.log_entry.insert(tk.END, log+'\n')
    
    #DATA UPDATE FUNCTION 
    def updateUI(self, ip_addr, sv_port, cl_port, stt, log):      
        #frame IP Address - Port Server
        self.addr_entry.delete(1.0,tk.END)
        self.addr_entry.insert(tk.END, ip_addr)

        #Server Port
        self.port_sv_entry.delete(1.0,tk.END)
        self.port_sv_entry.insert(tk.END, sv_port)

        #frame Status
        self.stt_entry.delete(1.0,tk.END)
        self.stt_entry.insert(tk.END, stt)

        #Client Port
        self.port_cl_entry.delete(1.0,tk.END)
        self.port_cl_entry.insert(tk.END, cl_port)

        #frame Log
        self.log_entry.insert(tk.END, log +'\n')

'''def UI_server(ip_addr, sv_port, cl_port, stt, log):        
    root = Tk()
    root.geometry("500x300+450+200")
    app = Inerface(root)
    app.initUI(ip_addr, sv_port, cl_port, stt, log)
    root.mainloop()  

#UI_server(ip_addr, sv_port, cl_port, stt, log)
UI_server("localhost", "81", "89898", "Not conneted", "blah blah")
UI_server("localhost", "81", "89898", "Not conneted", "blah blah")'''
     
root = Tk()
root.geometry("500x300+450+200")
app = Inerface(root)
for i in range (1,100):
    app.updateUI("localhost", "81", "89898", "Not conneted", "blah blah")
root.mainloop()  