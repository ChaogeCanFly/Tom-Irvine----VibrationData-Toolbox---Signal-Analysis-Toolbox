##########################################################################
# program: vb_half_power_bandwidth_fc_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.0
# date: November 3, 2014
# description:  
#
#
##########################################################################

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
    
    
from vb_utilities import read_three_columns_from_dialog,WriteData2  

from numpy import sqrt,zeros,random,pi

import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec
    
######################################################################## 

class vb_half_power_bandwidth_fc:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(600,400)
        self.master.geometry("700x470")
        self.master.title("vb_half_power_bandwidth_fc_gui.py ver 1.0  by Tom Irvine") 
        
        crow=0        
        
        self.hwtext1=tk.Label(top,text='This method performs a curve-fit to determine the damping ratio for a system excited by')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=0,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text='an applied force.  This method is an extension of the half-power bandwidth method.')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=0,sticky=tk.W)
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='The input data must be a frequency response function with frequency & complex magnitude in')
        self.hwtext3.grid(row=crow, column=0, columnspan=6, pady=0,sticky=tk.W)    
        
        crow=crow+1

        self.hwtext4=tk.Label(top,text='three columns:  freq(Hz)  real  imaginary ')
        self.hwtext4.grid(row=crow, column=0, columnspan=6, pady=0,sticky=tk.W)           

###############################################################################

        crow=crow+1

        self.button_read = tk.Button(top, text="Read Input File", command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=20,sticky=tk.W)  

        crow=crow+1

        self.hwtext5=tk.Label(top,text='Select Response Type ')
        self.hwtext5.grid(row=crow, column=0, columnspan=1, pady=0)     
        
        crow=crow+1
        
        self.Lb1 = tk.Listbox(top,height=3,exportselection=0)
        self.Lb1.insert(1, "Acceleration")
        self.Lb1.insert(2, "Velocity")
        self.Lb1.insert(3, "Displacement")        
        self.Lb1.grid(row=crow, column=0, pady=1)
        self.Lb1.select_set(0) 
        
        self.hwtext7=tk.Label(top,text='Enter Curve-fit Frequency Limits (Hz) ')
        self.hwtext7.grid(row=crow, column=1, columnspan=2, pady=6,sticky=tk.S)  
 
        
        crow=crow+1   
        
        self.hwtext6=tk.Label(top,text='Enter Number of Trials ')
        self.hwtext6.grid(row=crow, column=0, columnspan=1, pady=6)    

        self.hwtext8=tk.Label(top,text='Start')
        self.hwtext8.grid(row=crow, column=1, columnspan=1, pady=0)   

        self.hwtext9=tk.Label(top,text='End')
        self.hwtext9.grid(row=crow, column=2, columnspan=1, pady=0)          
        
        
        crow=crow+1 
        
        self.ntrialsr=tk.StringVar()  
        self.ntrialsr.set('10000')  
        self.ntrials_entry=tk.Entry(top, width = 9,textvariable=self.ntrialsr)
        self.ntrials_entry.grid(row=crow, column=0)
        
        self.f1r=tk.StringVar()  
        self.f1r_entry=tk.Entry(top, width = 9,textvariable=self.f1r)
        self.f1r_entry.grid(row=crow, column=1)         
                
        self.f2r=tk.StringVar()  
        self.f2r_entry=tk.Entry(top, width = 9,textvariable=self.f2r)
        self.f2r_entry.grid(row=crow, column=2)                   
                
        crow=crow+1   

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 
        
        root=self.master    

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=20)   
                
        
###############################################################################
        
    def read_data(self):         
        self.f,self.frf_r,self.frf_i,num=read_three_columns_from_dialog('Select input file',self.master)
        
        self.button_calculate.config( state = 'normal')
        
###############################################################################  

    @classmethod
    def MFRF(cls,self):

        omega=self.om
        damp=self.damp
        rho=self.rho

        if(self.n1==0):  # acceleration
#              
            self.MFRF_R=((-omega**2/((1-rho**2)+(1j)*(2*damp*rho))).real) 
            self.MFRF_I=((-omega**2/((1-rho**2)+(1j)*(2*damp*rho))).imag)   
  
        if(self.n1==1):  # velocity
#            
            self.MFRF_R=(((1j)*omega/((1-rho**2)+(1j)*(2*damp*rho))).real)
            self.MFRF_I=(((1j)*omega/((1-rho**2)+(1j)*(2*damp*rho))).imag)            
   
        if(self.n1==2):  # displacement
#            
            self.MFRF_R=((1/((1-rho**2)+(1j)*(2*damp*rho))).real)    
            self.MFRF_I=((1/((1-rho**2)+(1j)*(2*damp*rho))).imag)   

###############################################################################

    def calculation(self):

        self.nt=int(self.ntrialsr.get())       

        self.f1=float(self.f1r.get())
        self.f2=float(self.f2r.get())        
        
        self.n1=int(self.Lb1.curselection()[0])
        
        
        if(self.n1==0):  # acceleration
