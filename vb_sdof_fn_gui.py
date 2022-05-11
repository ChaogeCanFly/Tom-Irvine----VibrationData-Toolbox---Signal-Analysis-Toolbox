################################################################################
# program: vb_sdof_fn_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 15, 2014
# description:  Natural Frequency of a Spring-Mass System 
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

from numpy import sqrt,pi


class vb_sdof_fn:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.18))
        h = int(2.*(h*0.28))
        self.master.geometry("%dx%d+0+0" % (w, h))

        
        self.master.title("vb_sdof_fn_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0
        
        self.hwtext7=tk.Label(top,text='Natural Frequency of an SDOF Spring-Mass System')
        self.hwtext7.grid(row=crow, column=0, columnspan=3,pady=14)        
        
        crow=crow+1
        
        self.hwtext0=tk.Label(top,text='Select Unit')
        self.hwtext0.grid(row=crow, column=0, pady=14)   
        
        self.hwtext1=tk.Label(top,text='Calculate')
        self.hwtext1.grid(row=crow, column=1, pady=14)     
                
###############################################################################

        crow=crow+1
        
        self.Lbu = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lbu.insert(1, "English")
        self.Lbu.insert(2, "metric")     
        self.Lbu.grid(row=crow, column=0, pady=1, padx=5,sticky=tk.N)
        self.Lbu.select_set(0)         

        self.Lbanalysis = tk.Listbox(top,height=4,width=20,exportselection=0)
        self.Lbanalysis.insert(1, "Natural Frequency")
        self.Lbanalysis.insert(2, "Mass")
        self.Lbanalysis.insert(3, "Stiffness")        
        self.Lbanalysis.grid(row=crow, column=1, pady=1, padx=5,sticky=tk.N)
        self.Lbanalysis.select_set(0)           
                
###############################################################################
                
        crow=crow+1   
        
        self.hwtext11=tk.Label(top,text='Input Data')
        self.hwtext11.grid(row=crow, column=0, columnspan=1,pady=16,sticky=tk.S)          

        crow=crow+1

        self.hwtext_box1=tk.Label(top,text='Stiffness (lbf/in)')
        self.hwtext_box1.grid(row=crow, column=0, columnspan=1, pady=2)  
        
        self.hwtext_box2=tk.Label(top,text='Mass (lbm)')
        self.hwtext_box2.grid(row=crow, column=1, columnspan=1,pady=2)  
        
###############################################################################
        
        crow=crow+1 

        self.box1r=tk.StringVar()  
        self.box1_entry=tk.Entry(top, width = 12,textvariable=self.box1r)
        self.box1_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.box1_entry.configure(state='normal')  

        
        self.box2r=tk.StringVar()  
        self.box2_entry=tk.Entry(top, width = 12,textvariable=self.box2r)
        self.box2_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.box2_entry.configure(state='normal')        

###############################################################################
        
        crow=crow+1 
                
        self.hwtext_box15=tk.Label(top,text='Results')
        self.hwtext_box15.grid(row=crow, column=0, columnspan=1,pady=16,sticky=tk.S) 
                
        crow=crow+1 
        
        self.hwtext_box14=tk.Label(top,text='Natural Freq (Hz)')
        self.hwtext_box14.grid(row=crow, column=0, columnspan=1,pady=1,sticky=tk.S)    
        
        self.hwtext_box15=tk.Label(top,text='1G Static Deflection (in)')
        self.hwtext_box15.grid(row=crow, column=1, columnspan=2,pady=1,sticky=tk.S) 

###############################################################################

        crow=crow+1
        
        self.resultr=tk.StringVar()  
        self.result_entry=tk.Entry(top, width = 14,textvariable=self.resultr)
        self.result_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.result_entry.configure(state='readonly')   
        
        self.sdeflr=tk.StringVar()  
        self.sdefl_entry=tk.Entry(top, width = 14,textvariable=self.sdeflr)
        self.sdefl_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.sdefl_entry.configure(state='readonly')  

###############################################################################
        
        crow=crow+1

        button1=tk.Button(top, text='Perform Analysis', command=self.PerformAnalysis)
        button1.grid(row=crow, column=0, padx=10, pady=10)
        button1.config( height = 2, width = 20 )        
          
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 20 )
        self.button_quit.grid(row=crow, column=1, padx=10,pady=10) 
        
        
        self.Lbu.bind("<<ListboxSelect>>", self.callback_analysis)        
        self.Lbanalysis.bind("<<ListboxSelect>>", self.callback_analysis)  
        self.box1_entry.bind("<Key>", self.callback_clear)    
        self.box2_entry.bind("<Key>", self.callback_clear)    
        
################################################################################
    
    def callback_clear(self,event):
        
        self.resultr.set('')
        self.sdeflr.set('')     
    
                       
    def callback_analysis(self,event):
                                 
        self.callback_clear(self)
        
        nu=1+int(self.Lbu.curselection()[0])
        na=1+int(self.Lbanalysis.curselection()[0])        


        if(nu==1):
            self.hwtext_box15.config(text="1G Static Deflection (in)" )     
        else:
            self.hwtext_box15.config(text="1G Static Deflection (mm)" )  



        if(na==1):   # Natural Frequency
            self.hwtext_box14.config(text='Natural Freq (Hz)')
            if(nu==1):
                self.hwtext_box1.config(text="Stiffness (lbf/in)" ) 
                self.hwtext_box2.config(text="Mass (lbm)" )           
            else:
                self.hwtext_box1.config(text="Stiffness (N/m)" )   
                self.hwtext_box2.config(text="Mass (kg)" )                  

        
        if(na==2):   # Mass
            self.hwtext_box1.config(text="Natural Freq (Hz)" )        
            if(nu==1):
                self.hwtext_box14.config(text='Mass (lbm)')                
                self.hwtext_box2.config(text="Stiffness (lbf/in)" )   
            else:
                self.hwtext_box14.config(text='Mass (kg)') 
                self.hwtext_box2.config(text="Stiffness (N/m)" ) 

        
        if(na==3):   # Stiffness
            self.hwtext_box1.config(text="Natural Freq (Hz)" )
            if(nu==1):
                self.hwtext_box14.config(text='Stiffness (lbf/in)')                  
                self.hwtext_box2.config(text="Mass (lbm)" )
            else:
                self.hwtext_box14.config(text='Stiffness (N/m)')                 
                self.hwtext_box2.config(text="Mass (kg)" )
                       
################################################################################

    def PerformAnalysis(self):

        a=float(self.box1r.get())
        b=float(self.box2r.get())
        
        nu=1+int(self.Lbu.curselection()[0])
        na=1+int(self.Lbanalysis.curselection()[0])

        tpi=2*pi

        if(na>=2):
            fn=a
            omega=tpi*fn
            om2=omega**2

        if(na!=2):
            m=b
            if(nu==1):
                m=m/386


        if(na==1):   # Natural Frequency
            k=a
            fn=sqrt(k/m)/tpi
            omega=tpi*fn
            om2=omega**2
            c=fn

        if(na==2):   # Mass
            k=b
            m=k/om2
            if(nu==1):
                m=m*386
            c=m    

        if(na==3):   # Stiffness
            k=m*om2
            c=k
            
        
        data1="%8.4g" %c
        self.resultr.set(data1)
        
        if(nu==1):
            defl=386/om2
        else:
            defl=9.81*1000/om2
        
        data2="%8.4g" %defl
        self.sdeflr.set(data2)        
        
        
###############################################################################
        
def quit(root):
    root.destroy()                    