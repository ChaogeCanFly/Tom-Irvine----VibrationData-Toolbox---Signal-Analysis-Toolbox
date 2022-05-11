###############################################################################
# program: vb_double_integrate_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.0
# date: January 19, 2015
# description:  
#    
#  This scripts integrates a time history
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
    
    
from vb_utilities import read_two_columns_from_dialog,sample_rate_check,WriteData2    

from vb_utilities import BUTTERWORTH,integrate_th,half_cosine_fade_perc

from numpy import mean,std,zeros,polyfit
from scipy import signal

import matplotlib.pyplot as plt

###############################################################################

class vb_double_integrate:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.28))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_double_integrate_gui.py ver 1.0  by Tom Irvine") 

        
        self.t=[]
        self.b=[]
        self.bb=[]
        self.v=[]        
        self.num=0        
        self.dt=0             
        self.sr=0     
        
        crow=0
        
        self.hwtext1=tk.Label(top,text='This script integrates an acceleration time history to velocity and displacement.')
        self.hwtext1.grid(row=crow, column=0, columnspan=6,pady=7,sticky=tk.W)      

        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=5, pady=7,sticky=tk.W)
        
        
        
        crow=crow+1
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W) 
        
        crow=crow+1
        
        self.hwtext3=tk.Label(top,text='Select Units')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)
        
        self.hwtext4=tk.Label(top,text='Acceleration Processing')
        self.hwtext4.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.S)

        self.hwtext5=tk.Label(top,text='Velocity Processing')
        self.hwtext5.grid(row=crow, column=2, columnspan=1, pady=7,sticky=tk.S)

        self.hwtext6=tk.Label(top,text='Displacement Processing')
        self.hwtext6.grid(row=crow, column=3, columnspan=1, pady=7,sticky=tk.S)        
                
        
        crow=crow+1
        
        self.Lb1 = tk.Listbox(top,height=4,width = 22,exportselection=0)
        self.Lb1.insert(1, "G, in/sec, in")
        self.Lb1.insert(2, "G, cm/sec, mm")
        self.Lb1.insert(3, "m/sec^2, cm/sec, mm")
        self.Lb1.grid(row=crow, column=0, columnspan=1, pady=1,sticky=tk.N)
        self.Lb1.select_set(0) 
        
        self.Lba = tk.Listbox(top,height=6,width = 26,exportselection=0)
        self.Lba.insert(1, "none")
        self.Lba.insert(2, "mean removal")
        self.Lba.insert(3, "1st order trend removal")
        self.Lba.insert(4, "2nd order trend removal")        
        self.Lba.insert(5, "3rd order trend removal")
        self.Lba.insert(6, "highpass filter")        
        self.Lba.grid(row=crow, column=1, columnspan=1, pady=1,padx=6,sticky=tk.N)
        self.Lba.select_set(0)      
        self.Lba.bind('<<ListboxSelect>>', self.Lba_change)         
        
        self.Lbv = tk.Listbox(top,height=5,width = 26,exportselection=0)
        self.Lbv.insert(1, "none")
        self.Lbv.insert(2, "mean removal")
        self.Lbv.insert(3, "1st order trend removal")
        self.Lbv.insert(4, "2nd order trend removal")        
        self.Lbv.insert(5, "3rd order trend removal")
        self.Lbv.grid(row=crow, column=2, columnspan=1, pady=1,padx=6,sticky=tk.N)
        self.Lbv.select_set(0)      

        self.Lbd = tk.Listbox(top,height=5,width = 26,exportselection=0)
        self.Lbd.insert(1, "none")
        self.Lbd.insert(2, "mean removal")
        self.Lbd.insert(3, "1st order trend removal")
        self.Lbd.insert(4, "2nd order trend removal")        
        self.Lbd.insert(5, "3rd order trend removal")
        self.Lbd.grid(row=crow, column=3, columnspan=1, pady=1,padx=6,sticky=tk.N)
        self.Lbd.select_set(0)       
        
###############################################################################

        crow=crow+1        

        self.hwtext33=tk.Label(top,text='Highpass Filter Freq (Hz)')
        self.hwtext33.grid(row=crow, column=0, columnspan=1, padx=10,pady=7)
        self.hwtext33.config(state = 'disabled')      
        
        self.hwtext44=tk.Label(top,text='Velocity Fade Percent')
        self.hwtext44.grid(row=crow, column=2, columnspan=1, padx=10,pady=7)
   
        self.hwtext55=tk.Label(top,text='Displacement Fade Percent')
        self.hwtext55.grid(row=crow, column=3, columnspan=1, padx=10,pady=7)
     

        crow=crow+1        
        
        self.f_string=tk.StringVar()  
        self.f_string.set('')  
        self.f_string_entry=tk.Entry(top, width = 10,textvariable=self.f_string)
        self.f_string_entry.grid(row=crow, column=0,columnspan=1,padx=10, pady=2,sticky=tk.N)        
        self.f_string_entry.config(state = 'disabled')         
      
        self.fv_string=tk.StringVar()  
        self.fv_string.set('0')  
        self.fv_string_entry=tk.Entry(top, width = 10,textvariable=self.fv_string)
        self.fv_string_entry.grid(row=crow, column=2,columnspan=1,padx=10, pady=2,sticky=tk.N) 
        
        self.fd_string=tk.StringVar()  
        self.fd_string.set('0')  
        self.fd_string_entry=tk.Entry(top, width = 10,textvariable=self.fd_string)
        self.fd_string_entry.grid(row=crow, column=3,columnspan=1,padx=10, pady=2,sticky=tk.N)         
      
        
