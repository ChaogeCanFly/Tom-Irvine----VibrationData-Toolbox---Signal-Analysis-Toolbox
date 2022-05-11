################################################################################
# program: vb_white_noise_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.7
# date: April 30, 2014
# description:  Generate white noise
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
    
    
from scipy.signal import lfilter



from numpy import histogram,pi,tan,cos,sin,zeros,std

import matplotlib.pyplot as plt

from vb_utilities import WriteData2,signal_stats

import random


class vb_white_noise:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))
  
        
        self.master.title("vb_white_noise_gui.py ver 1.7  by Tom Irvine")         
                
        self.TT=[]
        self.a =[]    
        self.np=0   
        self.lpf=0             
                
 
        crow=0  
 
        self.hwtext1=tk.Label(top,text='Generate White Noise')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=10,sticky=tk.SW)

        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='Std Dev')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.SW)
        
        self.hwtext7=tk.Label(top,text='Band Limit?')
        self.hwtext7.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.SW)
                 
        crow=crow+1

        self.ampr=tk.StringVar()  
        self.ampr.set('')  
        self.amp_entry=tk.Entry(top, width = 10,textvariable=self.ampr)
        self.amp_entry.grid(row=crow, column=0,padx=10, pady=1,sticky=tk.NW)

        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "yes")
        self.Lb1.insert(2, "no")
        self.Lb1.grid(row=crow, column=1, padx=5, pady=1,sticky=tk.NW)
        self.Lb1.select_set(0)  
        self.Lb1.bind('<<ListboxSelect>>',self.filter_option)        

        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='Duration (sec)')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.SW)
        
        self.hwtext25=tk.Label(top,text='Low Pass Frequency (Hz)')
        self.hwtext25.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.SW)

        crow=crow+1

        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 10,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=0,padx=10, pady=1,sticky=tk.NW)
        
        self.lpfr=tk.StringVar()  
        self.lpfr.set('')  
        self.lpf_entry=tk.Entry(top, width = 10,textvariable=self.lpfr)
        self.lpf_entry.grid(row=crow, column=1,padx=10, pady=1,sticky=tk.NW)
        self.lpf_entry.config(state = 'normal')  

        
        crow=crow+1        
        
        self.hwtext4=tk.Label(top,text='Sample Rate (Hz)')
        self.hwtext4.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.SW)
        
        crow=crow+1
           
        self.srr=tk.StringVar()  
        self.srr.set('')  
        self.sr=tk.Entry(top, width = 10,textvariable=self.srr)
        self.sr.grid(row=crow, column=0,padx=10, pady=1,sticky=tk.NW)


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


    def filter_option(self,val):
        sender=val.widget
        n= int(sender.curselection()[0])
        
        if(n==0):
            self.lpf_entry.config(state = 'normal') 
        else:
            self.lpfr.set('')
            self.lpf_entry.config(state = 'disabled')             

###############################################################################

    def calculation(self):     
        
        n= int(self.Lb1.curselection()[0])         

        if not self.ampr.get():
            tkMessageBox.showwarning('Warning','Enter std dev',parent=self.button_calculate)
            return
            
        if not self.srr.get():    
            tkMessageBox.showwarning('Warning','Enter sample rate',parent=self.button_calculate)            
            return            
            
        if not self.durr.get():
            tkMessageBox.showwarning('Warning','Enter duration',parent=self.button_calculate)            
            return
             
        sigma=float(self.ampr.get())
        sr=float(self.srr.get())
        dur=float(self.durr.get())

        dt=1./sr
       
        self.np=int(dur/dt)   
            
        
        if(self.np==0):
            tkMessageBox.showwarning('Warning','Enter number of point = 0')
            print('\n self.np=%d  dur=%8.4g  dt=%8.4g  \n' %(self.np,dur,dt))
            print(" error ")
            return            
    
        mu=0
        
        for i in range(0,int(self.np)):
            self.a.append(random.gauss(mu, sigma))
            self.TT.append(i*dt)


        if(n==0):
            self.lpf=float(self.lpfr.get())            
            
            if(self.lpf>0.3*sr):
                self.lpf=0.3*sr

            self.a=vb_white_noise.Butterworth_filter(self.TT,self.a,self.np,self.lpf,dt)            


        print (" ")   
        print ("Signal statistics")           
        
        sd=std(self.a)
        
        self.a*=sigma/sd
        
        sr,dt,ave,sd,rms,skewness,kurtosis,dur=signal_stats(self.TT, self.a,self.np)
        
#        print(len(self.TT))
#        print(len(self.a))        
        
        plt.ion()
        plt.clf()   
        plt.figure(1)

        plt.plot(self.TT, self.a, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel('Amp')  
        plt.title('White Noise Time History')
    
        plt.draw()      
        
        
        plt.figure(2)
        hist, bins = histogram(self.a, bins=21, density=False)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width) 
        plt.ylabel('Counts')
        plt.xlabel('Amplitude')
        plt.title('Histogram')
        plt.draw()       
        self.button_ex.config(state = 'normal' )

    @classmethod
    def Butterworth_filter(cls,ttime,y,np,f,dt):

        l=6     # sixth-order    
        
        a=zeros((4,4),'f')	
        b=zeros((4,4),'f')
        s=(1+1j)*zeros(20,'f')

