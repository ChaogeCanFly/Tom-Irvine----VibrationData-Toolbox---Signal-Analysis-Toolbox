##########################################################################
# program: vb_Rayleigh_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.0
# date: May 1, 2014
# description:  
#
##########################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk    
    import tkinter.messagebox as tkMessageBox
    

from math import exp


    
######################################################################## 

class vb_Rayleigh:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.18))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_Rayleigh_gui.py ver 1.0  by Tom Irvine") 
        
        
        crow=0        
        
        self.hwtext1=tk.Label(top,text='This script integrates the Rayleigh distribution to find probability from zero to the upper limit.')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)


###############################################################################

        crow=crow+1

        self.hwtext1 = tk.Label(top, text="Enter Upper Limit")
        self.hwtext1.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)
        
        self.hwtext3 = tk.Label(top, text="Probability within limits")
        self.hwtext3.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.S)       
        
        crow=crow+1
        
        self.zr=tk.StringVar()  
        self.zr.set('')  
        self.z_entry=tk.Entry(top, width = 10,textvariable=self.zr)
        self.z_entry.grid(row=crow, column=0,sticky=tk.N)    
        self.z_entry.bind("<KeyRelease>", self.OnKeyPress)  
        
        self.p1r=tk.StringVar()  
        self.p1r.set('')  
        self.p1_entry=tk.Entry(top, width = 16,textvariable=self.p1r)
        self.p1_entry.grid(row=crow, column=1,padx=5, pady=1,sticky=tk.N) 
        self.p1_entry.config(state = 'disable')        
        
        crow=crow+1
       
        self.hwtext5 = tk.Label(top, text="Probability of exceeding limits")
        self.hwtext5.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.S)        
       
        crow=crow+1
        
        self.p2r=tk.StringVar()  
        self.p2r.set('')  
        self.p2_entry=tk.Entry(top, width = 16,textvariable=self.p2r)
        self.p2_entry.grid(row=crow, column=1,padx=5, pady=1,sticky=tk.N) 
        self.p2_entry.config(state = 'disable')              

  
        crow=crow+1

        self.button_calculate = \
        tk.Button(top, text="Calculate", command=self.calculation)

        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 
        
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=20)  
  
###############################################################################

    def OnKeyPress(self,event):
        self.p1r.set(' ')
        self.p1_entry.config(state = 'disable')   
        self.p2r.set(' ')
        self.p2_entry.config(state = 'disable')   


    def calculation(self):
        
        z=float(self.zr.get())

        p=1-exp(-z**2/2.)
   
        q=p
        w=1.-q
        
        ps1='%14.9g' %q
        ps2='%14.9g' %w
        
        self.p1r.set(ps1)
        self.p2r.set(ps2)

        self.p1_entry.config(state = 'normal')   
        self.p2_entry.config(state = 'normal')           
        
###############################################################################

def quit(root):
    root.destroy()

###############################################################################