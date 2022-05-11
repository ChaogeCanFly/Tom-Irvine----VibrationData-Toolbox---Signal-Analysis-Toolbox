################################################################################
# program: vb_damped_sine_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.8
# date: May 12, 2014
# description:  Generate damped sine function
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
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename

           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename
    


from numpy import exp,sin,linspace,zeros

from math import pi

import matplotlib.pyplot as plt

from vb_utilities import WriteData2


class vb_damped_sine:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window

        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))        
        
        
        self.master.title("vb_damped_sine_gui.py ver 1.7  by Tom Irvine")         
                
        self.TT=[]
        self.a =[]    
        self.np=0                
                
 
        crow=0  
 
        self.hwtext1=tk.Label(top,text='Generate Damped Sine Function')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=10,sticky=tk.SW)

################

        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='Amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.SW)
      
        self.hwtext21=tk.Label(top,text='Frequency')
        self.hwtext21.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.SW)           

        crow=crow+1

        self.ampr=tk.StringVar()  
        self.ampr.set('')  
        self.amp_entry=tk.Entry(top, width = 10,textvariable=self.ampr)
        self.amp_entry.grid(row=crow, column=0,padx=10, pady=1,sticky=tk.NW)

        self.freqr=tk.StringVar()  
        self.freqr.set('')  
        self.freq_entry=tk.Entry(top, width = 10,textvariable=self.freqr)
        self.freq_entry.grid(row=crow, column=1,padx=10, pady=1,sticky=tk.NW)

################

        crow=crow+1
        
        self.hwtext3=tk.Label(top,text='Delay Time (sec)')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.SW)
      
        self.hwtext31=tk.Label(top,text='Damping Ratio < 1')
        self.hwtext31.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.SW)           


        crow=crow+1

        self.delayr=tk.StringVar()  
        self.delayr.set('')  
        self.delay_entry=tk.Entry(top, width = 10,textvariable=self.delayr)
        self.delay_entry.grid(row=crow, column=0,padx=10, pady=1,sticky=tk.NW)

        self.dampr=tk.StringVar()  
        self.dampr.set('')  
        self.damp_entry=tk.Entry(top, width = 10,textvariable=self.dampr)
        self.damp_entry.grid(row=crow, column=1,padx=10, pady=1,sticky=tk.NW)
 
################

        crow=crow+1
        
        self.hwtext4=tk.Label(top,text='Duration (sec)')
        self.hwtext4.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.SW)
      
        self.hwtext41=tk.Label(top,text='Sample Rate (Hz)')
        self.hwtext41.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.SW)           


        crow=crow+1

        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 10,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=0,padx=10, pady=1,sticky=tk.NW)

        self.srr=tk.StringVar()  
        self.srr.set('')  
        self.sr_entry=tk.Entry(top, width = 10,textvariable=self.srr)
        self.sr_entry.grid(row=crow, column=1,padx=10, pady=1,sticky=tk.NW)
 
        
###########        
  
        crow=crow+1
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 12)
        self.button_calculate.grid(row=crow, column=0,columnspan=1, padx=10,pady=20) 

        
        self.button_ex = tk.Button(top, text="Export Data", command=self.export)
        self.button_ex.config( height = 2, width = 12,state = 'disabled' )
        self.button_ex.grid(row=crow, column=1,columnspan=1, padx=10,pady=3) 
        
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))

        self.button_quit.config( height = 2, width = 12 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=10,pady=20)

###############################################################################

    def calculation(self):     
        freq=float(self.freqr.get())
        amp=float(self.ampr.get())
        damp=float(self.dampr.get())
        sr=float(self.srr.get())

        dur=float(self.durr.get())

        delay=float(self.delayr.get())

        dt=1./sr
        omega=2.*pi*freq    
    
        if freq>(sr/20):
            sr=freq*20
            dt=1/sr
       
        self.np=int(dur/dt)   
    
   
        self.TT=linspace(0,self.np*dt,(self.np+1))

        self.np=len(self.TT)   
        self.a = zeros(self.np,'f')  
        
        
        for i in range(0,self.np):
            if(self.TT[i]>=delay):
                t=self.TT[i]-delay
                self.a[i] = amp*exp(-damp*omega*t)*sin(omega*t)       

        plt.ion()
        plt.clf()   
        plt.figure(1)

        plt.plot(self.TT, self.a, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel('Amp')  
        plt.title('Damped Sine Time History')
    
        plt.draw()        

        self.button_ex.config(state = 'normal' )


    def export(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n')    
 
        WriteData2(self.np,self.TT,self.a,output_file)


def quit(root):
    root.destroy()        