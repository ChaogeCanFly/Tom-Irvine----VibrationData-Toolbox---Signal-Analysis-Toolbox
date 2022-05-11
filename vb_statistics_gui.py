################################################################################
# program: vb_statistics_gui.py
# author: Tom Irvine
# version: 1.7
# date: October 24, 2014
# description:  Descriptive statistics of an signal.
#               The input file must have two columns: time(sec) & amplitude
################################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
        

import matplotlib.pyplot as plt

import numpy as np


from vb_utilities import read_two_columns_from_dialog,signal_stats,sample_rate_check


class vb_statistics:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
#        self.master.minsize(800,800)
#        self.master.geometry("800x800")
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.35))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        
        self.master.title("vb_statistics_gui.py ver 1.7  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Descriptive Statistics of Time History Signal')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text= \
                 'The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

################################################################################

        crow=crow+1

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label ')
        self.hwtext3.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W)
        
        self.hwtext12=tk.Label(top,text='Histogram Bins')
        self.hwtext12.grid(row=crow, column=3, columnspan=1, padx=10, pady=7,sticky=tk.W)    
                
################################################################################

        crow=crow+1
        
        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)

        self.bins_string=tk.StringVar()  
        self.bins_string.set('31')  
        self.bins_string_entry=tk.Entry(top, width = 10,textvariable=self.bins_string)
        self.bins_string_entry.grid(row=crow, column=3,columnspan=1,padx=10, pady=7,sticky=tk.W)        

################################################################################

        crow=crow+1 
        
        self.hwtext11=tk.Label(top,text='Results')
        self.hwtext11.grid(row=crow, column=1, columnspan=3, pady=10)
        
        
################################################################################        
        
        crow=crow+1  

        self.textWidget = tk.Text(top, width=36, height = 19)
        self.textWidget.grid(row=crow, column=1,columnspan=3, pady=10)      
        
################################################################################

        crow=crow+1         

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=1,columnspan=1, pady=10,sticky=tk.W)   
        
        self.button_replot_histogram = tk.Button(top, text="Replot Histogram",command=self.replot_histogram)
        self.button_replot_histogram.config( height = 2, width = 15, state = 'disabled')
        self.button_replot_histogram.grid(row=crow, column=2,columnspan=1,padx=10, pady=10,sticky=tk.W)

 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=3,columnspan=1, padx=10,pady=20)
      
################################################################################

 
    def replot_histogram(self):        
      
        self.plot_histogram(self)
        
    @classmethod    
    def plot_histogram(cls,self):

        plt.close(2)
        plt.figure(2)  
        nbins=int(self.bins_string.get())
        hist, bins = np.histogram(self.b, bins=nbins, density=False)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width) 
        plt.ylabel('Counts')
        plt.xlabel(self.y_string.get())
        plt.title('Histogram')
        plt.draw()          
      
        plt.close(3)
        plt.figure(3)  
        nbins=int(self.bins_string.get())
        hist, bins = np.histogram(self.b, bins=nbins, density=False)
        
        cumulative = np.cumsum(hist)                
        
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, cumulative, align = 'center', width = width) 
        plt.ylabel('Counts')
        plt.xlabel(self.y_string.get())
        plt.title('Cumulative Histogram')
        plt.draw()   


        plt.close(4)
        plt.figure(4)  
        nbins=np.floor(0.5*int(self.bins_string.get()))
        hist, bins = np.histogram(self.v, bins=nbins, density=False)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width) 
        plt.ylabel('Counts')
        plt.xlabel(self.y_string.get())
        plt.title('Absolute Peak Histogram')
        plt.draw()           
      
      
################################################################################      

    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        dur=self.a[self.num-1]-self.a[0]
        self.dt=dur/float(self.num)
        
        self.sr=1./self.dt
        
        sr,dt,mean,sd,rms,skew,kurtosis,dur=signal_stats(self.a,self.b,self.num)
        
        bb=self.b-mean

        v=differentiate_function(bb,self.num,self.dt)

        rf=(np.std(v)/np.std(self.b))/(2*np.pi);


        amax=max(self.b) 
        amin=min(self.b)
        aamin=abs(amin)        
        
        mmax=amax;
        
        if(aamin>mmax):
            mmax=aamin

        crest=mmax/sd            
       
###############################################################################
       
        y=np.zeros(self.num,'f')
        self.v=np.zeros(self.num,'f')       
       
        y=self.b
        k=0
        self.v[0]=y[0]

        k=1

        for i in range (1,(self.num-1)):
            
            slope1=(  y[i]-y[i-1])
            slope2=(y[i+1]-y[i])

            if((slope1*slope2)<=0):
                self.v[k]=y[i]
                k+=1
                 
            
        last_v=k        
        self.v[k]=y[self.num-1]    
        
        self.v=abs(self.v[0:last_v])
        
#        for i in range (0,last_v):
#            print ("%8.4g" %self.v[i])            
            
       
###############################################################################       

        
        q_sr=  " sample rate = %8.4g sps \n" %sr
        q_dt=  "   time step = %8.4g sec \n\n" %dt

        q_dur= "    duration = %8.4g sec  \n" %dur
        q_num= "         num = %9.6g  \n\n" %self.num             
        
        q_mean="        mean = %8.4g \n" %mean
        q_sd=  "     std dev = %8.4g \n" %sd
        q_rms= "         rms = %8.4g \n\n" %rms
        
        q_max= "         max = %8.4g \n" %amax
        q_min= "         min = %8.4g \n" %amin
        q_crest="crest factor = %8.4g \n\n" %crest


        q_skew="    skewness = %8.4g \n" %skew       
        q_kurt="    kurtosis = %8.4g \n\n" %kurtosis
        
        q_rf=" Rice Characteristic Frequency \n   = %8.4g Hz " %rf
        
        self.textWidget.delete(1.0, tk.END)
        
        self.textWidget.insert('1.0',q_sr)
        self.textWidget.insert('end',q_dt)
        
        self.textWidget.insert('end',q_dur)       
        self.textWidget.insert('end',q_num)
          
        self.textWidget.insert('end',q_max)       
        self.textWidget.insert('end',q_min) 
        self.textWidget.insert('end',q_crest)        
        
        self.textWidget.insert('end',q_mean)  
        self.textWidget.insert('end',q_sd)  
        self.textWidget.insert('end',q_rms)          

        self.textWidget.insert('end',q_skew)       
        self.textWidget.insert('end',q_kurt)         
        
        self.textWidget.insert('end',q_rf) 
                      
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)
        
        self.button_replot_histogram.config(state = 'normal')         

        plt.ion()
        plt.clf()           
        plt.close(1)
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Input Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.plot_histogram(self)
        
     
# textWidget.insert('1.0',"A Value")              

  
################################################################################
  
def differentiate_function(y,n,dt):
    """
    y is a 1-D array.
    n is the length of y
    dt is the time step
    Return: v is the differentiated functino
    """    
    ddt=12.*dt
    
    v=np.zeros(n,'f')

    v[0]=( -y[2]+4.*y[1]-3.*y[0] )/(2.*dt)
    v[1]=( -y[3]+4.*y[2]-3.*y[1] )/(2.*dt)

    for i in range (2,n-2):
        v[i]=( -y[i+2] +8.*y[i+1] -8.*y[i-1] +y[i-2] ) / ddt
    
    v[n-2]=( y[n-2]-y[n-4] )/(2.*dt)
    v[n-1]=( y[n-2]-y[n-3] )/dt          
    
    return v

def quit(root):
    root.destroy()