###############################################################################
             
        crow=crow+1        

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 20,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 
        
               
        root=self.master                       
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 20 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=20) 
        
        crow=crow+1

        self.button_sa = tk.Button(top, text="Save Acceleration", command=self.save_accel)
        self.button_sa.config( height = 2, width = 20,state = 'disabled')
        self.button_sa.grid(row=crow, column=0,columnspan=1, pady=18, padx=5) 

        self.button_sv = tk.Button(top, text="Save Velocity", command=self.save_velox)
        self.button_sv.config( height = 2, width = 20,state = 'disabled')
        self.button_sv.grid(row=crow, column=1,columnspan=1, pady=18, padx=5) 

        self.button_sd = tk.Button(top, text="Save Displacement", command=self.save_disp)
        self.button_sd.config( height = 2, width = 20,state = 'disabled')
        self.button_sd.grid(row=crow, column=2,columnspan=1, pady=18, padx=5) 

###############################################################################

    def Lba_change(self,val):
        sender=val.widget
        nat= 1+int(sender.curselection()[0])
        
#        print ('nat=%d' %nat)

        if(nat==6):
            self.hwtext33.config(state = 'normal')
            self.f_string_entry.config(state = 'normal')                 
        else:
            self.hwtext33.config(state = 'disabled')       
            self.f_string_entry.config(state = 'disabled')  

         
###############################################################################
        
    def calculation(self):

        self.acc=zeros(self.num,'f')
        self.v=zeros(self.num,'f')
        self.d=zeros(self.num,'f')
 
        iunit=1+int(self.Lb1.curselection()[0])
        na=1+int(self.Lba.curselection()[0])      
        nv=1+int(self.Lbv.curselection()[0])  
        nd=1+int(self.Lbd.curselection()[0])  
        
        
    
###########

        if(na==1):    
            self.acc=self.b  
          
        if(na==2):  # remove mean
            self.acc=self.b-mean(self.b)
            
        if(na==3):  # remove first order
            self.acc=signal.detrend(self.b) 
            
        if(na==4):  # remove second order
            ac=polyfit(self.t, self.b, 2)        
        
            for i in range(0,self.num-1):
                pr=(ac[0]*(self.t[i])**2+ac[1]*self.t[i]+ac[2])
                self.acc[i]=self.b[i] - pr

        if(na==5):  # remove third order
            acc=polyfit(self.t, self.b, 3)        
        
            for i in range(0,self.num-1):
                cu=(acc[0]*(self.t[i])**3+ acc[1]*(self.t[i])**2+acc[2]*(self.t[i])+acc[3]) 
                self.acc[i]=self.b[i] - cu 

        if(na==6):
            sfh= self.f_string.get() 
            fh=float(sfh)
            l=6       # order
            f=fh
            fl=0      # unused
            iband=2   # highpass
            iphase=1  # refiltering
            self.acc=BUTTERWORTH(l,f,fh,fl,self.dt,iband,iphase,self.b).Butterworth_filter_main()            
        
########

        self.vv=integrate_th(self.num,self.acc,self.dt)
        
        if(nv==1):
            self.v=self.vv
          
        if(nv==2):  # remove mean
            self.v=self.vv-mean(self.vv)
            
        if(nv==3):  # remove first order
            self.v=signal.detrend(self.vv) 
            
        if(nv==4):  # remove second order
            vc=polyfit(self.t, self.vv, 2)        
        
            for i in range(0,self.num-1):
                pr=(vc[0]*(self.t[i])**2+vc[1]*self.t[i]+vc[2])
                self.v[i]=self.vv[i] - pr

        if(nv==5):  # remove third order
            vcc=polyfit(self.t, self.vv, 3)        
        
            for i in range(0,self.num-1):
                cu=(vcc[0]*(self.t[i])**3+ vcc[1]*(self.t[i])**2+vcc[2]*(self.t[i])+vcc[3]) 
                self.v[i]=self.vv[i] - cu         

        fvp=float(self.fv_string.get())
        
        if(fvp>=1.0e-04):
            temp1=self.v

            temp2=half_cosine_fade_perc(temp1,fvp)
            
            self.v=zeros(self.num,'f')
            self.v=temp2 

           
