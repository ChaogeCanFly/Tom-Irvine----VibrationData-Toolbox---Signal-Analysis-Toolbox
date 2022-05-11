###########################################################################
# program: vb_half_power_curvefit_gui.py
# author: Tom Irvine
# version: 1.0
# date: May 28, 2014
# 
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


from vb_utilities import read_two_columns_from_dialog

import matplotlib.pyplot as plt

import numpy as np

###############################################################################

class vb_half_power_curvefit:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(1050,550)
        self.master.geometry("1050x550")

        self.master.title("vb_half_power_curvefit_gui.py  ver 1.0  by Tom Irvine")
        
        
###############################################################################
        
        crow=0

        self.hwtext1=tk.Label(top,text='This method performs a curve-fit to determine the damping ratio for a system excited by base excitation or an applied force.') 
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=9,sticky=tk.SW)
        
        crow=crow+1         
        
        self.hwtext2=tk.Label(top,text='This method is an extension of the half-power bandwidth method. The input data must be a frequency response function with two columns: freq(Hz) & amp') 
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=1,sticky=tk.NW)    
        
        crow=crow+1            

        self.hwtext3=tk.Label(top,text='Select Excitation Type') 
        self.hwtext3.grid(row=crow, column=1, columnspan=1, pady=15,sticky=tk.S)  

        crow=crow+1     

        self.button_read = tk.Button(top, text="Read Input File", command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=1,sticky=tk.N) 

        self.Lb1 = tk.Listbox(top,height=2,width=16,exportselection=0)
        self.Lb1.insert(1, "Base Excitation")
        self.Lb1.insert(2, "Applied Force")     
        self.Lb1.grid(row=crow, column=1, columnspan=1, padx=10, pady=1,sticky=tk.N)
        self.Lb1.select_set(0)  
