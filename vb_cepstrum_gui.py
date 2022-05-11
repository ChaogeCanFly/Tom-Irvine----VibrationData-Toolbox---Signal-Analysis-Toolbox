###############################################################################
# program: vb_cepstrum_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.3
# date: September 17, 2013
# description:
#
#  This script calculates the cepstrum & autocepstrum of a time history signal.
#
#  The time history must have two columns: time(sec) & amplitude
#
###############################################################################

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



from vb_utilities import read_two_columns_from_dialog,sample_rate_check 


from math import log,log10,atan2,pi

from numpy import zeros,mean

from numpy import argmax,linspace

from scipy.fftpack import fft,ifft

from scipy.signal import correlate

import matplotlib.pyplot as plt

###############################################################################

class vb_cepstrum:

    def __init__(self,parent):        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window        

        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.16))
        h = int(2.*(h*0.22))
        self.master.geometry("%dx%d+0+0" % (w, h))        
        
        
        self.master.title("vb_cepstrum_gui.py ver 1.2  by Tom Irvine") 

        self.a=[]
        self.b=[]
        self.num=0
        self.dt=0        
        self.sr=0
        
        
        crow=0

        self.hwtext1=tk.Label(top,text='Cepstrum Functions')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=10,sticky=tk.W)
        
        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=10,sticky=tk.W)

###############################################################################

        crow=crow+1

        self.button_read = tk.Button(top, text="Read Input File", command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=20,sticky=tk.W)  

###############################################################################

        crow=crow+1

        self.hwtext5=tk.Label(top,text='Select Analysis')
        self.hwtext5.grid(row=crow, column=0, columnspan=1, pady=10)

        self.hwtext4=tk.Label(top,text='Mean Removal')
        self.hwtext4.grid(row=crow, column=1, columnspan=1, padx=20, pady=10)

###############################################################################

        crow=crow+1
        
        self.Lb_cp = tk.Listbox(top,height=3,exportselection=0)
        self.Lb_cp.insert(1, "Cepstrum")
        self.Lb_cp.insert(2, "Auto Cepstrum")
        self.Lb_cp.insert(3, "Both")        
        self.Lb_cp.grid(row=crow, column=0, pady=4,sticky=tk.N)
        self.Lb_cp.select_set(0)  
        

        self.Lb_mr = tk.Listbox(top,height=2,exportselection=0)
        self.Lb_mr.insert(1, "Yes")
        self.Lb_mr.insert(2, "No")
        self.Lb_mr.grid(row=crow, column=1, padx=20, pady=4,sticky=tk.N)
        self.Lb_mr.select_set(0) 

###############################################################################

        crow=crow+1

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0, pady=20) 
        
        root=self.master 
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=10,pady=20)

###############################################################################

    def read_data(self):      
        
        plt.close('all')
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Acceleration File',self.master)
        
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
        plt.ylabel('Amplitude')  
        plt.title('Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal') 
        
        
    def calculate(self):
        
###############################################################################
        
        ian=int(self.Lb_cp.curselection()[0])
        imr=int(self.Lb_mr.curselection()[0]) 
        
        if(imr==0):
            self.b=self.b-mean(self.b)        
       
        idx,freq,ff,z,zz,ph,nhalf,df,num_fft=FFT(self.a,self.b,self.dt).fft_data()        
       
        fig_num=2

        if(ian!=1):

            plt.close(fig_num)        
            plt.figure(fig_num)
            fig_num=fig_num+1
            plt.plot(ff,zz)
            plt.grid(True)
            plt.title(' FFT Magnitude ')
            plt.ylabel(' Amplitude ')
            plt.xlabel(' Frequency (Hz) ')
            plt.grid(True, which="both")
            plt.draw()  

            plt.figure(fig_num)
            fig_num=fig_num+1
            plt.plot(ff,ph*(180./pi))
            plt.grid(True)
            plt.title(' FFT Phase ')
            plt.ylabel(' Phase (deg) ')
            plt.xlabel(' Frequency (Hz) ')
            plt.grid(True, which="both")
            plt.draw()      

            a=z.real + z.imag*1j

            nnn=len(a)

            b=zeros(nnn,'f')

            for i in range(0,nnn):
                b[i]=log10(abs(a[i]))

            NHS=len(ff) 

            plt.figure(fig_num)
            fig_num=fig_num+1
            plt.plot(ff,b[0:NHS])
            plt.grid(True)
            plt.title(' log(abs(fft(a)) ')
            plt.ylabel(' Magnitude ')
            plt.xlabel(' Frequency (Hz) ')
            plt.grid(True, which="both")
            plt.draw() 

            c=ifft(b)

            plt.close(fig_num)
            plt.figure(fig_num)
            fig_num=fig_num+1

            plt.plot(self.a[1:int(NHS)],(c[1:int(NHS)].real))
            plt.title('Cepstrum  ifft(log(abs(fft(a))))')
            plt.ylabel('Amplitude')
            plt.xlabel('Quefrency(sec)')
            plt.grid(True) 
            plt.draw()        
        
