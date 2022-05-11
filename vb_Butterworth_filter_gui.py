################################################################################
# program: vb_Butterworth_filter_gui.py
# author: Tom Irvine
# version: 2.1
# date: January 16, 2015
# description:  Butterworth sixth-order filter
#               The input file must have two columns: time(sec) & amplitude
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

import numpy as np

import matplotlib.pyplot as plt



from vb_utilities import read_two_columns_from_dialog,\
                                       sample_rate_check,signal_stats,WriteData2

from scipy.signal import lfilter
from math import pi,cos,sin,tan

from matplotlib.gridspec import GridSpec 

################################################################################

class vb_Butterworth_filter:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.26))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_Butterworth_filter_gui.py ver 2.1  by Tom Irvine")         
        
        self.dt=0
        self.sr=0
        
        self.f=0
        self.fl=0
        self.fh=0
        
        self.freq=0
        
        self.f1=0
        self.f2=0
        
        self.ttime=[]
        self.y=[]
        self.yt=[]
        
        self.l=6
        
        self.iphase=0
        self.iband=0  
        
        self.ns=0
                
################################################################################        
        
        crow=0

        self.hwtext1b=tk.Label(top,text='This script applies a sixth-order Butterworth filter to a time history.')
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

        self.hwtext4=tk.Label(top,text='Select Filter Type')
        self.hwtext4.grid(row=crow, column=1,padx=10, pady=7)    
        
        self.hwtext5=tk.Label(top,text='Refiltering for Phase Correction?')
        self.hwtext5.grid(row=crow, column=2,padx=10, pady=7)          

################################################################################

        crow=crow+1        
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=1)
                        
        self.Lb_ws = tk.Listbox(top,height=3,exportselection=0)
        self.Lb_ws.insert(1, "lowpass")
        self.Lb_ws.insert(2, "highpass")
        self.Lb_ws.insert(3, "bandpass")        
        self.Lb_ws.grid(row=crow, column=1,padx=10,sticky=tk.N)
        self.Lb_ws.select_set(0)
        self.Lb_ws.bind('<<ListboxSelect>>',self.set_labels)
        
        self.Lb_pc = tk.Listbox(top,height=3,exportselection=0)
        self.Lb_pc.insert(1, "yes")
        self.Lb_pc.insert(2, "no")
        self.Lb_pc.grid(row=crow, column=2,padx=10,sticky=tk.N)
        self.Lb_pc.select_set(0)        

################################################################################

        crow=crow+1  
        
        self.s1=tk.StringVar()
        self.s1.set("Enter Lowpass Freq (Hz)")
        self.hwtext5=tk.Label(top,textvariable=self.s1)
        self.hwtext5.grid(row=crow, column=0,padx=5, pady=18,sticky=tk.S)    

        self.s2=tk.StringVar()           
        self.s2.set(" ")
        self.hwtext6=tk.Label(top,textvariable=self.s2)
        self.hwtext6.grid(row=crow, column=1,padx=10, pady=18,sticky=tk.S)  

################################################################################

        crow=crow+1 

        self.f1r=tk.StringVar()
        self.f1_entry=tk.Entry(top, width = 8,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=0,padx=3, pady=1,sticky=tk.N)        

        self.f2r=tk.StringVar()
        self.f2_entry=tk.Entry(top, width = 8,textvariable=self.f2r,state = 'disabled')
        self.f2_entry.grid(row=crow, column=1,padx=3, pady=1,sticky=tk.N)   
        
################################################################################

        crow=crow+1  

        self.button_calculate = tk.Button(top, text="Calculate", command=self.Butterworth_filter_main)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0, pady=20,sticky=tk.S) 
        
        self.button_transfer = tk.Button(top, text="Display Transfer Function", command=self.Butterworth_transfer)
        self.button_transfer.config( height = 2, width = 26)
        self.button_transfer.grid(row=crow, column=1, pady=20,sticky=tk.S)         
        
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2, padx=10,pady=20,sticky=tk.S)
        
################################################################################
    
        crow=crow+1  

        self.button_sav = tk.Button(top, text="Export Filtered Data", command=self.export_fd)
        self.button_sav.config( height = 2, width = 16,state = 'disabled' )
        self.button_sav.grid(row=crow, column=0,columnspan=2, pady=1, padx=1)         

