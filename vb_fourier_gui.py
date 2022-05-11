################################################################################
# program: vb_fourier_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 2.0
# date: May 23, 2014
# description:  Fourier Transform
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
    import ttk
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename     
    import tkinter.ttk as ttk    

import matplotlib.pyplot as plt

import numpy as np

from math import atan2

from time import sleep


from vb_utilities import WriteData2,WriteData3,sample_rate_check,\
                                                    read_two_columns_from_dialog

from matplotlib.gridspec import GridSpec

class vb_Fourier:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
#        self.master.minsize(800,800)
#        self.master.geometry("800x800")
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.35))
        self.master.geometry("%dx%d+0+0" % (w, h))
                
        
        self.master.title("vb_fourier_gui.py ver 2.0  by Tom Irvine")    
  
  
        self.mstring=''
        
        self.a=[]
        self.b=[]

        self.num=0 
        
        self.dur=0

        self.ff=[]
        self.freq=[]

        self.zz=[]
        self.z=[] 
        
        self.ph=[]
        self.f_real=[]
        self.f_imag=[]
        self.idx=0
        self.nhalf=0
        
        self.f1r=0
        self.f2r=0
        
        self.dt=0
        

        crow=0

        self.hwtext1=tk.Label(top,text='Fourier Transform')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)


        crow+=1 

        self.hwtext2=tk.Label(top, \
            text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=3,sticky=tk.W)
        
        crow+=1 

        self.hwtext13=tk.Label(top, text='The number of input points should be <= 10000 for speed.')
        self.hwtext13.grid(row=crow, column=0, columnspan=6, pady=3,sticky=tk.W)


        crow+=1 

        self.hwtext14=tk.Label(top, text='Otherwise, an FFT should be used instead.')
        self.hwtext14.grid(row=crow, column=0, columnspan=6, pady=3,sticky=tk.W)

################################################################################
  
        crow+=1 

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, columnspan=2, pady=11,sticky=tk.E)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=11,sticky=tk.W)

################################################################################

        crow+=1 
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W)  

################################################################################

        crow+=1 

        self.hwtext4=tk.Label(top,text='Mean Removal')
        self.hwtext4.grid(row=crow, column=0, columnspan=1, pady=7)

        self.hwtext5=tk.Label(top,text='Window')
        self.hwtext5.grid(row=crow, column=1, columnspan=1, pady=7)

################################################################################

        crow+=1 

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

        crow+=1 

        self.hwtextf1=tk.Label(top,text='Min Freq (Hz)')
        self.hwtextf1.grid(row=crow, column=0,padx=5, pady=8)

        self.hwtextf2=tk.Label(top,text='Max Freq (Hz)')
        self.hwtextf2.grid(row=crow, column=1,padx=5, pady=8)

################################################################################

        crow+=1 

        self.f1r=tk.StringVar()  
        self.f1r.set('')  
        self.f1_entry=tk.Entry(top, width = 8,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=0,padx=5, pady=1)

        self.f2r=tk.StringVar()  
        self.f2r.set('')  
        self.f2_entry=tk.Entry(top, width = 8,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=1,padx=5, pady=1)


################################################################################

        crow+=1 

        self.button_calculate = \
        tk.Button(top, text="Calculate", command=self.Fourier_calculation)

        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=1, padx=8,pady=20) 
        
        self.button_replot = \
        tk.Button(top, text="Replot", command=self.Fourier_replot)
            
        self.button_replot.config( height = 2, width = 18,state = 'disabled')
        self.button_replot.grid(row=crow, column=1,columnspan=1,padx=8,pady=20)  
        
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=10,pady=20)

###############################################################################

        crow+=1

        self.hwtext9=tk.Label(top,text='Progress')
        self.hwtext9.grid(row=crow, column=0, columnspan=1, pady=8,sticky=tk.E)
        
        self.pbar = ttk.Progressbar(top, orient='horizontal', mode='determinate')   
        self.pbar.grid(row=crow, column=1,columnspan=2, padx=5, pady=1,sticky=tk.W)

################################################################################

        crow+=1 

        self.s=tk.StringVar()
        self.hwtext5=tk.Label(top,textvariable=self.s)
        self.hwtext5.grid(row=crow, column=0, columnspan=3, pady=5)  

################################################################################

        crow+=1 

        self.hwtext_exFT=\
                        tk.Label(top,text='Export Fourier Transformation Data')
        self.hwtext_exFT.grid(row=crow, column=0,pady=6)  
        self.hwtext_exFT.config(state = 'disabled')

################################################################################
    
        crow+=1 

        self.button_Fourier_Transformationm = \
           tk.Button(top, text="Magnitude", command=self.export_Fourier_Transformationm)
        self.button_Fourier_Transformationm.config( height = 2, width = 18,state = 'disabled' )
        self.button_Fourier_Transformationm.grid(row=crow, column=0,columnspan=1, pady=1, padx=8)  

        self.button_Fourier_Transformationmp = tk.Button(top, text="Magnitude & Phase", \
                                                      command=self.export_Fourier_Transformationmp)
        self.button_Fourier_Transformationmp.config( height = 2, width = 20,state = 'disabled' )
        self.button_Fourier_Transformationmp.grid(row=crow, column=1,columnspan=1, pady=1, padx=8) 

        self.button_Fourier_Transformationc = \
           tk.Button(top, text="Complex", command=self.export_Fourier_Transformationc)
        self.button_Fourier_Transformationc.config( height = 2, width = 18,state = 'disabled' )
        self.button_Fourier_Transformationc.grid(row=crow, column=2,columnspan=1, pady=1, padx=8) 
        
