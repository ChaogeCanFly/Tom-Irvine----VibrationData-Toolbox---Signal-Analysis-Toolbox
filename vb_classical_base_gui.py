########################################################################
# program: vb_classical_base_gui.py
# author: Tom Irvine
# Email: tom@irvinemail.org
# version: 1.5
# date: August 26, 2017
# description:  
#    
#  This program calculates the response of a single-degree-of-freedom
#  system to a user-selected classical base input.
#              
########################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename
    from ttk import Treeview
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    from tkinter.ttk import Treeview
    import tkinter.messagebox as tkMessageBox   

import numpy as np

from math import sqrt,pi,sin,cos,exp,log10

import matplotlib.pyplot as plt

from vb_utilities import WriteData2,WriteData3

###############################################################################

class vb_classical_pulse_base:
      
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.30))
        h = int(2.*(h*0.32))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_classical_base_gui.py ver 1.5  by Tom Irvine")         
        
        
        self.Q=0
        self.damp=0
        
        self.fn=[]
        self.omegan=[]
        self.omegad=[]   
        self.domegan=[]
        self.omegan2=[]
        self.dt=[]
        self.nt=[]
 
        self.amax=[]
        self.amin=[]
        self.pvmax=[]
        self.pvmin=[]           
        self.rdmax=[]
        self.rdmin=[]        
 
        self.den=[]
        self.tt=[]
        self.acc=[]
        self.yb=[]
        self.rd=[]
        
        self.amp=0
        self.dur=0
        self.fstart=0
        self.fend=0
        self.oct=2.**(1./24.)
        self.numf=0
        self.omega=0

        self.rd_initial = 0.
        self.rv_initial = 0.               
        
        self.omega =0.
        self.omega2=0.       
        self.rd_scale=0.
        
        self.n_at=0

        
        crow=0
        
        self.hwtext1=tk.Label(top,text='SDOF Response to Classical Base Input')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=10,sticky=tk.W)  

        crow=crow+1        

        self.hwtext_blank1=tk.Label(top,text='')
        self.hwtext_blank1.grid(row=crow, column=0, columnspan=1, pady=1) 
        
        crow=crow+1       
        
        self.hwtext1=tk.Label(top,text='Select Analysis')
        self.hwtext1.grid(row=crow, column=0, columnspan=1, pady=5,sticky=tk.SW)

        self.hwtextLbx=tk.Label(top,text='Select Units')
        self.hwtextLbx.grid(row=crow, column=1,padx=3)        

        crow=crow+1
        
        self.Lb_at = tk.Listbox(top,height=2,width=25,exportselection=0)
        self.Lb_at.insert(1, "Time History Response")
        self.Lb_at.insert(2, "SRS")
        self.Lb_at.grid(row=crow, column=0, columnspan=1, pady=1,sticky=tk.NW)
        self.Lb_at.select_set(0) 
        self.Lb_at.bind("<<ListboxSelect>>", self.SelectAnalysis)  
        
        self.Lb_scale = tk.Listbox(top,height=2,exportselection=0)
        self.Lb_scale.insert(1, "G, in/sec, in")
        self.Lb_scale.insert(2, "G, cm/sec, mm")
        self.Lb_scale.grid(row=crow, column=1, pady=1)
        self.Lb_scale.select_set(0)         
        self.Lb_scale.bind('<<ListboxSelect>>', self.unit_change) 

        crow=crow+1        

        self.hwtext_blank2=tk.Label(top,text='')
        self.hwtext_blank2.grid(row=crow, column=0, columnspan=1, pady=1) 
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='Select Base Input Pulse')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=5,sticky=tk.SW) 
        
        self.hwtext_base_accel=tk.Label(top,text='Enter Acceleration (G)')
        self.hwtext_base_accel.grid(row=crow, column=1, columnspan=1, padx=18, pady=5,sticky=tk.S)
        
        self.hwtext_fn=tk.Label(top,text='Enter Duration (sec)')
        self.hwtext_fn.grid(row=crow, column=2, columnspan=1, padx=18, pady=5,sticky=tk.S)        
        
        crow=crow+1

        self.Lb_pulse = tk.Listbox(top,height=2,width=25,exportselection=0)
        self.Lb_pulse.insert(1, "Half-Sine")
        self.Lb_pulse.insert(2, "Terminal Sawtooth")
        self.Lb_pulse.grid(row=crow, column=0, columnspan=1, pady=1,sticky=tk.NW)
        self.Lb_pulse.select_set(0)         
           
  
        self.Ar=tk.StringVar()  
        self.Ar.set('')  
        self.A_entry=tk.Entry(top, width = 12,textvariable=self.Ar)
        self.A_entry.grid(row=crow, column=1,padx=18, pady=1,sticky=tk.N)  

        self.Tr=tk.StringVar()  
        self.Tr.set('')  
        self.T_entry=tk.Entry(top, width = 12,textvariable=self.Tr)
        self.T_entry.grid(row=crow, column=2,padx=18, pady=1,sticky=tk.N)  

