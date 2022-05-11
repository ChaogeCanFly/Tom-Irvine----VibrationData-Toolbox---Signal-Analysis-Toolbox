###########################################################################
# program: vb_number_octaves_gui.py
# author: Tom Irvine
# version: 1.1
# date: April 27, 2014
# 
###############################################################################

from __future__ import print_function

from numpy import log
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    import tkinter.messagebox as tkMessageBox

###############################################################################

class vb_number_octaves:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.14))
        h = int(2.*(h*0.19))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_number_octaves_gui.py  ver 1.1  by Tom Irvine")
        
        
        crow=0        
        
        self.hwtext1=tk.Label(top,text='Enter Frequencies (Hz)')
        self.hwtext1.grid(row=crow, column=1, pady=7,sticky=tk.W)               
        
        
###############################################################################
        
        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='1')
        self.hwtext2.grid(row=crow, column=0, pady=4,sticky=tk.E)  
        
        self.freq1=tk.StringVar()  
        self.freq1=tk.Entry(top, width = 12,textvariable=self.freq1)
        self.freq1.grid(row=crow, column=1,padx=1, pady=4)
        
        crow=crow+1
        
        self.hwtext3=tk.Label(top,text='2')
        self.hwtext3.grid(row=crow, column=0, pady=4,sticky=tk.E)         
        
        self.freq2=tk.StringVar()  
        self.freq2=tk.Entry(top, width = 12,textvariable=self.freq2)
        self.freq2.grid(row=crow, column=1,padx=1, pady=4)

        
###############################################################################

        crow=crow+1        
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate_main)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=1,padx=1, pady=10,sticky=tk.SE) 
        
        crow=crow+1         
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=1,pady=10,sticky=tk.SE) 

        crow=crow+1
          
        self.hwtext_results=tk.Label(top,text='Number of Octaves')
        self.hwtext_results.grid(row=crow, column=1, columnspan=2, pady=12)

        crow=crow+1

        self.Qr=tk.StringVar()  
        self.Q_entry=tk.Entry(top, width = 12,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=1) 
        self.Q_entry.configure(state='readonly')

        self.freq1.bind("<Key>", self.callback_noct)
        self.freq2.bind("<Key>", self.callback_noct)
        
###############################################################################          

    def callback_noct(self,event):
        self.Qr.set('')

    def calculate_main(self):
        
        f1=float(self.freq1.get())
        f2=float(self.freq2.get())
        
        if(f1>f2):
            temp=f1
            f1=f2
            f2=temp
            
        noct=log(f2/f1)/log(2)
        
        buf = "%7.3g" %noct        
         
        self.Qr.set(buf)       
        
        
def quit(root):
    root.destroy()         