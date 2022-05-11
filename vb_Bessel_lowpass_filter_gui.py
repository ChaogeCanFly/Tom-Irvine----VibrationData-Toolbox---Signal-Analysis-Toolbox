###########################################################################
# program: vb_Bessel_lowpass_filter.py
# author: Tom Irvine
# version: 1.2
# date: September 11, 2013
# description:  Bessel two-pole lowpass filter
#               The input file must have two columns: time(sec) & amplitude
###########################################################################

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



import numpy as np

import matplotlib.pyplot as plt


from vb_utilities import read_two_columns_from_dialog,\
                                       sample_rate_check,signal_stats,WriteData2

from scipy.signal import lfilter
from math import pi,tan,atan2


#*******************************************************************************

class vb_Bessel_lowpass_filter:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.22))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_Bessel_lowpass_filter_gui.py ver 1.2  by Tom Irvine") 
        
        self.ttime=[]
        self.y=[]
        self.yf=[]
        self.dt=0
        self.fc=0
        self.scale=np.sqrt(3*(-1+np.sqrt(5))/2)

################################################################################        
        
        crow=0

        self.hwtext1b=tk.Label(top,text='This script applies a Bessel two-pole lowpass filter to a time history.')
        self.hwtext1b.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)
        
        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

################################################################################

        crow=crow+1

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, pady=7,sticky=tk.E)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=1,columnspan=3,padx=0, pady=7,sticky=tk.W)
        
################################################################################

        crow=crow+1        
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=1)
        
################################################################################

        crow=crow+1  
        
        self.s1=tk.StringVar()
        self.s1.set("Enter Lowpass Freq (Hz)")
        self.hwtext5=tk.Label(top,textvariable=self.s1)
        self.hwtext5.grid(row=crow, column=0,padx=5, pady=18,sticky=tk.S)    

################################################################################

        crow=crow+1 

        self.fcr=tk.StringVar()
        self.fc_entry=tk.Entry(top, width = 8,textvariable=self.fcr)
        self.fc_entry.grid(row=crow, column=0,padx=3, pady=1,sticky=tk.N)         
        
################################################################################
        
        crow=crow+1  

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0, pady=20,sticky=tk.S) 
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=10,pady=20,sticky=tk.S)
        
################################################################################
    
        crow=crow+1  

        self.button_sav = tk.Button(top, text="Export Filtered Data", command=self.export_fd)
        self.button_sav.config( height = 2, width = 18,state = 'disabled' )
        self.button_sav.grid(row=crow, column=0,columnspan=2, pady=1, padx=1)

################################################################################         
        
            
    def export_fd(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output time history filename: ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.num,self.ttime,self.yf,output_file) 
        
################################################################################        
        
    def calculate(self):
        self.fc=float(self.fcr.get())
        
        OM=tan(pi*self.fc*self.dt/self.scale)

        OM2=OM**2

        den=1+3*OM+3*OM2

        b0=3*OM2/den
        b1=2*b0
        b2=b0

        a1=2*(-1+3*OM2)/den
        a2=(1-3*OM+3*OM2)/den      

        print ("\n Apply filter ")

        bc=[b0,b1,b2]

        ac=[1,a1,a2]
    
        self.yf=lfilter(bc, ac, self.y, axis=-1, zi=None)  

        plt.close(2)
        plt.figure(2)

        plt.plot(self.ttime, self.yf, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        
        out1='Lowpass Filtered Time History fc='+str(self.fc)+' Hz'

        plt.title(out1)

###
    
        fmin=self.fc/100;
        if(fmin>1.):
            fmin=1
    
        fmax=5*self.fc

        nf=1
    
        nf=int(np.ceil(48.*np.log(fmax/fmin)/np.log(2.)))   
    
        print ("\n nf = %d " % nf)

        f=np.zeros(nf,'f')
        H=np.zeros(nf,'complex')
        H_mag=np.zeros(nf,'f')
        H_phase=np.zeros(nf,'f')    
    
        f[0]=fmin
            
        for i in range(1,int(nf)): 
            f[i]=f[i-1]*2**(1./48.)
    
    
        for i in range(0,int(nf)):    
            s=(1J)*(self.scale*f[i]/self.fc)
            H[i]=3./(s**2+3*s+3)
            H_phase[i]=(180./pi)*atan2(H[i].imag,H[i].real)
            H_mag[i]=abs(H[i])

 
        plt.close(3)    
        plt.figure(3)
        plt.plot(f, H_mag)
        title_string= ' Transfer Magnitude  fc='+str(self.fc)+' Hz'
        plt.title(title_string)
        plt.xlabel('Frequency (Hz) ')
        plt.ylabel('Magnitude')
        plt.grid(True, which="both")
        plt.xscale('linear')
        plt.yscale('linear')
        plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
        plt.draw()

        plt.close(4)
        plt.figure(4)
        plt.plot(f, H_phase)
        title_string= ' Transfer Phase  fc='+str(self.fc)+' Hz'
        plt.title(title_string)
        plt.xlabel('Frequency (Hz) ')
        plt.ylabel('Phase(deg)')
        plt.grid(True, which="both")
        plt.xscale('linear')
        plt.draw()

        print ("\n Output Signal ")
        
        sr,self.dt,ave,sd,rms,skewness,kurtosis,dur=signal_stats(self.ttime, self.yf,self.num) 

        self.button_sav.config(state = 'normal') 
                
###
        
    def read_data(self):            
            
        self.ttime,self.y,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        self.ns=self.num
        
        dur=self.ttime[self.num-1]-self.ttime[0]
        self.dt=dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.ttime,self.y,self.num,self.sr,self.dt)
        
        plt.ion()
        plt.clf()
        plt.figure(1)

        plt.plot(self.ttime, self.y, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Time History')
    
        plt.draw()

        print ("\n Input Signal ")
        print ("\n samples = %d " % self.num)
        
        sr,self.dt,ave,sd,rms,skewness,kurtosis,dur=signal_stats(self.ttime, self.y,self.num) 
 
        self.button_calculate.config(state = 'normal')  
         
################################################################################

def quit(root):
    root.destroy()

################################################################################