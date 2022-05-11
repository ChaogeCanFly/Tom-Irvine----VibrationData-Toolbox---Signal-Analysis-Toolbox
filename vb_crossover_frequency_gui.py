###########################################################################
# program: vb_crossover_frequency_gui.py
# author: Tom Irvine
# version: 1.1
# date: April 27, 2014
# 
###############################################################################

from __future__ import print_function

from numpy import pi,sqrt
    
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

class vb_crossover_frequency:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.24))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_crossover_frequency_gui.py  ver 1.1  by Tom Irvine")
        
        crow=0        
        
        self.hwtext1=tk.Label(top,text='Units')
        self.hwtext1.grid(row=crow, column=0, pady=7)     
        
        self.hwtext2=tk.Label(top,text='Amplitude Pairs')
        self.hwtext2.grid(row=crow, column=1, pady=7)            
        
        crow=crow+1        
        
        self.Lbu = tk.Listbox(top,height=4,width=21,exportselection=0)
        self.Lbu.insert(1, "G, in/sec, in")
        self.Lbu.insert(2, "G, m/sec, mm")
        self.Lbu.insert(3, "m/sec^2, m/sec, mm")
        self.Lbu.grid(row=crow, column=0, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lbu.select_set(0)          
        
        self.Lba = tk.Listbox(top,height=5,width=34,exportselection=0)
        self.Lba.insert(1, "disp (zero-peak) -> velocity")
        self.Lba.insert(2, "disp (zero-peak) -> acceleration")
        self.Lba.insert(3, "disp (peak-peak) -> velocity")
        self.Lba.insert(4, "disp (peak-peak) -> acceleration")
        self.Lba.insert(5, "velocity -> acceleration")       
        self.Lba.grid(row=crow, column=1, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lba.select_set(0)  
        
############################################################################### 
        
        crow=crow+1

        self.hwtext10=tk.Label(top,text='Displacement (zero-peak)')
        self.hwtext10.grid(row=crow, column=0, pady=7,sticky=tk.E) 

        crow=crow+1

        self.amp1=tk.StringVar()  
        self.amp1=tk.Entry(top, width = 12,textvariable=self.amp1)
        self.amp1.grid(row=crow, column=0,padx=1, pady=2,sticky=tk.E)

        self.hwtext12=tk.Label(top,text='inch')
        self.hwtext12.grid(row=crow, column=1, pady=2,sticky=tk.W) 
        

############################################################################### 

        crow=crow+1

        self.hwtext11=tk.Label(top,text='Velocity (zero-peak)')
        self.hwtext11.grid(row=crow, column=0, pady=7,sticky=tk.E)  
              
        crow=crow+1

        self.amp2=tk.StringVar()  
        self.amp2=tk.Entry(top, width = 12,textvariable=self.amp2)
        self.amp2.grid(row=crow, column=0,padx=1, pady=2,sticky=tk.E)        

        self.hwtext13=tk.Label(top,text='in/sec')
        self.hwtext13.grid(row=crow, column=1, pady=2,sticky=tk.W)
        
        crow=crow+1

        self.hwtext15=tk.Label(top,text='Cross-Over Frequency (Hz)')
        self.hwtext15.grid(row=crow, column=0, pady=4)         
        
        crow=crow+1

        self.fcr=tk.StringVar()  
        self.fc=tk.Entry(top, width = 12,textvariable=self.fcr)
        self.fc.grid(row=crow, column=0,padx=1, pady=2,sticky=tk.E)   
        self.fc.configure(state='readonly')

###############################################################################        
        
        crow=crow+1    

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate_main)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0,padx=1, pady=10) 
                     
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=1,pady=10) 


        self.amp1.bind("<Key>", self.callback_clear)
        self.amp2.bind("<Key>", self.callback_clear) 

        self.Lbu.bind("<<ListboxSelect>>", self.callback_labels)  
        self.Lba.bind("<<ListboxSelect>>", self.callback_labels)  

###############################################################################


    def callback_clear(self,event):
        self.fcr.set('')
        

    def callback_labels(self,event):
        