###############################################################################

        crow=crow+1

        self.hwtext_fn=tk.Label(top,text='Enter Natural Frequency (Hz)')
        self.hwtext_fn.grid(row=crow, column=0, columnspan=1, padx=14, pady=10,sticky=tk.S)

     
        self.hwtext_Q=tk.Label(top,text='Enter Q')
        self.hwtext_Q.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S)
        
         
        self.idisp_text_r=tk.StringVar()    
        self.idisp_text_r.set('Initial Rel Disp (in)')         
        self.hwtext_idisp=tk.Label(top,textvariable=self.idisp_text_r)
        self.hwtext_idisp.grid(row=crow, column=2, columnspan=1, pady=10)        
        self.hwtext_idisp.config(state = 'normal')         

        self.ivel_text_r=tk.StringVar()    
        self.ivel_text_r.set('Initial Rel Vel (in/sec)')         
        self.hwtext_ivel=tk.Label(top,textvariable=self.ivel_text_r)
        self.hwtext_ivel.grid(row=crow, column=3, columnspan=1, pady=10)        
        self.hwtext_ivel.config(state = 'normal')       
        
        crow=crow+1        

        self.fnr=tk.StringVar()  
        self.fnr.set('')  
        self.fn_entry=tk.Entry(top, width = 12,textvariable=self.fnr)
        self.fn_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)  

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 12,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N) 
        
        self.idispr=tk.StringVar()  
        self.idispr.set('0')  
        self.idisp_entry=tk.Entry(top, width = 12,textvariable=self.idispr)
        self.idisp_entry.grid(row=crow, column=2,padx=14, pady=1,sticky=tk.N) 
         
        self.ivelr=tk.StringVar()  
        self.ivelr.set('0')  
        self.ivel_entry=tk.Entry(top, width = 12,textvariable=self.ivelr)
        self.ivel_entry.grid(row=crow, column=3,padx=14, pady=1,sticky=tk.N)        
        
        
        crow=crow+1      
        
        self.hwtext_start_freq=tk.Label(top,text='Enter Starting Frequency (Hz)')
        self.hwtext_start_freq.grid(row=crow, column=0, columnspan=1, padx=14, pady=15)
        self.hwtext_start_freq.config(state='disabled')
        
        self.hwtext_end_freq=tk.Label(top,text='Enter Ending Frequency (Hz)')
        self.hwtext_end_freq.grid(row=crow, column=1, columnspan=1, padx=14, pady=15)
        self.hwtext_end_freq.config(state='disabled') 
        
        crow=crow+1    

        self.fstartr=tk.StringVar() 
        self.fstart_entry=tk.Entry(top, width = 12,textvariable=self.fstartr)
        self.fstart_entry.grid(row=crow, column=0,padx=18, pady=1,sticky=tk.N) 
        self.fstart_entry.config(state='disabled') 
        
        self.fendr=tk.StringVar() 
        self.fend_entry=tk.Entry(top, width = 12,textvariable=self.fendr)
        self.fend_entry.grid(row=crow, column=1,padx=18, pady=1,sticky=tk.N)         
        self.fend_entry.config(state='disabled')
        
        crow=crow+1    
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate_main)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 

        root=self.master     

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=16) 
        
        crow=crow+1    
        
        self.etext=tk.StringVar()  
        self.etext.set('Export Time History Response')          
        self.hwtext_export=tk.Label(top,textvariable=self.etext)                
        self.hwtext_export.grid(row=crow, column=0,columnspan=2, padx=10,pady=10) 
        self.hwtext_export.config(state = 'disabled')
        
        crow=crow+1   
        
        self.button_acceleration = tk.Button(top, text="Acceleration", command=self.export_acceleration)
        self.button_acceleration.config( height = 2, width = 15,state='disabled')
        self.button_acceleration.grid(row=crow, column=0,columnspan=1, pady=1) 

        self.button_rel_disp = tk.Button(top, text="Rel Disp", command=self.export_rel_disp)
        self.button_rel_disp.config( height = 2, width = 15,state='disabled')
        self.button_rel_disp.grid(row=crow, column=1,columnspan=1, pady=1) 
        
