################################################################################
# program: vb_power_trans_gui.py
# author: Tom Irvine
# version: 1.1
# date: September 27, 2014
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

from matplotlib.ticker import ScalarFormatter

from numpy import array,zeros



from vb_utilities import read_two_columns_from_dialog
from vb_utilities import WriteData2


class vb_power_trans:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window

        self.topp=top
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.30))
        h = int(2.*(h*0.26))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_power_trans_gui.py ver 1.1  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Each input file must have two columns:  freq(Hz) & PSD (unit^2/Hz) ')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow+=1        

        self.hwtext15=tk.Label(top,text='X-axis Label')
        self.hwtext15.grid(row=crow, column=0, columnspan=1, padx=10, pady=8) 

        self.hwtext17=tk.Label(top,text='Y-axis Label')
        self.hwtext17.grid(row=crow, column=1, columnspan=1, padx=10, pady=8) 
 
        self.hwtext41=tk.Label(top,text='Title')
        self.hwtext41.grid(row=crow, column=2, columnspan=1, padx=10, pady=8) 
        
        
        crow+=1 

        self.xlabel_string=tk.StringVar()  
        self.xlabel_string.set('Frequency (Hz)')  
        self.xlabel_string_entry=tk.Entry(top, width = 26,textvariable=self.xlabel_string)
        self.xlabel_string_entry.grid(row=crow, column=0,columnspan=1,padx=10, pady=5)         
        
        self.ylabel_string=tk.StringVar()  
        self.ylabel_string.set('Trans (G^2/G^2)')  
        self.ylabel_string_entry=tk.Entry(top, width = 26,textvariable=self.ylabel_string)
        self.ylabel_string_entry.grid(row=crow, column=1,columnspan=1,padx=10, pady=5)         
        
        self.t_string=tk.StringVar()  
        self.t_string.set('Power Transmissibility')  
        self.t_string_entry=tk.Entry(top, width = 26,textvariable=self.t_string)
        self.t_string_entry.grid(row=crow, column=2,columnspan=1,padx=10, pady=5)
        

################################################################################
        
        crow+=1         
        
        self.hwtext2=tk.Label(top,text='X-axis Limits ')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=7)       
            
        self.hwtext3=tk.Label(top,text='Y-axis Limits ')
        self.hwtext3.grid(row=crow, column=1, columnspan=1, pady=7) 
                    
        crow+=1 

        self.Lbxlim = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbxlim.insert(1, "Automatic")
        self.Lbxlim.insert(2, "Manual")       
        self.Lbxlim.grid(row=crow, column=0, padx=10, pady=1,sticky=tk.N)
        self.Lbxlim.select_set(0)        
        
        self.Lbylim = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbylim.insert(1, "Automatic")
        self.Lbylim.insert(2, "Manual")       
        self.Lbylim.grid(row=crow, column=1, padx=10, pady=1,sticky=tk.N)
        self.Lbylim.select_set(0)        
        
                
        crow+=1 
 
        
        self.hwtext91=tk.Label(top,text='Xmin')
        self.hwtext91.grid(row=crow, column=0, columnspan=1, pady=3,sticky=tk.S)  
        
        self.hwtext97=tk.Label(top,text='Ymin')
        self.hwtext97.grid(row=crow, column=1, columnspan=1, pady=3,sticky=tk.S)              
                

        crow+=1 
  
        self.xmin_string=tk.StringVar()  
        self.xmin_string.set('')  
        self.xmin_string_entry=tk.Entry(top, width = 12,textvariable=self.xmin_string)
        self.xmin_string_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=1,sticky=tk.N)  
        self.xmin_string_entry.config(state = 'disabled')   
     
        self.ymin_string=tk.StringVar()  
        self.ymin_string.set('')  
        self.ymin_string_entry=tk.Entry(top, width = 12,textvariable=self.ymin_string)
        self.ymin_string_entry.grid(row=crow, column=1,columnspan=1,padx=5, pady=1,sticky=tk.N)          
        self.ymin_string_entry.config(state = 'disabled')           
        
               
        
        crow=crow+1

        self.hwtext92=tk.Label(top,text='Xmax')
        self.hwtext92.grid(row=crow, column=0, columnspan=1, pady=0,sticky=tk.S)             

        self.hwtext99=tk.Label(top,text='Ymax')
        self.hwtext99.grid(row=crow, column=1, columnspan=1, pady=0,sticky=tk.S)      
         
        crow=crow+1
         
        self.xmax_string=tk.StringVar()  
        self.xmax_string.set('')  
        self.xmax_string_entry=tk.Entry(top, width = 12,textvariable=self.xmax_string)
        self.xmax_string_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=1,sticky=tk.N)
        self.xmax_string_entry.config(state = 'disabled')             
          
        self.ymax_string=tk.StringVar()  
        self.ymax_string.set('')  
        self.ymax_string_entry=tk.Entry(top, width = 12,textvariable=self.ymax_string)
        self.ymax_string_entry.grid(row=crow, column=1,columnspan=1,padx=5, pady=1,sticky=tk.N)          
        self.ymax_string_entry.config(state = 'disabled')             
          
