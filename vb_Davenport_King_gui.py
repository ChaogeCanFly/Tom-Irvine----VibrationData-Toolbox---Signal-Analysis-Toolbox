################################################################################
# program: vb_Davenport_King_gui.py
# author: Tom Irvine
# version: 1.1
# date: January 30, 2015
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
    
from vb_utilities import WriteData2

import matplotlib.pyplot as plt

from numpy import zeros,exp,pi,sqrt




class vb_Davenport_King:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.19))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_Davenport_King_gui.py ver 1.1  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Davenport-King Wind Velocity PSD for Horizontal Gustiness')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)


        crow=crow+1

        self.hwtext2=tk.Label(top,text='Select Units')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)


        self.v_text=tk.StringVar()  
        self.v_text.set('Mean Velocity (ft/sec) at 33 ft')  
        self.hwtext_v=tk.Label(top,textvariable=self.v_text)        
        self.hwtext_v.grid(row=crow, column=1,columnspan=1,padx=15,sticky=tk.S)
        
        
################################################################################

        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lb1.insert(1, "English")
        self.Lb1.insert(2, "metric")

        self.Lb1.grid(row=crow, column=0, padx=16, pady=4,sticky=tk.N)
        self.Lb1.select_set(0)         
        self.Lb1.bind('<<ListboxSelect>>',self.unit_option)                           
                          
        self.mean_veloxr=tk.StringVar()  
        self.mean_veloxr.set('')  
        self.mean_velox_entry=tk.Entry(top, width = 10,textvariable=self.mean_veloxr)
        self.mean_velox_entry.grid(row=crow, column=1,sticky=tk.N)                    
                            
                          
################################################################################

        crow=crow+1                          
                          
        self.scale_text=tk.StringVar()  
        self.scale_text.set('Scale Length (ft)')  
        self.hwtext_scale=tk.Label(top,textvariable=self.scale_text)        
        self.hwtext_scale.grid(row=crow, column=0,columnspan=1,padx=15, pady=10,sticky=tk.S)   

        self.drag_text=tk.StringVar()  
        self.drag_text.set('Surface Drag Coefficient')  
        self.hwtext_drag=tk.Label(top,textvariable=self.drag_text)        
        self.hwtext_drag.grid(row=crow, column=1,columnspan=1,padx=15, pady=10,sticky=tk.S)                        
                          
################################################################################

        crow=crow+1                          
        
        self.scaler=tk.StringVar()  
        self.scaler.set('4000')  
        self.scale_entry=tk.Entry(top, width = 10,textvariable=self.scaler)
        self.scale_entry.grid(row=crow, column=0, pady=5,sticky=tk.N)  

        self.dragr=tk.StringVar()  
        self.dragr.set(' ')  
        self.drag_entry=tk.Entry(top, width = 10,textvariable=self.dragr)
        self.drag_entry.grid(row=crow, column=1, pady=5,sticky=tk.N)                                      
                          
################################################################################                          
                

        crow=crow+1                
                
        self.button_calculate = tk.Button(top, text="Calculate",command=self.calculate_data)
        self.button_calculate.config( height = 2, width = 16 )
        self.button_calculate.grid(row=crow, column=0,columnspan=1, padx=5, pady=10,sticky=tk.S)       
        
################################################################################
      

        self.button_sav = tk.Button(top, text="Export PSD", command=self.save_data)
        self.button_sav.config( height = 2, width = 16,state = 'disabled' )
        self.button_sav.grid(row=crow, column=1,columnspan=1, padx=5, pady=10, sticky=tk.S)         

  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 16 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=5, pady=10,sticky=tk.S)
        
        
      
################################################################################  

    def save_data(self):   

        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n')    
 
        self.np=len(self.f)
        
        WriteData2(self.np,self.f,self.W,output_file)

################################################################################  

    def calculate_data(self):   
        
        n=1+int(self.Lb1.curselection()[0])   
       
        V=float(self.mean_veloxr.get())
        
        L=float(self.scaler.get())     
       
        k=float(self.dragr.get())           
               
        num=1000
 
        f=zeros(num,'f')
        W=zeros(num,'f')
 
        for i in range(0,num):
 
            f[i]=(i+1)/10.
            fbar=f[i]*L/V
    
            a=L/V
            b=(2+fbar**2)**(5/6.)
    
            W[i]=4*k*V**2*a/b       
    


        self.f=f
        self.W=W
        
        
        self.button_sav.config(state='normal')
      
        plt.ion()
        plt.clf()
        plt.figure(1)
        plt.plot(f, W, linewidth=1.0,color='b')        # disregard error       
        plt.grid(True)

        if(n==1):                
            plt.ylabel('Wind Velocity (ft/sec)^2/Hz' )
            out1=('Davenport-King Spectrum  V=%g ft/sec, L=%g ft, k=%g' %(V,L,k)) 
        else:
            plt.ylabel('Wind Velocity (m/sec)^2/Hz' )
            out1=('Davenport-King Spectrum  V=%g m/sec, L=%g m, k=%g' %(V,L,k)) 
            
        
        plt.xlabel('Frequency (Hz)')
               
        plt.title(out1)            
        plt.xscale('log')
        plt.yscale('log')        
    
###############################################################################


    def unit_option(self,val):
        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):
            self.v_text.set('Mean Velocity (ft/sec) at 33 ft') 
            self.scale_text.set('Scale Length (ft)') 
            self.scaler.set('4000')  
        else:
            self.v_text.set('Mean Velocity (m/sec) at 10 m')  
            self.scale_text.set('Scale Length (m)')  
            self.scaler.set('1300')              
        
###############################################################################

def quit(root):
    root.destroy()
    
    