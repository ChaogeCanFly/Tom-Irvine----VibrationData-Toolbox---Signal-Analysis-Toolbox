################################################################################
# program: vb_scatter_plot_gui.py
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
    import tkMessageBox    
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    import tkinter.messagebox as tkMessageBox   
     

import matplotlib.pyplot as plt

import numpy as np


from vb_utilities import read_two_columns_from_dialog,signal_stats


class vb_scatter_plot:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.topp=top
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.24))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_scatter_plot_gui.py ver 1.2  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Plot Scatter Plot for Two Time Histories')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text= \
                 'Each input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)
        
################################################################################

        crow=crow+1

        self.hwtext4=tk.Label(top,text='Enter Plot Title ')
        self.hwtext4.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W)
                          
        crow=crow+1
        
        self.t_string=tk.StringVar()  
        self.t_string.set('Scatter Plot')  
        self.t_string_entry=tk.Entry(top, width = 26,textvariable=self.t_string)
        self.t_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)         


################################################################################
                          
        crow=crow+1

        self.hwtext3=tk.Label(top,text='Enter Time History 1, Y-axis Label ')
        self.hwtext3.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W)                          

        crow=crow+1
        
        self.y1_string=tk.StringVar()  
        self.y1_string.set('')  
        self.y1_string_entry=tk.Entry(top, width = 26,textvariable=self.y1_string)
        self.y1_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)
           
################################################################################
                          
        crow=crow+1

        self.hwtext5=tk.Label(top,text='Enter Time History 2, Y-axis Label ')
        self.hwtext5.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W)                          

        crow=crow+1
        
        self.y2_string=tk.StringVar()  
        self.y2_string.set('')  
        self.y2_string_entry=tk.Entry(top, width = 26,textvariable=self.y2_string)
        self.y2_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W) 
       
################################################################################

        crow=crow+1         

        self.button_read1 = tk.Button(top, text="Read Input File 1",command=self.read_data_1)
        self.button_read1.config( height = 2, width = 15 )
        self.button_read1.grid(row=crow, column=0,columnspan=1, padx=10,pady=10)   

        self.button_read2 = tk.Button(top, text="Read Input File 2",command=self.read_data_2)
        self.button_read2.config( height = 2, width = 15 )
        self.button_read2.grid(row=crow, column=1,columnspan=1, padx=10,pady=10)          
        
        self.button_plot = tk.Button(top, text="Plot",command=self.plot_data)
        self.button_plot.config( height = 2, width = 15,state = 'disabled'  )
        self.button_plot.grid(row=crow, column=2,columnspan=1, padx=10,pady=10)         
        
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=3,columnspan=1, padx=10,pady=20)
      
################################################################################  

    def read_data_1(self):            
            
        self.a1,self.b1,self.num1=read_two_columns_from_dialog('Select Input File',self.master)


        tl2=self.topp

        if(self.num1>=1):
            tkMessageBox.showinfo(" ", "Data file 1 read",parent=tl2)
        else:                
            tkMessageBox.showinfo(" ", "Data file 1 not read",parent=tl2)                
        
        
    def read_data_2(self):            
            
        self.a2,self.b2,self.num2=read_two_columns_from_dialog('Select Input File',self.master) 
        
        tl2=self.topp        
        
        if(self.num2>=1):
            tkMessageBox.showinfo(" ", "Data file 2 read",parent=tl2)
        else:                
            tkMessageBox.showinfo(" ", "Data file 2 not read",parent=tl2)          
        
        self.button_plot.config(state = 'normal')
        
        
    def plot_data(self):         
  
        if(self.num1==self.num2):

            plt.ion()    
            plt.close(1)
            plt.figure(1)

            plt.plot(self.b2, self.b1,marker='*',linestyle='none',color='b')     # disregard error       
       
            plt.grid(True)
            plt.xlabel(self.y1_string.get())
            plt.ylabel(self.y2_string.get())  
            plt.title('t_string')
    
            plt.draw()
        else:    
            tkMessageBox.showinfo("Plot Failed", "Data files have different lengths")   
            
################################################################################


def quit(root):
    root.destroy()