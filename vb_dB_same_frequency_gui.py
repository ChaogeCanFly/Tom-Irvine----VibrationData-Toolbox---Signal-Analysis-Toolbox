###########################################################################
# program: vb_dB_same_frequency_gui.py
# author: Tom Irvine
# version: 1.0
# date: May 30, 2014
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
    

from numpy import log10    

###############################################################################

class vb_dB_same_frequency:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.22))
        h = int(2.*(h*0.18))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_dB_same_frequency_gui.py  ver 1.0  by Tom Irvine")
                
        
        crow=0

        self.hwtext1=tk.Label(top,text='Select Dimension')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=7)   
        
        self.hwtext2=tk.Label(top,text='Select Analysis')
        self.hwtext2.grid(row=crow, column=2, columnspan=1, pady=7)       
        
        crow=crow+1
        
        self.Lb1 = tk.Listbox(top,height=3,width=34,exportselection=0)
        self.Lb1.insert(1, "Shock Response Spectrum (G)")
        self.Lb1.insert(2, "Overall (GRMS)")     
        self.Lb1.insert(3, "Power Spectral Density (G^2/Hz)")      
        self.Lb1.grid(row=crow, column=0, columnspan=2, pady=4)
        self.Lb1.select_set(0) 
        self.Lb1.bind("<<ListboxSelect>>", self.dimension)          

        self.Lb2 = tk.Listbox(top,height=3,width=50,exportselection=0)
        self.Lb2.insert(1, "Calculate dB difference between two levels")
        self.Lb2.insert(2, "Find new level given dB difference and one level")       
        self.Lb2.grid(row=crow, column=2, columnspan=2, pady=4)
        self.Lb2.select_set(0) 
        self.Lb2.bind("<<ListboxSelect>>", self.analysis)    
        
        crow=crow+1        

        self.hwtext3=tk.Label(top,text='Enter Data')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=9,sticky=tk.SE) 

        self.hwtext8=tk.Label(top,text='Result')
        self.hwtext8.grid(row=crow, column=2, columnspan=1, pady=9,sticky=tk.S)
        
        
        crow=crow+1
        
        self.ar=tk.StringVar()  
        self.a_entry=tk.Entry(top, width = 10,textvariable=self.ar)
        self.a_entry.grid(row=crow, column=0, pady=9,sticky=tk.E)  

        self.a_text=tk.StringVar()  
        self.a_text.set('Point 1 SRS(G)')         
        self.hwtext5=tk.Label(top,textvariable=self.a_text)
        self.hwtext5.grid(row=crow, column=1, columnspan=2, padx=4, pady=7,sticky=tk.W) 
        
        self.resultr=tk.StringVar()  
        self.result_entry=tk.Entry(top, width = 15,textvariable=self.resultr)
        self.result_entry.grid(row=crow, column=2, pady=5) 
        self.result_entry.config(state='readonly')        

        crow=crow+1

        self.br=tk.StringVar()  
        self.b_entry=tk.Entry(top, width = 10,textvariable=self.br)
        self.b_entry.grid(row=crow, column=0, pady=9,sticky=tk.E)  
        
        self.b_text=tk.StringVar()  
        self.b_text.set('Point 2 SRS(G)')         
        self.hwtext6=tk.Label(top,textvariable=self.b_text)
        self.hwtext6.grid(row=crow, column=1, columnspan=2, padx=4, pady=7,sticky=tk.W)         
        
        
        crow=crow+1       
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 
                
        root=self.master             

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=20)
        
        
        self.a_entry.bind("<Key>", self.callback_clear)
        self.b_entry.bind("<Key>", self.callback_clear)         
 
###############################################################################
 
    def calculation(self):
        n=1+int(self.Lb1.curselection()[0])   
        m=1+int(self.Lb2.curselection()[0])  
    
        A=float(self.ar.get())
        B=float(self.br.get())    

        if(m==1):
            if(n==1 or n==2):
                C=20*log10(B/A)
            else:
                C=10*log10(B/A)
   
            out1='%8.3g dB' %C
        else:
            if(n==1 or n==2):
                C=A*10**(B/20)
                
                if(n==1):
                    out1='%8.3g G' %C
                else:
                    out1='%8.3g GRMS' %C                    
   
            if(n==3):
                C=A*10**(B/10)
                out1='%8.3g G^2/Hz' %C       
         
        self.resultr.set(out1) 


    def callback_clear(self,event):
        self.resultr.set(' ')             
    
 
    def dimension(self,event): 
        self.change(self)         
         
    def analysis(self,event): 
        self.change(self)   


    @classmethod
    def change(cls,self):
        
        self.callback_clear(self)        
        
        n1=int(self.Lb1.curselection()[0])   
        n2=int(self.Lb2.curselection()[0])  
        
        if(n1==0):
            self.a_text.set('Point 1 SRS(G)')             

        if(n1==1):
            self.a_text.set('Point 1 (GRMS)') 
            
        if(n1==2):
            self.a_text.set('Point 1 PSD(G^2/Hz)')     
            
        if(n2==0):   
            if(n1==0):
                self.b_text.set('Point 2 SRS(G)')             

            if(n1==1):
                self.b_text.set('Point 2 (GRMS)') 
            
            if(n1==2):
                self.b_text.set('Point 2 PSD(G^2/Hz)')   
        
        else:        
            self.b_text.set('dB Difference')                               
                
                
                
    
###############################################################################    
    
def quit(root):
    root.destroy()              