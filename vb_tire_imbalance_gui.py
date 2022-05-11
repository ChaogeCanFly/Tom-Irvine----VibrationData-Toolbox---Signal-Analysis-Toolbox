################################################################################
# program: vb_tire_imbalance_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 22, 2014
# description:  
################################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename    
    

from numpy import pi



class vb_tire_imbalance:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_tire_imbalance_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Speed')
        self.hwtext1.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)

        self.hwtext3=tk.Label(top,text='1X Frequency (Hz)')
        self.hwtext3.grid(row=crow, column=2, columnspan=1, pady=7,sticky=tk.S)
    

        crow=crow+1
        
        self.speedr=tk.StringVar()  
        self.speedr.set('')  
        self.speed_entry=tk.Entry(top, width = 12,textvariable=self.speedr)
        self.speed_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=3,sticky=tk.N)         
        
        self.Lbs = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lbs.insert(1, "mph")
        self.Lbs.insert(2, "ft/sec")
        self.Lbs.insert(3, "km/hr")
        self.Lbs.grid(row=crow, column=1, columnspan=1, padx=1, pady=4,sticky=tk.NW)
        self.Lbs.select_set(0)
        

        self.f1r=tk.StringVar()  
        self.f1r.set('')  
        self.f1_entry=tk.Entry(top, width = 9,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=2,columnspan=1,padx=5, pady=3,sticky=tk.NE)   
        self.f1_entry.config(state='readonly')
        
        
        crow=crow+1                

        self.hwtext2=tk.Label(top,text='Diameter')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.N)        
        
        self.hwtext5=tk.Label(top,text='2X Frequency (Hz)')
        self.hwtext5.grid(row=crow, column=2, columnspan=1, pady=7,sticky=tk.N)        
        
        
        crow=crow+1
        
        self.diameterr=tk.StringVar()  
        self.diameterr.set('')  
        self.diameter_entry=tk.Entry(top, width = 12,textvariable=self.diameterr)
        self.diameter_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=3,sticky=tk.N)         
        
        self.Lbd = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbd.insert(1, "inch")
        self.Lbd.insert(2, "cm")
        self.Lbd.grid(row=crow, column=1, columnspan=1, padx=1, pady=4,sticky=tk.NW)
        self.Lbd.select_set(0)        

        self.f2r=tk.StringVar()  
        self.f2r.set('')  
        self.f2_entry=tk.Entry(top, width = 9,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=2,columnspan=1,padx=5, pady=3,sticky=tk.NE)   
        self.f2_entry.config(state='readonly')
        
        
################################################################################

        crow=crow+1         
    
        self.button_calculate = tk.Button(top, text="Calculate",command=self.calculate)
        self.button_calculate.config( height = 2, width = 15, state='normal' )
        self.button_calculate.grid(row=crow, column=0,columnspan=1, padx=2, pady=15)     
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=15)
        
        
        self.Lbs.bind("<<ListboxSelect>>", self.callback_clear)    
        self.Lbd.bind("<<ListboxSelect>>", self.callback_clear)                
      
        self.diameter_entry.bind("<Key>", self.callback_clear)  
        self.speed_entry.bind("<Key>", self.callback_clear)          
      
      
################################################################################  


    def callback_clear(self,event):
        
        self.f1r.set(' ') 
        self.f2r.set(' ')         


    def calculate(self):   
        
        speed=float(self.speedr.get())
        dia=float(self.diameterr.get())
        
        iunit_speed=1+int(self.Lbs.curselection()[0])
        iunit_dia  =1+int(self.Lbd.curselection()[0])        
        
#
# convert speed to m/sec
#
        if(iunit_speed==1):
            speed=speed*0.44704

#
        if(iunit_speed==2):
            speed=speed*0.3048

#   
        if(iunit_speed==3):  
            speed=speed* 0.27778 

#
        if(iunit_dia==1):
            dia=dia*0.0254

#
        if(iunit_dia==2):
            dia=dia*0.01 

#
        circum = pi*dia
        freq = speed/circum
#        

        s1= '%6.3g' %freq
        s2= '%6.3g' %(2*freq)


        self.f1r.set(s1) 
        self.f2r.set(s2) 

        
################################################################################


def quit(root):
    root.destroy()