################################################################################
                
        a,b=vb_white_noise.coefficients(a,b,dt,f,l,np,s)
        
        y=vb_white_noise.apply(a,b,ttime,y)

        return y
    

    @classmethod    
    def apply(cls,a,b,ttime,y):
    
        ns=len(y)    

#  cascade stage 1

        print("\n  stage 1")
        ik=1
        yt=vb_white_noise.stage1(ns,a,b,y,ik)
	
#  cascade stage 2

        print("  stage 2")
        ik=2
        y=vb_white_noise.stage2(ns,a,b,yt,ik)
	
#  cascade stage 3

        print("  stage 3")
        ik=3
        yt=vb_white_noise.stage1(ns,a,b,y,ik)
    
        y=yt
        
#        sd=std(y)

        return y
        
    @classmethod    
    def stage1(cls,ns,a,b,y,ik):
        yt=zeros(ns,'f')
        bc=b[ik][0:3]
        ac=a[ik][0:3]
        ac[0]=1
        yt=lfilter(bc, ac, y, axis=-1, zi=None) 
        
        return yt    
        
        
    @classmethod    
    def stage2(cls,ns,a,b,yt,ik):
        y=zeros(ns,'f')
        bc=b[ik][0:3]
        ac=a[ik][0:3]
        ac[0]=1
        y=lfilter(bc, ac, yt, axis=-1, zi=None)       

        return y
        

    @classmethod    
    def coefficients(cls,a,b,dt,f,l,np,s):
        
#*** normalize the frequency ***

        targ=pi*f*dt   # radians
    
        print (" targ = %8.4g " %targ)
             
        om=tan(targ)   
    
        print ("   om = %8.4g " %om)

#*** solve for the poles *******

        a1,a2,a3,s=vb_white_noise.poles(np,s,l,f)

#*** solve for alpha values ****

        print("\n alpha ")    
        alpha=zeros(2*l,'f')
        alpha=2*s.real    
    
##    for i in range(0,len(alpha)):
##        print ("  %5.3f +j %5.3f " %(alpha[i].real,alpha[i].imag))

#*** solve for filter coefficients **

        a,b=vb_white_noise.lco(om,l,a,b,alpha)
    
#*** plot digital transfer function **

#    dtrans();

#*** check stability ****************
    
        vb_white_noise.stab(l,a)
                    
        return a,b


    @classmethod	
    def lco(cls,om,l,a,b,alpha):
        
        print ("lco")
    
        om2=om**2
        
        print (om2)
        print (alpha)

        for k in range(1,int((l/2)+1)):
    
            den = om2-alpha[k-1]*om+1.
            
            print (den)
		
            a[k][0]=0.
            a[k][1]=2.*(om2 -1.)/den
            a[k][2]=( om2 +alpha[k-1]*om+ 1.)/den

            b[k][0]=om2/den
            b[k][1]=2.*b[k][0]
            b[k][2]=b[k][0]

            print ("\n filter coefficients")		
            print (" a[%i][1]=%10.5g  a[%i][2]=%10.5g" %(k,a[k][1],k,a[k][2]))
            print (" b[%i][0]=%10.5g  b[%i][1]=%10.5g  b[%i][2]=%10.5g" %(k,b[k][0],k,b[k][1],k,b[k][2]))
    
        return a,b

    @classmethod	
    def poles(cls,np,s,l,freq):
        arg=0
        a1=0
        a2=complex(0.,0.)
        h=complex(0.,0.)
        theta=complex(0.,0.)
    
        s=(1+1j)*zeros(20,'f') 
        
#    print("\n  calculate print ")

        print ("\n poles ")
	
        for k in range(0,int(2*l)):
            arg=(2.*(k+1) +l-1)*pi/(2.*l)
            s[k]=cos(arg)+sin(arg)*(1j)
            print (" %4.3f  +j %4.3f " %(s[k].real,s[k].imag))
         
        for i in range(0,201):   
            arg = i/40.        
        
            h=complex( s[0].real,( arg - s[0].imag  ))

        for j in range(1,int(l)):
            
            theta=complex( -s[j].real,( arg - s[j].imag ))
            
            temp=h*theta
            h=temp
               
            x=1/h
            h=x
               
            a1 = freq*arg
	   
            a2=abs(h)            
           
            a3 = a2**2
            
        return a1,a2,a3,s     
     


    @classmethod	
    def stab(cls,l,a):
    
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

        for i in range(1,int((l/2)+1)):
        
            at1= -a[i][1]
            at2= -a[i][2]

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
    
    
    def export(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n')    
 
        WriteData2(self.np,self.TT,self.a,output_file)


def quit(root):
    root.destroy()        