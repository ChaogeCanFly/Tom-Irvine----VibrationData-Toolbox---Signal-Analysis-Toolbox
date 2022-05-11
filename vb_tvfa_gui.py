################################################################################
# program: vb_tvfa_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 12, 2014
# description:  Time varying frequency & amplitude
#               
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

from numpy import sqrt,pi,zeros,array,floor,mean,std

from scipy import stats

from vb_utilities import read_two_columns_from_dialog,sample_rate_check


class vb_tvfa:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.18))
        h = int(2.*(h*0.18))
        self.master.geometry("%dx%d+0+0" % (w, h))        
        
        
        self.master.title("vb_tvfa.py ver 1.0  by Tom Irvine")    
        
###############################################################################


        self.a=[]
        self.b=[]
        self.ac=[]
        self.d=[]        
        self.num=0    
        self.dt=0    
        self.n=0        


        crow=0

        self.hwtext1=tk.Label(top,text='Time Varying Frequency & Amplitude')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.W)

        crow+=1 

        self.hwtext2=tk.Label(top, \
            text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=3,sticky=tk.W)
        

################################################################################
  
        crow+=1 

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, columnspan=2, padx=5,pady=11,sticky=tk.W)
        
        crow+=1 

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=5,sticky=tk.N)
        
################################################################################
  
        crow+=1 

        self.hwtext5=tk.Label(top,text='Enter Segment Duration (sec)')
        self.hwtext5.grid(row=crow, column=0, columnspan=2, padx=5,pady=11,sticky=tk.W)

        crow+=1 

        self.segment_durationr=tk.StringVar()  
        self.segment_durationr.set('')  
        self.segment_duration_entry=tk.Entry(top, width = 12,textvariable=self.segment_durationr)
        self.segment_duration_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=5,sticky=tk.N)        

################################################################################

        crow+=1 
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, padx=1,pady=10,sticky=tk.W)     


        self.button_calculate = \
                     tk.Button(top, text="Calculate", command=self.calculate)

        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=1,columnspan=1, padx=10,pady=10) 
        
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=10,pady=10)
        
###############################################################################

    def calculate(self):

        amp=self.b
        tim=self.a
        seg=float(self.segment_durationr.get())

        n = len(amp)
        
        mu=mean(amp)
        sd=std(amp)
        mx=max(amp)
        mi=min(amp)
        rms=sqrt(sd**2+mu**2)

        kt=0.
        tt_max=0.
        tt_min=0.

        for i in range(0,n):
            if( amp[i]==mx):
                tt_max=tim[i]
        
            if( amp[i]==mi):
                tt_min=tim[i]

        kt=stats.kurtosis(amp,fisher=False)

        print(' ')
        print(' time stats ')
        print(' ')
        tmx=max(tim)
        tmi=min(tim)

        print(' start  = %g sec     = %g sec            ' %(tmi,tmx))

        dt=(tmx-tmi)/float(n)

        sr=1./dt

        print(' SR  = %8.4g samples/sec    dt = %8.4g sec  ' %(sr,dt))
        print('\n number of samples = %d  ' %n)

        print(' ')
        print(' amplitude stats ')
        print(' ')
            
        print(' number of points = %d '%n)
        print(' mean = %8.4g    std = %8.4g    rms = %8.4g ' %(mu,sd,rms))
        print(' max  = %9.4g  at  = %8.4g sec            ' %(mx,tt_max))
        print(' min  = %9.4g  at  = %8.4g sec            ' %(mi,tt_min))
        print('\n kurtosis  = %8.4g ' %(kt))

        dur=tmx-tmi

        if(seg>dur/4):
            seg=dur/4
            ss='%8.3g' %seg
            self.segment_durationr.set(ss)

        ns=int(floor(sr*seg))

        nnn=int(floor((tmx-tmi)/seg))
        
        print('\n ns=%d  nnn=%d \n' %(ns,nnn))

        zc=zeros(nnn,'f')
        sds=zeros(nnn,'f')
        rms=zeros(nnn,'f')
        av=zeros(nnn,'f')
        peak=zeros(nnn,'f')
        tt=zeros(nnn,'f')

        j=0
        for i in range(0,nnn):
            if((j+ns)>n):
                break
            
            zc[i]=0
            x=zeros(ns,'f')
            x=amp[j:j+ns]   
            sds[i]=std(x)
            av[i]=mean(x)
            peak[i]=max(abs(x))
            rms[i]=sqrt( sds[i]**2 + av[i]**2 )
            tt[i]=(tim[j]+tim[j+ns])/2.

            for k in range(1,len(x)): 
                if(x[k]*x[k-1]<0):
                    zc[i]=zc[i]+1        

            j=j+ns

        n=len(tt)
                
        if(n>=1):
            if(tt[n-1]<tt[n-2]):
                tt.pop(n)
                sds.pop(n)
                av.pop(n)             
                peak.pop(n)
                rms.pop(n)
            
        freq=zc/(2*seg)
        
        plt.figure(2)
        plt.plot(tt, peak, linewidth=1.0, label="peak")        # disregard error  
        plt.plot(tt, rms,  linewidth=1.0, label="rms")        # disregard error  
        plt.plot(tt, sds,  linewidth=1.0, label="std dev")        # disregard error  
        plt.plot(tt, av,   linewidth=1.0, label="mean")        # disregard error          
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Segmented Time History')
        plt.legend(loc="upper right")  
        x1,x2,y1,y2 = plt.axis()
        plt.axis((x1,x2,y1,2*y2))
        plt.draw()
    
     
        plt.figure(3)
        plt.plot(tt, freq, linewidth=1.0)        # disregard error        
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel('Frequency (Hz)')  
        plt.title('Frequency')
        plt.draw()


        plt.figure(4)
        plt.plot(freq,peak,linestyle='None',marker="*")        # disregard error        
        plt.grid(True)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel(self.y_string.get())  
        plt.title('Peak vs. Frequency')
        plt.draw()
        plt.show()

###############################################################################                   

    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        self.a=array(self.a)
        self.b=array(self.b)        
        
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
        plt.title('Input Time History')
    
        plt.draw()
        plt.show()

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')    
        
###############################################################################
        
def quit(root):
    root.destroy()                    