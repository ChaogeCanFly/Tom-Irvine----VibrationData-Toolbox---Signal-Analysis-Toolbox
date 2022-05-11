###########################################################################
# program: vb_sine_curvefit_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 2, 2014
# description:  Sine & Damped Sine Curve-fit script.
#               The input file must have two columns: time(sec) & amplitude
###############################################################################

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

import numpy as np

import matplotlib.pyplot as plt

from scipy.fftpack import fft


from vb_utilities import read_two_columns_from_dialog,sample_rate_check,WriteData2


###############################################################################

class vb_sine_curvefit:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))        

        self.master.title("vb_sine_curvefit_gui.py  ver 1.0  by Tom Irvine")  

        self.dt=0
        self.sr=0
        self.num=0
        
        self.start_time=0
        self.end_time=0          
        
        self.num_sines=0       
        self.ntrials=0        
        
        self.ttime=[]
        self.y=[]
        
        self.tp=2*np.pi


################################################################################        
        
        crow=0

        self.hwtext1b=tk.Label(top,text='This script performs a sine or damped sine curve-fit for a time history.')
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
        
        self.hwtext4=tk.Label(top,text='Select Type')
        self.hwtext4.grid(row=crow, column=0, pady=7)               
        
        self.hwtext5=tk.Label(top,text='Enter Number of Sines')
        self.hwtext5.grid(row=crow, column=1, pady=7)           
                
        self.hwtext6=tk.Label(top,text='Enter Trials per Frequency')
        self.hwtext6.grid(row=crow, column=2, pady=7)       
        
################################################################################
        
        crow=crow+1

        self.Lb3 = tk.Listbox(top,height=3,width=16,exportselection=0)
        self.Lb3.insert(1, "Sine")
        self.Lb3.insert(2, "Damped Sine")
        self.Lb3.grid(row=crow, column=0, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lb3.select_set(0)        

        self.num_sines=tk.StringVar()  
        self.num_sines_entry=tk.Entry(top, width = 12,textvariable=self.num_sines)
        self.num_sines_entry.grid(row=crow, column=1,padx=10, pady=1,sticky=tk.N)

        self.ntrials=tk.StringVar()  
        self.ntrials.set('100000')  
        self.ntrials_entry=tk.Entry(top, width = 12,textvariable=self.ntrials)
        self.ntrials_entry.grid(row=crow, column=2,padx=10, pady=1,sticky=tk.N)
        
################################################################################

        crow=crow+1

        self.hwtext7=tk.Label(top,text='Start Time (sec)')
        self.hwtext7.grid(row=crow, column=0, pady=7)           
                
        self.hwtext8=tk.Label(top,text='End Time (sec)')
        self.hwtext8.grid(row=crow, column=1, pady=7)    

################################################################################

        crow=crow+1

        self.start_time=tk.StringVar()  
        self.start_time_entry=tk.Entry(top, width = 12,textvariable=self.start_time)
        self.start_time_entry.grid(row=crow, column=0,padx=10, pady=4)

        self.end_time=tk.StringVar()  
        self.end_time_entry=tk.Entry(top, width = 12,textvariable=self.end_time)
        self.end_time_entry.grid(row=crow, column=1,padx=10, pady=4)
        
        
################################################################################

        crow=crow+1        
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=10,pady=10)
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate_main)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=1,padx=10, pady=10,sticky=tk.S) 
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2, padx=10,pady=10,sticky=tk.S)        
        
 ################################################################################       

    def calculate_main(self):
        self.ntype= int(self.Lb3.curselection()[0])  

        self.ts=float(self.start_time.get())
        self.te=float(self.end_time.get())          
        
        self.nfr=1
            
        try:
            ix=int(self.num_sines.get())
            if(ix>=1 and ix<=10000):
                self.nfr=ix
        except ValueError:
            pass
        else:
            pass

        if(self.nfr==1):
            self.num_sines.set('1')
        
        self.nt=int(self.ntrials.get())
 
        self.s_amp=self.y                 
        self.s_tim=self.ttime
        
        self.tmi=min(self.s_tim)
        self.tmx=max(self.s_tim)


        if(self.ts>self.tmx):
            self.ts=self.tmi

        if(self.te<self.tmi):
            self.ts=self.tmx
          
        self.n1=int(np.floor((self.ts-self.tmi)/self.dt))
        self.n2=int(np.floor((self.te-self.tmi)/self.dt))
        
        self.n=len(self.s_tim)


        if(self.n1<0):
            self.n1=1

        if(self.n2>self.n):
            self.n2=self.n

        self.t=self.s_tim[self.n1:self.n2]

        self.a=self.s_amp[self.n1:self.n2]

        self.np=len(self.t)

        self.n=self.np
        self.num2=self.np        
        
        self.running_sum=np.zeros(self.n,'f')

        self.fmax=0.

