##########################################################################
# program: vb_normal_gui.py
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
    

from math import erfc,sqrt


    
######################################################################## 

class vb_normal:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.18))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_normal_gui.py ver 1.0  by Tom Irvine") 
        
        
        crow=0        
        
        self.hwtext1=tk.Label(top,text='This script integrates the normal distribution to find the probability between two limits.')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)


###############################################################################

        crow=crow+1

        self.hwtext1 = tk.Label(top, text="Enter Lower Limit z1")
        self.hwtext1.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)
        
        self.hwtext3 = tk.Label(top, text="Probability within limits")
        self.hwtext3.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.S)       
        
        crow=crow+1
        
        self.z1r=tk.StringVar()  
        self.z1r.set('')  
        self.z1_entry=tk.Entry(top, width = 10,textvariable=self.z1r)
        self.z1_entry.grid(row=crow, column=0,sticky=tk.N)    
        self.z1_entry.bind("<KeyRelease>", self.OnKeyPress)  
        
        self.p1r=tk.StringVar()  
        self.p1r.set('')  
        self.p1_entry=tk.Entry(top, width = 16,textvariable=self.p1r)
        self.p1_entry.grid(row=crow, column=1,padx=5, pady=1,sticky=tk.N) 
        self.p1_entry.config(state = 'disable')        
        
        crow=crow+1

        self.hwtext2 = tk.Label(top, text="Enter Upper Limit z2")
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)
       
        self.hwtext5 = tk.Label(top, text="Probability of exceeding limits")
        self.hwtext5.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.S)        
       
        crow=crow+1
        
        self.z2r=tk.StringVar()  
        self.z2r.set('')  
        self.z2_entry=tk.Entry(top, width = 10,textvariable=self.z2r)
        self.z2_entry.grid(row=crow, column=0,sticky=tk.N)         
        self.z2_entry.bind("<KeyRelease>", self.OnKeyPress)       
     
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
        
        z1=float(self.z1r.get())
        z2=float(self.z2r.get())
        
        if(z1>z2):
            temp=z1
            z1=z2
            z2=temp
        
        normal_cdf = lambda x: ( 1./2.*erfc(-x/sqrt(2.)))
        
        p1 = normal_cdf(z1)
        p2 = normal_cdf(z2)
   
        q=p2-p1
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