################################################################################

        crow=crow+1    

        self.Lbxa = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbxa.insert(1, "Linear")
        self.Lbxa.insert(2, "Log")       
        self.Lbxa.grid(row=crow, column=0, padx=10, pady=12,sticky=tk.N)
        self.Lbxa.select_set(1) 
        
        self.Lbya = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbya.insert(1, "Linear")
        self.Lbya.insert(2, "Log")       
        self.Lbya.grid(row=crow, column=1, padx=10, pady=12,sticky=tk.N)
        self.Lbya.select_set(1)  


###############################################################################

        crow=crow+1         

        self.button_read1 = tk.Button(top, text="Read Response PSD File",command=self.read_data1)
        self.button_read1.config( height = 2, width = 25 )
        self.button_read1.grid(row=crow, column=0,columnspan=1,padx=4, pady=10,sticky=tk.W)   
        
        self.button_read2 = tk.Button(top, text="Read Input PSD File",command=self.read_data2)
        self.button_read2.config( height = 2, width = 25 )
        self.button_read2.grid(row=crow, column=1,columnspan=1,padx=4, pady=10,sticky=tk.W) 

        crow=crow+1       
        
        self.button_plot12 = tk.Button(top, text="Plot Transmissibility",command=self.plot12)
        self.button_plot12.config( height = 2, width = 25 )
        self.button_plot12.grid(row=crow, column=0,columnspan=1,padx=1, pady=10,sticky=tk.W)           
  
        
        self.button_ex = tk.Button(top, text="Export Data", command=self.export)
        self.button_ex.config( height = 2, width = 18,state = 'disabled' )
        self.button_ex.grid(row=crow, column=1,columnspan=1, padx=10,pady=3)   
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 18 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=1,pady=10)

        self.Lbxlim.bind("<<ListboxSelect>>", self.callback_limits)    
        self.Lbylim.bind("<<ListboxSelect>>", self.callback_limits)   
         
################################################################################  

    def callback_limits(self,event):  

        nxlim=1+int(self.Lbxlim.curselection()[0])   
        nylim=1+int(self.Lbylim.curselection()[0])


        if(nxlim==1):
            self.xmin_string_entry.config(state = 'disabled')   
            self.xmax_string_entry.config(state = 'disabled')
            self.xmin_string.set('') 
            self.xmax_string.set('') 
        else:
            self.xmin_string_entry.config(state = 'normal')    
            self.xmax_string_entry.config(state = 'normal')    
  
  
        if(nylim==1):
            self.ymin_string_entry.config(state = 'disabled') 
            self.ymax_string_entry.config(state = 'disabled')
            self.ymin_string.set('') 
            self.ymax_string.set('')              
        else:
            self.ymin_string_entry.config(state = 'normal')
            self.ymax_string_entry.config(state = 'normal')            

  


    def read_data1(self):            
            
        self.a1,self.b1,self.num1=read_two_columns_from_dialog('Select Response PSD File',self.master)
        
        if(self.num1>=1):
            tl2=self.topp
            tkMessageBox.showinfo(" ", "Data File 1 Read",parent=tl2)
        
        
    def read_data2(self):            
            
        self.a2,self.b2,self.num2=read_two_columns_from_dialog('Select Input PSD File',self.master)

        if(self.num2>=1):
            tl2=self.topp
            tkMessageBox.showinfo(" ", "Data File 2 Read",parent=tl2)
    
