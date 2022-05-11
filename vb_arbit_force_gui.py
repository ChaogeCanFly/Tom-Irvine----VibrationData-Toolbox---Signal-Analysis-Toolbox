##########################################################################
# program: vb_arbit_force_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.1
# date: October 24, 2014
# description:  
#
# Calculate the response of an SDOF system to an applied force.
# The file must have two columns: time(sec) & force
#
# The numerical engine is a Smallwood-type ramp invariant digital
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

class vb_arbit_force:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.25))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_arbit_force_gui.py ver 1.1  by Tom Irvine") 
        
        self.damp=0
        self.Q=0
        self.fn=0
        self.a_resp=[]
        self.rd_resp=[]        
        self.ac=[]
        self.num=0
        
        crow=0        
        
        self.hwtext1=tk.Label(top,text='SDOF Response for Applied Force')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & Force')
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
        self.hwtextQ.grid(row=crow, column=2,padx=0,sticky=tk.E)

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 5,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=3,sticky=tk.W)

###############################################################################
        
        crow=crow+1  

        self.hwtextfn=tk.Label(top,text='Select Units')
        self.hwtextfn.grid(row=crow, column=0,columnspan=1,padx=15)
        
        
        self.mass_text=tk.StringVar()  
        self.mass_text.set('Enter Mass (lbm)')         
        self.hwtext_mass=tk.Label(top,textvariable=self.mass_text)        
        self.hwtext_mass.grid(row=crow, column=1,columnspan=1,padx=15)


        crow=crow+1
        
        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "lbf & lbm")
        self.Lb1.insert(2, "N & kg")
        self.Lb1.grid(row=crow, column=0, pady=1,sticky=tk.E)
        self.Lb1.select_set(0) 
        self.Lb1.bind('<<ListboxSelect>>',self.unit_option)  


        self.massr=tk.StringVar()  
        self.massr.set(' ')  
        self.mass_entry=tk.Entry(top, width = 10,textvariable=self.massr)
        self.mass_entry.grid(row=crow, column=1)
        
###############################################################################
        
        crow=crow+1   

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 
        
        root=self.master    

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=10,pady=20)  
        
        crow=crow+1        
        
        self.hwtextext_ex=tk.Label(top,text='Export Response Data')
        self.hwtextext_ex.grid(row=crow, column=0,pady=10)  
        self.hwtextext_ex.config(state = 'disabled')
        
        crow=crow+1   
        
        self.button_sa = tk.Button(top, text="Acceleration", command=self.export_accel)
        self.button_sa.config( height = 2, width = 15,state = 'disabled' )
        self.button_sa.grid(row=crow, column=0,columnspan=1, pady=3, padx=1)  

        self.button_sv = tk.Button(top, text="Velocity", command=self.export_vel)
        self.button_sv.config( height = 2, width = 15,state = 'disabled' )
        self.button_sv.grid(row=crow, column=1,columnspan=1, pady=3, padx=1)    
        
        self.button_sd = tk.Button(top, text="Displacement", command=self.export_disp)
        self.button_sd.config( height = 2, width = 15,state = 'disabled' )
        self.button_sd.grid(row=crow, column=2,columnspan=1, pady=3, padx=1)  

        self.button_sft = tk.Button(top, text="Transmitted Force", command=self.export_trans_force)
        self.button_sft.config( height = 2, width = 15,state = 'disabled' )
        self.button_sft.grid(row=crow, column=3,columnspan=1, pady=3, padx=1)           

###############################################################################  

    def calculation(self):
        
        self.Q=float(self.Qr.get())        

        self.mass=float(self.massr.get())
        
        self.mass_orig=self.mass



        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):
            self.mass=self.mass/386.     


        self.a=np.array(self.a)
        self.b=np.array(self.b)


        self.damp=1./(2.*self.Q) 
        self.fn=float(self.fnr.get())
        
        self.omegan=2*np.pi*self.fn
        self.omegad=self.omegan*sqrt(1.-(self.damp**2))  
        
        self.domegadt=self.damp*self.omegan*self.dt
 
        self.eee1=exp(-self.domegadt)
        self.eee2=exp(-2.*self.domegadt)
        
        self.cosd=cos(self.omegad*self.dt)
        self.sind=sin(self.omegad*self.dt)

        self.ecosd=self.eee1*self.cosd
        self.esind=self.eee1*self.sind 

        self.ac=np.zeros(3) 

        self.ac[0]= 1
        self.ac[1]= -2.*self.ecosd
        self.ac[2]= self.eee2

        self.omeganT=self.omegan*self.dt


        
        self.accel_arbit_force(self)
        self.vel_arbit_force(self)        
        self.disp_arbit_force(self)
        self.trans_force(self)
                
        
        
        self.hwtextext_ex.config(state = 'normal')
        self.button_sa.config(state = 'normal')
        self.button_sv.config(state = 'normal')
        self.button_sd.config(state = 'normal')        
        self.button_sft.config(state = 'normal')            
        
        
