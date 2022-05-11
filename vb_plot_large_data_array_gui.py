###########################################################################
# program: vb_plot_large_data_array_gui.py
# author: Tom Irvine
# version: 1.2
# date: May 12, 2014
# 
###############################################################################

from __future__ import print_function

from numpy import sin,log,log10,zeros,ceil,linspace,logspace,pi,array

import matplotlib.pyplot as plt

from vb_utilities import WriteData2
    
from scipy.signal import decimate    
    
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

###############################################################################

class vb_plot_large_data_array:
    def __init__(self,parent,TT,a,xl,yl,ti,fig_num):
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(300,450)
        self.master.geometry("400x450")
        self.master.title("vb_plot_large_data_array.py  ver 1.0  by Tom Irvine")       
    
        self.x=TT
        self.y=a
        
        self.xl=xl
        self.yl=yl
        self.ti=ti
        
        self.fig_num=fig_num
        
        print(len(self.x))
        print(len(self.y))
        
        crow=0         

        self.hwtext4=tk.Label(top,text='Plotting option for arrays > 500K coordinates')
        self.hwtext4.grid(row=crow, column=0, pady=7)

        crow=crow+1           
        
        self.hwtext5=tk.Label(top,text='Plot options affect data appearance only.')
        self.hwtext5.grid(row=crow, column=0, pady=7)
        
        crow=crow+1           
        
        self.hwtext6=tk.Label(top,text='The raw data array remains unmodified.')
        self.hwtext6.grid(row=crow, column=0, pady=7)
        
        crow=crow+1           
        
        self.button_plot1 = tk.Button(top, text="Plot with Markers Only", command=self.calculate_plot1)
        self.button_plot1.config( height = 2, width = 25)
        self.button_plot1.grid(row=crow, column=0,padx=2, pady=10,sticky=tk.S) 

        crow=crow+1                   
        
        self.button_plot2 = tk.Button(top, text="Plot Downsample/Decimate", command=self.calculate_plot2)
        self.button_plot2.config( height = 2, width = 25)
        self.button_plot2.grid(row=crow, column=0,padx=2, pady=10,sticky=tk.S)    
        
        crow=crow+1                   
        
        self.button_plot3 = tk.Button(top, text="Plot Max & Min per Segment", command=self.calculate_plot3)
        self.button_plot3.config( height = 2, width = 25)
        self.button_plot3.grid(row=crow, column=0,padx=2, pady=10,sticky=tk.S)         
        
        crow=crow+1    
            
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=0, padx=2,pady=10,sticky=tk.S)        

###############################################################################
        
    def calculate_plot1(self):        
        
        print('view plot')        
        
        plt.ion()
        plt.clf()   
        plt.figure(self.fig_num)
        plt.plot(self.x, self.y,'b*')  
        plt.grid(True)
        plt.xlabel(self.xl)
        plt.ylabel(self.yl)  
        plt.title(self.ti)           
     
###############################################################################
        
    def calculate_plot2(self):     
    
        n=len(self.x) 
        
        ratio=len(self.x)/500000.
            
        cr=ceil(ratio)            
            
        q=int(cr) 
        
        print(ratio,cr,q)
            
        self.y = decimate(self.y, q, ftype="iir")

        tmax=self.x[n-1]         
        
        m=len(self.y)
        
        print(n,m,q)
        
        self.x=linspace(0,tmax,m) 
        
        print(len(self.x))
        print(len(self.y))        
        
        print('view plot')      
        
        plt.ion()
        plt.clf()   
        plt.figure(self.fig_num)
        plt.plot(self.x, self.y,linewidth=1.0,color='b')
        plt.grid(True)
        plt.xlabel(self.xl)
        plt.ylabel(self.yl)  
        plt.title(self.ti)          
        
###############################################################################
        
        
    def calculate_plot3(self):     
    
        n=len(self.x) 
        
        ratio=2*len(self.x)/500000.
            
        cr=ceil(ratio)            
            
        q=int(cr) 
        
        print(ratio,cr,q)

        yy=[]
        xx=[]
        
        dt=(self.x[n-1]-self.x[0])/float(n)
        
        for i in range(0,n,q):
            yy.append(max(self.y[i:i+q]))
            yy.append(min(self.y[i:i+q]))
            tt=i*dt
            xx.append(tt)
            xx.append(tt)
        
        xx=array(xx)
        yy=array(yy)
        
        print('view plot')      
        
        plt.ion()
        plt.clf()   
        plt.figure(self.fig_num)
        plt.plot(xx,yy,linewidth=1.0,color='b')
        plt.grid(True)
        plt.xlabel(self.xl)
        plt.ylabel(self.yl)  
        plt.title(self.ti)          
        
###############################################################################

def quit(root):
    root.destroy()                    