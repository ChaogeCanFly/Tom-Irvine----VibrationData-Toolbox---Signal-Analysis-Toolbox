##########################################################################
# program: vb_cross_correlation_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.2
# date: September 11, 2013
# description:  Calculate the cross_correlation of a time history.
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
    
class vb_cross_correlation:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.17))
        h = int(2.*(h*0.23))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_cross_correlation_gui.py ver 1.2  by Tom Irvine")    
    
        self.a1=[]
        self.b1=[]
        self.a2=[]
        self.b2=[]
        
        self.num1=0
        self.num2=0        
        
        self.dt1=0  
        self.dt2=0          
        
        self.cc=[]
        self.d=[]        
    
  
        self.n=0        


        crow=0

        self.hwtext1=tk.Label(top,text='Cross-correlation of Two Signals')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.W)

        crow+=1 

        self.hwtext2=tk.Label(top, \
            text='Each input file must have two columns:  time(sec) & amplitude')
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
        
        self.button_read = tk.Button(top, text="Read Input Files",command=self.read_data_two)
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
        
        self.button_sa = tk.Button(top, text="Cross-correlation", command=self.export_cross_correlation)
        self.button_sa.config( height = 2, width = 15,state = 'disabled' )
        self.button_sa.grid(row=crow, column=0,columnspan=2, pady=3, padx=1)          
        
################################################################################
        
    def calculation(self): 
        
        if((self.dt1-self.dt2)/self.dt2 < 0.001):


            if(self.num1<self.num2):
                self.a2=self.a2[0:self.num1]        
                self.b2=self.b2[0:self.num1]    

            if(self.num1>self.num2):
                self.a1=self.a1[0:self.num2]        
                self.b1=self.b1[0:self.num2]


            self.cc = correlate(self.b1,self.b2)

            self.n=len(self.cc)

            self.cc=2*self.cc/self.n

            dur=self.n*self.dt1/2;
            self.d=linspace( -dur, dur, self.n )
    
            print (min(self.d))
            print (max(self.d))

            idx = argmax(self.cc) 
            
            if(abs(self.d[idx])<self.dt1/10.):
                self.d[idx]=0.              
    
            print (" ")
            print (" Maximum:  Delay=%8.4g sec   Amp=%8.4g " %(self.d[idx],self.cc[idx]))

            title_string= "Cross-correlation  Max: Delay=%6.3g sec   Amp=%7.4g " %(self.d[idx],self.cc[idx])

            print (" ")
            print (" view plots")


            plt.close(3)
            plt.figure(3)

            plt.plot(self.d, self.cc, linewidth=1.0,color='b')        # disregard error
       
            plt.grid(True)
            plt.xlabel('Delay (sec)')
            plt.ylabel('Rxy')  
            plt.title(title_string)
    
            plt.draw()

            plt.show()        
    
        else:
    
            print (" ")
            print (" dt error ")                
        

        
        self.hwtextext_ex.config(state = 'normal')
        self.button_sa.config( state = 'normal' )        

################################################################################

    def export_cross_correlation(self):
        output_file_path = asksaveasfilename(parent=self.master,\
               title="Enter the cross_correlation filename: ")       
        output_file = output_file_path.rstrip('\n')
        WriteData2(self.n,self.d,self.cc,output_file) 
        
################################################################################        

    def read_data_two(self):            
            
        self.a1,self.b1,self.num1=read_two_columns_from_dialog('Select First Input File',self.master)
        
        self.a1=array(self.a1)
        self.b1=array(self.b1)        
        
        dur1=self.a1[self.num1-1]-self.a1[0]
        self.dt1=dur1/float(self.num1)
        
        self.sr1=1./self.dt1
        
        self.sr1,self.dt1=sample_rate_check(self.a1,self.b1,self.num1,self.sr1,self.dt1)
        
###
        
        self.a2,self.b2,self.num2=read_two_columns_from_dialog('Select Second Input File',self.master)
        
        self.a2=array(self.a2)
        self.b2=array(self.b2)        
        
        dur2=self.a2[self.num2-1]-self.a2[0]
        self.dt2=dur2/float(self.num2)
        
        self.sr2=1./self.dt2
        
        self.sr2,self.dt2=sample_rate_check(self.a2,self.b2,self.num2,self.sr2,self.dt2)        

###
        plt.clf()
        plt.figure(1)

        plt.plot(self.a1, self.b1, linewidth=1.0,color='b')        # disregard error
 
        
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('First Input Time History')
    
        plt.draw()

        plt.figure(2)

        plt.plot(self.a2, self.b2, linewidth=1.0,color='b')        # disregard error
 
        
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(self.y_string.get())  
        plt.title('Second Input Time History')
    
        plt.draw()

        print ("\n file 1: samples = %d " % self.num1)
        print ("\n file 2: samples = %d " % self.num2)        
        
        self.button_calculate.config(state = 'normal')    
        
        
################################################################################

def quit(root):
    root.destroy()        
        