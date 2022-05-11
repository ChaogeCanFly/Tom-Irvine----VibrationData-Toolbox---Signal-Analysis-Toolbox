################################################################################
# program: vb_turbine_generator_gui.py
# author: Tom Irvine
# version: 1.1
# date: June 27, 2014
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

from numpy import zeros


class vb_turbine_generator:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_turbine_generator_gui.py ver 1.1  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Rotor Speed')
        self.hwtext1.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)

        self.hwtext3=tk.Label(top,text='Frequency Results')
        self.hwtext3.grid(row=crow, column=2, columnspan=1, pady=7,sticky=tk.S)
    
        crow=crow+1
        
        self.speedr=tk.StringVar()  
        self.speedr.set('')  
        self.speed_entry=tk.Entry(top, width = 12,textvariable=self.speedr)
        self.speed_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=3,sticky=tk.N)         
        
        self.Lbs = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lbs.insert(1, "Hz")
        self.Lbs.insert(2, "RPM")
        self.Lbs.grid(row=crow, column=1, columnspan=1, padx=1, pady=4,sticky=tk.NW)
        self.Lbs.select_set(0)


        self.textWidget = tk.Text(top, width=40, height = 11,font = "TkDefaultFont 9")
        self.textWidget.grid(row=crow, column=2,columnspan=5, rowspan=3, pady=2)   
        
        
        crow=crow+1          

        self.hwtext2=tk.Label(top,text='Number of Vanes')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)                            
        
        crow=crow+1
        
        self.vanesr=tk.StringVar()  
        self.vanesr.set('')  
        self.vanes_entry=tk.Entry(top, width = 12,textvariable=self.vanesr)
        self.vanes_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=1,sticky=tk.N)         
        
        crow=crow+1                

        self.hwtext3=tk.Label(top,text='Number of Poles')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)    

        crow=crow+1      
        
        self.polesr=tk.StringVar()  
        self.polesr.set('')  
        self.poles_entry=tk.Entry(top, width = 9,textvariable=self.polesr)
        self.poles_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=1,sticky=tk.N)   

        
################################################################################

        crow=crow+1         
    
        self.button_calculate = tk.Button(top, text="Calculate",command=self.calculate)
        self.button_calculate.config( height = 2, width = 15, state='normal' )
        self.button_calculate.grid(row=crow, column=0,columnspan=1, padx=2, pady=15)     
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=15)
        

        self.poles_entry.bind("<Key>", self.callback_clear)  
        self.vanes_entry.bind("<Key>", self.callback_clear)  
        self.speed_entry.bind("<Key>", self.callback_clear)          
        
        self.Lbs.bind("<<ListboxSelect>>", self.callback_clear)    

        
################################################################################

      
    def callback_clear(self,event):
        
        self.textWidget.delete(1.0, tk.END)     


    def calculate(self):   
        
        f=float(self.speedr.get())
        v=float(self.vanesr.get())
        p=float(self.polesr.get())        
        
        n=1+int(self.Lbs.curselection()[0])
       
       
        if(n==2):
            f=f/60.


        freq=zeros(8,'f')

        freq[0]=f    
        freq[1]=f*v      
        freq[2]=2*f*v 
        freq[3]=3*f*v
        freq[4]=f*p    
        freq[5]=2*f*p  
        freq[6]=3*f*p 
        freq[7]=(1./2.)*f*p 
        
        


        S0='Rotor Speed'
        S1='Rotor Speed x %d Vanes' %v   
        S2='2 x Rotor Speed x %d Vanes' %v 
        S3='3 x Rotor Speed x %d Vanes' %v 
        S4='Rotor Speed x %d Poles' %p   
        S5='2 x Rotor Speed x %d Poles' %p 
        S6='3 x Rotor Speed x %d Poles' %p 
        S7='(1/2) x Rotor Speed x %d Poles' %p 
       
        S=[]
        S.append(S0)
        S.append(S1)
        S.append(S2)
        S.append(S3)
        S.append(S4)
        S.append(S5)
        S.append(S6)
        S.append(S7)        
        
        
        
        fff=zeros((len(freq),2),'f');

        for i in range (0,len(freq)):
            fff[i,0]=freq[i]
            fff[i,1]=i       
       
       
        ggg=fff[fff[:,0].argsort(),]



        string1='  %8.4g Hz,  %s \n' %(ggg[0,0],S[int(ggg[0,1])])
        string2='  %8.4g Hz,  %s \n' %(ggg[1,0],S[int(ggg[1,1])])        
        string3='  %8.4g Hz,  %s \n' %(ggg[2,0],S[int(ggg[2,1])])
        string4='  %8.4g Hz,  %s \n' %(ggg[3,0],S[int(ggg[3,1])])  
        string5='  %8.4g Hz,  %s \n' %(ggg[4,0],S[int(ggg[4,1])])
        string6='  %8.4g Hz,  %s \n' %(ggg[5,0],S[int(ggg[5,1])])        
        string7='  %8.4g Hz,  %s \n' %(ggg[6,0],S[int(ggg[6,1])])
        string8='  %8.4g Hz,  %s ' %(ggg[7,0],S[int(ggg[7,1])])        

        
        self.textWidget.delete(1.0, tk.END)
        
        self.textWidget.insert('1.0',string1)
        self.textWidget.insert('end',string2)
        
        self.textWidget.insert('end',string3)       
        self.textWidget.insert('end',string4)
          
        self.textWidget.insert('end',string5)       
        self.textWidget.insert('end',string6) 
        self.textWidget.insert('end',string7)            
        self.textWidget.insert('end',string8)
        
###############################################################################
        
def quit(root):
    root.destroy()                    