###############################################################################          
    
    @classmethod       
    def accel_arbit_force(cls,self):

        self.a_coeff(self)
                     
            
        self.a_resp=lfilter(self.af, self.ac, self.b, axis=-1, zi=None)            
#

        n1=int(self.Lb1.curselection()[0])
        
        
        if(n1==0):
            self.a_resp=self.a_resp/386.     
        else:    
            self.a_resp=self.a_resp/9.81        
        
        
        a_pos= max(self.a_resp)
        a_neg= min(self.a_resp)     
        a_sd=np.std(self.a_resp)


        plt.ion()        
        plt.close(2)
        plt.figure(2)

        plt.plot(self.a, self.a_resp, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')


        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):   
            plt.ylabel('Accel (G)')   
            print ("\n Accel (G)") 
            out1='SDOF Acceleration Response  mass=%g lbm, fn=%g Hz, Q=%g ' %(self.mass_orig,self.fn,self.Q)
        else:
            plt.ylabel('Accel (m/sec^2)')     
            print ("\n Accel (m/sec^2)")
            out1='SDOF Acceleration Response  mass=%g kg, fn=%g Hz, Q=%g ' %(self.mass_orig,self.fn,self.Q)


        print ("\n  max = %8.4g   min = %8.4g   std dev = %8.4g"    % (a_pos,a_neg,a_sd))  
        
        plt.title(out1)    
        plt.draw()

    @classmethod   
    def vel_arbit_force(cls,self):        

        self.v_coeff(self)
            
        self.v_resp=lfilter(self.vf, self.ac, self.b, axis=-1, zi=None)            
#
        v_pos= max(self.v_resp)
        v_neg= min(self.v_resp)     
        v_sd=np.std(self.v_resp)


        plt.ion()           
        plt.close(3)
        plt.figure(3)

        plt.plot(self.a, self.v_resp, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')


        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):   
            plt.ylabel('Vel (in/sec)')   
            print ("\n Vel (in/sec)") 
            out1='SDOF Velocity Response  mass=%g lbm, fn=%g Hz, Q=%g ' %(self.mass_orig,self.fn,self.Q)
        else:
            plt.ylabel('Vel (m/sec)')     
            print ("\n Vel (m/sec)")
            out1='SDOF Velocity Response  mass=%g kg, fn=%g Hz, Q=%g ' %(self.mass_orig,self.fn,self.Q)

       
        print ("\n  max = %8.4g   min = %8.4g  std dev = %8.4g"    % (v_pos,v_neg,v_sd))      
                         
        
        plt.title(out1)    
        plt.draw()
        

    @classmethod      
    def disp_arbit_force(cls,self):
    
        self.d_coeff(self)
        
            
        self.d_resp=lfilter(self.df, self.ac, self.b, axis=-1, zi=None) 


        n1=int(self.Lb1.curselection()[0])
        
        if(n1==1):
            self.d_resp=self.d_resp*1000
           
