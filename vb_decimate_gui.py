################################################################################
# program: vb_decimate_gui.py
# author: Tom Irvine
# version: 1.0
# date: January 12, 2015
# description:  
################################################################################

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
    
    
from vb_utilities import WriteData2

import matplotlib.pyplot as plt

from numpy import ceil,floor


from vb_utilities import read_two_columns_from_dialog,signal_stats

from vb_utilities import BUTTERWORTH


class vb_decimate:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.22))
        h = int(2.*(h*0.28))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_decimate_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Decimate a signal.')
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
        self.y_string_entry.grid(row=crow, column=2,columnspan=2,padx=5, pady=3)    

################################################################################ 

        crow=crow+1

        self.hwtext4=tk.Label(top,text='Downsampling Factor')
        self.hwtext4.grid(row=crow, column=0, columnspan=1, pady=5,sticky=tk.S)        

        self.hwtext5=tk.Label(top,text='Apply Lowpass Filter Prior to Downsampling')
        self.hwtext5.grid(row=crow, column=1, columnspan=2, padx=6,pady=5,sticky=tk.S)     
                       
        self.hwtext6=tk.Label(top,text='Lowpass Filter Frequency (Hz)')
        self.hwtext6.grid(row=crow, column=3, columnspan=2, padx=6,pady=5,sticky=tk.S)                 

              
        crow=crow+1
        
        myframe=tk.Frame(top)
        myframe.grid(row=crow, column=0,padx=3)
        scrollbar = tk.Scrollbar(myframe) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Lb3 = tk.Listbox(myframe, width=5, yscrollcommand=scrollbar.set) 
        self.Lb3.pack()
        scrollbar.config(command=self.Lb3.yview)        
        
        
        self.Lb3.insert(1, "2")  
        self.Lb3.insert(2, "3")          
        self.Lb3.insert(3, "4")  
        self.Lb3.insert(4, "5")          
        self.Lb3.insert(5, "6")  
        self.Lb3.insert(6, "7")          
        self.Lb3.insert(7, "8")  
        self.Lb3.insert(8, "9")             
        self.Lb3.insert(9, "10")          
        self.Lb3.insert(10, "11")  
        self.Lb3.insert(11, "12")         
        self.Lb3.insert(12, "13")  
        self.Lb3.insert(13, "14")         
        self.Lb3.insert(14, "15")  
        self.Lb3.insert(15, "16")          
        self.Lb3.insert(16, "17")  
        self.Lb3.insert(17, "18")         
        self.Lb3.insert(18, "19")  
        self.Lb3.insert(19, "20") 
        
        self.Lb3.select_set(0)        
      
      
        self.Lb4 = tk.Listbox(top,height=2,width=6,exportselection=0)
        self.Lb4.insert(1, "Yes")  
        self.Lb4.insert(2, "No")          
        
        self.Lb4.grid(row=crow, column=1, columnspan=1, padx=10, pady=4,sticky=tk.NE)
        self.Lb4.select_set(0)
              

        self.lpfr=tk.StringVar()  
        self.lpfr.set(' ')  
        self.lpf_entry=tk.Entry(top, width = 9,textvariable=self.lpfr)
        self.lpf_entry.grid(row=crow, column=3, columnspan=2,sticky=tk.N)              
      
              
        
################################################################################

        crow=crow+1         

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, padx=2, pady=10)   
        
        self.button_extract = tk.Button(top, text="Decimate",command=self.decimate)
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


    def decimate(self):   
        
        ndec=2+int(self.Lb3.curselection()[0])   
        
        nf=1+int(self.Lb4.curselection()[0])          

        self.num=len(self.a)       

###############################################################################

        t=self.a
        y=self.b

        if(nf==1):
            self.fc=float(self.lpfr.get())
            
            if(self.fc>=0.5*self.sr):
                strer='cutoff frequency must be < Nyquist frequency'
                tkMessageBox.showerror('Error',strer)  
                return
        
            f=self.fc
            fh=f
            fl=f
            
            iphase=1 # refilter for phase correction
            
            
            dt=self.dt
            l=6      # order
            iband =1 # lowpass
        
            y=BUTTERWORTH(l,f,fh,fl,dt,iband,iphase,y).Butterworth_filter_main()        



            print (" ")   
            print ("Filtered signal statistics")           
        
            sr,dt,ave,sd,rms,skewness,kurtosis,dur=signal_stats(t, y,self.num)        
        

###############################################################################
        
        self.td=t[0:self.num:ndec]
        self.yd=y[0:self.num:ndec]       
        
        self.button_save.config(state='normal' )        
        
        
        plt.ion()
        plt.clf()      
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel(self.xstr)
        plt.ylabel(self.ystr)  
        plt.title(self.tstr)
    
        plt.draw()        
        
        
        plt.figure(2)

        plt.plot(self.td, self.yd, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel(self.xstr)
        plt.ylabel(self.ystr)  
        
        plt.title("Decimated: "+self.tstr)
    
        plt.draw()
  
        self.button_extract.config( height = 2, width = 15, state='normal' )        
             
   
################################################################################        
        

    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
                
        sr,dt,mean,sd,rms,skew,kurtosis,dur=signal_stats(self.a,self.b,self.num)
        
        self.sr=sr
        self.dt=dt

        print("\n") 
        print("      sr=%8.4g samples/sec" %sr)
        print("    mean=%8.4g" %mean)
        print(" std dev=%8.4g" %sd) 
        print("     rms=%8.4g" %rms)
        
        print("\n %d points \n" %self.num)   
        
        self.xstr=self.x_string.get()
        self.ystr=self.y_string.get()
        self.tstr=self.t_string.get()

        plt.ion()
        plt.clf()      
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel(self.xstr)
        plt.ylabel(self.ystr)  
        plt.title(self.tstr)
    
        plt.draw()
  
        self.button_extract.config( height = 2, width = 15, state='normal' )
        
###############################################################################
                
    def save_data(self):   

        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n')    
 
        self.np=len(self.td)
        
        WriteData2(self.np,self.td,self.yd,output_file)
        
        
###############################################################################        


def quit(root):
    root.destroy()