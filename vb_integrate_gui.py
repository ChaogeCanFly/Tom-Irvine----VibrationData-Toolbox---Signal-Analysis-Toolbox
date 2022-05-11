###############################################################################
# program: vb_integrate_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.4
# date: May 23, 2014
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

from vb_utilities import BUTTERWORTH

from numpy import mean,zeros,pi,cos
from scipy import signal

import matplotlib.pyplot as plt

###############################################################################

class vb_integrate:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.25))
        h = int(2.*(h*0.36))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_integrate_gui.py ver 1.4  by Tom Irvine") 

        
        self.a=[]
        self.b=[]
        self.bb=[]
        self.v=[]        
        self.num=0        
        self.dt=0             
        self.sr=0     
        
        crow=0
        
        self.hwtext1=tk.Label(top,text='Integrate Time History')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)
        
        crow=crow+1
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W) 
        

        crow=crow+1

        self.hwtext2=tk.Label(top,text='Select trend removal prior to integration')
        self.hwtext2.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.W)
        
        self.hwtext3=tk.Label(top,text='Enter Highpass Filter Freq (Hz)')
        self.hwtext3.grid(row=crow, column=2, columnspan=2, padx=20,pady=7)
        self.hwtext3.config(state = 'disabled')
        
        
        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=4,width = 28,exportselection=0)
        self.Lb1.insert(1, "mean remove")
        self.Lb1.insert(2, "linear trend removal")
        self.Lb1.insert(3, "Butterworth highpass filter")
        self.Lb1.insert(4, "none")        
        self.Lb1.grid(row=crow, column=0, columnspan=2, pady=1)
        self.Lb1.select_set(0) 
        self.Lb1.bind('<<ListboxSelect>>', self.Lb1_change)        
        
        self.f_string=tk.StringVar()  
        self.f_string.set('')  
        self.f_string_entry=tk.Entry(top, width = 10,textvariable=self.f_string)
        self.f_string_entry.grid(row=crow, column=2,columnspan=1,padx=20, pady=2,sticky=tk.N)        
        self.f_string_entry.config(state = 'disabled') 

        
        crow=crow+1

        self.hwtext71=tk.Label(top,text='Apply Fade in?')
        self.hwtext71.grid(row=crow, column=0, columnspan=1, pady=12,sticky=tk.W)
        
        self.hwtext72=tk.Label(top,text='Enter percent')
        self.hwtext72.grid(row=crow, column=1, columnspan=1,padx=10, pady=12,sticky=tk.W)   
        
        self.hwtext73=tk.Label(top,text='Apply Fade out?')
        self.hwtext73.grid(row=crow, column=3, columnspan=1, pady=12,sticky=tk.W)

        self.hwtext74=tk.Label(top,text='Enter percent')
        self.hwtext74.grid(row=crow, column=4, columnspan=1,padx=10, pady=12,sticky=tk.W)  


        crow=crow+1
        
        self.Lbfi = tk.Listbox(top,height=2,width = 10,exportselection=0)
        self.Lbfi.insert(1, "yes")
        self.Lbfi.insert(2, "no")        
        self.Lbfi.grid(row=crow, column=0, columnspan=1, pady=1)
        self.Lbfi.select_set(0) 
        self.Lbfi.bind('<<ListboxSelect>>', self.Lbfi_change)        
        
        self.fi_string=tk.StringVar()  
        self.fi_string.set('  1') 
        self.fi_string_entry=tk.Entry(top, width = 10,textvariable=self.fi_string)
        self.fi_string_entry.grid(row=crow, column=1,columnspan=1,padx=20, pady=1,sticky=tk.N)          


        self.Lbfo = tk.Listbox(top,height=2,width = 10,exportselection=0)
        self.Lbfo.insert(1, "yes")
        self.Lbfo.insert(2, "no")        
        self.Lbfo.grid(row=crow, column=3, columnspan=1, pady=1)
        self.Lbfo.select_set(0) 
        self.Lbfo.bind('<<ListboxSelect>>', self.Lbfo_change) 

        
        self.fo_string=tk.StringVar()  
        self.fo_string.set('  1') 
        self.fo_string_entry=tk.Entry(top, width = 10,textvariable=self.fo_string)
        self.fo_string_entry.grid(row=crow, column=4,columnspan=1,padx=20, pady=1,sticky=tk.N)  