################################################################################
        

    def export_acceleration(self):
         
        if(self.n_at==0):
            str="Enter the acceleration time history filename"
        else:
            str="Enter the acceleration SRS filename"
        
        output_file_path = asksaveasfilename(parent=self.master,title=str)                  
        output_file = output_file_path.rstrip('\n')    
 
        if(self.n_at==0):
            WriteData2(self.ex_nt[0],self.ex_tt,self.ex_acc,output_file)        
        else:
            nf=len(self.ex_fn)
            WriteData3(nf,self.ex_fn,self.ex_amax,self.ex_amin,output_file)

################################################################################
        
    def export_rel_disp(self):
         
        if(self.n_at==0):
            str="Enter the relative displacement time history filename"
        else:
            str="Enter the relative displacement SRS filename"
        
        output_file_path = asksaveasfilename(parent=self.master,title=str)                  
        output_file = output_file_path.rstrip('\n')    
 
        if(self.n_at==0):
            WriteData2(self.ex_nt[0],self.ex_tt,self.ex_rd,output_file)        
        else:
            nf=len(self.ex_fn)
            WriteData3(nf,self.ex_fn,self.ex_rdmax,self.ex_rdmin,output_file)
            
################################################################################        
        
    def calculate_main(self):
        

        self.Q=float(self.Qr.get())
        self.damp=1./(2.*self.Q)
        
        self.amp=float(self.Ar.get())
        self.dur=float(self.Tr.get())      
        
        self.rd_initial=float(self.idispr.get())
        self.rv_initial =float(self.ivelr.get())        
        
        
        

        self.omega = pi/self.dur
        self.omega2=self.omega**2

##        
        self.n_scale= int(self.Lb_scale.curselection()[0])
        
        if(self.n_scale==0):
            self.amp*=386.
        else:
            self.rd_initial/=1000.
            self.rv_initial/=100.
            self.amp*=9.81
        
        self.n_at= int(self.Lb_at.curselection()[0])



        if(self.n_at==0):  # time history
        
        
            f_string=self.fnr.get()
            
            if len(f_string) == 0: 
                tkMessageBox.showerror('Warning:','Enter natural frequency',parent=self.button_calculate)  
                
            
            fff=float(f_string)
            self.fn.append(fff)
            self.numf=1
            

            
        else:         # SRS
            self.fstart=float(self.fstartr.get())        
            self.fend=float(self.fendr.get())
            
            self.fn.append(self.fstart)
 
            for i in range(1,1000):
                self.fn.append(self.fn[i-1]*self.oct)
                if(self.fn[i]>self.fend):
                    self.numf=i
                    break           

        for i in range(0,self.numf):
            self.omegan.append(2*pi*self.fn[i])
            self.omegad.append(self.omegan[i]*sqrt(1-self.damp**2))
            self.domegan.append(self.damp*self.omegan[i])
            self.omegan2.append(self.omegan[i]**2)
            self.den.append((self.omega2-self.omegan2[i])**2.+\
                                 (2.*self.damp*self.omega*self.omegan[i])**2.)

            self.amax=np.zeros(self.numf,'f')
            self.amin=np.zeros(self.numf,'f')
            
            self.pvmax=np.zeros(self.numf,'f')
            self.pvmin=np.zeros(self.numf,'f')            

            self.rdmax=np.zeros(self.numf,'f')
            self.rdmin=np.zeros(self.numf,'f')

            period=1/self.fn[i]
    
            self.dt.append(period/32.)
    
            if self.dur/8. < self.dt[i]:
               self.dt[i]=self.dur/8.       
    
            if(self.n_at==0):       # time history    
                a_dur=6*period
                if a_dur < (self.dur+5*period):
                    a_dur = self.dur+5*period
            else:              # srs 
                a_dur=self.dur+period             

            self.nt.append(int(a_dur/self.dt[i]))            

