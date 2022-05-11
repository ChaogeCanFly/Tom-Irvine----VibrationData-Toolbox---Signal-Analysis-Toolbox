###########################################################################
# program: vb_amplitude_conversion_gui.py
# author: Tom Irvine
# version: 1.0
# date: February 14, 2014
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

class vb_amplitude_conversion:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.10))
        h = int(2.*(h*0.18))
        self.master.geometry("%dx%d+0+0" % (w, h))



        self.master.title("vb_amplitude_conversion_gui.py  ver 1.0  by Tom Irvine")
        
        crow=0
        
        self.hwtext3=tk.Label(top,text='Select Analysis')
        self.hwtext3.grid(row=crow, column=1, pady=7)         
        
        crow=crow+1       
        
        self.Lb3 = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lb3.insert(1, "Sine")
        self.Lb3.insert(2, "SRS")       
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
            from vb_sine_amplitude_gui import vb_sine_amplitude        
            vb_sine_amplitude(win)              

        m=m+1

        if(n==m):
            from vb_srs_amplitude_gui import vb_srs_amplitude        
            vb_srs_amplitude(win)              

        m=m+1
        
        
            
def quit(root):
    root.destroy()              