# automatically estimate frequencies from FFT & zero-crossings

        self.istr=2  
        
        self.fl=np.zeros(self.nfr,'f')
        self.fu=np.zeros(self.nfr,'f')   
         
        for i in range(0,self.nfr):

            self.fu[i]=self.sr/8
     

        self.dur=self.t[self.num2-1]-self.t[0]

        self.dt=self.dur/(self.num2-1)
        self.sr=1./self.dt 

        self.x1r=np.zeros(self.nfr,'f')
        self.x2r=np.zeros(self.nfr,'f')
        self.x3r=np.zeros(self.nfr,'f')
        self.x4r=np.zeros(self.nfr,'f')
        self.x5r=np.zeros(self.nfr,'f')

       
        if(self.ntype==0):
            self.sine_curvefit_main(self)
            
            self.syn=np.zeros(self.n,'f')
    
            for ie in range(0,self.nfr):
	
                for i in range(0,self.n):

                    tt=self.t[i]-self.t[0]
                    self.syn[i]=self.syn[i]+self.x1r[self.ie]*np.sin(self.x2r[self.ie]*tt-self.x3r[self.ie])
            
        else:
            self.damped_sine_curvefit_main(self)         
            
            self.syn=np.zeros(self.n,'f')
    
            for self.ie in range(0,self.nfr):
                
                domegan=self.x4r[self.ie]*self.x2r[self.ie];
                omegad=self.x2r[self.ie]*np.sqrt(1.-self.x4r[self.ie]**2);
	
                for i in range(0,self.n):
                    
                    tt=self.t[i]-self.t[0]       
                    
                    if( tt > self.x5r[self.ie] ):
                        ta=tt-self.x5r[self.ie]            
                        self.syn[i]=self.syn[i]+self.x1r[self.ie]*np.exp(-domegan*ta)*np.sin(omegad*ta-self.x3r[self.ie])
          
            
        
#        print('plot data')
        
        plt.close(2)
        plt.figure(2)
            
        plt.plot(self.s_tim,self.s_amp, label="original")
        plt.plot(self.t,self.syn, label="synthesis")
        plt.legend(loc="upper right")                   
        plt.ylabel(self.y_string.get())                  
        plt.xlabel('Time(sec)')
        plt.draw()         
        
        
    @classmethod
    def damped_sine_curvefit_main(cls,self):
        
        for self.ie in range(0,self.nfr):

            print("\n frequency case %d \n" %(self.ie+1))

            self.flow=self.fl[self.ie]
            self.fup =self.fu[self.ie]

            self.sf_engine2(self)
            
        print(' ')
        print(' Results')
        print(' ')
        print(' Case   Amplitude   fn(Hz)    Phase(rad)  damp  delay(sec) ')

        for self.ie in range(0,self.nfr):
            m=self.ie+1
            print(' %d    %9.4f  %9.4f  %9.4f %9.4f %9.4f  '\
            %(m,self.x1r[self.ie],self.x2r[self.ie]/self.tp,self.x3r[self.ie],self.x4r[self.ie],self.x5r[self.ie]))
            
###############################################################################
            

    @classmethod
    def sine_curvefit_main(cls,self):
        
        for self.ie in range(0,self.nfr):

            print("\n frequency case %d \n" %(self.ie+1))
 
            self.flow=self.fl[self.ie]
            self.fup =self.fu[self.ie]
            
            self.sfa_engine(self)
  
             
        print(' ')
        print(' Results')
        print(' ')
        print(' Case   Amplitude   fn(Hz)    Phase(rad)  ')

        for ie in range(0,self.nfr):
            m=ie+1
            print(' %d    %9.4f    %9.4f  %9.4f' %(m,self.x1r[self.ie],self.x2r[self.ie]/self.tp,self.x3r[self.ie]))

###############################################################################

    @classmethod
    def fft_data(cls,self):
        
