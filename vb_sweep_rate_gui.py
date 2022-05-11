###########################################################################
# program: vb_sweep_rate_gui.py
# author: Tom Irvine
# version: 1.1
# date: April 27, 2014
# 
###############################################################################

from __future__ import print_function

from numpy import log
    
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

class vb_sweep_rate:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.14))
        h = int(2.*(h*0.24))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_sweep_rate_gui .py  ver 1.1  by Tom Irvine")
        
        
      
        crow=0
        
        self.hwtext6=tk.Label(top,text='Select Sweep Type')
        self.hwtext6.grid(row=crow, column=1, pady=7)         

        self.hwtext4=tk.Label(top,text='Enter Duration (min)')
        self.hwtext4.grid(row=crow, column=2, pady=7)   
        
        crow=crow+1       
        
        self.Lb3 = tk.Listbox(top,height=2,width=15,exportselection=0)
        self.Lb3.insert(1, "Log")
        self.Lb3.insert(2, "Linear")      
        self.Lb3.grid(row=crow, column=1, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lb3.select_set(0)                       
        
        self.duration=tk.StringVar()  
        self.duration=tk.Entry(top, width = 12,textvariable=self.duration)
        self.duration.grid(row=crow, column=2,padx=1, pady=4,sticky=tk.N)

        
        crow=crow+1
        
        self.hwtext1=tk.Label(top,text='Enter Frequencies (Hz)')
        self.hwtext1.grid(row=crow, column=1, pady=10,sticky=tk.W)               
        
###############################################################################
        
        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='1')
        self.hwtext2.grid(row=crow, column=0, pady=4,sticky=tk.E)  
        
        self.freq1=tk.StringVar()  
        self.freq1=tk.Entry(top, width = 12,textvariable=self.freq1)
        self.freq1.grid(row=crow, column=1,padx=1, pady=4)
        
        crow=crow+1
        
        self.hwtext3=tk.Label(top,text='2')
        self.hwtext3.grid(row=crow, column=0, pady=4,sticky=tk.E)         
        
        self.freq2=tk.StringVar()  
        self.freq2=tk.Entry(top, width = 12,textvariable=self.freq2)
        self.freq2.grid(row=crow, column=1,padx=1, pady=4)        
        
        crow=crow+1        
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate_main)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=1,padx=1, pady=10,sticky=tk.SE) 
                     
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2, padx=6,pady=10,sticky=tk.SE) 

        crow=crow+1  
        
        self.hwtext7=tk.Label(top,text='Results')
        self.hwtext7.grid(row=crow, column=1, pady=10,sticky=tk.W)               
        
        crow=crow+1  
        
        self.hwtext8=tk.Label(top,text='Total Cycles')
        self.hwtext8.grid(row=crow, column=1, pady=2,sticky=tk.W) 
        
        crow=crow+1 
        
        self.SWPRr=tk.StringVar()  
        self.SWPR_entry=tk.Entry(top, width = 17,textvariable=self.SWPRr)
        self.SWPR_entry.grid(row=crow, column=1) 
        self.SWPR_entry.configure(state='readonly')        

        crow=crow+1  
        
        self.hwtext9=tk.Label(top,text='Octaves')
        self.hwtext9.grid(row=crow, column=1, pady=10,sticky=tk.W)                

        crow=crow+1         

        self.NOCTr=tk.StringVar()  
        self.NOCT_entry=tk.Entry(top, width = 17,textvariable=self.NOCTr)
        self.NOCT_entry.grid(row=crow, column=1) 
        self.NOCT_entry.configure(state='readonly')
        
        self.freq1.bind("<Key>", self.callback_clear)
        self.freq2.bind("<Key>", self.callback_clear)        
        self.duration.bind("<Key>", self.callback_clear)  
        self.Lb3.bind("<<ListboxSelect>>", self.callback_clear)  
                
        
###############################################################################

    def callback_clear(self,event):
        self.SWPRr.set('')
        self.NOCTr.set('')        

###############################################################################

    def calculate_main(self):
        
        Tmin=float(self.duration.get())
        f1=float(self.freq1.get())
        f2=float(self.freq2.get())
        
        if(f1>f2):
            temp=f1
            f1=f2
            f2=temp
            
        octaves=log(f2/f1)/log(2)
        
        n=int(self.Lb3.curselection()[0]) 
        

        if(n==0):  # log
            r=octaves/Tmin
            buf1 = "%7.3g oct/min" %r
       
        else:      # linear
            r=(f2-f1)/Tmin
            buf1 = "%7.3g Hz/min" %r            
        
                
        self.SWPRr.set(buf1)  

        buf2 = "%7.3g" %octaves        
        self.NOCTr.set(buf2)
        

def quit(root):
    root.destroy()         
                      