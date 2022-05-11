###########################################################################
# program: vb_generate_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.5
# date: October 24, 2014
# description:  generate time histories
#
###########################################################################
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
    import Tkinter as tk
           
if sys.version_info[0] == 3:   
    import tkinter as tk 



################################################################################

class vb_generate:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(300,320)
        self.master.geometry("400x420")

        self.master.title("vb_generate_gui.py ver 1.5  by Tom Irvine")         
        
     
        crow=0
        
        self.hwtext2=tk.Label(top,text='Select Signal')
        self.hwtext2.grid(row=crow, column=0, columnspan=2, pady=10,sticky=tk.SW)
        
        crow=crow+1     
        
        self.Lb_ws = tk.Listbox(top,height=7,exportselection=0)
        self.Lb_ws.insert(1, "sine")
        self.Lb_ws.insert(2, "cosine")
        self.Lb_ws.insert(3, "damped sine")        
        self.Lb_ws.insert(4, "white noise")
        self.Lb_ws.insert(5, "pink noise")        
        self.Lb_ws.insert(6, "sine sweep")
        self.Lb_ws.grid(row=crow, column=0,padx=10,sticky=tk.NW)
        self.Lb_ws.select_set(0)
        
        crow=crow+1  

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0, pady=15,sticky=tk.SW) 
        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=10,pady=15,sticky=tk.SW)

################################################################################

    def calculation(self):       
       
         n=int(self.Lb_ws.curselection()[0]) 
         
         win = tk.Toplevel()

         if(n==0):
             from vb_generate_sine_gui import vb_generate_sine        
             vb_generate_sine(win)     
             
         if(n==1):
             from vb_generate_cosine_gui import vb_generate_cosine        
             vb_generate_cosine(win)    
             
         if(n==2):
             from vb_damped_sine_gui import vb_damped_sine        
             vb_damped_sine(win)              
             
         if(n==3):
             from vb_white_noise_gui import vb_white_noise        
             vb_white_noise(win)   
             
         if(n==4):
             from vb_pink_noise_gui import vb_pink_noise        
             vb_pink_noise(win)                      
             
         if(n==5):
             from vb_sine_sweep_gui import vb_sine_sweep        
             vb_sine_sweep(win)                 

################################################################################

def quit(root):
    root.destroy()