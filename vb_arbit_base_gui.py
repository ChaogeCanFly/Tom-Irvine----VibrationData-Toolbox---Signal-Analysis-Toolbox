##########################################################################
# program: vb_arbit_base_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 2.2
# date: April 30, 2014
# description:  
#
# Calculate the response of an SDOF system to a base input.
# The file must have two columns: time(sec) & accel(G)
#
# The numerical engine is the Smallwood ramp invariant digital
# recursive filtering relationship
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
    
    
from vb_utilities import read_two_columns_from_dialog,sample_rate_check,WriteData2  

from scipy.signal import lfilter
from math import exp,sqrt,cos,sin

import matplotlib.pyplot as plt

import numpy as np

    
######################################################################## 

class vb_arbit_base:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.25))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_arbit_base_gui.py ver 2.2  by Tom Irvine") 
        
        self.damp=0
        self.Q=0
        self.fn=0
        self.a_resp=[]
        self.rd_resp=[]        
        self.ac=[]
        self.num=0
        
        crow=0        
        
        self.hwtext1=tk.Label(top,text='SDOF Response for Base Excitation')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & accel(G)')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=5,sticky=tk.W)

###############################################################################

        crow=crow+1

        self.button_read = tk.Button(top, text="Read Input File", command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=20,sticky=tk.W)  
        
        self.hwtextfn=tk.Label(top,text='fn (Hz) =')
        self.hwtextfn.grid(row=crow, column=1,padx=15,sticky=tk.E)
        
        self.fnr=tk.StringVar()  
        self.fnr.set('')  
        self.fn_entry=tk.Entry(top, width = 10,textvariable=self.fnr)
        self.fn_entry.grid(row=crow, column=2,sticky=tk.W)        

        self.hwtextQ=tk.Label(top,text='Q=')
        self.hwtextQ.grid(row=crow, column=3,padx=0,sticky=tk.E)

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 5,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=4,sticky=tk.W)

###############################################################################
        
        crow=crow+1  

        self.hwtextfn=tk.Label(top,text='Select Displacement Unit')
        self.hwtextfn.grid(row=crow, column=0,columnspan=2,padx=15,sticky=tk.W)

        crow=crow+1
        
        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "inch")
        self.Lb1.insert(2, "mm")
        self.Lb1.grid(row=crow, column=0, pady=1,sticky=tk.E)
        self.Lb1.select_set(0) 
        
###############################################################################
        
        crow=crow+1   

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=2, pady=20) 
        
        root=self.master    

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=2, padx=10,pady=20)  
        
        crow=crow+1        
        
        self.hwtextext_ex=tk.Label(top,text='Export Response Data')
        self.hwtextext_ex.grid(row=crow, column=0,pady=10)  
        self.hwtextext_ex.config(state = 'disabled')
        
        crow=crow+1   
        
        self.button_sa = tk.Button(top, text="Acceleration", command=self.export_accel)
        self.button_sa.config( height = 2, width = 15,state = 'disabled' )
        self.button_sa.grid(row=crow, column=0,columnspan=2, pady=3, padx=1)  

        self.button_srd = tk.Button(top, text="Rel Disp", command=self.export_rd)
        self.button_srd.config( height = 2, width = 15,state = 'disabled' )
        self.button_srd.grid(row=crow, column=2,columnspan=2, pady=3, padx=1)         

