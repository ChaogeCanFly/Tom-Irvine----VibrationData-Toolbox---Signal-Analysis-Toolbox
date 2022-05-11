################################################################################
# program: vb_differentiate_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.2
# date: September 11, 2013
# description:  Differentiate a time history
#
################################################################################
# 
# Note:  for use within Spyder IDE, set: 
#    
# Run > Configuration > Interpreter >
#    
# Excecute in an external system terminal
#
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




import matplotlib.pyplot as plt

import numpy as np

from vb_utilities import WriteData2,sample_rate_check,\
                                                    read_two_columns_from_dialog



class vb_differentiate:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.32))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_differentiate_gui.py ver 1.2  by Tom Irvine")    
  
   
        crow=0

        self.hwtext1=tk.Label(top,text='Differentiate Time History')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow+=1 

        self.hwtext2=tk.Label(top, \
            text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=3,sticky=tk.W)

###############################################################################

        crow+=1 
        
        self.hwtext1t=tk.Label(top,text='Select Input Type')
        self.hwtext1t.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.W)

        crow+=1 
        
        self.Lb1 = tk.Listbox(top,height=3,exportselection=0)
        self.Lb1.insert(1, "Displacement")
        self.Lb1.insert(2, "Velocity")
        self.Lb1.insert(3, "Acceleration")        
        self.Lb1.grid(row=crow, column=0, columnspan=2, pady=4)
        self.Lb1.select_set(0)         

###############################################################################
  
        crow+=1 

        self.hwtext3=tk.Label(top,text='Enter Input Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, columnspan=2, pady=11,sticky=tk.E)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=11,sticky=tk.W)
        
################################################################################
  
        crow+=1 

        self.hwtext3b=tk.Label(top,text='Enter Output Time History Y-axis Label')
        self.hwtext3b.grid(row=crow, column=0, columnspan=2, pady=11,sticky=tk.E)

        self.dy_string=tk.StringVar()  
        self.dy_string.set('')  
        self.dy_string_entry=tk.Entry(top, width = 26,textvariable=self.dy_string)
        self.dy_string_entry.grid(row=crow, column=2,columnspan=3,padx=5, pady=11,sticky=tk.W)        

################################################################################

        crow+=1 
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.W)  


###############################################################################
  
        crow+=1 

        self.hwtext3s=tk.Label(top,text='Divide Output by Scale Factor?')
        self.hwtext3s.grid(row=crow, column=0, columnspan=2, pady=11)
        
        self.hwtext3sf=tk.Label(top,text='Scale Factor')
        self.hwtext3sf.grid(row=crow, column=2, columnspan=2, pady=11) 
        
###############################################################################        

        crow+=1 
        
        self.Lb2 = tk.Listbox(top,height=3,exportselection=0)
        self.Lb2.insert(1, "yes")
        self.Lb2.insert(2, "no")        
        self.Lb2.grid(row=crow, column=0, columnspan=2, pady=4,sticky=tk.N)
        self.Lb2.select_set(1) 
        self.Lb2.bind('<<ListboxSelect>>',self.set_scale)
        
        self.scale_string=tk.StringVar()  
        self.scale_string.set('1')  
        self.scale_string_entry=tk.Entry(top, width = 26,textvariable=self.scale_string)
        self.scale_string_entry.grid(row=crow, column=2,columnspan=1,padx=5, pady=4,sticky=tk.N)
        self.scale_string_entry.config(state = 'disabled')

################################################################################

        crow+=1 

        self.button_calculate = \
        tk.Button(top, text="Calculate", command=self.differentiate_calculation)

        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=2, pady=20) 
        
 
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=2, padx=10,pady=20)  

################################################################################
        
        crow+=1 

        self.button_differentiated = \
           tk.Button(top, text="Export Differentiated Time History", command=self.export_differentiated)
        self.button_differentiated.config( height = 2, width = 30,state = 'disabled' )
        self.button_differentiated.grid(row=crow, column=0,columnspan=2, pady=1, padx=1)        
        
################################################################################
        
    def set_scale(self,val):       
        sender=val.widget
        n= int(sender.curselection()[0])
        
        if(n==0):
            self.scale_string_entry.config(state = 'normal')
        else:    
            self.scale_string_entry.config(state = 'disabled')                          


    def export_differentiated(self):
        output_file_path = asksaveasfilename(parent=self.master,\
               title="Enter the output filename ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.num,self.a,self.v,output_file) 
        
################################################################################
        
    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
        self.dur=self.a[self.num-1]-self.a[0]
        self.dt=self.dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)
        
        plt.ion()
        plt.clf()

        self.plot_input(self)

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')  


    @classmethod         
    def plot_input(cls,self):

        plt.close(1)
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error   
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        
        itt=int(self.Lb1.curselection()[0])
        
        if(itt==0):
            plt.title('Displacement Time History')                         
        if(itt==1):
            plt.title('Velocity Time History')               
        if(itt==2):
            plt.title('Acceleration Time History')               
    
        plt.draw()


    def differentiate_calculation(self):

        ddt=12.*self.dt
    
        self.v=np.zeros(self.num,'f')

        self.v[0]=( -self.b[2]+4.*self.b[1]-3.*self.b[0] )/(2.*self.dt)
        self.v[1]=( -self.b[3]+4.*self.b[2]-3.*self.b[1] )/(2.*self.dt)

        for i in range (2,int(self.num-2)):
            self.v[i]=( -self.b[i+2] +8.*self.b[i+1] -8.*self.b[i-1] +self.b[i-2] ) / ddt
    
        self.v[self.num-2]=( self.b[self.num-2]-self.b[self.num-4] )/(2.*self.dt)
        self.v[self.num-1]=( self.b[self.num-2]-self.b[self.num-3] )/self.dt      

        iss=int(self.Lb1.curselection()[0]) 
        
        if(iss==0):
            scale=float(self.scale_string.get())
            self.v=self.v/scale
        
        self.plot_input(self)        
        
        plt.close(2)
        plt.figure(2)     
        plt.plot(self.a,self.v)
        plt.grid(True)
        
        itt=int(self.Lb1.curselection()[0])       
        
        if(itt==0):
            plt.title('Velocity Time History')                         
        if(itt==1):
            plt.title('Acceleration Time History')               
        if(itt==2):
            plt.title('Jerk Time History')  
        
        plt.ylabel(self.dy_string.get()) 
        plt.xlabel(' Time (sec) ')
        plt.grid(True, which="both")
        plt.draw()  
        
        self.button_differentiated.config(state = 'normal')
   
            
###############################################################################

def quit(root):
    root.destroy()