#        self.Lb1.bind('<<ListboxSelect>>',self.velocity_unit_option)   

        crow=crow+1   

        self.hwtext4=tk.Label(top,text='Initial Plot X-axis Limits') 
        self.hwtext4.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.S) 
        
        self.hwtext5=tk.Label(top,text='Select Response Type') 
        self.hwtext5.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.S) 

        self.hwtext6=tk.Label(top,text='Select Amplitude Dimension') 
        self.hwtext6.grid(row=crow, column=2, columnspan=2, pady=10,sticky=tk.SW) 
        
        
        crow=crow+1           
         
        self.Lb2 = tk.Listbox(top,height=2,width=16,exportselection=0)
        self.Lb2.insert(1, "Automatic")
        self.Lb2.insert(2, "Manual")     
        self.Lb2.grid(row=crow, column=0, columnspan=1, padx=10, pady=3,sticky=tk.N)
        self.Lb2.select_set(0)  
        self.Lb2.bind('<<ListboxSelect>>',self.frequency_option) 
        
        self.Lb3 = tk.Listbox(top,height=3,width=20,exportselection=0)
        self.Lb3.insert(1, "Acceleration")
        self.Lb3.insert(2, "Velocity")
        self.Lb3.insert(3, "Displacement")        
        self.Lb3.grid(row=crow, column=1, columnspan=1, padx=10, pady=3,sticky=tk.N)
        self.Lb3.select_set(0)         
        
        self.Lb4 = tk.Listbox(top,height=2,width=15,exportselection=0)
        self.Lb4.insert(1, "Amplitude")
        self.Lb4.insert(2, "Amplitude^2")
        self.Lb4.grid(row=crow, column=2, columnspan=1, padx=5, pady=3,sticky=tk.N)
        self.Lb4.select_set(0)   

        crow=crow+1            
        
        self.hwtext7=tk.Label(top,text='Min Freq (Hz)') 
        self.hwtext7.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.S) 
        
        self.hwtext8=tk.Label(top,text='Enter Number of Trials') 
        self.hwtext8.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.S) 
        
        self.hwtext10=tk.Label(top,text='Enter Curve-fit Frequencies (Hz)') 
        self.hwtext10.grid(row=crow, column=2, columnspan=2, pady=10,sticky=tk.SW) 

        crow=crow+1    
        
        self.fminr=tk.StringVar()  
        self.fmin_entry=tk.Entry(top, width = 10,textvariable=self.fminr)
        self.fmin_entry.grid(row=crow, column=0) 
        self.fmin_entry.config(state = 'disabled')        
        
        self.ntrialsr=tk.StringVar()  
        self.ntrialsr.set('10000')  
        self.ntrials_entry=tk.Entry(top, width = 10,textvariable=self.ntrialsr)
        self.ntrials_entry.grid(row=crow, column=1)        

        self.hwtext12=tk.Label(top,text='Start') 
        self.hwtext12.grid(row=crow, column=1, columnspan=2, pady=10,sticky=tk.E)
        
        self.fstartr=tk.StringVar()  
        self.fstart_entry=tk.Entry(top, width = 10,textvariable=self.fstartr)
        self.fstart_entry.grid(row=crow, column=3,sticky=tk.W)
          

        crow=crow+1            
        
        self.hwtext9=tk.Label(top,text='Max Freq (Hz)') 
        self.hwtext9.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.S) 

        self.hwtext13=tk.Label(top,text='End') 
        self.hwtext13.grid(row=crow, column=2, columnspan=1,pady=10,sticky=tk.E)

        self.fendr=tk.StringVar()  
        self.fend_entry=tk.Entry(top, width = 10,textvariable=self.fendr)
        self.fend_entry.grid(row=crow, column=3,sticky=tk.W)            

        
        crow=crow+1           

        self.fmaxr=tk.StringVar()  
        self.fmax_entry=tk.Entry(top, width = 10,textvariable=self.fmaxr)
        self.fmax_entry.grid(row=crow, column=0)         
        self.fmax_entry.config(state = 'disabled')


        crow=crow+1    

        self.button_plot = tk.Button(top, text="Plot Input FRF",command=self.plot_input)
        self.button_plot.config( height = 2, width = 15,state = 'disabled')
        self.button_plot.grid(row=crow, column=0,columnspan=1,padx=5,pady=10)

        self.button_calculate = tk.Button(top, text="Calculate",command=self.calculate)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled' )
        self.button_calculate.grid(row=crow, column=1,columnspan=1,padx=5,pady=10)
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2, padx=3,pady=10) 

###############################################################################

    def plot_input(self): 
        n2=int(self.Lb2.curselection()[0])   # plot limits
        
        iresp=1+int(self.Lb3.curselection()[0])   # response type
        irat =1+int(self.Lb4.curselection()[0])   # amplitude type
        
        plt.ion()
        plt.close(1)
        plt.figure(1)    
        
        plt.plot(self.a,self.b)
        plt.xscale('log')
        plt.yscale('log')
        
        plt.grid(True)
        plt.xlabel('Frequency (Hz)')  
                                
        if(n2==1):
            fmin=float(self.fminr.get())
            fmax=float(self.fmaxr.get())
            plt.xlim([fmin,fmax])

            ymax=0
            ymin=1.0e+20
            for i in range(0,len(self.a)):
                if(self.a[i]>=fmin and self.a[i]<=fmax):
                    if(self.b[i]>ymax):
                        ymax=self.b[i]
                    if(self.b[i]<ymin):
                        ymin=self.b[i]  
                        
            print(ymin,ymax)         
            
            
            lymax=np.log10(ymax)
            lymin=np.log10(ymin)
            
            c1=int(np.ceil(lymax))
            c2=int(np.floor(lymin))
        
            ymax=10.**(c1)
            ymin=10.**(c2)
                        
            if(ymin==ymax):
                ymin=ymax/10.

            
            plt.xlim([fmin,fmax])
            plt.ylim([ymin,ymax])

            
            
        if(iresp==1):
            plt.title('Acceleration FRF')              
        if(iresp==2):
            plt.title('Velocity FRF')  
        if(iresp==3):            
            plt.title('Displacement FRF')              

        if(irat==1):
            plt.ylabel('Amplitude')                 
        else:            
            plt.ylabel('Amplitude^2') 
            
        plt.draw()     
             
        self.button_calculate.config( state = 'normal')        

    
    def calculate(self):

        iex  =1+int(self.Lb1.curselection()[0])   # excitation type
        iresp=1+int(self.Lb3.curselection()[0])   # response type
        irat =1+int(self.Lb4.curselection()[0])   # amplitude type


        if(iresp==1):