###############################################################################
        
        crow=crow+1

        self.hwtext21=tk.Label(top,text='Multiply Output by Scale Factor?')
        self.hwtext21.grid(row=crow, column=0, columnspan=2, pady=15,sticky=tk.W)
        
        self.hwtext22=tk.Label(top,text='Enter Scale Factor')
        self.hwtext22.grid(row=crow, column=2, columnspan=1,padx=20, pady=15,sticky=tk.W)   
        
        
        crow=crow+1          
        
        self.Lbsc = tk.Listbox(top,height=2,width = 10,exportselection=0)
        self.Lbsc.insert(1, "yes")
        self.Lbsc.insert(2, "no")        
        self.Lbsc.grid(row=crow, column=0, columnspan=1, pady=1)
        self.Lbsc.select_set(0) 
        self.Lbsc.bind('<<ListboxSelect>>', self.Lbsc_change)
        
         
        self.sc_string=tk.StringVar()  
        self.sc_string.set('  1') 
        self.sc_string_entry=tk.Entry(top, width = 10,textvariable=self.sc_string)
        self.sc_string_entry.grid(row=crow, column=2,columnspan=1,padx=20, pady=1,sticky=tk.N)        
                 
        crow=crow+1

        self.hwtext25=tk.Label(top,text='Enter Input Signal Type')
        self.hwtext25.grid(row=crow, column=0, columnspan=2, pady=7)   
        
        self.hwtext3a=tk.Label(top,text='Enter Input Y-axis Label')
        self.hwtext3a.grid(row=crow, column=2, columnspan=2, pady=11)
        
        self.hwtext3b=tk.Label(top,text='Enter Output Y-axis Label')
        self.hwtext3b.grid(row=crow, column=4, columnspan=2, pady=11)         
         
        crow=crow+1

        self.Lbstype = tk.Listbox(top,height=2,width = 18,exportselection=0)
        self.Lbstype.insert(1, "Acceleration")
        self.Lbstype.insert(2, "Velocity")      
        self.Lbstype.grid(row=crow, column=0, columnspan=2, padx=6,pady=1)
        self.Lbstype.select_set(0) 

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=2,padx=5, pady=1,sticky=tk.N)
        
        self.dy_string=tk.StringVar()  
        self.dy_string.set('')  
        self.dy_string_entry=tk.Entry(top, width = 26,textvariable=self.dy_string)
        self.dy_string_entry.grid(row=crow, column=4,columnspan=2,padx=5, pady=1,sticky=tk.N) 
         
###############################################################################
             
        crow=crow+1        

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 20,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=2, pady=20) 
        
        
        self.button_sav = tk.Button(top, text="Export Integrated Signal", command=self.export_th)
        self.button_sav.config( height = 2, width = 20,state = 'disabled' )
        self.button_sav.grid(row=crow, column=2,columnspan=2, pady=1, padx=1) 
               
        root=self.master                       
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 20 )
        self.button_quit.grid(row=crow, column=4,columnspan=2, padx=10,pady=20) 
        
###############################################################################        
    
    
    def export_th(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output time history filename: ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.num,self.a,self.v,output_file) 
    
    
    def Lbfi_change(self,val):
        sender=val.widget
        nat= int(sender.curselection()[0])
        
#        print ('nat=%d' %nat)

        if(nat==0):
            self.hwtext72.config(state = 'normal')
            self.fi_string_entry.config(state = 'normal')                 
        else:
            self.hwtext72.config(state = 'disabled')       
            self.fi_string_entry.config(state = 'disabled')    
            
            
    def Lbfo_change(self,val):
        sender=val.widget
        nat= int(sender.curselection()[0])
        