#   Truncate to 2**n

        num=len(self.a)

        noct=int(np.log(num)/np.log(2))

        num_fft=2**noct

        bb=self.a[0:num_fft]
        

        dur_fft=self.t[num_fft-1]-self.t[0]

        df=1/dur_fft
      
        z =fft(bb)

        nhalf=num_fft/2

        print (" ")
        print (" %d samples used for FFT " %num_fft)
        print ("df = %8.4g Hz" %df)

        zz=np.zeros(nhalf,'f')
        ff=np.zeros(nhalf,'f')

        freq=np.zeros(num_fft,'f')

        z/=float(num_fft)

        for k in range(0,int(num_fft)):
            freq[k]=k*df
    
        ff=freq[0:nhalf]
        
    
        for k in range(0,int(nhalf)):    

            if(k > 0):			 
                zz[k]=2.*abs(z[k])
            else:    
                zz[k]= abs(z[k])
  

        idx = np.argmax(abs(zz)) 
        
        self.fft_freq=ff[idx]
  
  


    @classmethod
    def sfa_engine(cls,self):
        
        self.yr=np.zeros(self.nt,'f')

        self.find_starting_frequency(self)
 
        sd=np.std(self.a)

        am=sd

        errormax=1.0e+53
        
        tz=float(self.t[0])   
        
        ta=np.zeros(self.n,'f')        
        
        for i in range(0,self.n):
            ta[i]=float(self.t[i])-tz        

        print(' ')
        print('  Trial     Error      Amplitude   Freq(Hz)   Phase(rad)  ')

        jk=0

        for j in range(0,self.nt):
            
            if(np.random.random()<0.5):
                freq_est=self.zcf
            else:    
                freq_est=self.fft_freq
        
            jk=jk+1
           
            if(jk==10000):
                print('\n %ld ' %(j+1))
                jk=0
    
            x1=np.random.random()
            x2=np.random.random()
            x3=np.random.random()
      
            x1= am*(x1**2)
            x2=((self.fup-self.flow)*x2+self.flow)*self.tp
            x3=x3*self.tp
 
            if(np.random.random()<0.8):
                x2=freq_est*self.tp*(0.98+0.04*np.random.random())

            if(np.random.random()<0.5 and j>int(np.floor(self.nt/10))):
      
                x1=self.x1r[self.ie]
                x2=self.x2r[self.ie]
                x3=self.tp*np.random.random()
    
            if(np.random.random()<0.4 and j>int(np.floor(self.nt/10))):
      
                x1=self.x1r[self.ie]
                x2=self.x2r[self.ie]
                x3=self.x3r[self.ie]+self.tp*(0.05-0.1*np.random.random())
    

            if(np.random.random()<0.3 and j>int(np.floor(self.nt/10))):
      
                x1=self.x1r[self.ie]*(0.98+0.04*np.random.random())
                x2=self.x2r[self.ie]
                x3=self.x3r[self.ie]
    
            if(np.random.random()<0.2 and j>int(np.floor(self.nt/10))):
      
                x1=self.x1r[self.ie]
                x2=self.x2r[self.ie]*(0.98+0.04*np.random.random())
                x3=self.x3r[self.ie]
    
        
            if(np.random.random()<0.1 and j>int(np.floor(self.nt/10))):
      
                x1=self.x1r[self.ie]*(0.98+0.04*np.random.random())
                x2=self.x2r[self.ie]*(0.98+0.04*np.random.random())
                x3=self.x3r[self.ie]+self.tp*(0.05-0.1*np.random.random())
    
        
            if(x2 > self.fup*self.tp ):
                x2 = self.fup*self.tp
        
            if(x2 < self.flow*self.tp):
                x2 = self.flow*self.tp
    
            if(j==0):
                x1=0.
            else:
                if(x1<1.0e-12):
                    x1=am*np.random.random()
        
            x1=abs(x1)

            mt=len(self.t)
            error=np.zeros(mt,'f')
            y=np.zeros(mt,'f')
                        
            y=x1*np.sin(x2*ta-x3)
                    
            error=self.a-y

            if(np.std(error)<errormax):

                self.syna=-(error-self.a)
                self.error_rth=error
                errormax=np.std(error)
		 
                self.x1r[self.ie]=x1
                self.x2r[self.ie]=x2
                self.x3r[self.ie]=x3
                self.yr=y

                print(' %6ld  %13.4e  %10.4g %9.4f %9.4f  ' %(j,errormax,x1,x2/self.tp,x3))



        self.cnew=np.zeros(self.n,'f')
                                                        
#        for i in range(0,n):
#            self.cnew[i]=self.running_sum[i]+self.yr[i]  
			
        self.cnew=self.running_sum+self.yr   
   
        self.a=self.error_rth

        ave=np.mean(self.a)  
        sd=np.std(self.a)
	
        print('\n  ave=%12.4g  sd=%12.4g \n' %(ave,sd))
        
        self.running_sum=self.syna


###############################################################################

    @classmethod
    def find_starting_frequency(cls,self):
       
        self.zcf=0
        self.fft_freq=0


        self.amp=self.a-np.mean(self.a)
        
        self.n=len(self.amp)        
        
        nzc=0
        pzc=0
        
        mh=len(self.a)-2
        