##      disp('  1= acceleration ')
##      disp('  2= acceleration^2 ')
            if(irat==1):
                tlabel='Acceleration'
#    
                if(iex==1):
                    MFRF=lambda omega, rho, damp: (np.sqrt((1+(2*damp*rho)**2)/((1-rho**2)**2+(2*damp*rho)**2)))      
                else:
                    MFRF=lambda omega, rho, damp: (np.sqrt(omega**2/((1-rho**2)**2+(2*damp*rho)**2)))             
    
            else:
                tlabel='Acceleration^2'
#    
                if(iex==1):
                    print(" * ref 1 * ")
                    MFRF=lambda omega, rho, damp: ((1.+(2.*damp*rho)**2)/((1.-rho**2)**2+(2.*damp*rho)**2))        
                else:
                    MFRF=lambda omega, rho, damp: ((omega**2/((1-rho**2)**2+(2*damp*rho)**2)))          

#
        if(iresp==2):
##      disp('  1= velocity ')
##      disp('  2= velocity**2 ')
  
            if(irat==1):
                tlabel='Velocity'
#    
                if(iex==1):
                    MFRF=lambda omega, rho, damp: (np.sqrt(((1+(2*damp*rho)**2)/omega)/((1-rho**2)**2+(2*damp*rho)**2)))       
                else:
                    MFRF=lambda omega, rho, damp: (np.sqrt(omega/((1-rho**2)**2+(2*damp*rho)**2)))              
#      
            else:
                tlabel='Velocity^2'
#    
                if(iex==1):
                    MFRF=lambda omega, rho, damp: (((1+(2*damp*rho)**2)/omega)/((1-rho**2)**2+(2*damp*rho)**2))       
                else:
                    MFRF=lambda omega, rho, damp: ((omega/((1-rho**2)**2+(2*damp*rho)**2)))          
      
#
        if(iresp==3):
##      disp('  1= displacement ')
##      disp('  2= displacement**2 ')
  
            if(irat==1):
                tlabel='Displacement'
#    
                if(iex==1):
                    MFRF=lambda omega, rho, damp: (np.sqrt(((1+(2*damp*rho)**2)/omega**2)/((1-rho**2)**2+(2*damp*rho)**2)))        
                else:
                    MFRF=lambda omega, rho, damp: (np.sqrt(1/((1-rho**2)**2+(2*damp*rho)**2)))            
#      
            else:
                tlabel='Displacement^2'
