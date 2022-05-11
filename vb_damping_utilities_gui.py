################################################################################
# program: vb_damping_utilities_gui.py
# author: Tom Irvine
# version: 1.2
# date: October 13, 2014
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
        


class vb_damping_utilities:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(400,270)
        self.master.geometry("450x370")
        self.master.title("vb_damping_utilities.py ver 1.2  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Select Analysis')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.Lb3 = tk.Listbox(top,height=4,width=45,exportselection=0)
        self.Lb3.insert(1, "Damping Value Conversion")        
        self.Lb3.insert(2, "Half-power Bandwidth Curve-fit")
        self.Lb3.insert(3, "Half-power Bandwidth Curve-fit, Modal Analysis")       

        
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

  
        win = tk.Toplevel()
    
        n=int(self.Lb3.curselection()[0])   

        m=0 
        
        if(n==m):
            from vb_damping_conversion_gui import vb_damping_conversion        
            vb_damping_conversion(win)  

        m=m+1

        if(n==m):
            from vb_half_power_curvefit_gui import vb_half_power_curvefit        
            vb_half_power_curvefit(win)          
 
        m=m+1    
    
        if(n==m):
            from vb_half_power_bandwidth_fc_gui import vb_half_power_bandwidth_fc        
            vb_half_power_bandwidth_fc(win)  

###############################################################################
        
def quit(root):
    root.destroy()                    