#        print('  mh=%d  ' %mh)  
        
        for i in range(0,mh):

           if(self.amp[i] <=0 and self.amp[i+1] > 0):
               pzc=pzc+1
       
           if(self.amp[i] >=0 and self.amp[i+1] < 0):
               nzc=nzc+1      
       
#        print('  nzc=%d   pzc=%d  ' %(nzc,pzc))        
       
        self.zcf=((pzc+nzc)/2)/self.dur  
        
        self.fft_data(self)
        

        print(' zero crossing frequency = %8.4g Hz ' %self.zcf)   

        print(' FFT frequency = %8.4g Hz ' %self.fft_freq)
    
###############################################################################

    @classmethod
    def sf_engine2(cls,self):
        
        self.yr=np.zeros(self.nt,'f')

        self.find_starting_frequency(self)
 
        sd=np.std(self.a)


        errormax=1.0e+53
        
        tz=float(self.t[0])   
        
        ta=np.zeros(self.n,'f')        
        
        for i in range(0,self.n):
            ta[i]=float(self.t[i])-tz  


        dur=max(ta)-min(ta)

        print(' ')
        print(' i   Error    Amplitude   Freq(Hz)   Phase(rad)  damp  delay(sec) ')


        for j in range(0,self.nt):

            if(np.random.random()<0.5):
                freq_est=self.zcf
            else:    
                freq_est=self.fft_freq
            
                r6=np.random.random()   
                r7=np.random.random()  

            if(j<10 or r6<0.5):
                
                r1=0.9+0.2*np.random.random()
                r2=0.9+0.2*np.random.random()
                r3=np.random.random()
                r4=np.random.random()
                r5=np.random.random()                
            
                x1=max(self.amp)*r1
                x2=self.tp*freq_est*r2
                x3=self.tp*r3
                x4=0.20*r4
                x5=0.03*dur*r5             

            else:
                
                if(r7<0.7):
                    r1=0.99+0.02*np.random.random()                
                    r2=0.99+0.02*np.random.random()  
                    r3=0.99+0.02*np.random.random()  
                    r4=0.99+0.02*np.random.random()  
                    r5=0.99+0.02*np.random.random()  
                else:
                    r1=0.98+0.04*np.random.random()                
                    r2=0.98+0.04*np.random.random()  
                    r3=0.98+0.04*np.random.random()  
                    r4=0.98+0.04*np.random.random()  
                    r5=0.98+0.04*np.random.random()                   
                
                x1=self.x1r[self.ie]*r1
                x2=self.x2r[self.ie]*r2
                x3=self.x3r[self.ie]*r3
                x4=self.x4r[self.ie]*r4
                x5=self.x5r[self.ie]*r5                  
            
            

            error=0.
        
            domegan=x4*x2
            omegad=x2*np.sqrt(1.-x4**2)


            tb=np.zeros(self.n,'f')

            for i in range(0,self.n):
                if(ta[i]>x5):
                    nq=i
                    break
                    
                
            tb=ta[nq:self.n]-x5                
                
            self.yr=np.zeros(self.n,'f') 
            
            self.yr[nq:self.n]=x1*np.exp(-domegan*tb)*np.sin(omegad*tb-x3)
                
            error=np.sum(abs(self.amp-self.yr))
  
            error=np.sqrt(error)

            if(error<errormax):

                self.x1r[self.ie]=x1
                self.x2r[self.ie]=x2
                self.x3r[self.ie]=x3
                self.x4r[self.ie]=x4
                self.x5r[self.ie]=x5

                print(' %6d %8.3e %8.3g %9.4f %9.4f %9.4f %8.3f ' \
                                             %(j,error,x1,x2/self.tp,x3,x4,x5))
          
                errormax=error
                
                self.yq=self.yr
                

        self.a=(self.a-self.yq)
    
        ave=np.mean(self.a)   
        sd=np.std(self.a)
   
        print('\n  ave=%12.4g  sd=%12.4g \n' %(ave,sd))


###############################################################################

    def read_data(self):            
            
        self.ttime,self.y,self.num=read_two_columns_from_dialog('Select Input File',self.master)

        for index, item in enumerate(self.ttime):
            self.ttime[index] = float(item)        
    
        for index, item in enumerate(self.y):
            self.y[index] = float(item)    
            
        
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

        print ("\n samples = %d " % self.num)
 
        self.button_calculate.config(state = 'normal')  
         
################################################################################

def quit(root):
    root.destroy()

################################################################################  