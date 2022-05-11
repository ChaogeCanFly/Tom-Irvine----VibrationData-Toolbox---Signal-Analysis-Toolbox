################################################################################
# program: vb_spl_plot_gui.py
# author: Tom Irvine
# version: 1.1
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

from numpy import log10


from vb_utilities import read_two_columns_from_dialog,signal_stats


class vb_spl_plot:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.16))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_spl_plot_gui.py ver 1.1  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Plot Sound Pressure Level')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text= \
                 'The input file must have two columns:  Frequency (Hz) & SPL (dB)')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)
        
        
################################################################################

        crow=crow+1         

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=1,columnspan=1, pady=10,sticky=tk.W)   
        
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=3,columnspan=1, padx=10,pady=20)
      
################################################################################  

    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        

        ref=20.e-06        
        
        oaspl=0        
        
        for i in range(0,self.num):
            oaspl+=ref*(10**(self.b[i]/20.))
        
        p_rms = 20*log10(oaspl/ref)
        
        out1='Sound Pressure Level  OASPL=%7.4g dB ref 20 micro Pa' %p_rms
        

        print('\n OASPL=%9.5g dB ref 20 micro Pa' %p_rms)
 
        plt.ion()              
        plt.close(1)
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Sound Pressure (dB)')  
        plt.title(out1)
        plt.xscale('log')
         
        plt.draw()
  
################################################################################


def quit(root):
    root.destroy()