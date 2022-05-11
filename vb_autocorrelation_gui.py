##########################################################################
# program: vb_autocorrelation_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.3
# date: September 11, 2013
# description:  Calculate the autocorrelation of a time history.
#               The file must have two columns: time(sec) & amplitude.
##########################################################################

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

    

from vb_utilities import read_two_columns_from_dialog,sample_rate_check,WriteData2  


from numpy import linspace,argmax,array

from scipy.signal import correlate

import matplotlib.pyplot as plt

from matplotlib import interactive
interactive(True)
    
########################################################################
    
class vb_autocorrelation:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.16))
        h = int(2.*(h*0.22))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_autocorrelation_gui.py ver 1.3  by Tom Irvine")    
    
        self.a=[]
        self.b=[]
        self.ac=[]
        self.d=[]        
        self.num=0    
        self.dt=0    
        self.n=0        


        crow=0

        self.hwtext1=tk.Label(top,text='Autocorrelation')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.W)

        crow+=1 

        self.hwtext2=tk.Label(top, \
            text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=3,sticky=tk.W)
        

################################################################################
  
        crow+=1 

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, columnspan=2, pady=11,sticky=tk.E)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=11,sticky=tk.W)

################################################################################

        crow+=1 
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W)     

################################################################################

        crow+=1 

        self.button_calculate = \
                     tk.Button(top, text="Calculate", command=self.calculation)

        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=2, pady=20) 
        
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=2, padx=10,pady=20)
        
        crow=crow+1        
        
        self.hwtextext_ex=tk.Label(top,text='Export Data')
        self.hwtextext_ex.grid(row=crow, column=0,pady=10)  
        self.hwtextext_ex.config(state = 'disabled')
        
        crow=crow+1   
        
        self.button_sa = tk.Button(top, text="Autocorrelation", command=self.export_autocorrelation)
        self.button_sa.config( height = 2, width = 15,state = 'disabled' )
        self.button_sa.grid(row=crow, column=0,columnspan=2, pady=3, padx=1)          
        
################################################################################
        
    def calculation(self):  

        self.ac = correlate(self.b,self.b)

        self.n=len(self.ac)

        self.ac=2*self.ac/self.n

        dur=self.n*self.dt/2;
        self.d=linspace( -dur, dur, self.n )

        idx = argmax(self.ac) 
        
        if(abs(self.d[idx])<self.dt/10.):
            self.d[idx]=0.            
    
        print (" ")
        print (" Maximum:  Delay=%8.4g sec   Amp=%8.4g " %(self.d[idx],self.ac[idx]))

        title_string= "Autocorrelation  Max: Delay=%6.3g sec   Amp=%7.4g " %(self.d[idx],self.ac[idx])

        print (" ")
        print (" view plots")


        plt.close(2)
        plt.figure(2)

        plt.plot(self.d, self.ac, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Delay (sec)')
        plt.ylabel('Rxx')  
        plt.title(title_string)
    
        plt.draw()
        
        self.hwtextext_ex.config(state = 'normal')
        self.button_sa.config( state = 'normal' )        

################################################################################

    def export_autocorrelation(self):
        output_file_path = asksaveasfilename(parent=self.master,\
               title="Enter the autocorrelation filename: ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.n,self.d,self.ac,output_file) 
        
################################################################################        

    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        self.a=array(self.a)
        self.b=array(self.b)        
        
        dur=self.a[self.num-1]-self.a[0]
        self.dt=dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)
        

        plt.clf()
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
 
        
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Input Time History')
    
        plt.draw()
        plt.show()


        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')    
        
        
################################################################################

def quit(root):
    root.destroy()        
        