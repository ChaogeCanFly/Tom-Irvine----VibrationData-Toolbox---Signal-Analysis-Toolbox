##########################################################################
# program: vb_Poisson_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.0
# date: May 1, 2014
# description:  
#
#
##########################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk    
    import tkinter.messagebox as tkMessageBox
    

from math import exp,factorial


    
######################################################################## 

class vb_Poisson:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.22))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_Poisson_gui.py ver 1.0  by Tom Irvine") 
        
        
        crow=0        
        
        self.hwtext1=tk.Label(top,text='The Poisson distribution gives the probability of a random X where the \n number of successes occurs during a given time interval or in a specified region. ')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)        
        
###############################################################################

        crow=crow+1
        self.hwtext15=tk.Label(top,text='Select Analysis')
        self.hwtext15.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.S)     
        
        crow=crow+1
        
        self.Lb3 = tk.Listbox(top,height=3,width=34,exportselection=0)
        self.Lb3.insert(1, "Single X value")        
        self.Lb3.insert(2, "Range of value X1 to X2, inclusive")        
        self.Lb3.grid(row=crow, column=0, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lb3.select_set(0)        
        self.Lb3.bind("<<ListboxSelect>>", self.OnKeyPress)
        
        crow=crow+1

        self.hwtext1 = tk.Label(top, text="Input Mean mu")
        self.hwtext1.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)
       
        self.hwtext2 = tk.Label(top, text="Input Random Variable X (integer)")
        self.hwtext2.grid(row=crow, column=1, columnspan=3, pady=7,sticky=tk.S)       
       
        crow=crow+1
        
        self.mur=tk.StringVar()  
        self.mur.set('')  
        self.mu_entry=tk.Entry(top, width = 10,textvariable=self.mur)
        self.mu_entry.grid(row=crow, column=0,sticky=tk.N)    
        self.mu_entry.bind("<KeyRelease>", self.OnKeyPress)  
        
        self.x1r=tk.StringVar()  
        self.x1r.set('')  
        self.x1_entry=tk.Entry(top, width = 10,textvariable=self.x1r)
        self.x1_entry.grid(row=crow, column=1,sticky=tk.NE)    
        self.x1_entry.bind("<KeyRelease>", self.OnKeyPress)  

        self.hwtext8=tk.Label(top,text='X1')
        self.hwtext8.grid(row=crow, column=2, padx=1, columnspan=1,sticky=tk.NW)
 
        crow=crow+1
        
        self.x2r=tk.StringVar()  
        self.x2r.set('')  
        self.x2_entry=tk.Entry(top, width = 10,textvariable=self.x2r)
        self.x2_entry.grid(row=crow, column=1,sticky=tk.NE)    
        self.x2_entry.bind("<KeyRelease>", self.OnKeyPress)  
        self.x2_entry.config(state='disable')
        
        self.hwtext7=tk.Label(top,text='X2')
        self.hwtext7.grid(row=crow, column=2, padx=1, columnspan=1,sticky=tk.NW)

        crow=crow+1
        
        self.hwtext31 = tk.Label(top, text="Probability")
        self.hwtext31.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)  
        
        self.hwtext51 = tk.Label(top, text="1 - Probability")
        self.hwtext51.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.S)   

        crow=crow+1

        self.p1r=tk.StringVar()  
        self.p1r.set('')  
        self.p1_entry=tk.Entry(top, width = 16,textvariable=self.p1r)
        self.p1_entry.grid(row=crow, column=0,padx=5, pady=1,sticky=tk.N) 
        self.p1_entry.config(state = 'disable')        


        self.p2r=tk.StringVar()  
        self.p2r.set('')  
        self.p2_entry=tk.Entry(top, width = 16,textvariable=self.p2r)
        self.p2_entry.grid(row=crow, column=1,padx=5, pady=1,sticky=tk.N) 
        self.p2_entry.config(state = 'disable') 
          
        
###############################################################################

        crow=crow+1

        self.button_calculate = \
        tk.Button(top, text="Calculate", command=self.calculation)

        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 
        
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=20)  
  
###############################################################################

    def OnKeyPress(self,event):
        self.p1r.set(' ')
        self.p1_entry.config(state = 'disable')   
        self.p2r.set(' ')
        self.p2_entry.config(state = 'disable')   

        n=int(self.Lb3.curselection()[0])  
        
        if(n==1):
            self.x2_entry.config(state = 'normal')  
        else:   
            self.x2_entry.config(state = 'disable')  
            self.x2r.set('')

    def calculation(self):
        
        n=int(self.Lb3.curselection()[0])  
        
        X1 =int(self.x1r.get())

        mu=float(self.mur.get())  
        
        if(n==0):
            FX1=exp(-mu)*(mu**X1)/factorial(X1)
            q=FX1
            
        else:
            X2 =int(self.x2r.get()) 

            FXR=0    
    
            for i in range(X1,(X2+1)):
                a=exp(-mu)*(mu**i)/factorial(i)
                FXR=FXR+a
                
            q=FXR
        
        w=1-q

        ps1='%14.9g' %q
        ps2='%14.9g' %w
        
        self.p1r.set(ps1)
        self.p2r.set(ps2)

        self.p1_entry.config(state = 'normal')   
        self.p2_entry.config(state = 'normal')          
        
###############################################################################

def quit(root):
    root.destroy()

###############################################################################