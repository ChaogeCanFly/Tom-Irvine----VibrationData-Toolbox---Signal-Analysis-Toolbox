################################################################################
# program: vb_peak_sigma_random_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.6
# date: September 11, 2013
# description:  SDOF system peak sigma response to random base input
#
################################################################################
# 
# Note:  for use within Spyder IDE, set: 
#    
# Run > Configuration > Interpreter >
#    
# Excecute in an external system terminal
#
################################################################################

from __future__ import print_function

import sys

if sys.version_info[0] == 2:
    import Tkinter as tk
           
if sys.version_info[0] == 3:   
    import tkinter as tk 
    


import numpy as np


class vb_peak_sigma_random :

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.24))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_peak_sigma_random_gui.py ver 1.6  by Tom Irvine")    
  
        self.mstring=''
        self.num=0
        self.num_fft=0
        self.nhalf=0
        self.freq=[]
        self.ff=[]
        self.zz=[]
        self.z=[]
        self.ph=[]
        
        self.a=[]
        self.b=[]
        
        crow=0

        self.hwtext1=tk.Label(top,text=' ')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=0,sticky=tk.W)

        crow=crow+1
        
        self.hwtext1=tk.Label(top,text='Consider a single-degree-of-freedom system subjected to a stationary')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=0,sticky=tk.W)

        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='random vibration base input. This script calculates the maximum expected  ')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=0,sticky=tk.W)

        crow=crow+1
        
        self.hwtext3=tk.Label(top,text='peak response in terms of the sigma value, via the Rayleigh distribution.  ')
        self.hwtext3.grid(row=crow, column=0, columnspan=6, pady=0,sticky=tk.W)
        


################################################################################

        crow=crow+1

        self.hwtextf1=tk.Label(top,text='Enter Natural Frequency (Hz)')
        self.hwtextf1.grid(row=crow, column=0,padx=20, pady=20)

        self.hwtextf2=tk.Label(top,text='Enter Duration (sec)')
        self.hwtextf2.grid(row=crow, column=2,padx=5, pady=20)

################################################################################

        crow=crow+1

        self.fnr=tk.StringVar()  
        self.fnr.set('')  
        self.fn_entry=tk.Entry(top, width = 8,textvariable=self.fnr)
        self.fn_entry.grid(row=crow, column=0,padx=5, pady=1)
        self.fn_entry.bind("<KeyRelease>", self.OnKeyPress)         

        self.Tr=tk.StringVar()  
        self.Tr.set('')  
        self.T_entry=tk.Entry(top, width = 8,textvariable=self.Tr)
        self.T_entry.grid(row=crow, column=2,padx=5, pady=1)
        self.T_entry.bind("<KeyRelease>", self.OnKeyPress)  

################################################################################

        crow=crow+1

        self.button_calculate = \
        tk.Button(top, text="Calculate", command=self.calculation)

        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0,columnspan=2, pady=20) 
        
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=2, padx=10,pady=20)

        crow=crow+1
        
        self.hwtext_res=tk.Label(top,text='Peak Response Value')
        self.hwtext_res.grid(row=crow, column=0,padx=20, pady=20)        

        crow=crow+1
        
        self.psr=tk.StringVar()  
        self.psr.set('')  
        self.ps_entry=tk.Entry(top, width = 16,textvariable=self.psr)
        self.ps_entry.grid(row=crow, column=0,padx=5, pady=1,sticky=tk.N) 
        self.ps_entry.config(state = 'disabled')
        

################################################################################

    def OnKeyPress(self,event):
        self.psr.set(' ')
        self.ps_entry.config(state = 'disable')        


    def calculation(self):
        
        self.ps_entry.config(state = 'normal')
 
        fn= float(self.fnr.get())   
        T = float(self.Tr.get())        
 
        a=fn*T
        c=np.sqrt(2*np.log(a));
        ps=c + 0.5772/c
        
        pss="%7.3g sigma" %ps        
        
        self.psr.set(pss)
    
################################################################################

def quit(root):
    root.destroy()