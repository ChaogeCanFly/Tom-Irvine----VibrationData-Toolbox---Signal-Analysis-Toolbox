################################################################################
# program: vb_tangential_velocity_gui.py
# author: Tom Irvine
# version: 1.1
# date: May 23, 2014
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
        


from numpy import pi


class vb_tangential_velocity:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_tangential_velocity_gui.py ver 1.1  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Rotor Speed')
        self.hwtext1.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)

        self.hwtext3=tk.Label(top,text='Velocity Results')
        self.hwtext3.grid(row=crow, column=2, columnspan=1, pady=7,sticky=tk.S)
    
        crow=crow+1
        
        self.speedr=tk.StringVar()  
        self.speedr.set('')  
        self.speed_entry=tk.Entry(top, width = 12,textvariable=self.speedr)
        self.speed_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=3,sticky=tk.N)         
        
        self.Lbs = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lbs.insert(1, "Hz")
        self.Lbs.insert(2, "rad/sec")        
        self.Lbs.insert(3, "RPM")
        self.Lbs.grid(row=crow, column=1, columnspan=1, padx=1, pady=4,sticky=tk.NW)
        self.Lbs.select_set(0)


        self.textWidget = tk.Text(top, width=30, height = 4,font = "TkDefaultFont 9")
        self.textWidget.grid(row=crow, column=2,columnspan=1, rowspan=1, pady=2)   
        
        
        crow=crow+1                

        self.hwtext3=tk.Label(top,text='Radius')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)    

        crow=crow+1      
        
        self.radiusr=tk.StringVar()  
        self.radiusr.set('')  
        self.radius_entry=tk.Entry(top, width = 9,textvariable=self.radiusr)
        self.radius_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=1,sticky=tk.N)   

        self.Lbr = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lbr.insert(1, "inches")
        self.Lbr.insert(2, "feet")        
        self.Lbr.insert(3, "meters")
        self.Lbr.grid(row=crow, column=1, columnspan=1, padx=1, pady=4,sticky=tk.NW)
        self.Lbr.select_set(0)
        
################################################################################

        crow=crow+1         
    
        self.button_calculate = tk.Button(top, text="Calculate",command=self.calculate)
        self.button_calculate.config( height = 2, width = 15, state='normal' )
        self.button_calculate.grid(row=crow, column=0,columnspan=1, padx=2, pady=15)     
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=15)
        

        self.radius_entry.bind("<Key>", self.callback_clear)  
        self.speed_entry.bind("<Key>", self.callback_clear)  
                
        self.Lbr.bind("<<ListboxSelect>>", self.callback_clear)    
        self.Lbs.bind("<<ListboxSelect>>", self.callback_clear)  
        
################################################################################

      
    def callback_clear(self,event):
        
        self.textWidget.delete(1.0, tk.END)     


    def calculate(self):   
        
        frequency=float(self.speedr.get())
        radius=float(self.radiusr.get())
     
        
        iunit_frequency=1+int(self.Lbs.curselection()[0])
        iunit_radius=1+int(self.Lbr.curselection()[0])      
 
 
        feet_per_meters=3.281
        meters_per_feet=1/feet_per_meters
 
        meters_per_inch=0.0254
 
        if(iunit_frequency==2):
           frequency=frequency/(2*pi)

        if(iunit_frequency==3):
           frequency=frequency/60.

        if(iunit_radius==1): # convert inches to meters
           radius=radius*meters_per_inch    

        if(iunit_radius==2):  # convert feet to meters
           radius=radius*meters_per_feet 

 
        vel_mps=2*pi*frequency*radius
        vel_fps=vel_mps*feet_per_meters


        string1='  %8.4g ft/sec \n' %vel_fps
        string2='  %8.4g meters/sec ' %vel_mps     
    
        
        self.textWidget.delete(1.0, tk.END)
        
        self.textWidget.insert('1.0',string1)
        self.textWidget.insert('end',string2)
        

        
       

###############################################################################
        
def quit(root):
    root.destroy()                    