##

        n_pulse= int(self.Lb_pulse.curselection()[0])

        
        if(n_pulse==0):
            vb_classical_pulse_base.calculate_half_sine(self)
        else:
            vb_classical_pulse_base.calculate_terminal_sawtooth(self)
            
         
            

        if(self.n_at==0):
            
            print (" ")
            print (" Acceleration ")
            print ("    Max= %8.4g G   Min= %8.4g G " %(self.amax[0],self.amin[0]))
            print (" ")
            print (" Relative Displacement ")
            
            if(self.n_scale==0):
                print ("    Max= %8.4g in   Min= %8.4g in " %(self.rdmax[0],self.rdmin[0]))
            else:
                print ("    Max= %8.4g mm   Min= %8.4g mm " %(self.rdmax[0],self.rdmin[0]))

                
 
        

            print (" ")
            print ("View plots")            
            
            vb_classical_pulse_base.classical_plot_th(self.Q,f_string,\
                                      self.tt,self.acc,self.yb,self.rd,self.n_scale)
                    
        else:
            
            nf=len(self.fn)
            na=len(self.amax)

            if(nf>na):
                self.fn=self.fn[0:na]
            

            for i in range(0,self.numf):
                self.pvmax[i]=self.rdmax[i]*self.omegan[i]
                self.pvmin[i]=self.rdmin[i]*self.omegan[i]
            
                if(self.n_scale==1):
                    self.pvmax[i]/=10.
                    self.pvmin[i]/=10.                
            
            fignum=1
            srs_type=1
            unit=self.n_scale
            stitle="accel_SRS"
            x_pos=self.amax
            x_neg=self.amin
            vb_classical_pulse_base.classical_srs_plot_pn(fignum,srs_type,unit,\
                                             self.fn,x_pos,x_neg,stitle,self.Q)
                                             
            fignum=2
            srs_type=2
            unit=self.n_scale
            stitle="pv_SRS"
            x_pos=self.pvmax
            x_neg=self.pvmin
            vb_classical_pulse_base.classical_srs_plot_pn(fignum,srs_type,unit,\
                                             self.fn,x_pos,x_neg,stitle,self.Q)                                             
                                             
            fignum=3
            srs_type=3
            unit=self.n_scale
            stitle="rd_SRS"
            x_pos=self.rdmax
            x_neg=self.rdmin
            vb_classical_pulse_base.classical_srs_plot_pn(fignum,srs_type,unit,\
                                             self.fn,x_pos,x_neg,stitle,self.Q)  
                                             
        self.hwtext_export.config(state = 'normal')                                         
        self.button_acceleration.config(state='normal')
        self.button_rel_disp.config(state='normal')
    
  
        self.ex_fn=self.fn
        self.ex_amax=self.amax
        self.ex_amin=self.amin
        self.ex_rdmax=self.rdmax
        self.ex_rdmin=self.rdmin       
  
        self.ex_nt=self.nt
        self.ex_tt=self.tt
        self.ex_acc=self.acc
        self.ex_rd=self.rd
  