################################################################################
    
    def export_fd(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output time history filename: ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.num,self.ttime,self.y,output_file) 

################################################################################

    def set_labels(self,val):       
        sender=val.widget
        n= int(sender.curselection()[0])
        
        self.s2.set("")
        
        self.f2_entry.config(state = 'disabled') 
        
        if(n==0):
            self.s1.set("Low Pass Freq (Hz)")
            
        if(n==1):
            self.s1.set('High Pass Freq (Hz)')            
            
        if(n==2):
            self.s1.set('Lower Freq (Hz)') 
            self.s2.set('Higher Freq (Hz)') 
            self.f2_entry.config(state = 'normal')             
        
        
###############################################################################        
        
    def Butterworth_transfer(self):

        ntype= int(self.Lb_ws.curselection()[0]) 
        self.iband=ntype+1        
        
        nref= int(self.Lb_pc.curselection()[0]) 
        self.iphase=nref+1
        

        print ('iband=%d' %self.iband)
        print ('iphase=%d' %self.iphase)
        
        typ=self.iband
        ire=self.iphase

        if(typ == 1):
            title_label='Lowpass Filtered Time History'
            print (title_label)
            fc=float(self.f1r.get())
            lpf=fc
             
        if(typ == 2):
            title_label='Highpass Filtered Time History' 
            print (title_label)            
            fc=float(self.f1r.get())
            hpf=fc
                        
        if(typ == 3):
            title_label='Bandpass Filtered Time History'
            print(" This bandpass filter is implemented as a ")
            print(" highpass filter and lowpass filter in series. ")

            hpf=float(self.f1r.get())
            lpf=float(self.f2r.get())
            fc=lpf    


        nn=5000
        df=fc/100.


        H=np.zeros((nn,1),dtype=complex)

        fH=np.zeros((nn,1),'f')	
        theta=np.zeros((nn,1),'f')	        


        for i in range(0,nn):

            ff=(i+1)*df
            s=complex(0,(ff/fc))

            if(typ==2):  # highpass
                s=1/s
    

            H1=s**2-2*cos(7*pi/12.)*s+1
            H2=s**2-2*cos(9*pi/12.)*s+1
            H3=s**2-2*cos(11*pi/12.)*s+1    
            A=H1*H2*H3
    
            A=1/A
            H[i]=A
            fH[i]=ff

            if(ire==1):   # refiltering 
                H[i]=H[i]*H[i].conj()

    
        if(typ==3):  # bandpass
        
            G1=np.zeros((nn,1),dtype=complex)

            G1=H

            H=np.zeros((nn,1),dtype=complex)
            fc=hpf
    
            for i in range(0,nn): 
                ff=(i+1)*df       
                s=complex(0,(ff/fc))
                s=1/s
        
                H1=s**2-2*cos(7*pi/12.)*s+1
                H2=s**2-2*cos(9*pi/12.)*s+1
                H3=s**2-2*cos(11*pi/12.)*s+1    
                A=H1*H2*H3
    
                A=1/A
                H[i]=A*G1[i]
                
                if(ire==1):  # refiltering 
                    H[i]=H[i]*H[i].conj()
        
