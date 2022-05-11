################################################################################
# program: vb_ft_mp_plot_gui.py
# author: Tom Irvine
# version: 1.2
# date: December 11, 2014
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
        

import matplotlib.pyplot as plt

from numpy import sin,cos,pi,zeros

from matplotlib.gridspec import GridSpec

from vb_utilities import read_three_columns_from_dialog


class vb_ft_mp_plot:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_ft_mp_plot_gui.py ver 1.2  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Plot Fourier Transform')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text= \
                 'The input file must have three columns:  freq(Hz) & magnitude & phase')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)
        
################################################################################
        
        crow=crow+1

        self.hwtext5=tk.Label(top,text='Select Input Phase Unit')
        self.hwtext5.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.W)

        crow=crow+1
        
        self.Lbu = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbu.insert(1, "rad")
        self.Lbu.insert(2, "deg")
        self.Lbu.grid(row=crow, column=0, columnspan=1, pady=4, padx=10)
        self.Lbu.select_set(0) 

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
        
        self.hwtext3=tk.Label(top,text='Enter X-axis Label ')
        self.hwtext3.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W) 
        
        crow=crow+1              
        
        self.x_string=tk.StringVar()  
        self.x_string.set('Frequency (Hz)')  
        self.x_string_entry=tk.Entry(top, width = 26,textvariable=self.x_string)
        self.x_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)                          
                          
################################################################################
                          
        crow=crow+1

        self.hwtext3=tk.Label(top,text='Enter Y-axis Label ')
        self.hwtext3.grid(row=crow, column=0, columnspan=3, pady=7,sticky=tk.W)                          

        crow=crow+1
        
        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=0,columnspan=3,padx=5, pady=3,sticky=tk.W)
           

################################################################################

        crow+=1 

        self.hwtextf1=tk.Label(top,text='Min Freq (Hz)')
        self.hwtextf1.grid(row=crow, column=0,padx=5, pady=8)

        self.hwtextf2=tk.Label(top,text='Max Freq (Hz)')
        self.hwtextf2.grid(row=crow, column=1,padx=5, pady=8)

################################################################################

        crow+=1 

        self.f1r=tk.StringVar()  
        self.f1r.set('')  
        self.f1_entry=tk.Entry(top, width = 8,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=0,padx=5, pady=1)

        self.f2r=tk.StringVar()  
        self.f2r.set('')  
        self.f2_entry=tk.Entry(top, width = 8,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=1,padx=5, pady=1)

        
################################################################################

        crow=crow+1         

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10)   
        
        self.button_replot = tk.Button(top, text="Replot",command=self.replot)
        self.button_replot.config( height = 2, width = 15, state='disabled')  
        self.button_replot.grid(row=crow, column=1,columnspan=1, pady=10)   
                
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=10,pady=20)
      
################################################################################  

    def read_data(self):            
        
        self.ff,self.zz,self.ph,self.num=read_three_columns_from_dialog('Select Input File',self.master)
                
        print("\n %d points \n" %self.num)  
        
        unit=1+int(self.Lbu.curselection()[0])
        
        self.zi=zeros(self.num,'f')
        self.zr=zeros(self.num,'f')
        
        if(unit==1):
            for i in range(0,self.num):
                self.ph[i]=self.ph[i]*(180./pi)
      
        for i in range(0,self.num):
            arg=self.ph[i]*(pi/180)
            self.zi[i]=self.zz[i]*sin(arg)               
            self.zr[i]=self.zz[i]*cos(arg)        
      
        self.button_replot.config( state='normal')     
    
        self.plotd(self)   
        
###############################################################################

    def replot(self): 
        self.plotd(self)       
        
        
    @classmethod    
    def plotd(cls,self):    

        y1=-180
        y2= 180
        
####         
        string1=self.f1r.get()

        if len(string1) == 0:
            tkMessageBox.showwarning('Warning','Enter Starting Frequency ',parent=self.button_read)
            return
        else:
            x1=float(string1);
        
        
        string2=self.f2r.get()        
        
        if len(string2)==0:
            tkMessageBox.showwarning('Warning','Enter End Frequency ',parent=self.button_read)            
            return   
        else:
            x2=float(string2)
        
        
        ylab=self.y_string.get() 

        if len(ylab) == 0:
            tkMessageBox.showwarning('Warning','Enter Y-axis Label ',parent=self.button_read)            
            return    
            
        tt=self.t_string.get()     

####  
        plt.ion()
        plt.figure(1)
        
        gs1 = GridSpec(3, 1)
                                  
        ax1=plt.subplot(gs1[:-2, :])   
        plt.plot(self.ff,self.ph)
        
        plt.title(tt)
        plt.grid(True)
        plt.ylabel(' Phase (deg) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.ylim([y1,y2])
        plt.setp( ax1.get_xticklabels(), visible=False)
        plt.yticks([-180,-90,0,90,180])
        plt.draw()      

        plt.subplot(gs1[-2:0, :])
        plt.plot(self.ff,self.zz)
        
        plt.grid(True)
        plt.ylabel(ylab) 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.draw()            
        
####  
        
        plt.figure(2)     
        plt.plot(self.ff,self.zz)
        plt.grid(True)
        plt.title(tt)
        plt.ylabel(self.y_string.get()) 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")
        plt.xlim([x1,x2])
        plt.draw()
          
####  
  
        plt.figure(3)  
        
        plt.subplot(2,1,1)
        plt.plot(self.ff,self.zi)  
        plt.title(tt)
        plt.ylabel('Imag')         
        plt.setp( ax1.get_xticklabels(), visible=False) 
        plt.grid(True, which="both")        
        plt.xlim([x1,x2])
        plt.draw()

        
        plt.subplot(2,1,2) 
        plt.plot(self.ff,self.zr)        
        plt.ylabel('Real') 
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(True, which="both")        
        plt.xlim([x1,x2])
        plt.draw()        
  
################################################################################


def quit(root):
    root.destroy()