#        print(' in callback labels')
        
        self.fcr.set('')
        
        nu=int(self.Lbu.curselection()[0])         
        na=int(self.Lba.curselection()[0]) 

        nunit=nu+1
        npair=na+1
    
        if(npair==1):        # disp (zero-peak): -> velocity
            text1='displacement (zero-peak):'
            text2='velocity'
            
            if(nunit==1): # G, in/sec, in
                text_unit_1 = 'inch'
                text_unit_2 = 'in/sec'        
    
            if(nunit==2): # G, m/sec, mm
                text_unit_1 = 'mm'
                text_unit_2 = 'm/sec'           
    
            if(nunit==3): # m/sec^2, m/sec, mm
                text_unit_1 = 'mm'
                text_unit_2 = 'm/sec'          
        
        if(npair==2):     # disp (zero-peak): -> acceleration 
            text1='displacement (zero-peak):'
            text2='acceleration'    
    
            if(nunit==1): # G, in/sec, in
                text_unit_1 = 'inch'
                text_unit_2 = 'G'          
    
            if(nunit==2): # G, m/sec, mm
                text_unit_1 = 'mm'
                text_unit_2 = 'G'        
    
            if(nunit==3): # m/sec^2, m/sec, mm
                text_unit_1 = 'mm'
                text_unit_2 = 'm/sec^2'        
     

        if(npair==3):     # disp (peak-peak): -> velocity 
            text1='displacement (peak-peak):'
            text2='velocity'     
    
            if(nunit==1): # G, in/sec, in
                text_unit_1 = 'inch'
                text_unit_2 = 'in/sec'          
    
            if(nunit==2): # G, m/sec, mm
                text_unit_1 = 'mm'
                text_unit_2 = 'm/sec'          
    
            if(nunit==3): # m/sec^2, m/sec, mm
                text_unit_1 = 'mm'
                text_unit_2 = 'm/sec'         
     
 
        if(npair==4):     # disp (peak-peak): -> acceleration
            text1='displacement (peak-peak):'
            text2='acceleration'     
    
            if(nunit==1): # G, in/sec, in
                text_unit_1 = 'inch'
                text_unit_2 = 'G'         
    
            if(nunit==2): # G, m/sec, mm
                text_unit_1 = 'mm'
                text_unit_2 = 'G'          
    
            if(nunit==3): # m/sec^2, m/sec, mm
                text_unit_1 = 'mm' 
                text_unit_2 = 'm/sec^2'         
     

        if(npair==5):     # velocity -> acceleration
            text1='velocity'
            text2='acceleration'     
    
            if(nunit==1): # G, in/sec, in
                text_unit_1 = 'in/sec'        
                text_unit_2 = 'G'          
    
            if(nunit==2): # G, m/sec, mm
                text_unit_1 = 'm/sec'
                text_unit_2 = 'G'        
    
            if(nunit==3): # m/sec^2, m/sec, mm
                text_unit_1 = 'm/sec'
                text_unit_2 = 'm/sec^2'      
     

        self.hwtext10.config(text=text1)
        self.hwtext12.config(text=text_unit_1)
        self.hwtext11.config(text=text2)
        self.hwtext13.config(text=text_unit_2)    
    

    def calculate_main(self):
        
        amp1=float(self.amp1.get())
        amp2=float(self.amp2.get())
        
        nu=int(self.Lbu.curselection()[0])         
        na=int(self.Lba.curselection()[0]) 


        nunit=nu+1
        npair=na+1
        
#        print("nunit=%d" %nunit)
#        print("npair=%d" %npair)        
        
        
        if(npair==1 or npair==3):
            d=amp1
            v=amp2
    
        if(npair==2 or npair==4):
            d=amp1
            a=amp2
 
        if(npair==5):
            v=amp1
            a=amp2
    
 
        if(nunit==1): # G, in/sec, in
            if(npair==1): # disp (zero-peak): -> velocity
                pass
            if(npair==2): # disp (zero-peak): -> acceleration
                a=a*386
    
            if(npair==3): # disp (peak-peak): -> velocity
                d=d/2
    
            if(npair==4): # disp (peak-peak): -> acceleration
                d=d/2
                a=a*386
    
            if(npair==5): # velocity -> acceleration
                a=a*386
       

        if(nunit==2): # G, m/sec, mm
            d=d/1000
            
            if(npair==1): # disp (zero-peak): -> velocity
                pass
            if(npair==2): # disp (zero-peak): -> acceleration
                a=a*9.81
    
            if(npair==3): # disp (peak-peak): -> velocity
                d=d/2
    
            if(npair==4): # disp (peak-peak): -> acceleration
                d=d/2 
                a=a*9.81
    
            if(npair==5): # velocity -> acceleration
                a=a*9.81
       
 
        if(nunit==3): # m/sec^2, m/sec, mm
            d=d/1000
            if(npair==1): # disp (zero-peak): -> velocity
                pass
            if(npair==2): # disp (zero-peak): -> acceleration
                pass
            if(npair==3): # disp (peak-peak): -> velocity
                d=d/2        
    
            if(npair==4): # disp (peak-peak): -> acceleration
                d=d/2 
    
            if(npair==5): # velocity -> acceleration
                pass       

        fc=0
 
        if(npair==1 or npair==3):
            fc=( v/d )
    
        if(npair==2 or npair==4):
            fc=sqrt( a/d )
 
        if(npair==5):
            fc=( a/v )
    
        fc=fc/(2*pi)

        buf1 = "%8.4g" %fc        
        self.fcr.set(buf1)   
        
################################################################################
        
        
def quit(root):
    root.destroy()        