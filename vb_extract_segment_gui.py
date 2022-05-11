################################################################################
# program: vb_extract_segment_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 17, 2014
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

from numpy import ceil,floor


from vb_utilities import read_two_columns_from_dialog,signal_stats


class vb_extract_segment:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_extract_segment_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Plot Time History Signal & Extract Segment')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text= \
                 'The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)
        
################################################################################

        crow=crow+1

        self.hwtext4=tk.Label(top,text='Enter Plot Title ')
        self.hwtext4.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W)
                          
        crow=crow+1
        
        self.t_string=tk.StringVar()  
        self.t_string.set('')  
        self.t_string_entry=tk.Entry(top, width = 26,textvariable=self.t_string)
        self.t_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)         

################################################################################

        crow=crow+1

        self.hwtext4=tk.Label(top,text='Enter Time History X-axis Label ')
        self.hwtext4.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.S)
        
        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label ')
        self.hwtext3.grid(row=crow, column=2, columnspan=2, pady=7,sticky=tk.S)          
                          
        crow=crow+1
        
        self.x_string=tk.StringVar()  
        self.x_string.set('Time (sec)')  
        self.x_string_entry=tk.Entry(top, width = 26,textvariable=self.x_string)
        self.x_string_entry.grid(row=crow, column=0,columnspan=2,padx=5, pady=3)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=2,padx=5, pady=3,)                          
                          
        crow=crow+1
        
        self.hwtext41=tk.Label(top,text='Start Time (sec) ')
        self.hwtext41.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.W)    
    
        self.hwtext42=tk.Label(top,text='End Time (sec) ')
        self.hwtext42.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.W)  
        
################################################################################

        crow=crow+1       

        self.tmin_string=tk.StringVar()  
        self.tmin_string.set('')  
        self.tmin_string_entry=tk.Entry(top, width = 12,textvariable=self.tmin_string)
        self.tmin_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)          
        
        
        self.tmax_string=tk.StringVar()  
        self.tmax_string.set('')  
        self.tmax_string_entry=tk.Entry(top, width = 12,textvariable=self.tmax_string)
        self.tmax_string_entry.grid(row=crow, column=1,columnspan=3,padx=5, pady=3,sticky=tk.W)          
        
################################################################################

        crow=crow+1         

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, padx=2, pady=10)   
        
        self.button_extract = tk.Button(top, text="Extract",command=self.extract_data)
        self.button_extract.config( height = 2, width = 15, state='disabled' )
        self.button_extract.grid(row=crow, column=1,columnspan=1, padx=2, pady=10)   
  
        self.button_save = tk.Button(top, text="Save",command=self.save_data)
        self.button_save.config( height = 2, width = 15, state='disabled' )
        self.button_save.grid(row=crow, column=2,columnspan=1, padx=2, pady=10)     
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=3,columnspan=1, padx=2,pady=20)
      
################################################################################  

    def save_data(self):   

        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n')    
 
        self.np=len(self.c)
        
        WriteData2(self.np,self.c,self.d,output_file)


    def extract_data(self):   
        
        tmin=float(self.tmin_string.get())
        tmax=float(self.tmax_string.get())
        
        dur=self.a[self.num-1]-self.a[0]
 
        n1=int(ceil(self.num*(tmin-self.a[0])/dur))
        n2=int(floor(self.num*(tmax-self.a[0])/dur))

        if(n1<0):
            n1=0
            
        if(n2>self.num-1):
            n2=self.num-1
 
        self.c=self.a[n1:n2]
        self.d=self.b[n1:n2]
        
        
        
        plt.close(2)
        plt.figure(2)

        plt.plot(self.c, self.d, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel(self.x_string.get())
        plt.ylabel(self.y_string.get())  
        plt.title(self.t_string.get())
    
        plt.draw()        
        
        self.button_save.config( height = 2, width = 15, state='normal' )
        
        

    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
                
        sr,dt,mean,sd,rms,skew,kurtosis,dur=signal_stats(self.a,self.b,self.num)

        print("\n") 
        print("      sr=%8.4g samples/sec" %sr)
        print("    mean=%8.4g" %mean)
        print(" std dev=%8.4g" %sd) 
        print("     rms=%8.4g" %rms)
        
        print("\n %d points \n" %self.num)        
      
        plt.close(1)
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel(self.x_string.get())
        plt.ylabel(self.y_string.get())  
        plt.title(self.t_string.get())
    
        plt.draw()
  
        self.button_extract.config( height = 2, width = 15, state='normal' )
        
################################################################################


def quit(root):
    root.destroy()