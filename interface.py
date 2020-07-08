from tkinter import Tk, Frame, BOTH, X, Y, NONE, LEFT, Label, Entry, Text, W
import tkinter as tk

#LOAD DATA FUNCTION

#DATA UPDATE FUNCTION
ip_addr = "127.0.0.1" 
sv_port = "80" 
cl_port = "52352" 
stt = "Connected" 
log = "ABCDEF"

class Inerface(Frame):
    def __init__(self, parent):
        #khung giao dien chinh
        Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        self.initUI(ip_addr, sv_port, cl_port, stt, log)
  
    def initUI(self, ip_addr, sv_port, cl_port, stt, log):
        #cai dat thong tin: ten, khoi tao de ve len khung giao dien
        self.parent.title("[MMT_18_5]209_214_215")
        self.pack(fill=BOTH, expand=1)
        #frame IP Address - Port Server
        frame1 = Frame(self)
        frame1.pack(fill= X)
 
        addr_lb = Label(frame1, text="IP Address:", width=10, anchor=W)
        addr_lb.pack(side=LEFT, padx=5, pady=5)           
 
        addr_entry = Text(frame1, width=12, height=1)
        addr_entry.pack(side=LEFT,fill=NONE, padx=5, pady=5, expand=0)
        addr_entry.insert(tk.END, ip_addr)

        #Server Port
        port_sv_lb = Label(frame1, text="Server Port:")
        port_sv_lb.pack(side=LEFT, padx=30, pady=5)           
 
        port_sv_entry = Text(frame1, width=7, height=1)
        port_sv_entry.pack(side=LEFT,fill=NONE, padx=5, pady=5, expand=0)
        port_sv_entry.insert(tk.END, sv_port)

        #frame Status
        frame2 = Frame(self)
        frame2.pack(fill= X)
 
        stt_lb = Label(frame2, text="Status:", width=10, anchor=W)
        stt_lb.pack(side=LEFT, padx=5, pady=5)           
 
        stt_entry = Text(frame2, width=12, height=1)
        stt_entry.pack(side=LEFT,fill=NONE, padx=5, pady=5, expand=0)
        stt_entry.insert(tk.END, stt)

        #Client Port
        port_cl_lb = Label(frame2, text="Client Port:")
        port_cl_lb.pack(side=LEFT, padx=30, pady=5)           
 
        port_cl_entry = Text(frame2, width=7, height=1)
        port_cl_entry.pack(side=LEFT,fill=NONE, padx=5, pady=5, expand=0)
        port_cl_entry.insert(tk.END, cl_port)

        #frame Log
        frame3 = Frame(self)
        frame3.pack(fill= BOTH, expand=True)
 
        log_lb = Label(frame3, text="Logging:", width=10, anchor=W)
        log_lb.pack(side=LEFT, padx=5, pady=5)           
 
        log_entry = Text(frame3, width=47, height=12)
        log_entry.pack(side=LEFT, fill=NONE, padx=5, pady=5, expand=0)
        log_entry.insert(tk.END, log)
       
def UI_server(ip_addr, sv_port, cl_port, stt, log):        
    root = Tk()
    root.geometry("500x300+450+200")
    app = Inerface(root)
    root.mainloop()  

#UI_server(ip_addr, sv_port, cl_port, stt, log)
UI_server("localhost", "81", "89898", "Not conneted", "blah blah")
