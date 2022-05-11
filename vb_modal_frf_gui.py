################################################################################
# program: vb_modal_frf_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.1
# date: October 21, 2014
# description:  Calculate the FRF from a force and response time history pair
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
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    import tkinter.messagebox as tkMessageBox    
    
    
from vb_utilities import read_two_columns_from_dialog,read_three_columns_from_dialog,WriteData2  

from numpy import array,zeros,log,log10,pi,sqrt,linspace,round,ceil,interp

from numpy import cos,sin,std,floor,argmax,histogram

import matplotlib.pyplot as plt

from vb_utilities import WriteData2,signal_stats,sample_rate_check

from scipy.fftpack import fft,ifft

import random


class vb_modal_frf:

    def __init__(self,parent): 
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.26))
        self.master.geometry("%dx%d+0+0" % (w, h))   


        self.master.title("vb_modal_frf_gui.py ver 1.0  by Tom Irvine")         
                
        self.fig_num=1     
        
                
###############################################################################     
     
        crow=0
        
        self.hwtext3=tk.Label(top,text='This script calculates the FRF from a force and response time history pair.')
        self.hwtext3.grid(row=crow, column=0,columnspan=4, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext4=tk.Label(top,text='Select Input Data Format')
        self.hwtext4.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W) 
        
        crow=crow+1   
    
        self.Lb1 = tk.Listbox(top,height=3,width=45,exportselection=0)
        self.Lb1.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W) 
        self.Lb1.insert(1, "Common array: time(sec) & force & response")
        self.Lb1.insert(2, "Two separate arrays, each: time(sec) & amplitude")
        self.Lb1.select_set(0) 
        
        crow=crow+1

        self.hwtext5=tk.Label(top,text='Select Analysis Type')
        self.hwtext5.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.W) 
        
        crow=crow+1   
    
        self.Lb2 = tk.Listbox(top,height=3,width=45,exportselection=0)
        self.Lb2.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W) 
        self.Lb2.insert(1, "Ensemble Average - best for steady state data")
        self.Lb2.insert(2, "Single Recored - best for transient data")        
        self.Lb2.select_set(0)         
        
        crow=crow+1   
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 25 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=8,sticky=tk.N)        
        
     
        crow=crow+1   
        
        self.button_read = tk.Button(top, text="Go to Analysis Page",command=self.analysis)
        self.button_read.config( height = 2, width = 25 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=8,sticky=tk.N)   
        
        crow=crow+1   
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=0, padx=8,pady=10)        
     
###############################################################################

    def analysis(self):   

        plt.close("all")   
        win = tk.Toplevel()
    
        self.analysis_type=int(self.Lb2.curselection()[0])    
                    
        if(self.analysis_type==0):  # ensemble
            from vb_modal_ensemble_gui import vb_modal_ensemble_frf      
            vb_modal_ensemble_frf(win,self.t,self.c)
            
        else:                  # single record  
            from vb_modal_single_frf_gui import vb_modal_single_frf      
            vb_modal_single_frf(win,self.t,self.c)         
        
       

    def read_data(self):            
        
        self.iunit=int(self.Lb1.curselection()[0]) 

        if(self.iunit==0):  # common array
            self.t,self.a,self.b,self.num =read_three_columns_from_dialog('Select Input File',self.master)
            
            La=len(self.a)              
            
        else:
            self.t,self.a,self.num  =read_two_columns_from_dialog('Select Force Input File',self.master)          
            self.tb,self.b,self.num =read_two_columns_from_dialog('Select Response File',self.master)    
            
            La=len(self.a)    
            Lb=len(self.b)
            
            if(La!=Lb):
                tkMessageBox.showinfo("Warning"," Vector length error",parent=self.button_read_data) 
                return
                
            if(abs(self.t[0]-self.tb[0])>0.0005):
                tkMessageBox.showinfo("Warning"," Vector synch error",parent=self.button_read_data) 
                return                
            
        self.c=zeros([La,2],'f')             
            
        for i in range(0,La):
            self.c[i,0]=self.a[i]
            self.c[i,1]=self.b[i]            
            
            
###############################################################################        

def quit(root):
    root.destroy()        
    
###############################################################################            