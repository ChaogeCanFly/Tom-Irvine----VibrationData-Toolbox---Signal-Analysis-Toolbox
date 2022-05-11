################################################################################
# program: vb_circular_plate_bending_gui.py
# author: Tom Irvine
# version: 1.1
# date: April 9, 2014
# description:  
#               
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


class vb_circular_plate_bending:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.14))
        h = int(2.*(h*0.19))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_circular_plate_bending_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Select Construction')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.Lbu = tk.Listbox(top,height=2,width=21,exportselection=0)
        self.Lbu.insert(1, "Homogeneous")
        self.Lbu.insert(2, "Honeycomb Sandwich")
        self.Lbu.grid(row=crow, column=0, columnspan=1, pady=4, padx=10)
        self.Lbu.select_set(0)   
      
      
        crow=crow+1

        button1=tk.Button(top, text='Perform Analysis', command=self.PerformAnalysis)
        button1.grid(row=crow, column=0, padx=10, pady=10)
        button1.config( height = 2, width = 30 )        
        
        crow=crow+1        
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 30 )
        self.button_quit.grid(row=crow, column=0, padx=10,pady=10) 
        
################################################################################

    def PerformAnalysis(self):

        plt.close("all") 
  
        win = tk.Toplevel()
    
        n=int(self.Lbu.curselection()[0])   

        m=0 

        if(n==m):
            from vb_circular_homogeneous_gui import vb_circular_homogeneous        
            vb_circular_homogeneous(win)
        
        m=m+1
    
        if(n==m):
            from vb_circular_honeycomb_gui import vb_circular_honeycomb        
            vb_circular_honeycomb(win)


###############################################################################
        
def quit(root):
    root.destroy()                    