###############################################################################
    
    
    def export(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n')    
 
        num=len(self.ft) 
        WriteData2(num,self.ft,self.pt,output_file)    
        


###############################################################################    
        
    def plot12(self):          
        
        num1=len(self.a1) 
        self.b1
        num2=len(self.a2)
        self.b2        
        
        num=num1
        if(num>num2):
            num=num2
            
            
        if(num1==0): 
            tkMessageBox.showwarning("Warning","arrays have zero length",parent=self.button_read1)            


        nxlim=1+int(self.Lbxlim.curselection()[0])   
        nylim=1+int(self.Lbylim.curselection()[0])  
        
        
        nxa=1+int(self.Lbxa.curselection()[0])           
        nya=1+int(self.Lbya.curselection()[0])               
        
        self.ft=[]
        self.pt=[]
        
        fmin=0
        fmax=1.0e+20
        
        if(nxlim==2):
            
            fmin=float(self.xmin_string.get())
            fmax=float(self.xmax_string.get())
            x1=fmin
            x2=fmax
            
        
        for i in range(0,num):
            
            if(self.a1[i]>=1.0e-08 and self.a1[i]<=1.0e+08):
                
                diffr=abs( (self.a1[i]-self.a2[i])/self.a1[i])                
                
                if(diffr>0.02): 
                    tkMessageBox.showwarning("Warning","frequency sync error",parent=self.button_plot12)                        

                r=self.b1[i]/self.b2[i]
                
                if(r>=1.0e-08 and r<=1.0e+12):

                    self.ft.append(self.a1[i])            
                    self.pt.append(r)
        


        nfn=1
        plt.ion()        
        plt.close(nfn)
#        plt.gca().set_autoscale_on(False)
        fig2=plt.figure(nfn)        
        

        line2,=plt.plot(self.ft, self.pt)

#        plt.plot(self.ft, self.pt)


        plt.title(self.t_string.get())       
        plt.xlabel(self.xlabel_string.get())     
        plt.ylabel(self.ylabel_string.get()) 
        
        plt.grid(True)
            
        if(nxa==2):
            plt.xscale('log')              

        if(nya==2):
            plt.yscale('log')    
            

        plt.grid(True)     

                    
          
        if(nxlim==2):
                  
            if(x1==20 and x2==2000):
                
                ax=plt.gca().xaxis
                ax.set_major_formatter(ScalarFormatter())
                plt.ticklabel_format(style='plain', axis='x', scilimits=(x1,x2))    
              
                extraticks=[20,2000]
                plt.xticks(list(plt.xticks()[0]) + extraticks)              
              
                plt.xlim([x1,x2])
            
        if(nylim==2):
            y1=float(self.ymin_string.get())
            y2=float(self.ymax_string.get())            
            plt.ylim([y1,y2])
            


        fig2.canvas.mpl_connect('pick_event', DataCursor(plt.gca()))
        line2.set_picker(3) # Tolerance in points

        self.button_ex.config( height = 2, width = 18,state = 'normal' )

################################################################################

def quit(root):
    root.destroy()

################################################################################

class DataCursor(object):
    text_template = 'x: %0.2f\ny: %8.4g'
    x, y = 0.0, 0.0
    xoffset, yoffset = -20, 20
    text_template = 'x: %0.2f\ny: %8.4g'

    def __init__(self, ax):
        self.ax = ax
        self.annotation = ax.annotate(self.text_template, 
                xy=(self.x, self.y), xytext=(self.xoffset, self.yoffset), 
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                )
        self.annotation.set_visible(False)

    def __call__(self, event):
        self.event = event
        2# xdata, ydata = event.artist.get_data()
        # self.x, self.y = xdata[event.ind], ydata[event.ind]
        self.x, self.y = event.mouseevent.xdata, event.mouseevent.ydata
        if self.x is not None:
            self.annotation.xy = self.x, self.y
            self.annotation.set_text(self.text_template % (self.x, self.y))
            self.annotation.set_visible(True)
            event.canvas.draw()
                