####  
      
        while(len(self.amax)>0):
            self.amax = np.delete(self.amax, [0], axis=0)       

        while(len(self.amin)>0):
            self.amin = np.delete(self.amin, [0], axis=0)  
  
        while(len(self.pvmax)>0):
            self.pvmax = np.delete(self.pvmax, [0], axis=0)       

        while(len(self.pvmin)>0):
            self.pvmin = np.delete(self.pvmin, [0], axis=0)   
  
        while(len(self.rdmax)>0):
            self.rdmax = np.delete(self.rdmax, [0], axis=0)       

        while(len(self.rdmin)>0):
            self.rdmin = np.delete(self.rdmin, [0], axis=0)     
  
####  
  
        while(len(self.fn)>0):
            self.fn = np.delete(self.fn, [0], axis=0)    
   
        while(len(self.omegan)>0):
            self.omegan = np.delete(self.omegan, [0], axis=0)     
   
        while(len(self.omegad)>0):
            self.omegad = np.delete(self.omegad, [0], axis=0)     
   
        while(len(self.domegan)>0):
            self.domegan = np.delete(self.domegan, [0], axis=0) 
            
        while(len(self.omegan2)>0):
            self.omegan2 = np.delete(self.omegan2, [0], axis=0)   
            
        while(len(self.den)>0):
            self.den = np.delete(self.den, [0], axis=0)  
            
        while(len(self.dt)>0):
            self.dt = np.delete(self.dt, [0], axis=0)              
            
        while(len(self.nt)>0):
            self.nt = np.delete(self.nt, [0], axis=0)               
            
        self.fn=[]
        self.omegan=[]
        self.omegad=[]   
        self.domegan=[]
        self.omegan2=[]
        self.dt=[]
        self.nt=[]
        self.amax=[]
        self.amin=[]
        self.pvmax=[]
        self.pvmin=[]        
        self.rdmax=[]
        self.rdmin=[]        
        self.den=[]            
   
    
    @classmethod       
    def classical_plot_th(cls,Q,fff,tt,acc,yb,rd,n_scale):
        
        
        
        title_string_acc='Acceleration SDOF Response fn= '+ fff +' Hz   Q='+str(Q)
        title_string_rd='Rel Disp  SDOF Response fn= '+ fff +' Hz   Q='+str(Q)        
#
        for i in range(1,200):
            if(Q==float(i)):
                title_string_acc='Acceleration SDOF Response fn= '+ fff +' Hz   Q='+str(i)
                title_string_rd='Rel Disp  SDOF Response fn= '+ fff +' Hz   Q='+str(i)                    
                break
#
        plt.close(1)
        plt.figure(1)
        plt.plot(tt, acc, label="response")
        plt.plot(tt, yb, label="input")
        plt.xlabel('Time (sec)')
        plt.ylabel('Accel (G)')
        plt.grid(True)
        plt.title(title_string_acc)
        plt.legend(loc="upper right") 
        plt.draw()
#
        plt.close(2)
        plt.figure(2)
        plt.plot(tt, rd)
        plt.xlabel('Time (sec)')

        if(n_scale==0): 
            plt.ylabel('Rel Disp (in)')
        else:
            plt.ylabel('Rel Disp (mm)')            
        
        plt.grid(True)
        plt.title(title_string_rd)
        axes = plt.gca()
        myformatter = plt.ScalarFormatter(useMathText=True)
        myformatter.set_powerlimits((-3,3))
        axes.yaxis.set_major_formatter(myformatter)
        plt.draw()
        plt.show()
