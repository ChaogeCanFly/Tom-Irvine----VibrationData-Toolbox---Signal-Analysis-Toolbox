###########################################################################
# program: vb_sine_sweep_parameters_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 3, 2014
# 
###############################################################################

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

###############################################################################

class vb_sine_sweep_parameters:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.14))
        h = int(2.*(h*0.19))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_sine_sweep_parameters_gui.py  ver 1.0  by Tom Irvine")
        
        crow=0
        
        self.hwtext3=tk.Label(top,text='Select Analysis')
        self.hwtext3.grid(row=crow, column=1, pady=7)         
        
        crow=crow+1       
        
        self.Lb3 = tk.Listbox(top,height=4,width=28,exportselection=0)
        self.Lb3.insert(1, "Cross-over Frequency")
        self.Lb3.insert(2, "Number of Octaves")
        self.Lb3.insert(3, "Sweep Rate")
        self.Lb3.insert(4, "Total Sine Cycles")        
        self.Lb3.grid(row=crow, column=1, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lb3.select_set(0)
        
        crow=crow+1
               
        self.button_go = tk.Button(top, text="Perform Analysis",command=self.analysis_go)
        self.button_go.config( height = 2, width = 15 )
        self.button_go.grid(row=crow, column=1,columnspan=1,padx=10,pady=10)
        
        crow=crow+1
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=6,pady=10) 
        
         
###############################################################################

    def analysis_go(self):
    
        win = tk.Toplevel()
    
        n=int(self.Lb3.curselection()[0])   

        m=0 

        if(n==m):
            from vb_crossover_frequency_gui import vb_crossover_frequency        
            vb_crossover_frequency(win)         

        m=m+1

        if(n==m):
            from vb_number_octaves_gui import vb_number_octaves      
            vb_number_octaves(win)         

        m=m+1
    
        if(n==m):
            from vb_sweep_rate_gui import vb_sweep_rate       
            vb_sweep_rate(win)   
                
        m=m+1

        if(n==m):
            from vb_total_sine_cycles_gui import vb_total_sine_cycles        
            vb_total_sine_cycles(win)
            
            
def quit(root):
    root.destroy()              