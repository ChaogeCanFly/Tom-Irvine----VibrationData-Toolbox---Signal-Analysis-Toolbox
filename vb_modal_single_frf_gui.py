################################################################################
# program: vb_modal_single_frf_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.2
# date: November 12, 2014
# description:  Calculate the frf from a force and response time history
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
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    import tkinter.messagebox as tkMessageBox    
    

from numpy import array,zeros,log,log10,pi,sqrt,linspace,round,ceil,interp

from numpy import mean

from math import atan2

import matplotlib.pyplot as plt

from vb_utilities import WriteData2,WriteData3

from scipy.fftpack import fft

from matplotlib.gridspec import GridSpec


class vb_modal_single_frf:

    def __init__(self,parent,t,c): 
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()        
        w = int(2.*(w*0.22))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_modal_single_frf_gui.py ver 1.2  by Tom Irvine")         
                
        self.fig_num=1    
        
        self.c=c
        self.t=t
        L=len(t)
        Lm1=L-1
        self.dt=(t[Lm1]-t[0])/Lm1
        
                
###############################################################################     
     
        crow=0
        
        self.hwtext1=tk.Label(top,text='Calculate the frf from a force and response time history, single record')
        self.hwtext1.grid(row=crow, column=0,columnspan=4, pady=6,sticky=tk.W)        
        
        crow=crow+1    
        
        self.hwtext3=tk.Label(top,text='Response Type')
        self.hwtext3.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S)                 

        self.hwtext4=tk.Label(top,text='Unit')
        self.hwtext4.grid(row=crow, column=1, columnspan=1, padx=4, pady=10,sticky=tk.S) 
        
        crow=crow+1        
        
        self.Lb1 = tk.Listbox(top,height=3,exportselection=0)
        self.Lb1.grid(row=crow, column=0, columnspan=1, padx=4, pady=10,sticky=tk.S)      
        self.Lb1.insert(1, "Acceleration")
        self.Lb1.insert(2, "Velocity")
        self.Lb1.insert(3, "Displacement")
        self.Lb1.select_set(0)  
        
        self.runitr=tk.StringVar()  
        self.runitr.set('G')  
        self.runit_entry=tk.Entry(top, width = 9,textvariable=self.runitr)
        self.runit_entry.grid(row=crow, column=1,padx=4, pady=1,sticky=tk.N)           
        
        crow=crow+1    
        
        self.hwtext5=tk.Label(top,text='Select Input Unit')
        self.hwtext5.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S)
        
        self.hwtext6=tk.Label(top,text='Mean Removal')
        self.hwtext6.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)       
        
        crow=crow+1        
        
        self.Lb2 = tk.Listbox(top,height=2,width=13,exportselection=0)
        self.Lb2.grid(row=crow, column=0, columnspan=1, padx=4, pady=10,sticky=tk.S)        
        self.Lb2.insert(1, "Force (lbf)")
        self.Lb2.insert(2, "Force (N)")
        self.Lb2.select_set(0)  
      
        self.Lb3 = tk.Listbox(top,height=2,width=6,exportselection=0)
        self.Lb3.grid(row=crow, column=1, columnspan=1, padx=4, pady=10,sticky=tk.S)        
        self.Lb3.insert(1, "yes")
        self.Lb3.insert(2, "no")
        self.Lb3.select_set(0)      
      
        crow=crow+1    
        
        self.hwtext7=tk.Label(top,text='Plot Frequencies (Hz)')
        self.hwtext7.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.S)      
      
        crow=crow+1    
      
        self.hwtext8=tk.Label(top,text='Minimum')
        self.hwtext8.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S) 
        
        self.hwtext9=tk.Label(top,text='Maximum')
        self.hwtext9.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)       
      
        crow=crow+1   
             
        self.fminr=tk.StringVar()   
        self.fmin_entry=tk.Entry(top, width = 12,textvariable=self.fminr)
        self.fmin_entry.grid(row=crow, column=0,padx=4, pady=1,sticky=tk.N)          
        
        self.fmaxr=tk.StringVar()   
        self.fmax_entry=tk.Entry(top, width = 12,textvariable=self.fmaxr)
        self.fmax_entry.grid(row=crow, column=1,padx=4, pady=1,sticky=tk.N)  


        crow=crow+1    
        
        self.button_calculate = tk.Button(top, text="Calculate FRF", command=self.calculation)
        self.button_calculate.config( height = 2, width = 18)
        self.button_calculate.grid(row=crow, column=0, pady=20)         
        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,pady=20) 
        

        crow=crow+1

        self.hwtextext_exfft=tk.Label(top,text='Export Transfer Function Data')
        self.hwtextext_exfft.grid(row=crow, column=0,columnspan=2,pady=10)  
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
        
        
###############################################################################
        
    def calculation(self):
      
        nLb1= int(self.Lb1.curselection()[0])         
        nLb2= int(self.Lb2.curselection()[0])   
        nLb3= int(self.Lb3.curselection()[0])           
        
        if(nLb3==1):
            self.c[:,0]-=mean(self.c[:,0])
            self.c[:,1]-=mean(self.c[:,1])


##        print('max1 %8.4g' %max(self.c[:,0]))
##        print('max2 %8.4g' %max(self.c[:,1]))
            