#    
    @classmethod    
    def classical_srs_plot_pn(cls,fignum,srs_type,unit,fn,x_pos,x_neg,stitle,Q):
        """
        Plot and SRS with both positive and negative curves.
           srs_type = 1 for acceleration
                    = 2 for pseudo velocity
                    = 3 for relative displacement

               unit = 0 for English
                    = 1 for metric

                 fn = natural frequency

        x_pos,x_eng = postive, negative SRS
    
               damp = damping ratio

             stitle = output figure filename
        """
        x_neg=abs(x_neg)
        
        if(srs_type !=1 and srs_type !=2 and srs_type !=3):
            srs_type=1

        if(unit !=0 and unit !=1):
            unit=0

        if(srs_type==1): # acceleration
            astr='Acceleration'
            ymetric='Peak Accel (G)'
   

        if(srs_type==2): # pseudo velocity
            astr='Pseudo Velocity'

            if(unit==0): # English
                ymetric='Pseudo Velocity (in/sec)'
            if(unit==1): # metric
                ymetric='Pseudo Velocity (cm/sec)'


        if(srs_type==3): # relative displacement
            astr='Relative Displacement'

            if(unit==0): # English
                ymetric='Relative Disp (in)'
            if(unit==1): # metric
                ymetric='Relative Disp (mm)'

        plt.close(fignum)
        plt.figure(fignum)
        plt.plot(fn, x_pos, label="positive")
        plt.plot(fn, x_neg, label="negative")
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
        
        amax=max(x_pos)
        bmax=max(x_neg)
        amin=min(x_pos)
        bmin=min(x_neg)
        
        if(bmax>amax):
            amax=bmax
            
        if(bmin<amin):
            amin=bmin
        
        a2=10**(np.ceil(0.2+log10(amax)))
        a1=10**(np.floor(log10(amin)))
        if(a1<a2/10000):
            a1=a2/10000
            
            
        plt.ylim([a1,a2])
#
        title_string= astr + ' Shock Response Spectrum Q='+str(Q)
#
        for i in range(1,200):
            if(Q==float(i)):
                title_string= astr +' Shock Response Spectrum Q='+str(i)
                break;
#
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')
        plt.ylabel(ymetric)
        plt.grid(True, which="both")
        plt.savefig(stitle)
        plt.legend(loc="upper right")
        plt.draw()

################################################################################
    
    @classmethod        
    def calculate_half_sine(cls,self):
       
        for k in range (0,self.numf):        
        
            ntp1=self.nt[k]+1
    
            self.yb=np.zeros(ntp1,'f')
            self.acc=np.zeros(ntp1,'f')
            self.rd=np.zeros(ntp1,'f')
            self.tt=np.zeros(ntp1,'f')

            a1=self.rd_initial;
            a2=(self.rv_initial+self.domegan[k]*self.rd_initial)/self.omegad[k]

            b1=2.*self.damp*self.omega*self.omegan[k]
            b2=(self.omega2-self.omegan2[k])

            c1=2.*self.domegan[k]*self.omegad[k]
            c2=self.omega2-self.omegan2[k]*(1.-2*(self.damp**2.))

            zT,vT=vb_classical_pulse_base.find_half_sine_residual(self.dur,\
                      self.omega,self.omegad[k],self.omegan[k],self.domegan[k],
                                        a1,a2,b1,b2,c1,c2,self.amp,self.den[k])