# fH=fH*fc*tpi

        if(ire==1):
            if(typ==1):
                out1=' Butterworth Lowpass Filter 6th order Refiltering fc=' +str(lpf)+' Hz'
    
            if(typ==2):
                out1=' Butterworth Highpass Filter 6th order Refiltering fc=' +str(hpf)+' Hz'
    
            if(typ==3):
                out1=' Butterworth Bandpass Filter 6th order Refiltering' +str(hpf)+' to '+str(lpf)+' Hz' 
    
        else:
            if(typ==1):
                out1=' Butterworth Lowpass Filter 6th order fc=' +str(lpf)+' Hz' 
    
            if(typ==2):
                out1=' Butterworth Highpass Filter 6th order fc=' +str(hpf)+' Hz'
    
            if(typ==3):
                out1=' Butterworth Bandpass Filter 6th order' +str(hpf)+' to '+str(lpf)+' Hz' 
                

        if(typ<3):
            xmax=10**(np.ceil(0.01+np.log10(fc)))
            xmin=10**(np.floor(-0.01+np.log10(fc)))
        else:
            xmax=10**(np.ceil(0.01+np.log10(lpf)))
            xmin=10**(np.floor(-0.01+np.log10(hpf)))    
                
        ymax=1
        ymin=ymax/100
        
        x1=xmin
        x2=xmax
        
        
        for i in range(0,nn):        
            theta[i]=np.angle(H[i])*180/pi
     

        plt.ion()
        plt.clf()
        plt.figure(3)
        
        gs1 = GridSpec(3, 1)
                                  
        ax1=plt.subplot(gs1[:-2, :])   
        plt.plot(fH,theta)
        
        plt.title(out1)
        plt.grid(True)
        plt.ylabel(' Phase (deg) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.ylim([-180,180])
        plt.xscale('log')
        plt.setp( ax1.get_xticklabels(), visible=False)
        plt.yticks([-180,-90,0,90,180])
        plt.draw()      

        plt.subplot(gs1[-2:0, :])
        plt.plot(fH,abs(H))
        
        plt.grid(True)
        plt.ylabel(' Magnitude ')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.ylim([0.01,2])
        plt.xscale('log')
        plt.yscale('log')        
        plt.draw()                  
              
###############################################################################
     
    def Butterworth_filter_main(self):   
        
        self.y=self.y_original 

        self.a=np.zeros((4,4),'f')	
        self.b=np.zeros((4,4),'f')
        self.alpha=np.zeros(2*self.l,'f')       
        self.s=(1+1j)*np.zeros(20,'f')
        self.om=0

        ntype= int(self.Lb_ws.curselection()[0]) 
        self.iband=ntype+1        
        
        nref= int(self.Lb_pc.curselection()[0]) 
        self.iphase=nref+1
        

        print ('iband=%d' %self.iband)
        print ('iphase=%d' %self.iphase)
        
        iflag=0

        if(self.iband == 1):
            title_label='Lowpass Filtered Time History'
            print (title_label)
            self.f=float(self.f1r.get())
            
            if(self.f>=0.5*self.sr):
                strer='cutoff frequency must be < Nyquist frequency'
                tkMessageBox.showerror('Error',strer)
                iflag=1
 
        if(self.iband == 2):
            title_label='Highpass Filtered Time History' 
            print (title_label)            
            self.f=float(self.f1r.get())
             
            if(self.f>=0.5*self.sr):
                strer='cutoff frequency must be < Nyquist frequency'
                tkMessageBox.showerror('Error',strer)
                iflag=1
            
            
        if(self.iband == 3):
            title_label='Bandpass Filtered Time History'
            print(" This bandpass filter is implemented as a ")
            print(" highpass filter and lowpass filter in series. ")

            self.fh=float(self.f1r.get())
            self.fl=float(self.f2r.get())
                
            if(self.fh>0.5*self.sr):
                strer='error: lower frequency must be < Nyquist frequency'
                tkMessageBox.showerror('Error',strer)
                iflag=1
            
            if(self.fl>0.5*self.sr):
                strer='error: upper frequency must be < Nyquist frequency' 
                tkMessageBox.showerror('Error',strer)
                self.f=self.fh
                iflag=1
                
################################################################################

        if(iflag==0):

            self.freq=self.f
        

            if(self.iband !=3):
                self.coefficients(self)
            
    
            if(self.iband == 1 or self.iband ==2):
                self.applymethod(self)

            if(self.iband == 3):
                self.f=self.fh
                self.freq=self.f
            
                print("\n Step 1")
                self.iband=2
    
                self.coefficients(self)
                self.applymethod(self)

                self.f=self.fl
                self.freq=self.f

                print("\n Step 2")
                self.iband=1
    
                self.coefficients(self)
                self.applymethod(self)  


            print (" ")   
            print ("Filtered signal statistics")           
        
            sr,dt,ave,sd,rms,skewness,kurtosis,dur=signal_stats(self.ttime, self.y,self.num)

            self.button_sav.config(state = 'normal')  

            plt.close(2)
            plt.figure(2)
 
       
            nn=len(self.ttime)
  
            n= int(self.Lb_ws.curselection()[0])
          
            if(n==0):
                out1='Lowpass Filtered Time History fc='+str(self.freq)+' Hz'

            if(n==1):
                out1='Highpass Filtered Time History fc='+str(self.freq)+' Hz'

            if(n==2):
                out1='Bandpass Filtered Time History fc='+str(self.fh)+' to '+str(self.fl)+' Hz'                 

  
            tt=self.ttime  
            y=self.y
            
            iflag=0
            
            ijk=0

            while(iflag==0):
                
                ijk+=1
                
                if(ijk==5):
                    break
                
                nn=len(tt)
                print(nn)                
            
                try:
                
                    iflag=1              
                
                    plt.plot(tt, y, linewidth=1.0,color='b')        # disregard error    
                    plt.grid(True)
                    plt.xlabel('Time (sec)')
                    plt.ylabel(self.y_string.get())  
                 
                    if(nn>=1000000 and ijk==1):
                        ymin, ymax = plt.ylim()
                        ymin=2*ymin
                        ymax=2*ymax   
                        plt.ylim( ymin, ymax ) 
                    else:
                        ymin=10*ymin
                        ymax=10*ymax
                        plt.ylim( ymin, ymax ) 
                        
                    print(ymax)    
                 
                    plt.title(out1)
                    plt.draw()    
                
                except:
                    iflag=0    

             

################################################################################

    @classmethod
    def applymethod(cls,self):

        if(self.iphase==1):
            self.apply(self)
            self.apply(self) 	
        else:	
            self.apply(self)
        
    
    @classmethod
    def stage1(cls,self):
             
        self.yt=np.zeros(self.ns,'f')

        bc=self.b[self.ik][0:3]
        ac=self.a[self.ik][0:3]
        ac[0]=1
    
        self.yt=lfilter(bc, ac, self.y, axis=-1, zi=None)      

 
    @classmethod
    def stage2(cls,self):
    
        self.y=np.zeros(self.ns,'f')
    
        bc=self.b[self.ik][0:3]
        ac=self.a[self.ik][0:3]
        ac[0]=1

        self.y=lfilter(bc, ac, self.yt, axis=-1, zi=None)  
    
        
    @classmethod
    def apply(cls,self):
        
        self.coefficients(self)
    
        self.ns=len(self.y)    
    
        if(self.iphase==1):	
            print("\n begin reversal ")
            yr=np.zeros(self.ns,'f')
                        
            for i in range(0,self.ns):
                yr[self.ns-1-i]=self.y[i]
                
            self.y=yr
            
#  cascade stage 1

        print("\n  stage 1")
        self.ik=1
        self.stage1(self)
	
#  cascade stage 2

        print("  stage 2")
        self.ik=2
        self.stage2(self)
	
#  cascade stage 3

        print("  stage 3")
        self.ik=3
        self.stage1(self)
    
        self.y=self.yt
        
        sd=np.std(self.y)

################################################################################

    @classmethod    
    def coefficients(cls,self):
    
        self.a=np.zeros((4,4),'f')	
        self.b=np.zeros((4,4),'f')		
    
#*** normalize the frequency ***

        targ=pi*self.f*self.dt   # radians
    
        print (" targ = %8.4g " %targ)
             
        self.om=tan(targ)   
    
        print ("   om = %8.4g " %self.om)

#*** solve for the poles *******

        self.poles(self)

#*** solve for alpha values ****

        print("\n alpha ")    
    
        self.alpha=np.zeros(2*self.l,'f')
        self.alpha=2*self.s.real
    
##    for i in range(0,len(alpha)):
##        print ("  %5.3f +j %5.3f " %(alpha[i].real,alpha[i].imag))

#*** solve for filter coefficients **

        if( self.iband == 1 ):
            self.lco(self)
        else:
            self.hco(self)
    
#*** plot digital transfer function **

#    dtrans();

#*** check stability ****************
    
        self.stab(self)
                    
                
################################################################################

    @classmethod	
    def stab(cls,self):
    
        a1=0
        d1=0 
        d2=0 
        d3=0
        dlit=0

        at1=0
        at2=0
        als=0.5e-06
        h2=0

        als*=6.
    
        print ("\n stability reference threshold= %14.7e " %als)

        for i in range(1,int((self.l/2)+1)):
        
            at1= -self.a[i][1]
            at2= -self.a[i][2]

#       print("\n\n stability coordinates: (%12.7g, %14.7g) ",at1,at2)
        
            h2=at2
 
            a1=h2-1.
            d3=at1-a1
         
            a1=1.-h2
            d2=a1-at1
            d1=at2+1.
		
#       print("\n d1=%14.5g  d2=%14.5g  d3=%14.5g",d1,d2,d3)

            dlit=d1

            if(dlit > d2):
                dlit=d2
            if(dlit > d3):
                dlit=d3

            print ("\n stage %ld     dlit= %14.5g " %(i, dlit))

            if(dlit > als):
                print (" good stability")  			
				
            if( (dlit < als) and (dlit > 0.)):		  
                print(" marginally unstable ")
            
            if(dlit < 0.):
                print (" unstable ")	  	
                print ("\n")

################################################################################  

    @classmethod	
    def lco(cls,self):
    
        om2=self.om**2

        for k in range(1,int((self.l/2)+1)):
    
            den = om2-self.alpha[k-1]*self.om+1.
		
            self.a[k][0]=0.
            self.a[k][1]=2.*(om2 -1.)/den
            self.a[k][2]=( om2 +self.alpha[k-1]*self.om+ 1.)/den

            self.b[k][0]=om2/den
            self.b[k][1]=2.*self.b[k][0]
            self.b[k][2]=self.b[k][0]

            print ("\n filter coefficients")		
            print (" a[%i][1]=%10.5g  a[%i][2]=%10.5g" %(k,self.a[k][1],k,self.a[k][2]))
            print (" b[%i][0]=%10.5g  b[%i][1]=%10.5g  b[%i][2]=%10.5g" \
                               %(k,self.b[k][0],k,self.b[k][1],k,self.b[k][2]))
    
        print ("\n")
        
################################################################################
  
    @classmethod	
    def hco(cls,self):
    
        print ("\n filter coefficients")
    
        om2=self.om**2

        for k in range(1,int((self.l/2)+1)):
    
            den = om2-self.alpha[k-1]*self.om+1.    
		
            self.a[k][0]=0.
            self.a[k][1]=2.*(-1.+ om2)/den
            self.a[k][2]=( 1.+self.alpha[k-1]*self.om+ om2)/den

            self.b[k][0]= 1./den;
            self.b[k][1]=-2.*self.b[k][0]
            self.b[k][2]=    self.b[k][0]
        
            print ("\n a[%i][1]=%10.5g  a[%i][2]=%10.5g" %(k,self.a[k][1],k,self.a[k][2]))
            print (" b[%i][0]=%10.5g  b[%i][1]=%10.5g  b[%i][2]=%10.5g" \
                               %(k,self.b[k][0],k,self.b[k][1],k,self.b[k][2]))
            print ("\n")
        
################################################################################

    @classmethod	
    def poles(cls,self):
        arg=0
        a1=0
        a2=complex(0.,0.)
        h=complex(0.,0.)
        theta=complex(0.,0.)
    
        self.s=(1+1j)*np.zeros(20,'f') 
        
#    print("\n  calculate print ")

        print ("\n poles ")
	
        for k in range(0,int(2*self.l)):
            arg=(2.*(k+1) +self.l-1)*pi/(2.*self.l)
            self.s[k]=cos(arg)+sin(arg)*(1j)
            print (" %4.3f  +j %4.3f " %(self.s[k].real,self.s[k].imag))
         
        for i in range(0,201):   
            arg = i/40.        
        
            h=complex( self.s[0].real,( arg - self.s[0].imag  ))

        for j in range(1,int(self.l)):
            
            theta=complex( -self.s[j].real,( arg - self.s[j].imag ))
            
            temp=h*theta
            h=temp
               
            x=1/h
            h=x
               
            a1 = self.freq*arg
	   
            a2=abs(h)            
           
            a3 = a2**2    
     
################################################################################

    def read_data(self):       
        
        self.button_calculate.config(state = 'normal')   
            
        self.ttime,self.y,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        self.y_original=self.y        
        
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
        
        nn=len(self.ttime)        
        

        if(nn>=1000000):
            ymin, ymax = plt.ylim()
            ymin=2*ymin
            ymax=2*ymax   
            plt.ylim( ymin, ymax ) 
        
    
        plt.draw()

        print ("\n samples = %d " % self.num)
 
         
         
################################################################################

def quit(root):
    root.destroy()

################################################################################