#        
            tlabel='Acceleration'
            yl='Accel/Force'
            t_string='Accelerance Transfer Function'

        if(self.n1==1):  # velocity
#        
            tlabel='Velocity'
            yl='Velocity/Force'
            t_string='Mobility Transfer Function'
           
        if(self.n1==2):  # displacement
#        
            tlabel='Displacement'
            yl='Disp/Force'
            t_string='Receptance Transfer Function'
        
        df=self.f2-self.f1
        
        n=len(self.f)
        
        for i in range(0,n):
            if(self.f[i]>=self.f1):
                i1=i
                break
    
        for i in range(0,n):
            if(self.f[i]>self.f2):
                i2=i-1
                break
    
        maxa=0

        for i in range(i1,(i2+1)):
            if( sqrt(self.frf_r[i]**2+self.frf_i[i]**2 )>maxa):
                maxa=sqrt(self.frf_r[i]**2+self.frf_i[i]**2 )
                maxf=self.f[i]
    

        tpi=2*pi

        error_max=1.0e+90


        omega=zeros(n,'f')
 
        for i in range(0,n):
            omega[i]=tpi*self.f[i]

        Ar=0
#        Axr=0
        fnr=0
        dampr=0
        
        A=1
        
        for i in range(0,self.nt):
              
            if(i<5 or random.random()<0.5):
                
                A=0.6+0.8*random.random()                
                
                if(random.random()<0.3):
                    A=-A
        
                if(random.random()<0.5):
                    damp=0.5*(random.random())**2
                else:
                    damp=0.1*(random.random())           
        
        
                if(random.random()<0.5):
                    fn=self.f1+df*random.random()
                else:
                    fn=maxf
            
            else:
                
                if(random.random()<0.4):
                    fn=fnr*(0.995+0.01*random.random())  
                    damp=dampr*(0.99+0.02*random.random())       
                    A=Ar*(0.995+0.01*random.random())
                else:
                    if(random.random()<0.5):
                        fn=fnr*(0.995+0.01*random.random())
                    else:
                        damp=dampr*(0.995+0.01*random.random())                  
            

            if(fn<self.f1 or fn>self.f2):
                fn=maxf
    
            if(A<0.2 or A>5):
                A=maxa*(0.8+0.4*random.random())
    
            if(damp>0.5):
                damp=0.5*(random.random())**2        
    
            error=0    
    
            omegan=tpi*fn    
    
            c_r=zeros((i2+1),'f')
            c_i=zeros((i2+1),'f')   
            fc=zeros((i2+1),'f') 
                   
            self.damp=damp
    
            for j in range(i1,(i2+1)):
                
                self.rho=omega[j]/omegan
                self.om=omega[j]
                
                self.MFRF(self)

                c_r[j]=self.MFRF_R
                c_i[j]=self.MFRF_I 
                fc[j]=self.f[j]
   
            AX=A*maxa/max([max(abs(c_r)) , max(abs(c_i))])   
    
            c_r=AX*c_r
            c_i=AX*c_i    
            
            for j in range(i1,(i2+1)):
                bbb=abs((self.frf_r[j]-c_r[j]))+abs((self.frf_i[j]-c_i[j]))
                error+=bbb                
                
   
            if(error<error_max):
       
                error_max=error
                dampr=damp
                fnr=fn
                Ar=A
#                Axr=AX
                cr=c_r
                ci=c_i

                print(' %d  %8.4g  %8.4g  %8.4g' %(i,A,fn,damp))
        
            k=0

            nv=i2-i1+1
            fr=zeros(nv,'f')
            ar=zeros(nv,'f')
            ai=zeros(nv,'f')

            for j in range(i1,(i2+1)):
      
                fr[k]=self.f[j]
                ar[k]=cr[j]
                ai[k]=ci[j]
                k=k+1         
  
        Qr=1/(2*dampr)
        print('\n fn=%8.4g Hz \n Q=%8.4g \n damping ratio=%8.4g \n' %(fnr,Qr,dampr))
        
        
        print('View Plot')

        plt.ion()
        plt.close(6)
        fig=plt.figure(6)
        
        
        gs1 = GridSpec(2, 1)
                                                 
        ax1 = fig.add_subplot(gs1[0])
        plt.plot(self.f,self.frf_r,label="Input Data")
        plt.plot(fc,cr,label="Curve-fit")        
        
        
        plt.xlim([self.f1,self.f2])        
        plt.title(t_string)
        plt.grid(True)
        plt.ylabel('Real')
        plt.grid(True, which="both")
#        plt.legend(loc="upper right")  
        
        plt.legend(bbox_to_anchor=(1.1, 1.05))        
        
        plt.draw()      

        ax2 = fig.add_subplot(gs1[1]) 
        plt.plot(self.f,self.frf_i)
        plt.plot(fc,ci)   
        
        plt.xlim([self.f1,self.f2])        
        plt.grid(True)
        plt.ylabel('Imag') 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")    
        plt.draw()  

        
###############################################################################

def quit(root):
    root.destroy()

###############################################################################