#########    
        
        self.dd=integrate_th(self.num,self.v,self.dt)        
          
        if(nd==1):

            self.d=self.dd
          
        if(nd==2):  # remove mean

            self.d=self.dd-mean(self.dd)
            
        if(nd==3):  # remove first order

            self.d=signal.detrend(self.dd) 
            
        if(nd==4):  # remove second order
    
            dc=polyfit(self.t, self.dd, 2)        
        
            for i in range(0,self.num-1):
                pr=(dc[0]*(self.t[i])**2+dc[1]*self.t[i]+dc[2])
                self.d[i]=self.dd[i] - pr

        if(nd==5):  # remove third order
     
            dcc=polyfit(self.t, self.dd, 3)        
        
            for i in range(0,self.num-1):
                cu=(dcc[0]*(self.t[i])**3+ dcc[1]*(self.t[i])**2+dcc[2]*(self.t[i])+dcc[3]) 
                self.d[i]=self.dd[i] - cu         
       
        fdp=float(self.fd_string.get())
        
        if(fdp>=1.0e-04):          
            
            temp1=self.d

            temp2=half_cosine_fade_perc(temp1,fdp)
            
            self.d=zeros(self.num,'f')
            self.d=temp2        
       
########
          
        if(iunit==1):

            alab='Accel (G)'    
            vlab='Vel (in/sec)'   
            dlab='Disp (in)'               
            
            self.v*=386.
            self.d*=386.         
        
        if(iunit==2):
            
            alab='Accel (G)'    
            vlab='Vel (cm/sec)'   
            dlab='Disp (mm)'              
            
            self.v*=9.81*100.
            self.d*=9.81*1000.         
        
        if(iunit==3):
            
            alab='Accel (m/sec^2)'    
            vlab='Vel (cm/sec)'   
            dlab='Disp (mm)'             
            
            self.v*=100.
            self.d*=1000.        
            
            
###############################################################################

        print('\n Acceleration')  
        print('    mean=%8.4g ' %mean(self.acc)) 
        print(' std dev=%8.4g ' %std(self.acc))         
        print('     max=%8.4g ' %max(self.acc))         
        print('     min=%8.4g ' %min(self.acc)) 


        print('\n Velocity')  
        print('    mean=%8.4g ' %mean(self.v))            
        print(' std dev=%8.4g ' %std(self.v))     
        print('     max=%8.4g ' %max(self.v))         
        print('     min=%8.4g ' %min(self.v)) 
        
          
        print('\n Displacement')  
        print('    mean=%8.4g ' %mean(self.d))             
        print(' std dev=%8.4g ' %std(self.d))   
        print('     max=%8.4g ' %max(self.d))         
        print('     min=%8.4g ' %min(self.d))                     
                    
                    
###############################################################################

        self.button_sa.config( state = 'normal')
        self.button_sv.config( state = 'normal')
        self.button_sd.config( state = 'normal')

###############################################################################

        plt.ion()
        plt.clf()
        plt.close('all')
        plt.figure(1)
        plt.draw()     
        plt.plot(self.t,self.b)    
        plt.ylabel(alab) 
        plt.xlabel(' Time (sec) ')
        plt.grid(True, which="both") 
        plt.title('Input Acceleration Time History')
        
        
        plt.figure(2)
        ax=plt.subplot(3, 1, 1)
        plt.plot(self.t,self.acc)    
        plt.ylabel(alab)
        plt.grid(True, which="both")
            
        x1,x2,y1,y2 = plt.axis()
        yabs=max(abs(y1), abs(y2)) 
        plt.axis((x1,x2,-yabs,yabs))        
        ax.set_yticks([-yabs,0,yabs])     
        plt.draw()      

###

        ay=plt.subplot(3, 1, 2)    
        plt.plot(self.t,self.v) 
        plt.ylabel(vlab)
        plt.grid(True, which="both")    
     
        x1,x2,y1,y2 = plt.axis()
        yabs=max(abs(y1), abs(y2)) 
        plt.axis((x1,x2,-yabs,yabs))           
        ay.set_yticks([-yabs,0,yabs])     
        plt.draw()  

###

        az=plt.subplot(3, 1, 3)
        plt.plot(self.t,self.d)
        plt.ylabel(dlab)
        plt.xlabel(' Time (sec) ')
        plt.grid(True, which="both")

        x1,x2,y1,y2 = plt.axis()
        yabs=max(abs(y1), abs(y2)) 
        plt.axis((x1,x2,-yabs,yabs))         
        az.set_yticks([-yabs,0,yabs])              
        plt.draw()  

        
###############################################################################

    def read_data(self):            
            
        self.t,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        dur=self.t[self.num-1]-self.t[0]
        self.dt=dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.t,self.b,self.num,self.sr,self.dt)
             
        self.button_calculate.config(state = 'normal') 
                
###############################################################################

    def save_accel(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output acceleration filename: ")       
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.t)
        nb=len(self.acc)        
        n=min(na, nb)        
        
        WriteData2(n,self.t,self.tcc,output_file) 
        
###############################################################################

    def save_velox(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output velocity filename: ")       
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.t)
        nb=len(self.v)        
        n=min(na, nb)        
        
        WriteData2(n,self.t,self.v,output_file) 

###############################################################################

    def save_disp(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output displacement filename: ")       
        output_file = output_file_path.rstrip('\n')
        
        na=len(self.t)
        nb=len(self.d)        
        n=min(na, nb)        
        
        WriteData2(n,self.t,self.d,output_file)         

###############################################################################

def quit(root):
    root.destroy()

###############################################################################