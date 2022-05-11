################################################################################
# program: vb_nyquist_nichols_plots_gui.py
# author: Tom Irvine
# version: 1.0
# date: May 16, 2014
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

from numpy import pi,sqrt,sin,cos,zeros

from scipy import arctan2 


from vb_utilities import read_two_columns_from_dialog,read_three_columns_from_dialog


class vb_nyquist_nichols_plots:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.19))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_nyquist_nichols_plots_gui.py ver 1.1  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Nyquist & Nichols Plots')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)
        
################################################################################

        crow=crow+1

        self.hwtext4=tk.Label(top,text='Select Input Format ')
        self.hwtext4.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.W)
                                
################################################################################

        crow=crow+1
          
        self.Lbu = tk.Listbox(top,height=4,width=34,exportselection=0)
        self.Lbu.insert(1, "Freq & Complex")
        self.Lbu.insert(2, "Freq & Real & Imaginary")        
        self.Lbu.insert(3, "Freq & Magnitude & Phase(rad)")
        self.Lbu.insert(4, "Freq & Magnitude & Phase(deg)")        
        self.Lbu.grid(row=crow, column=0, columnspan=1, pady=4, padx=10)
        self.Lbu.select_set(0) 
        
################################################################################

        crow=crow+1         

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W)   
        
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=20)
      
################################################################################  

    def read_data(self):

        nu=1+int(self.Lbu.curselection()[0])              

        if(nu==1):            
            self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        else:
            self.a,self.b,self.c,self.num=read_three_columns_from_dialog('Select Input File',self.master)             
      
      
        self.ar=zeros(self.num,'f')
        self.ai=zeros(self.num,'f')
        self.am=zeros(self.num,'f')
        self.phase=zeros(self.num,'f')



        if(nu==1):
            for i in range(0,self.num):
                self.ar[i]=self.b[i].real
                self.ai[i]=self.b[i].imag
                self.am[i]=sqrt( self.ar[i]**2  +  self.ai[i]**2 )
                self.phase[i]= arctan2( self.ai[i],self.ar[i] )*180/pi # deg
        
        if(nu==2):
            for i in range(0,self.num):
                self.ar[i]=self.b[i]
                self.ai[i]=self.c[i]
                self.am[i]=sqrt( self.ar[i]**2  +  self.ai[i]**2 )
                self.phase[i]=arctan2( self.ai[i],self.ar[i] )*180/pi # deg
                
                
        if(nu==3):   
            for i in range(0,self.num):
                self.am[i]=self.b[i]
                self.phase[i]=self.c[i]          # rad
                self.ar[i]=self.am[i]*cos(self.phase[i])
                self.ai[i]=self.am[i]*sin(self.phase[i])
                self.phase[i]*=180/pi            # deg

        if(nu==4):
            for i in range(0,self.num):        
                self.am[i]=self.b[i]
                self.phase[i]=self.c[i]          # deg
                self.ar[i]=self.am[i]*cos(self.phase[i]*pi/180)
                self.ai[i]=self.am[i]*sin(self.phase[i]*pi/180)        

################################  

        plt.ion()
        plt.close(1)
        plt.figure(1)

        plt.plot(self.ar, self.ai, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Real')
        plt.ylabel('Imag')  
        plt.title('Nyquist Plot')
    
        plt.draw()
        
################################        
        
        plt.close(2)
        plt.figure(2)

        plt.plot(self.phase, self.am, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Phase (deg)')
        plt.ylabel('Magnitude')  
        plt.title('Nichols Plot')
    
        x1=-180
        x2= 180
        plt.xlim([x1,x2])
        plt.xticks([-180,-90,0,90,180])    
    
        plt.draw()        
  
################################################################################


def quit(root):
    root.destroy()