#
        d_pos= max(self.d_resp)
        d_neg= min(self.d_resp)     
        d_sd=np.std(self.d_resp)

        plt.ion()           
        plt.close(4)
        plt.figure(4)

        plt.plot(self.a, self.d_resp, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
   
        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):   
            plt.ylabel('Disp (in)')   
            print ("\n Disp (in)") 
            out1='SDOF Displacement Response  mass=%g lbm, fn=%g Hz, Q=%g ' %(self.mass_orig,self.fn,self.Q)
        else:
            plt.ylabel('Disp (mm)')     
            print ("\n Disp (mm)")
            out1='SDOF Displacement Response  mass=%g kg, fn=%g Hz, Q=%g ' %(self.mass_orig,self.fn,self.Q)



        print ("\n  max = %8.4g   min = %8.4g  std dev = %8.4g"    % (d_pos,d_neg,d_sd)) 
        
        plt.title(out1)    
        plt.draw()


    @classmethod   
    def trans_force(cls,self):        
        
        self.ft_resp=self.b-self.mass*self.a_resp        


        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):   
            self.ft_resp=self.b-(self.mass*self.a_resp*386)  
        else:
            self.ft_resp=self.b-(self.mass*self.a_resp*9.81)  

        
        ft_pos= max(self.ft_resp)
        ft_neg= min(self.ft_resp)     
        ft_sd=np.std(self.ft_resp)

                     
        plt.ion()           
        plt.close(5)
        plt.figure(5)

        plt.plot(self.a, self.ft_resp, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        
        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):
            plt.ylabel('Force (lbf)')   
            print ("\n Transmitted Force (lbf)") 
            out1='SDOF Transmitted Force  mass=%g lbm, fn=%g Hz, Q=%g ' %(self.mass_orig,self.fn,self.Q)
        else:
            plt.ylabel('Force (N)')     
            print ("\n Transmitted Force (N)")
            out1='SDOF Transmitted Force  mass=%g kg, fn=%g Hz, Q=%g ' %(self.mass_orig,self.fn,self.Q)
        
        
        print ("\n  max = %8.4g   min = %8.4g  std dev = %8.4g"    % (ft_pos,ft_neg,ft_sd))  
        
        
        plt.title(out1)    
        plt.draw()        

        

###############################################################################
        
    @classmethod           
    def a_coeff(cls,self):
        self.af=np.zeros(3)                
        self.af[0]=self.esind/(self.mass*self.omegad*self.dt)
        self.af[1]=-2*self.af[0]
        self.af[2]=self.af[0]        


    @classmethod   
    def v_coeff(cls,self): 
        self.vf=np.zeros(3) 
        VV1=-(self.damp*self.omegan/self.omegad)
        
        self.vf[0]=(-self.ecosd+VV1*self.esind)+1
        self.vf[1]=self.eee2-2*VV1*self.esind-1
        self.vf[2]=self.ecosd+VV1*self.esind-self.eee2        

        VD=(self.mass*self.omegan**2*self.dt)
        self.vf=self.vf/VD   
                

    @classmethod   
    def d_coeff(cls,self): 
        phi=2*(self.damp)**2-1
        DD1=(self.omegan/self.omegad)*phi
        DD2=2*DD1

        self.df=np.zeros(3)     
        self.df[0]=2*self.damp*(self.ecosd-1) +DD1*self.esind +self.omeganT
        self.df[1]=-2*self.omeganT*self.ecosd +2*self.damp*(1-self.eee2) -DD2*self.esind
        self.df[2]=(2*self.damp+self.omeganT)*self.eee2 +(DD1*self.esind-2*self.damp*self.ecosd)
    
        MD=(self.mass*self.omegan**3*self.dt)
        self.df=self.df/MD        
    
 
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

        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):
            plt.ylabel('Force (lbf)')   
        else:
            plt.ylabel('Force (N)')             

        
        plt.title('Force Input Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')    

###############################################################################

    def unit_option(self,val):
        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):
            self.mass_text.set('Enter Mass (lbm)') 
        else:
            self.mass_text.set('Enter Mass (kg)')         
        
###############################################################################        

    def export_accel(self):
        root=self.master    
        output_file_path = asksaveasfilename(parent=root,title="Enter the acceleration filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2(self.num,self.a,self.a_resp,output_file)        
        
    def export_vel(self):
        root=self.master    
        output_file_path = asksaveasfilename(parent=root,title="Enter the velocity filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2(self.num,self.a,self.v_resp,output_file)            
        
    def export_disp(self):
        root=self.master    
        output_file_path = asksaveasfilename(parent=root,title="Enter the displacement filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2(self.num,self.a,self.d_resp,output_file)  
        
    def export_trans_force(self):
        root=self.master    
        output_file_path = asksaveasfilename(parent=root,title="Enter the transmitted force filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2(self.num,self.a,self.ft_resp,output_file)          
        

###############################################################################

def quit(root):
    root.destroy()

###############################################################################