#  Find residual parameters


            for i in range (0,self.nt[k]):
                t=i*self.dt[k]
                self.tt[i+1]=t

                if t <= self.dur:
                    omegat=self.omega*t
                    omegadt=self.omegad[k]*t
                    domegant=self.domegan[k]*t

                    ee=exp(-domegant)
                    cwdt=cos(omegadt)
                    swdt=sin(omegadt)

                    cat = cos(omegat)
                    sat = sin(omegat)

                    ain= self.amp*sin(omegat)
				
                    rd1=ee         *(a1*cwdt + a2*swdt)
                    rd2=(self.amp/self.den[k])  *(b1*cat  + b2*sat )
                    rd3=-((self.amp/self.den[k])*ee*self.omega/self.omegad[k])*(c1*cwdt + c2*swdt)
				
                    self.rd[i+1]=rd1+rd2+rd3

                    rv1=-self.domegan[k]*rd1
                    rv1+=self.omegad[k]*ee*(-a1*swdt + a2*cwdt)
                    rv2=self.omega*(self.amp/self.den[k])  *(-b1*sat  + b2*cat )				
                    rv3=-self.domegan[k]*rd3
                    rv3+=-((self.amp/self.den[k])*ee*self.omega)*(-c1*swdt + c2*cwdt)

                    rv=rv1+rv2+rv3
                else:
                    ain=0.

                    tdur=t-self.dur
                    omegat=self.omega*(tdur)
                    omegadt=self.omegad[k]*(tdur)
                    domegant=self.domegan[k]*(tdur)

                    ee=exp(-domegant)
                    cwdt=cos(omegadt)
                    swdt=sin(omegadt)

                    a1=zT
                    a2=(vT+self.domegan[k]*zT)/self.omegad[k]

                    self.rd[i+1] = ee *(a1*cwdt + a2*swdt)

                    rv= -self.domegan[k]*self.rd[i+1]
                    rv+= self.omegad[k]*ee *(-a1*swdt + a2*cwdt);


                self.yb[i+1]=ain

                self.acc[i+1]= -self.omegan2[k]*self.rd[i+1]  - 2.*self.domegan[k]*rv
                  
    
                
            if(self.n_scale==0):
                self.acc/=386.
                self.yb/=386.
            else:
                self.acc/=9.81
                self.yb/=9.81
                self.rd*=1000
                               
    
            self.amax[k]=max(self.acc)
            self.amin[k]=abs(min(self.acc))

            self.rdmax[k]=max(self.rd)
            self.rdmin[k]=abs(min(self.rd))
            

################################################################################

    @classmethod
    def calculate_terminal_sawtooth(cls,self):
        

       
        for k in range (0,self.numf):        
        
            ntp1=self.nt[k]+1
    
            self.yb=np.zeros(ntp1,'f')
            self.acc=np.zeros(ntp1,'f')
            self.rd=np.zeros(ntp1,'f')
            self.tt=np.zeros(ntp1,'f')

            a1=self.rd_initial
            a2=(self.rv_initial+self.domegan[k]*self.rd_initial)/self.omegad[k]


            b1=2*self.damp/self.omegan[k]
            b2=(2*(self.damp**2)-1)/self.omegad[k]

            t=self.dur

            omegadt=self.omegad[k]*t
            ee=exp(-self.domegan[k]*t)
            cwdt=cos(omegadt)
            swdt=sin(omegadt)

            rdf=ee*(a1*cwdt + a2*swdt)

            zT=b1-t-ee*(b1*cwdt + b2*swdt)
            zT*=self.amp/(self.omegan2[k]*self.dur)
            zT+=rdf

            vT=-1+self.domegan[k]*ee*(b1*cwdt + b2*swdt)
            vT+=-self.omegad[k]*ee*(-b1*swdt + b2*cwdt)
            vT*=self.amp/(self.omegan2[k]*self.dur)
            
            vT+=-self.domegan[k]*rdf+self.omegad[k]*ee*(-a1*swdt + a2*cwdt)


            for i in range (0,self.nt[k]):
                t=i*self.dt[k]
                self.tt[i+1]=t

                if t <= self.dur:
                    ain=self.amp*t/self.dur
                    omegadt=self.omegad[k]*t
                    ee=exp(-self.domegan[k]*t)
                    cwdt=cos(omegadt)
                    swdt=sin(omegadt)
                    
                    rdf=ee*(a1*cwdt + a2*swdt)

                    self.rd[i+1]=b1-t-ee*(b1*cwdt + b2*swdt)
                    self.rd[i+1]*=self.amp/(self.omegan2[k]*self.dur)
                    
                    self.rd[i+1]+=rdf                     
                    

                    rv=-1+self.domegan[k]*ee*(b1*cwdt + b2*swdt)
                    rv+=-self.omegad[k]*ee*(-b1*swdt + b2*cwdt)
                    rv*=self.amp/(self.omegan2[k]*self.dur)
                    
                    rv+=-self.domegan[k]*rdf+self.omegad[k]*ee*(-b1*swdt + b2*cwdt)
          
                else:
                    ain=0.

                    tdur=t-self.dur
                    omegadt=self.omegad[k]*(tdur)
                    domegant=self.domegan[k]*(tdur)

                    ee=exp(-domegant)
                    cwdt=cos(omegadt)
                    swdt=sin(omegadt)

                    a1=zT
                    a2=(vT+self.domegan[k]*zT)/self.omegad[k]

                    self.rd[i+1] = ee *(a1*cwdt + a2*swdt)

                    rv= -self.domegan[k]*self.rd[i+1]
                    rv+= self.omegad[k]*ee *(-a1*swdt + a2*cwdt);


                self.yb[i+1]=ain

                self.acc[i+1]= -self.omegan2[k]*self.rd[i+1]  - 2.*self.domegan[k]*rv
                
                
            if(self.n_scale==0):
                self.acc/=386.
                self.yb/=386.
            else:
                self.acc/=9.81
                self.yb/=9.81
                self.rd*=1000
                               
    
            self.amax[k]=max(self.acc)
            self.amin[k]=abs(min(self.acc))

            self.rdmax[k]=max(self.rd)
            self.rdmin[k]=abs(min(self.rd))
                
    
