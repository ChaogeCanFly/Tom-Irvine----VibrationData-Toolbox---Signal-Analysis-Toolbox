################################################################################
# program: vb_structural_dynamics_gui.py
# author: Tom Irvine
# version: 1.1
# date: April 15, 2014
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


class vb_structural_dynamics:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(400,200)
        self.master.geometry("450x300")
        self.master.title("vb_structural_dynamics_gui.py ver 1.1  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Select Analysis')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.Lb3 = tk.Listbox(top,height=7,width=30,exportselection=0)
        self.Lb3.insert(1, "SDOF System Natural Frequency")        
        self.Lb3.insert(2, "Beam Bending")
        self.Lb3.insert(3, "Rod Longitudinal")       
        self.Lb3.insert(4, "Rectangular Plate Bending")
        self.Lb3.insert(5, "Circular Plate Bending")
        self.Lb3.insert(6, "Annular Plate Bending")        
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
            from vb_sdof_fn_gui import vb_sdof_fn        
            vb_sdof_fn(win)
            
        m=m+1        

        if(n==m):
            from vb_beam_bending_gui import vb_beam_bending        
            vb_beam_bending(win)
            
        m=m+1
        
        if(n==m):
            from vb_rod_longitudinal_gui import vb_rod_longitudinal        
            vb_rod_longitudinal(win)
            
        m=m+1
    
        if(n==m):
            from vb_rectangular_plate_bending_gui import vb_rectangular_plate_bending        
            vb_rectangular_plate_bending(win)
            
        m=m+1    
        
        if(n==m):
            from vb_circular_plate_bending_gui import vb_circular_plate_bending        
            vb_circular_plate_bending(win)
            
        m=m+1       
    
        if(n==m):
            from vb_annular_plate_bending_gui import vb_annular_plate_bending        
            vb_annular_plate_bending(win)
    
        m=m+1   

###############################################################################
        
def quit(root):
    root.destroy()                    