#    
                if(iex==1):
                    MFRF=lambda omega, rho, damp: (((1+(2*damp*rho)**2)/omega**2)/((1-rho**2)**2+(2*damp*rho)**2))        
                else:
                    MFRF=lambda omega, rho, damp: ((1/((1-rho**2)**2+(2*damp*rho)**2)))            
     

        nt=int(self.ntrialsr.get())        
        
        
        try:
            fstart=float(self.fstartr.get())
        except:    
            tkMessageBox.showwarning("warning", "Enter start frequency",parent=self.button_calculate)        
            return            
           
        try:           
            fend=float(self.fendr.get())   
        except:
            tkMessageBox.showwarning("warning", "Enter end frequency",parent=self.button_calculate)                    
            return
        
        
        
        if(fstart<min(self.a)):
            fstart=min(self.a)

        if(fend>max(self.a)):
            fend=max(self.a)
            

        
        n=len(self.a)        
        

        for i in range(0,n):
            if(self.a[i]>=fstart):
                i1=i
                break

        for i in range(i1,n):
            if(self.a[i]>fend):
                i2=i
                break
  

        fr=np.zeros(i2,'f')
        ar=np.zeros(i2,'f')
        
        maxb=0

        for i in range(i1,i2):                  
            if(self.b[i]>maxb):
                maxb=self.b[i]
                maxa=self.a[i]


        maxf=maxa 

        tpi=2*np.pi        
        

        error_max=1.0e+90

        Ar=0
        fnr=0
        dampr=0        
        
        print(' ')
        print('  i     A     fn     damp ')        
        

        for i in range(0,nt):
    
            if(i<5 or np.random.random()<0.6):
                A=(0.99+0.02*np.random.random())
                damp=0.5*np.random.random()**1.5
                fn=maxf*(0.995+0.01*np.random.random())

            else:
                if(np.random.random()<0.4):
                    fn=fnr*(0.995+0.01*np.random.random())  
                    damp=dampr*(0.99+0.02*np.random.random())       
                    A=Ar*(0.995+0.01*np.random.random())
                else:
                    if(np.random.random()<0.5):
                        fn=fnr*(0.995+0.01*np.random.random())
                    else:
                        damp=dampr*(0.995+0.01*np.random.random())                  
            
        
            if(fn<fstart or fn>maxf):
                fn=maxf
    
            if(A<0.2 or A>5):
                A=maxb*(0.8+0.4*np.random.random())
    
            if(damp>0.5):
                damp=0.5*(np.random.random())**2        
    
            error=0

            omegan=tpi*fn
            

            c=np.zeros(i2,'f')

            for j in range(i1,i2):
                omega=tpi*self.a[j]
                rho=omega/omegan
                c[j]=MFRF(omega, rho, damp)

            AX=A*maxb/max(c)
            c=AX*c

            for j in range(i1,i2):
                bbb=abs(np.log10(self.b[j]/c[j]))
                error=error+bbb
    
            if(error<error_max):
        
                error_max=error
                dampr=damp
                fnr=fn
                Ar=A
                cr=c

                print(' %d  %7.3g  %7.3g  %7.3g' %(i,A,fn,damp))

                k=0

                for j in range(i1,i2):
                    fr[k]=self.a[j]              
                    ar[k]=cr[j]
                    k=k+1
                    
                    


        Qr=1/(2*dampr)
                
        print('\n Results \n')
        print(' fn =%7.3g Hz \n damping ratio = %7.3g \n Q =%7.3g \n' %(fnr,dampr,Qr))
        
        
        frp=fr[0:k-1]
        arp=ar[0:k-1]
        
        plt.ion()
        plt.close(2)
        plt.figure(2)    
        
        plt.plot(self.a[i1:i2],self.b[i1:i2],label='Input Data')
        plt.plot(frp,arp,label='Curve-fit')     
        
        plt.legend(loc="upper right")         
        plt.xlabel('Frequency (Hz)') 
        plt.title(tlabel)         
        plt.grid(True)
        
###############################################################################        

    def frequency_option(self,event): 
        n=int(self.Lb2.curselection()[0])
        
        if(n==0):
            self.fmax_entry.config(state = 'disabled')
            self.fmin_entry.config(state = 'disabled')
            self.fmaxr.set(' ')
            self.fminr.set(' ')                
        else:
            self.fmax_entry.config(state = 'normal')
            self.fmin_entry.config(state = 'normal')   


    def read_data(self):            
            
        self.a,self.b,self.num=\
            read_two_columns_from_dialog('Select FRF File',self.master)


        self.button_plot.config( state = 'normal' )   
  
###############################################################################
    
def quit(root):
    root.destroy()              