###############################################################################
    
    def unit_change(self,val):
        
#        map(self.tree.delete, self.tree.get_children())        

        nfa_choice=int(self.Lb_scale.curselection()[0])

        if(nfa_choice==0):
         
            self.idisp_text_r.set('Initial Rel Disp (in)')
            self.ivel_text_r.set('Initial Rel Vel (in/sec)')  
                                  
        else:       
            
            self.idisp_text_r.set('Initial Rel Disp (mm)')
            self.ivel_text_r.set('Initial Rel Vel (cm/sec)') 
    
###############################################################################    

    def SelectAnalysis(self,event):
        
        n= int(self.Lb_at.curselection()[0])         
        
        if(n==0):
            self.hwtext_fn.config(state='normal')
            self.fn_entry.config(state='normal')  
#            
            self.hwtext_start_freq.config(state='disabled')            
            self.hwtext_end_freq.config(state='disabled')  
            self.fstart_entry.config(state='disabled') 
            self.fend_entry.config(state='disabled') 
            self.fstartr.set('')
            self.fendr.set('')     
            self.etext.set('Export Time History Response')  
        else:
            self.hwtext_fn.config(state='disabled')
            self.fn_entry.config(state='disabled')          
            self.fnr.set('')
#            
            self.hwtext_start_freq.config(state='normal')            
            self.hwtext_end_freq.config(state='normal')
            self.fstart_entry.config(state='normal') 
            self.fend_entry.config(state='normal')  
            self.etext.set('Export Shock Response Spectra')              
###############################################################################

    @classmethod
    def find_half_sine_residual(cls,dur,omega,omegad,omegan,domegan,\
                                                    a1,a2,b1,b2,c1,c2,amp,den):    
        t=dur
        omegat=omega*t
        omegadt=omegad*t
#    omegant=omegan*t
        domegant=domegan*t

        ee=exp(-domegant)
        cwdt=cos(omegadt)
        swdt=sin(omegadt)

        cat = cos(omegat)
        sat = sin(omegat)



#    ain= amp*sin(omegat)
				
        rd1=ee         *(a1*cwdt + a2*swdt)
        rd2=(amp/den)  *(b1*cat  + b2*sat )
        rd3=-((amp/den)*ee*omega/omegad)*(c1*cwdt + c2*swdt)
				

        rdT=rd1+rd2+rd3

        rv1=-domegan*rd1
        rv1+=omegad*ee*(-a1*swdt + a2*cwdt)

        rv2=omega*(amp/den)  *(-b1*sat  + b2*cat )				

        rv3=-domegan*rd3
        rv3+=-((amp/den)*ee*omega)*(-c1*swdt + c2*cwdt)
        

        rvT=rv1+rv2+rv3

        zT=rdT
        vT=rvT
    
        return zT,vT      


###############################################################################           

def quit(root):
    root.destroy()           