################################################################################


    def read_data(self):          
        
        self.s.set('  ')  
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        self.dur=self.a[self.num-1]-self.a[0]
        self.dt=self.dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)
        
        plt.ion()
        plt.clf()
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Input Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')  
        
        
    def Fourier_replot(self):
        self.Fourier_plots(self)       


    def Fourier_calculation(self):
        
        tpi=2.*np.pi

        self.dur=self.num*self.dt

        df=1./self.dur

        self.z=np.zeros(self.num,'f')
        self.freq=np.zeros(self.num,'f')

        self.f_real=np.zeros(self.num,'f')
        self.f_imag=np.zeros(self.num,'f')

        self.nhalf=int(float(self.num)/float(2))

        self.ph=np.zeros(self.nhalf,'f')
        self.zz=np.zeros(self.nhalf,'f')
        self.ff=np.zeros(self.nhalf,'f')
        
        imr=int(self.Lb1.curselection()[0]) 
        iw=int(self.Lb2.curselection()[0]) 

        if(imr==0 or iw==1):
            self.b=self.b-np.mean(self.b)
    
        if(iw==1):
            H=self.Hanning_initial(self.num)
            self.b=self.b*H         
        
        
        numf=float(self.num)

        ijk=0
        
        N=int(self.num)

        LLL=int(float(self.num)/20.)

#        print (" ")
#        print (" progress ")
#        print ("0   1   2   3   4   5   6   7   8   9   10")


        self.pbar['value'] = 0
        self.pbar['maximum'] = N
        
        self.freq = np.linspace(0,N*df,N) 
            
        for k in range (0,N):
  
            ijk+=1  
  
            if(ijk==LLL):
#                stdout.write("*")
                ijk=0
                self.pbar['value'] = k
                self.pbar.update()  #this works
                sleep(0.1)
                self.pbar.update_idletasks()
  

            arg = np.linspace(0,tpi*k*(self.num-1)/self.num,self.num) 

            sum_c=sum(self.b*np.cos(arg))
            sum_s=sum(self.b*np.sin(arg))

            self.f_real[k]+=sum_c
            self.f_imag[k]+=sum_s


            self.f_real[k]/=numf
            self.f_imag[k]/=(-numf)

            self.z[k]=np.sqrt((self.f_real[k]**2) + (self.f_imag[k]**2))

            if(k<self.nhalf):  
                if(k > 0):			 
                   self.zz[k]=2.*self.z[k];
                else:    
                   self.zz[k]= self.z[k];
            
                self.ff[k]=self.freq[k];
                self.ph[k]=atan2(self.f_real[k],self.f_imag[k]);
  
  
        self.pbar.stop()
        idx = np.argmax(self.zz)      
        
        print (" ")
        print (" Maximum:  Freq=%8.4g Hz   Amp=%8.4g " %(self.ff[idx],self.zz[idx])) 
        mstring=" Maximum:  Freq=%8.4g Hz   Amp=%8.4g " %(self.ff[idx],self.zz[idx])      

        self.s.set(mstring) 
        
        self.Fourier_plots(self)
        self.button_replot.config(state = 'normal')         
        
        
    @classmethod  
    def Fourier_plots(cls,self):       
        
        sx1= self.f1r.get()   
        sx2= self.f2r.get() 
  
        if sx1:
            if sx2:
                x1=float(sx1)  
                x2=float(sx2)  
    
    
        plt.ion()
        plt.close(2)
        plt.close(3)
                
             
###########################
        
        print('\n view plots ')

        y1=-180
        y2= 180

        fig2=plt.figure(2)
        
        gs1 = GridSpec(3, 1)
                                  
        ax1=plt.subplot(gs1[:-2, :])   
        plt.plot(self.ff,self.ph*(180./np.pi))
        
        plt.title('Fourier Magnitude & Phase')
        plt.grid(True)
        plt.ylabel(' Phase (deg) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.ylim([y1,y2])
        plt.setp( ax1.get_xticklabels(), visible=False)
        plt.yticks([-180,-90,0,90,180])
        plt.draw()      

        plt.subplot(gs1[-2:0, :])
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
        plt.plot(self.ff,self.zz)
        plt.grid(True)
        plt.title(' Fourier Magnitude ')
        plt.ylabel(self.y_string.get()) 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.draw()
        
        fig3.canvas.mpl_connect('pick_event', DataCursor(plt.gca()))
        line3.set_picker(3) # Tolerance in points     
          
###########################   
    
    
        self.hwtext_exFT.config(state = 'normal')
        self.button_Fourier_Transformationm.config(state = 'normal')
        self.button_Fourier_Transformationmp.config(state = 'normal')
        self.button_Fourier_Transformationc.config(state = 'normal')    
            

################################################################################
        
                
    def export_Fourier_Transformationm(self):
        output_file_path = asksaveasfilename(parent=self.master,\
               title="Enter the output Fourier Transformation filename (freq, mag): ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.nhalf,self.ff,self.zz,output_file) 

    def export_Fourier_Transformationmp(self):
        output_file_path = asksaveasfilename(parent=self.master,\
               title="Enter the output Fourier Transformation filename (freq, mag, phase(rad)): ")       
        output_file = output_file_path.rstrip('\n')
        WriteData3(self.nhalf,self.ff,self.zz,self.ph,output_file)

    def export_Fourier_Transformationc(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                              title="Enter the output Fourier Transformation (freq, real, imag): ")           
        output_file = output_file_path.rstrip('\n')
        WriteData3(self.num,self.freq,self.z.real,self.z.imag,output_file)
        
        
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
                    