###############################################################################  

    def calculation(self):
        
        self.Q=float(self.Qr.get())
        self.damp=1./(2.*self.Q); 
        self.fn=float(self.fnr.get())
        self.omega=2*np.pi*self.fn
        self.omegad=self.omega*sqrt(1.-(self.damp**2))        
        
        vb_arbit_base.a_coeff(self)
        vb_arbit_base.accel_arbit_base(self)
        vb_arbit_base.rd_arbit_base(self)
        
        self.hwtextext_ex.config(state = 'normal')
        self.button_sa.config(state = 'normal')
        self.button_srd.config(state = 'normal')
        
        
    def export_accel(self):
        root=self.master    
        output_file_path = asksaveasfilename(parent=root,title="Enter the acceleration filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2(self.num,self.a,self.a_resp,output_file)        
        
    def export_rd(self):
        root=self.master    
        output_file_path = asksaveasfilename(parent=root,title="Enter the relative displacement filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2(self.num,self.a,self.rd_resp,output_file)  

        
    def rd_arbit_base(self):        
        n= int(self.Lb1.curselection()[0])           
        
        rd_pos=0
        rd_neg=0
        bc=np.zeros(3,'f')
                    
        E =exp(  -self.damp*self.omega*self.dt)
        E2=exp(-2*self.damp*self.omega*self.dt)
             
        K=self.omegad*self.dt
        C=E*cos(K)
        S=E*sin(K)
            
        Omr=(self.omega/self.omegad)
        Omt=self.omega*self.dt
            
        P=2*self.damp**2-1
            
        b00=2*self.damp*(C-1)
        b01=S*Omr*P
        b02=Omt
            
        b10=-2*Omt*C
        b11= 2*self.damp*(1-E2)
        b12=-2*b01   

        b20=(2*self.damp+Omt)*E2
        b21= b01
        b22=-2*self.damp*C               
            
        bc[0]=b00+b01+b02
        bc[1]=b10+b11+b12
        bc[2]=b20+b21+b22
            
        bc=-bc/(self.omega**3*self.dt)
         
        self.rd_resp=lfilter(bc, self.ac, self.b, axis=-1, zi=None)

        if(n==0):
            scale=386.
        else:
            scale=9.81*1000
            
        rd_pos= scale*max(self.rd_resp)
        rd_neg= scale*min(self.rd_resp) 
        self.rd_resp=scale*self.rd_resp        
        
        if(n==0):        
            print ("\n Relative Displacement Response (inch)")
        else: 
            print ("\n Relative Displacement Response (mm)")        

        print ("\n  max = %8.4g   min = %8.4g  "    % (rd_pos,rd_neg))          


        plt.close(3)
        plt.figure(3)

        plt.plot(self.a, self.rd_resp, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')

        if(n==0):        
            plt.ylabel('Rel Disp (in)')
        else:
            plt.ylabel('Rel Disp (mm)')            
            
        out1='SDOF Response Time History  fn=%g Hz, Q=%g ' %(self.fn,self.Q)

        plt.title(out1)
    
        plt.draw()
        
###############################################################################          
        
    def accel_arbit_base(self):
                        
#  bc coefficients are applied to the excitation
            
        E=exp(-self.damp*self.omega*self.dt)
        K=self.omegad*self.dt
        C=E*cos(K)
        S=E*sin(K)
        Sp=S/K
        
        bc=np.zeros(3,'f')

        bc[0]=1.-Sp
        bc[1]=2.*(Sp-C)
        bc[2]=E**2-Sp

        self.a_resp=lfilter(bc, self.ac, self.b, axis=-1, zi=None)            
#
        a_pos= max(self.a_resp)
        a_neg= min(self.a_resp)     

        print ("\n Acceleration Response (G)")
        print ("\n  max = %8.4g   min = %8.4g  "    % (a_pos,a_neg))                       
        
        plt.close(2)
        plt.figure(2)

        plt.plot(self.a, self.a_resp, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel('Accel (G)')
        
        out1='SDOF Response Time History  fn=%g Hz, Q=%g ' %(self.fn,self.Q)
        

        plt.title(out1)
    
        plt.draw()
        

###############################################################################
        
    def a_coeff(self): 
        self.ac=np.zeros(3)    
        self.ac[0]=1   
        self.omegad=self.omega*sqrt(1.-(self.damp**2))        
        E=exp(-self.damp*self.omega*self.dt)
        K=self.omegad*self.dt
        C=E*cos(K)
        self.ac[1]=-2*C
        self.ac[2]=+E**2    
        

 
    def read_data(self):            
            
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
        plt.ylabel('Accel (G)')  
        plt.title('Base Input Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')    

###############################################################################

def quit(root):
    root.destroy()

###############################################################################