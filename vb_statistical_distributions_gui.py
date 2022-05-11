################################################################################
# program: vb_statistical_distributions_gui.py
# author: Tom Irvine
# version: 1.0
# date: May 1, 2014
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


class vb_statistical_distributions:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.18))
        h = int(2.*(h*0.18))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_statistical_distributions_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Select Analysis')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.Lb3 = tk.Listbox(top,height=4,width=30,exportselection=0)
        self.Lb3.insert(1, "Normal")        
        self.Lb3.insert(2, "Rayleigh")
        self.Lb3.insert(3, "Poisson")           
        self.Lb3.grid(row=crow, column=0, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lb3.select_set(0)
        

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
    
        n=int(self.Lb3.curselection()[0])   

        m=0 
        
        if(n==m):
            from vb_normal_gui import vb_normal        
            vb_normal(win)
            
        m=m+1        

        if(n==m):
            from vb_Rayleigh_gui import vb_Rayleigh        
            vb_Rayleigh(win)
            
        m=m+1
        
        if(n==m):
            from vb_Poisson_gui import vb_Poisson        
            vb_Poisson(win)
            
        m=m+1


###############################################################################
        
def quit(root):
    root.destroy()                    