###

        self.f1=float(self.fminr.get())
        self.f2=float(self.fmaxr.get())

        x1=self.f1
        x2=self.f2
       
###   
        num=len(self.t)

        dur=self.t[num-1]-self.t[0]

        dt=dur/float(num-1) 
        
                
                  
###  
        N=2**int(ceil(log(num)/log(2.)))            

        z1 =fft(self.c[:,0],n=N)
        z2 =fft(self.c[:,1],n=N)

        num_fft=len(z1)
        nhalf=int(num_fft/2.)
        
        df=1./(num_fft*dt)  

        print (" ")
        print (" %d samples used for FFT " %num_fft)
        print ("df = %8.4g Hz" %df)

        self.trans=zeros(nhalf,dtype=complex)
        self.freq=zeros(nhalf,'f') 
        self.ph=zeros(nhalf,'f') 
 
        nn=0
        for i in range(0,nhalf):
            self.trans[i]=z2[i]/z1[i]
            self.ph[i]=atan2(self.trans.imag[i],self.trans.real[i])
            self.freq[i]=i*df
            nn+=1
            if(self.freq[i]>=(x2-df)):
                break
            
        self.trans=self.trans[0:nn]    
        self.ph=self.ph[0:nn]            
        self.freq=self.freq[0:nn] 
###                    

        plt.ion()
        plt.close(1)  
        plt.figure(1)

        plt.plot(self.t, self.c[:,0], linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')

        
        if(nLb2==0):        
            plt.ylabel('Force (lbf)')
            force_unit='lbf'
        else:
            plt.ylabel('Force (N)')  
            force_unit='N'            
        
        plt.title('Applied Force Time History')
    
        plt.draw()


        plt.close(2)  
        plt.figure(2)

        plt.plot(self.t, self.c[:,1], linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')

        
        ss=self.runitr.get()        
        amp_unit=ss
        
        if(nLb1==0):        
            ylab='Accel'+ss 
            plt.title('Acceleration Response Time History')
            ylab_FT=' Accel/Force ' +str("(%s/%s)" %(amp_unit,force_unit))
    
        if(nLb1==1):        
            ylab='Vel'+ss 
            plt.title('Velocity Response Time History')  
            ylab_FT=' Vel/Force ' +str("(%s/%s)" %(amp_unit,force_unit)) 
             
        if(nLb1==2):
            ylab='Disp'+ss 
            plt.title('Displacement Response Time History')              
            ylab_FT=' Disp/Force ' +str("(%s/%s)" %(amp_unit,force_unit)) 

        plt.ylabel(ylab)  
        
    
        plt.draw()
        
###      

        y1=-180
        y2= 180

        plt.close(3)
        fig3=plt.figure(3)
        
        gs1 = GridSpec(3, 1)
                                  
        ax1=plt.subplot(gs1[:-2, :])   
        plt.plot(self.freq,self.ph*(180./pi))
        
        plt.title('Transfer Function Magnitude & Phase')
        plt.grid(True)
        plt.ylabel(' Phase (deg) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.ylim([y1,y2])
        plt.setp( ax1.get_xticklabels(), visible=False)
        plt.yticks([-180,-90,0,90,180])
        plt.draw()      

        plt.subplot(gs1[-2:0, :])
        line3,=plt.plot(self.freq,abs(self.trans))
        
        plt.grid(True)
        plt.ylabel(ylab_FT) 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.xscale('log')
        plt.yscale('log')        
        plt.draw()  

        fig3.canvas.mpl_connect('pick_event', DataCursor(plt.gca()))
        line3.set_picker(3) # Tolerance in points          
        
###########################
        plt.close(4)
        fig4=plt.figure(4)     
        line4,=plt.plot(self.freq,abs(self.trans))
        plt.grid(True)
        plt.title(' Transfer Function ')
        plt.ylabel(ylab_FT) 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.xscale('log')
        plt.yscale('log')
        plt.draw()
        
        fig4.canvas.mpl_connect('pick_event', DataCursor(plt.gca()))
        line4.set_picker(3) # Tolerance in points     
        
        

        self.hwtextext_exfft.config(state = 'normal')
        self.button_fftm.config(state = 'normal')
        self.button_fftmp.config(state = 'normal')
        self.button_fftc.config(state = 'normal')            
                                 
###    
                                 
    def export_fftm(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output FFT filename (freq, mag): ")       
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.freq)
        nb=len(self.trans)        
        n=min(na, nb)        
        
        WriteData2(n,self.freq,abs(self.trans),output_file) 

    def export_fftmp(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                title="Enter the output FFT filename (freq, mag, phase(rad)): ")       
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.freq)
        nb=len(abs(self.trans))        
        n=min(na, nb)   
        
        WriteData3(n,self.freq,abs(self.trans),self.ph,output_file)     

    def export_fftc(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                              title="Enter the output FFT (freq, real, imag): ")           
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.freq)
        nb=len(self.trans.real)        
        n=min(na, nb)           
        
        WriteData3(n,self.freq,self.trans.real,self.trans.imag,output_file)                            

###############################################################################
                      
def quit(root):
    root.destroy()
                       
###############################################################################  
                       
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
                                           