###############################################################################

        if(ian>=1):
            
            FFT_autocepstrum(self.a,self.b,self.dt,fig_num).FFT_acc()    
    
    
        plt.show() 

###############################################################################    

class FFT_autocepstrum:

    def __init__(self,t,amp,dt,fig_num):
        self.t=t
        self.amp=amp
        self.dt=dt
        self.fig_num=fig_num
        
    def FFT_acc(self):   

        ac = correlate(self.amp,self.amp)

        n=len(ac)

        ac=2*ac/n

        dur=n*self.dt/2;
        d=linspace( -dur, dur, n )


        plt.figure(self.fig_num)
        self.fig_num=self.fig_num+1
        plt.plot(d, ac, linewidth=1.0)
        plt.xlabel('Delay(sec)')
        plt.ylabel('Rxx')
        plt.grid(True)
        plt.title('Autocorrelation')
        plt.draw()


        idx,freq,ff,z,zz,ph,nhalf,df,num_fft=FFT(d,ac,self.dt).fft_data()   
    
        plt.figure(self.fig_num)     
        self.fig_num=self.fig_num+1
        plt.plot(ff,zz)
        plt.grid(True)
        plt.title(' FFT Magnitude of Autocorrelation ')
        plt.ylabel(' Amplitude ')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.draw()  


        plt.figure(self.fig_num)     
        self.fig_num=self.fig_num+1
        plt.plot(ff,ph*(180./pi))
        plt.grid(True)
        plt.title(' FFT Phase of Autocorrelation')
        plt.ylabel(' Phase (deg) ')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.draw()      

# a=z.real + z.imag*1j
        a=z

        nnn=len(a)

        b=zeros(nnn,'f')

        for i in range(0,nnn):
            b[i]=log10(abs(a[i]))

        nf=len(ff)

        plt.figure(self.fig_num)
        self.fig_num=self.fig_num+1     
        plt.plot(ff[0:nf],b[0:nf])
        plt.grid(True)
        plt.title('log(abs(fft(autocorrelation))')
        plt.ylabel(' Magnitude ')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.draw()  

############################################################################# 

        c=ifft(b)

        plt.figure(self.fig_num)
        self.fig_num=self.fig_num+1 

        plt.plot(self.t[1:nf],(c[1:nf].real))
        plt.title('Autocepstrum  ifft(log(abs(fft(autocorrelation))))')
        plt.ylabel('Amplitude')
        plt.xlabel('Quefrency(sec)')
        plt.grid(True) 
        plt.draw()  

###############################################################################

class FFT:

    def __init__(self,a,b,dt):
        self.a=a
        self.b=b
        self.dt=dt

        
    def fft_data(self):
        
#   Truncate to 2**n

        num=len(self.b)

        noct=int(log(num)/log(2))

        num_fft=2**noct

        bb=self.b[0:num_fft]

        dur_fft=num_fft*self.dt

        df=1/dur_fft
      
        
        z =fft(bb)

        nhalf=num_fft/2

        print (" ")
        print (" %d samples used for FFT " %num_fft)
        print ("df = %8.4g Hz" %df)

        zz=zeros(nhalf,'f')
        ff=zeros(nhalf,'f')
        ph=zeros(nhalf,'f')

        freq=zeros(num_fft,'f')

        z/=float(num_fft)

        for k in range(0,num_fft):
            freq[k]=k*df
    
        ff=freq[0:nhalf]
        

    
        for k in range(0,int(nhalf)):    

            if(k > 0):			 
                zz[k]=2.*abs(z[k])
            else:    
                zz[k]= abs(z[k])

            ph[k]=atan2(z.real[k],z.imag[k])
  

        idx = argmax(abs(zz))        

        print (" ")
        print (" Maximum:  Freq=%8.4g Hz   Amp=%8.4g " %(ff[idx],zz[idx]))
 
        return idx,freq,ff,z,zz,ph,nhalf,df,num_fft 
    
###############################################################################

def quit(root):
    root.destroy()    