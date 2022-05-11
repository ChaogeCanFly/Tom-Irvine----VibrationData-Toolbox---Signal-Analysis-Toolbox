################################################################################
# program: vb_time_history_plot_gui.py
# author: Tom Irvine
# version: 1.2
# date: May 23, 2014
# description:  
################################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
        

import matplotlib.pyplot as plt

import numpy as np


from vb_utilities import read_two_columns_from_dialog,signal_stats


class vb_time_history_plot:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.22))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_time_history_plot_gui.py ver 1.3  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Plot Time History Signal')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text= \
                 'The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)
        
################################################################################

        crow=crow+1

        self.hwtext4=tk.Label(top,text='Enter Plot Title ')
        self.hwtext4.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W)
                          
        crow=crow+1
        
        self.t_string=tk.StringVar()  
        self.t_string.set('')  
        self.t_string_entry=tk.Entry(top, width = 26,textvariable=self.t_string)
        self.t_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)         

################################################################################

        crow=crow+1

        self.hwtext4=tk.Label(top,text='Enter Time History X-axis Label ')
        self.hwtext4.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W)

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label ')
        self.hwtext3.grid(row=crow, column=2, columnspan=3, pady=7)     
                          
        crow=crow+1
        
        self.x_string=tk.StringVar()  
        self.x_string.set('Time (sec)')  
        self.x_string_entry=tk.Entry(top, width = 26,textvariable=self.x_string)
        self.x_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)    

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 32,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=3,sticky=tk.W)                      
                          

################################################################################
      
        crow=crow+1    
        
        self.hwtext90=tk.Label(top,text='Time Limits')
        self.hwtext90.grid(row=crow, column=0, columnspan=1, pady=12,sticky=tk.S)   

        self.hwtext92=tk.Label(top,text='Xmin')
        self.hwtext92.grid(row=crow, column=1, columnspan=1, pady=12,sticky=tk.S)   

        self.hwtext94=tk.Label(top,text='Xmax')
        self.hwtext94.grid(row=crow, column=2, columnspan=1, pady=12,sticky=tk.S)             
        
        crow=crow+1           
        
        self.Lbxlim = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbxlim.insert(1, "Automatic")
        self.Lbxlim.insert(2, "Manual")       
        self.Lbxlim.grid(row=crow, column=0, padx=10, pady=1,sticky=tk.N)
        self.Lbxlim.select_set(0)      
        
        self.xmin_string=tk.StringVar()  
        self.xmin_string.set('')  
        self.xmin_string_entry=tk.Entry(top, width = 12,textvariable=self.xmin_string)
        self.xmin_string_entry.grid(row=crow, column=1,columnspan=1,padx=5, pady=1,sticky=tk.N)
        self.xmin_string_entry.config(state = 'disabled')       
        
        self.xmax_string=tk.StringVar()  
        self.xmax_string.set('')  
        self.xmax_string_entry=tk.Entry(top, width = 12,textvariable=self.xmax_string)
        self.xmax_string_entry.grid(row=crow, column=2,columnspan=1,padx=5, pady=1,sticky=tk.N)
        self.xmax_string_entry.config(state = 'disabled')               
        
           
        
################################################################################

        crow=crow+1         

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, padx=5, pady=10,sticky=tk.W)   
        
        
        self.button_read = tk.Button(top, text="Plot",command=self.plot_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=1,columnspan=1, padx=10, pady=10,sticky=tk.W)   
        
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=10,pady=20)
        
        
        self.Lbxlim.bind("<<ListboxSelect>>", self.callback_limits)    
        
        
################################################################################  

    def callback_limits(self,event):  

        nxlim=1+int(self.Lbxlim.curselection()[0])   

        if(nxlim==1):
            self.xmin_string_entry.config(state = 'disabled')   
            self.xmax_string_entry.config(state = 'disabled')
            self.xmin_string.set('') 
            self.xmax_string.set('') 
        else:
            self.xmin_string_entry.config(state = 'normal')    
            self.xmax_string_entry.config(state = 'normal')    
  
        
      
################################################################################  

    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
                
        sr,dt,mean,sd,rms,skew,kurtosis,dur=signal_stats(self.a,self.b,self.num)

        print("\n") 
        print("      sr=%8.4g samples/sec" %sr)
        print("    mean=%8.4g" %mean)
        print(" std dev=%8.4g" %sd) 
        print("     rms=%8.4g" %rms)
        
        print("\n %d points \n" %self.num)      
        
    def plot_data(self): 
        
        nxlim=1+int(self.Lbxlim.curselection()[0]) 
        
        plt.ion()
        plt.close(1)
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel(self.x_string.get())
        plt.ylabel(self.y_string.get())  
        plt.title(self.t_string.get())

        if(nxlim==2):
            x1=float(self.xmin_string.get())
            x2=float(self.xmax_string.get())
            plt.xlim([x1,x2])
            
    
        plt.draw()
  
################################################################################


def quit(root):
    root.destroy()