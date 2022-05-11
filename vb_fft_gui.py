################################################################################
# program: vb_fft_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.9
# date: July 18, 2014
# description:  FFT
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

import matplotlib.pyplot as plt

import numpy as np

from math import atan2

from scipy.fftpack import fft

from vb_utilities import WriteData2,WriteData3,sample_rate_check,\
                                                    read_two_columns_from_dialog

from matplotlib.gridspec import GridSpec


class vb_FFT:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
##        self.master.minsize(800,700)
##        self.master.geometry("800x700")
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.23))
        h = int(2.*(h*0.32))
        self.master.geometry("%dx%d+0+0" % (w, h))
  
             
        self.master.title("vb_fft_gui.py ver 1.9  by Tom Irvine")    
  
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
        
        self.hwtext1=tk.Label(top,text='Fast Fourier Transform (FFT)')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)


        crow=crow+1

        self.hwtext2=tk.Label(top, \
            text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)


  ################################################################################

        crow=crow+1

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.E)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=7,sticky=tk.W)

################################################################################

        crow=crow+1
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W)  

################################################################################

        crow=crow+1

        self.hwtext4=tk.Label(top,text='Mean Removal')
        self.hwtext4.grid(row=crow, column=0, columnspan=1, pady=7)

        self.hwtext5=tk.Label(top,text='Window')
        self.hwtext5.grid(row=crow, column=1, columnspan=1, pady=7)

################################################################################

        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "Yes")
        self.Lb1.insert(2, "No")
        self.Lb1.grid(row=crow, column=0, pady=4)
        self.Lb1.select_set(0) 

        self.Lb2 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb2.insert(1, "Rectangular")
        self.Lb2.insert(2, "Hanning")
        self.Lb2.grid(row=crow, column=1, pady=4)
        self.Lb2.select_set(0) 

################################################################################

        crow=crow+1

        self.hwtextf1=tk.Label(top,text='Min Freq (Hz)')
        self.hwtextf1.grid(row=crow, column=0,padx=5, pady=8)

        self.hwtextf2=tk.Label(top,text='Max Freq (Hz)')
        self.hwtextf2.grid(row=crow, column=1,padx=5, pady=8)

################################################################################

        crow=crow+1

        self.f1r=tk.StringVar()  
        self.f1r.set('')  
        self.f1_entry=tk.Entry(top, width = 8,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=0,padx=5, pady=1)

        self.f2r=tk.StringVar()  
        self.f2r.set('')  
        self.f2_entry=tk.Entry(top, width = 8,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=1,padx=5, pady=1)


################################################################################

        crow=crow+1

        self.button_calculate = \
        tk.Button(top, text="Calculate FFT", command=self.fft_calculation)

        self.button_calculate.config( height = 2, width = 18,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=1,padx=8,pady=20) 
            
            
        self.button_replot = \
        tk.Button(top, text="Replot", command=self.fft_replot)
            
        self.button_replot.config( height = 2, width = 18,state = 'disabled')
        self.button_replot.grid(row=crow, column=1,columnspan=1,padx=8,pady=20)       
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=8,pady=20)

################################################################################

        crow=crow+1

        self.s=tk.StringVar()
        self.hwtext5=tk.Label(top,textvariable=self.s)
        self.hwtext5.grid(row=crow, column=0, columnspan=3, pady=7)  

################################################################################

        crow=crow+1

        self.hwtextext_exfft=tk.Label(top,text='Export FFT Data')
        self.hwtextext_exfft.grid(row=crow, column=0,pady=10)  
        self.hwtextext_exfft.config(state = 'disabled')

################################################################################
    
        crow=crow+1

        self.button_fftm = tk.Button(top, text="Magnitude", command=self.export_fftm)
        self.button_fftm.config( height = 2, width = 16,state = 'disabled' )
        self.button_fftm.grid(row=crow, column=0,columnspan=1, pady=1, padx=8)  

        self.button_fftmp = tk.Button(top, text="Magnitude & Phase", \
                                                      command=self.export_fftmp)
        self.button_fftmp.config( height = 2, width = 16,state = 'disabled' )
        self.button_fftmp.grid(row=crow, column=1,columnspan=1, pady=1, padx=8) 

        self.button_fftc = tk.Button(top, text="Complex", command=self.export_fftc)
        self.button_fftc.config( height = 2, width = 16,state = 'disabled' )
        self.button_fftc.grid(row=crow, column=2,columnspan=1, pady=1, padx=8) 
        
