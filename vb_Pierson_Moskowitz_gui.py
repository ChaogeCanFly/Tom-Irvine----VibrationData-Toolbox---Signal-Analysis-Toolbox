################################################################################
# program: vb_Pierson_Moskowitz_gui.py
# author: Tom Irvine
# version: 1.0
# date: January 26, 2015
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




class vb_Pierson_Moskowitz:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.19))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_Pierson_Moskowitz_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Pierson-Moskowitz Ocean Wave Height PSD')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text= \
                 'Select the wind speed (m/sec) at a height of 19.5 m above the sea surface')
        self.hwtext2.grid(row=crow, column=0, columnspan=4, pady=7,sticky=tk.W)
        
################################################################################

        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=13,width=4,exportselection=0)
        self.Lb1.insert(1, "10")
        self.Lb1.insert(2, "11")
        self.Lb1.insert(3, "12")
        self.Lb1.insert(4, "13")
        self.Lb1.insert(5, "14")
        self.Lb1.insert(6, "15")
        self.Lb1.insert(7, "16")
        self.Lb1.insert(8, "17")
        self.Lb1.insert(9, "18")
        self.Lb1.insert(10, "19")
        self.Lb1.insert(11, "20")
        self.Lb1.insert(12, "21")

        self.Lb1.grid(row=crow, column=0, padx=16, pady=4,sticky=tk.N)
        self.Lb1.select_set(0)         
                          
        self.button_calculate = tk.Button(top, text="Calculate",command=self.calculate_data)
        self.button_calculate.config( height = 2, width = 16 )
        self.button_calculate.grid(row=crow, column=1,columnspan=1, padx=5, pady=10,sticky=tk.S)       
        
################################################################################
      

        self.button_sav = tk.Button(top, text="Export PSD", command=self.save_data)
        self.button_sav.config( height = 2, width = 16,state = 'disabled' )
        self.button_sav.grid(row=crow, column=2,columnspan=1, padx=5, pady=10, sticky=tk.S)         

  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 16 )
        self.button_quit.grid(row=crow, column=3,columnspan=1, padx=5, pady=10,sticky=tk.S)
        
        
      
################################################################################  

    def save_data(self):   

        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n')    
 
        self.np=len(self.f)
        
        WriteData2(self.np,self.f,self.Sf,output_file)

################################################################################  

    def calculate_data(self):   
        
        n=1+int(self.Lb1.curselection()[0])   
       
        U=9+n

        g = 9.81
        alpha = 8.1e-03

        tpi=2*pi

        fm=(0.877*g/U)/tpi

        fmax=0.5

        m=200

        df = fmax/float(m)

        f=zeros(m,'f')

        Sf=zeros(m,'f')

        ms=0.

        for i in range(0,m):
            if( (i*df)<=fmax ):
                f[i]=(i+1)*df

                A=alpha*g**2/( (f[i]**5)*(tpi**4) )
                Sf[i]=A*exp(-(5/4.)*(fm/f[i])**4)
                ms=ms+Sf[i]*df
            else:
                break
            

        drms=sqrt(ms)

        print('\n Wind speed = %8.4g m/sec' %U)

        print('\n Overall level = %8.4g m RMS' %drms)

        print('\n Peak frequency = %8.4g Hz ' %fm)
       
        self.f=f
        self.Sf=Sf
  
        self.button_sav.config(state='normal')
      
        plt.ion()
        plt.clf()
        plt.figure(1)
        plt.plot(f, Sf, linewidth=1.0,color='b')        # disregard error       
        plt.grid(True)                
        plt.ylabel('Wave Spectral Density (m^2/Hz)')
        plt.xlabel('Frequency (Hz)')
        out1=(' Pierson-Moskowitz Spectrum  U = %g m/sec at 19.5 m ' %U)        
        plt.title(out1)        
        
        
################################################################################


def quit(root):
    root.destroy()