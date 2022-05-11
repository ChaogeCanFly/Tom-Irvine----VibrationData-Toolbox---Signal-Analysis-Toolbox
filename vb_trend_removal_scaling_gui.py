################################################################################
# program: vb_trend_removal_scaling_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.3
# date: May 23, 2014
# description:  Trend Removal & Scaling Options
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
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    

import matplotlib.pyplot as plt

import numpy as np



from vb_utilities import WriteData2,sample_rate_check,\
                                                    read_two_columns_from_dialog

from scipy.signal import detrend


class vb_trend_removal_scaling:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
##        self.master.minsize(650,400)
##        self.master.geometry("720x610")
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.26))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))        
        
        self.master.title("vb_trend_removal_scaling_gui.py ver 1.3  by Tom Irvine")    
  
        self.mstring=''
        
        self.a=[]
        self.b=[]
        self.c=[]
        
        self.num=0         
        self.dur=0
        self.dt=0
        
        self.iflag=0
     

        crow=0

        self.hwtext1=tk.Label(top,text='Trend Removal & Scaling Options')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)


        crow+=1 

        self.hwtext2=tk.Label(top, \
            text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=3,sticky=tk.W)
        

################################################################################
  
        crow+=1 

        self.hwtext3=tk.Label(top,text='Enter Input Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, columnspan=2, pady=11,sticky=tk.E)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=11,sticky=tk.W)
        
  
        crow+=1 

        self.hwtext39=tk.Label(top,text='Enter Output Time History Y-axis Label')
        self.hwtext39.grid(row=crow, column=0, columnspan=2, pady=11,sticky=tk.E)

        self.yo_string=tk.StringVar()  
        self.yo_string.set('')  
        self.yo_string_entry=tk.Entry(top, width = 26,textvariable=self.yo_string)
        self.yo_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=11,sticky=tk.W)        

################################################################################

        crow+=1 
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W)  

################################################################################

        crow+=1 

        self.hwtext7=tk.Label(top,text='Multiply Amplitude by Scale Factor?')
        self.hwtext7.grid(row=crow, column=0, columnspan=2, pady=11,sticky=tk.W)
        
        self.hwtext22=tk.Label(top,text='Enter Scale Factor')
        self.hwtext22.grid(row=crow, column=2, columnspan=1,padx=20, pady=11,sticky=tk.W)          
        self.hwtext22.config(state = 'disabled')

################################################################################

        crow+=1
        
        self.Lbsc = tk.Listbox(top,height=2,exportselection=0)
        self.Lbsc.insert(1, "No")
        self.Lbsc.insert(2, "Yes")
        self.Lbsc.grid(row=crow, column=0, pady=4,sticky=tk.N)
        self.Lbsc.select_set(0) 
        self.Lbsc.bind('<<ListboxSelect>>', self.Lbsc_change)        
        self.Lbsc.config(state = 'disabled')        
        
        
        self.sc_string=tk.StringVar()  
        self.sc_string.set('  1') 
        self.sc_string_entry=tk.Entry(top, width = 10,textvariable=self.sc_string)
        self.sc_string_entry.grid(row=crow, column=2,columnspan=1,padx=20, pady=1,sticky=tk.N) 
        self.sc_string_entry.config(state = 'disabled')
        
        self.button_calculate_scale = \
        tk.Button(top, text="Apply Scale", command=self.calculation_scale)
        self.button_calculate_scale.config( height = 2, width = 20,state = 'disabled')
        self.button_calculate_scale.grid(row=crow, column=3,columnspan=2, padx=10,pady=5) 
        

################################################################################

        crow+=1 

        self.hwtext71=tk.Label(top,text='Select Trend Removal')
        self.hwtext71.grid(row=crow, column=0, columnspan=2, pady=11,sticky=tk.W)        

        crow+=1                                  

        self.Lbtr = tk.Listbox(top,height=4,exportselection=0)
        self.Lbtr.insert(1, "None")
        self.Lbtr.insert(2, "Mean")
        self.Lbtr.insert(3, "First-order")
        self.Lbtr.insert(4, "Second-order")        
        self.Lbtr.grid(row=crow, column=0, pady=4,sticky=tk.N)
        self.Lbtr.select_set(0) 
        self.Lbtr.bind('<<ListboxSelect>>', self.Lbtr_change)
                                                              
################################################################################
        
        crow+=1 
                
        self.button_calculate_trend = \
        tk.Button(top, text="Perform Trend Removal", command=self.calculation_trend)
        self.button_calculate_trend.config( height = 2, width = 20,state = 'disabled')
        self.button_calculate_trend.grid(row=crow, column=0,columnspan=2, pady=20) 
        
        self.button_export = tk.Button(top, text="Export Output Data",command=self.export)
        self.button_export.config( height = 2, width = 20,state = 'disabled' )
        self.button_export.grid(row=crow, column=2,columnspan=2, pady=20)          
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 20 )
        self.button_quit.grid(row=crow, column=4,columnspan=2, padx=20,pady=20)
        
################################################################################


    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        self.c=np.array(self.b)        
        
        self.dur=self.a[self.num-1]-self.a[0]
        self.dt=self.dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)
        
        plt.ion()
        plt.clf()
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Input Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)

        if(self.num>=1):
            self.iflag=1
  
        self.Lbsc.config(state = 'normal')  
  

    def calculation_scale(self):
        isc=int(self.Lbsc.curselection()[0])   

        if(isc==1):
            scale=float(self.sc_string.get())   
            self.c=self.c*scale
            
        plt.close(2)
        plt.figure(2)     
        plt.plot(self.a,self.c)
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.yo_string.get())  
        plt.title('Output Time History')        
        plt.draw() 

        self.button_export.config(state = 'normal' )             
        

    def calculation_trend(self):
        itr=int(self.Lbtr.curselection()[0]) 
        
        if(itr==1):
            self.c=self.c-np.mean(self.c)
            
        if(itr==2):
            self.c=detrend(self.c, axis=-1, type='linear', bp=0)        
            
        if(itr==3):
            z=np.polyfit(self.a, self.c, 3)
            for i in range(0,self.num):
                self.c[i]-= ( z[0]*self.a[i]**2 + z[1]*self.a[i] +z[3]*self.a[i] )
            
        plt.close(2)
        plt.figure(2)     
        plt.plot(self.a,self.c)
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.yo_string.get())  
        plt.title('Output Time History')        
        plt.draw()  

        self.button_export.config(state='normal' )  

###############################################################################        

    def Lbtr_change(self,val):
        sender=val.widget
        nsc= int(sender.curselection()[0])       
        if(nsc>0 and self.iflag==1):
            self.button_calculate_trend.config(state = 'normal')                      
        else:
            self.button_calculate_trend.config(state = 'disabled')  
            
    def Lbsc_change(self,val):
        sender=val.widget
        nsc= int(sender.curselection()[0])
        if(nsc==1 and self.iflag==1):
            self.sc_string_entry.config(state = 'normal')
            self.hwtext22.config(state = 'normal')
            self.button_calculate_scale.config(state = 'normal')                      
        else:
            self.sc_string_entry.config(state = 'disabled')  
            self.hwtext22.config(state = 'disabled')            
            self.button_calculate_scale.config(state = 'disabled')   
            
################################################################################
                        
    def export(self):
        output_file_path = asksaveasfilename(parent=self.master,\
               title="Enter the output filename: ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.num,self.a,self.c,output_file) 

################################################################################

def quit(root):
    root.destroy()