#        print ('nat=%d' %nat)

        if(nat==0):
            self.hwtext74.config(state = 'normal')
            self.fo_string_entry.config(state = 'normal')                 
        else:
            self.hwtext74.config(state = 'disabled')       
            self.fo_string_entry.config(state = 'disabled')            
        
###############################################################################        
    
    def Lb1_change(self,val):
        sender=val.widget
        nat= int(sender.curselection()[0])
        
#        print ('nat=%d' %nat)

        if(nat==2):
            self.hwtext3.config(state = 'normal')
            self.f_string_entry.config(state = 'normal')                 
        else:
            self.hwtext3.config(state = 'disabled')       
            self.f_string_entry.config(state = 'disabled')  
            
###############################################################################        
    
    def Lbsc_change(self,val):
        sender=val.widget
        nsc= int(sender.curselection()[0])
        
        if(nsc==0):
            self.sc_string_entry.config(state = 'normal') 
        else:
            self.sc_string_entry.config(state = 'disabled') 
            
###############################################################################
        
    def calculation(self):
 
        imr=int(self.Lb1.curselection()[0])
        isc=int(self.Lbsc.curselection()[0])
        istype=int(self.Lbstype.curselection()[0])       
    
        ifade_in=int(self.Lbfi.curselection()[0])  
        ifade_out=int(self.Lbfo.curselection()[0])  
    
        
        if(imr==0):
            self.bb=self.b-mean(self.b)
            
        if(imr==1):
            self.bb=signal.detrend(self.b)  
            
        if(imr==2):
            sfh= self.f_string.get() 
            fh=float(sfh)
            l=6       # order
            f=fh
            fl=0      # unused
            iband=2   # highpass
            iphase=1  # refiltering
            self.bb=BUTTERWORTH(l,f,fh,fl,self.dt,iband,iphase,self.b).Butterworth_filter_main()
            
        if(imr==3):   # none
            self.bb=self.b
     
###############################################################################

        if(ifade_in==0):
            sfi= self.fi_string.get() 
            fper=float(sfi)                        
            fper=fper/100            
    
            na=int(round(fper*self.num))

            for i in range(0,int(na)):
                arg=pi*(( float(i)/float(na-1) )+1.) 
                self.bb[i]=self.bb[i]*0.5*(1+(cos(arg)))            
        
###############################################################################        
            
        if(ifade_out==0):            
            sfo= self.fo_string.get() 
            fper=float(sfo)
            fper=fper/100 
            
            na=int(round(fper*self.num))
            nb=self.num-na
            delta=self.num-1-nb
      
            for i in range(nb,int(self.num)):
                arg=pi*( (i-nb)/delta )
                self.bb[i]=self.bb[i]*(1+cos(arg))*0.5        
     
###############################################################################

        self.v=zeros(self.num,'f')

        self.v[0]=self.bb[0]*self.dt/2

        for i in range(1,int(self.num-1)):
            self.v[i]=self.v[i-1]+self.bb[i]*self.dt
            self.v[self.num-1]=self.v[self.num-2]+self.bb[self.num-1]*self.dt/2

        
        if(isc==0):
            scale=float(self.sc_string.get())
            self.v=self.v*scale 
            
        self.button_sav.config(state = 'normal')  
            
        plt.ion()
        plt.clf()
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())

        if(istype==0):
            plt.title('Acceleration Time History')
        else:    
            plt.title('Velocity Time History')
            
        plt.draw() 


        plt.figure(2)

        plt.plot(self.a, self.v, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.dy_string.get())
        
        if(istype==0):
            plt.title('Velocity Time History')
        else:    
            plt.title('Displacement Time History')
    
        plt.draw() 

           
        
###############################################################################

    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        dur=self.a[self.num-1]-self.a[0]
        self.dt=dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)
             
        self.button_calculate.config(state = 'normal') 
                
###############################################################################

def quit(root):
    root.destroy()

###############################################################################