################################################################################


    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        dur=self.a[self.num-1]-self.a[0]
        self.dt=dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)

        plt.ion()
        plt.clf()
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Time History')
    
        plt.draw()
        

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')  

        
    def fft_calculation(self):
        noct=int(np.log(self.num)/np.log(2))    
        self.num_fft=2**noct
    
        dur_fft=self.a[self.num_fft-1]-self.a[0]

        bb=self.b[0:self.num_fft]
    
        imr=int(self.Lb1.curselection()[0]) 
        iw=int(self.Lb2.curselection()[0]) 

        if(imr==0 or iw==1):
            bb=bb-np.mean(bb)
    
        if(iw==1):
            H=self.Hanning_initial(self.num_fft)
            bb=bb*H    
    
        df=1/dur_fft
      
        self.z =fft(bb)

        #self.nhalf=self.num_fft/2
        self.nhalf=self.num_fft//2 #added this since python3.5ish
        print (" ")
        print (" %d samples used for FFT " %self.num_fft)
        print ("df = %8.4g Hz" %df)
        
        self.zz=np.zeros(self.nhalf,'f')
        self.ff=np.zeros(self.nhalf,'f')
        self.ph=np.zeros(self.nhalf,'f')

        self.freq=np.zeros(self.num_fft,'f')

        self.z/=float(self.num_fft)

        for k in range(0,self.num_fft):
            self.freq[k]=k*df
    
        self.ff=self.freq[0:self.nhalf]
        
    
        for k in range(0,int(self.nhalf)):    

            if(k > 0):			 
                self.zz[k]=2.*abs(self.z[k])
            else:    
                self.zz[k]= abs(self.z[k])

            self.ph[k]=atan2(self.z.real[k],self.z.imag[k])  

        idx = np.argmax(np.abs(self.zz))        
 
        print (" ")
        print (" Maximum:  Freq=%8.4g Hz   Amp=%8.4g " %(self.ff[idx],self.zz[idx])) 
        
        mstring=" Maximum:  Freq=%8.4g Hz   Amp=%8.4g " %(self.ff[idx],self.zz[idx])
        self.s.set(mstring) 
    
        self.fft_plots(self)

        self.button_replot.config(state = 'normal')  



    def fft_replot(self):
       self.fft_plots(self)


    @classmethod  
    def fft_plots(cls,self):
          
        sx1= self.f1r.get()   
        sx2= self.f2r.get() 
  
        if sx1:
            x1=float(sx1) 
        else:
            x1=0
            self.f1r.set('0')  
            
            
        if sx2:
            x2=float(sx2)
        else:
            x2=self.sr/2.
            ss2='%8.4g' %x2
            self.f2r.set(ss2) 

    
        plt.close(2)
        plt.close(3)    
             
###########################
        
        print('\n view plots ')
        
        nn=len(self.ff)
        
        n1=0
        n2=nn-1
        
        for k in range(0,nn):
            
            n1=k
                        
            if(self.ff[k]>=x1):
                break
                
                
        for k in range(0,nn):
            
            n2=k
                        
            if(self.ff[k]>x2):
                break                
                
        if(n2==nn):
            n2=nn-1
                

        self.ff=self.ff[n1:n2]
        self.ph=self.ph[n1:n2]                
        self.zz=self.zz[n1:n2]  
                 

        y1=-180
        y2= 180
        
        plt.ion()

        fig2=plt.figure(2)
        
        gs1 = GridSpec(2, 1)
                                        
        ax1=plt.subplot(gs1[0,0])   
        plt.plot(self.ff,self.ph*(180./np.pi))
        
        plt.title('FFT Magnitude & Phase')
        plt.grid(True)
        plt.ylabel(' Phase (deg) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.ylim([y1,y2])
        plt.setp( ax1.get_xticklabels(), visible=False)
        plt.yticks([-180,-90,0,90,180])
        plt.draw()      

        plt.subplot(gs1[1,0])
        line2,=plt.plot(self.ff,self.zz)
        
        plt.grid(True)
        plt.ylabel(self.y_string.get()) 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])  
        plt.draw()     
        
        fig2.canvas.mpl_connect('pick_event', DataCursor(plt.gca()))
        line2.set_picker(3) # Tolerance in points        
        
###########################

        fig3=plt.figure(3)     
        line3,=plt.plot(self.ff,self.zz)
        plt.grid(True)
        plt.title(' FFT Magnitude ')
        plt.ylabel(self.y_string.get()) 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])  
        plt.draw()

        fig3.canvas.mpl_connect('pick_event', DataCursor(plt.gca()))
        line3.set_picker(3) # Tolerance in points


        self.hwtextext_exfft.config(state = 'normal')
        self.button_fftm.config(state = 'normal')
        self.button_fftmp.config(state = 'normal')
        self.button_fftc.config(state = 'normal')    
    


                
    def export_fftm(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output FFT filename (freq, mag): ")       
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.ff)
        nb=len(self.zz)        
        n=min(na, nb)        
        
        WriteData2(n,self.ff,self.zz,output_file) 

    def export_fftmp(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                title="Enter the output FFT filename (freq, mag, phase(rad)): ")       
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.ff)
        nb=len(self.zz)        
        n=min(na, nb)   
        
        WriteData3(n,self.ff,self.zz,self.ph,output_file)

    def export_fftc(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                              title="Enter the output FFT (freq, real, imag): ")           
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.freq)
        nb=len(self.z.real)        
        n=min(na, nb)           
        
        WriteData3(n,self.freq,self.z.real,self.z.imag,output_file)
        
        
    @classmethod         
    def Hanning_initial(cls,mmm):
        H=np.zeros(mmm,'f')
        tpi=2*np.pi    
        alpha=np.linspace(0,tpi,mmm)
        ae=np.sqrt(8./3.)
        H=ae*0.5*(1.-np.cos(alpha))                
        return H             

################################################################################
################################################################################

def quit(root):
    root.destroy()
    
class DataCursor(object):
    text_template = 'x: %0.2f\ny: %8.4g'
    x, y = 0.0, 0.0
    xoffset, yoffset = -20, 20
    text_template = 'x: %0.2f\ny: %8.4g'

    def __init__(self, ax):
        self.ax = ax
        self.annotation = ax.annotate(self.text_template, 
                xy=(self.x, self.y), xytext=(self.xoffset, self.yoffset), 
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                )
        self.annotation.set_visible(False)

    def __call__(self, event):
        self.event = event
        # xdata, ydata = event.artist.get_data()
        # self.x, self.y = xdata[event.ind], ydata[event.ind]
        self.x, self.y = event.mouseevent.xdata, event.mouseevent.ydata
        if self.x is not None:
            self.annotation.xy = self.x, self.y
            self.annotation.set_text(self.text_template % (self.x, self.y))
            self.annotation.set_visible(True)
            event.canvas.draw()
                