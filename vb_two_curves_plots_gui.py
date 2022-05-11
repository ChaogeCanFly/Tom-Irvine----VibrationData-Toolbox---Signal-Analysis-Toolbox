################################################################################
# program: vb_two_curves_plots_gui.py
# author: Tom Irvine
# version: 1.3
# date: September 27, 2014
# description:  
################################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    import tkMessageBox
      
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    import tkinter.messagebox as tkMessageBox       

import matplotlib.pyplot as plt

import numpy as np

from matplotlib.ticker import ScalarFormatter    


from vb_utilities import read_two_columns_from_dialog


class vb_two_curves_plots:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window

        self.topp=top
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.28))
        h = int(2.*(h*0.34))
        self.master.geometry("%dx%d+0+0" % (w, h))



        self.master.title("vb_two_curves_plots_gui.py ver 1.3  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Plot One or Two Curves. Each input file must have two columns:  time(sec) & amplitude ')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        
################################################################################
        
        crow+=1 

        self.hwtext4=tk.Label(top,text='Curve 1 Legend Title')
        self.hwtext4.grid(row=crow, column=0,padx=1,columnspan=1, pady=8)        

        self.hwtext15=tk.Label(top,text='X-axis Label')
        self.hwtext15.grid(row=crow, column=1, columnspan=1, padx=10, pady=8) 

        self.hwtext17=tk.Label(top,text='Y-axis Label')
        self.hwtext17.grid(row=crow, column=2, columnspan=1, padx=10, pady=8) 
 
        self.hwtext41=tk.Label(top,text='Title')
        self.hwtext41.grid(row=crow, column=3, columnspan=1, padx=10, pady=8) 
        
        
        crow+=1 
        
        self.t1_string=tk.StringVar()  
        self.t1_string.set('')  
        self.t1_string_entry=tk.Entry(top, width = 26,textvariable=self.t1_string)
        self.t1_string_entry.grid(row=crow, column=0,columnspan=1,padx=1, pady=5)        

        self.xlabel_string=tk.StringVar()  
        self.xlabel_string.set('')  
        self.xlabel_string_entry=tk.Entry(top, width = 26,textvariable=self.xlabel_string)
        self.xlabel_string_entry.grid(row=crow, column=1,columnspan=1,padx=10, pady=5)         
        
        self.ylabel_string=tk.StringVar()  
        self.ylabel_string.set('')  
        self.ylabel_string_entry=tk.Entry(top, width = 26,textvariable=self.ylabel_string)
        self.ylabel_string_entry.grid(row=crow, column=2,columnspan=1,padx=10, pady=5)         
        
        self.t_string=tk.StringVar()  
        self.t_string.set('')  
        self.t_string_entry=tk.Entry(top, width = 26,textvariable=self.t_string)
        self.t_string_entry.grid(row=crow, column=3,columnspan=1,padx=10, pady=5)

        
        crow+=1 

        self.hwtext6=tk.Label(top,text='Curve 1 Color')
        self.hwtext6.grid(row=crow, column=0, columnspan=1, pady=8,padx=1) 

        self.hwtext10=tk.Label(top,text='X-axis type')
        self.hwtext10.grid(row=crow, column=1, columnspan=1, padx=10, pady=8) 
 
        self.hwtext20=tk.Label(top,text='Y-axis type')
        self.hwtext20.grid(row=crow, column=2, columnspan=1, padx=10, pady=8) 

        self.hwtext51=tk.Label(top,text='Figure No.')
        self.hwtext51.grid(row=crow, column=3, columnspan=1, padx=1, pady=8,sticky=tk.E) 
        
        crow+=1 
         
        self.Lbc1 = tk.Listbox(top,height=4,width=10,exportselection=0)
        self.Lbc1.insert(1, "Black")
        self.Lbc1.insert(2, "Blue")
        self.Lbc1.insert(3, "Red")
        self.Lbc1.insert(4, "Green")       
        self.Lbc1.grid(row=crow, column=0, pady=1,sticky=tk.N)
        self.Lbc1.select_set(0)        
        
        self.Lbxa = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbxa.insert(1, "Linear")
        self.Lbxa.insert(2, "Log")       
        self.Lbxa.grid(row=crow, column=1, padx=10, pady=1,sticky=tk.N)
        self.Lbxa.select_set(0) 
        
        self.Lbya = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbya.insert(1, "Linear")
        self.Lbya.insert(2, "Log")       
        self.Lbya.grid(row=crow, column=2, padx=10, pady=1,sticky=tk.N)
        self.Lbya.select_set(0)        
        
        

        self.Lbfn = tk.Listbox(top,height=4,width=5,exportselection=0)
        self.Lbfn.insert(1, "1")
        self.Lbfn.insert(2, "2")
        self.Lbfn.insert(3, "3")
        self.Lbfn.insert(4, "4") 
        self.Lbfn.insert(5, "5")
        self.Lbfn.insert(6, "6")        
        self.Lbfn.grid(row=crow, column=3,columnspan=1, pady=1,sticky=tk.N+tk.S+tk.E)
        self.Lbfn.select_set(0)          
        
        # create a vertical scrollbar to the right of the listbox
        yscroll = tk.Scrollbar(top,command=self.Lbfn.yview, orient=tk.VERTICAL)
        yscroll.grid(row=crow, column=4, sticky=tk.N+tk.S+tk.W)
        self.Lbfn.configure(yscrollcommand=yscroll.set)
    


################################################################################
        
        crow+=1 

        self.hwtext8=tk.Label(top,text='Curve 2 Legend Title')
        self.hwtext8.grid(row=crow, column=0, columnspan=1, pady=8)  
        
        self.hwtext81=tk.Label(top,text='X-axis Limits')
        self.hwtext81.grid(row=crow, column=1, columnspan=1, pady=8)  
        
        self.hwtext82=tk.Label(top,text='Y-axis Limits')
        self.hwtext82.grid(row=crow, column=2, columnspan=1, pady=8)          
        
        
        self.hwtext61=tk.Label(top,text='Legend')
        self.hwtext61.grid(row=crow, column=3, columnspan=1, padx=10, pady=8) 
                        
        crow+=1 
        
        self.t2_string=tk.StringVar()  
        self.t2_string.set('')  
        self.t2_string_entry=tk.Entry(top, width = 26,textvariable=self.t2_string)
        self.t2_string_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=5) 

        self.Lbxlim = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbxlim.insert(1, "Automatic")
        self.Lbxlim.insert(2, "Manual")       
        self.Lbxlim.grid(row=crow, column=1, padx=10, pady=1,sticky=tk.N)
        self.Lbxlim.select_set(0)        
        
        self.Lbylim = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbylim.insert(1, "Automatic")
        self.Lbylim.insert(2, "Manual")       
        self.Lbylim.grid(row=crow, column=2, padx=10, pady=1,sticky=tk.N)
        self.Lbylim.select_set(0)        
        
        
        self.Lbleg = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbleg.insert(1, "On")
        self.Lbleg.insert(2, "Off")       
        self.Lbleg.grid(row=crow, column=3, padx=10, pady=1,sticky=tk.N)
        self.Lbleg.select_set(0)          
        
        crow+=1 

        self.hwtext10=tk.Label(top,text='Curve 2 Color')
        self.hwtext10.grid(row=crow, column=0, columnspan=1, padx=1, pady=8,sticky=tk.N)  
        
        self.hwtext91=tk.Label(top,text='Xmin')
        self.hwtext91.grid(row=crow, column=1, columnspan=1, pady=3,sticky=tk.S)  
        
        self.hwtext97=tk.Label(top,text='Ymin')
        self.hwtext97.grid(row=crow, column=2, columnspan=1, pady=3,sticky=tk.S)              
                
        self.hwtext61=tk.Label(top,text='Grid')
        self.hwtext61.grid(row=crow, column=3, columnspan=1, padx=10, pady=8) 

        crow+=1 

        self.Lbc2 = tk.Listbox(top,height=4,width=10,exportselection=0)
        self.Lbc2.insert(1, "Black")
        self.Lbc2.insert(2, "Blue")
        self.Lbc2.insert(3, "Red")
        self.Lbc2.insert(4, "Green")       
        self.Lbc2.grid(row=crow, column=0, rowspan=3, pady=1,sticky=tk.N)
        self.Lbc2.select_set(0)   

        self.xmin_string=tk.StringVar()  
        self.xmin_string.set('')  
        self.xmin_string_entry=tk.Entry(top, width = 12,textvariable=self.xmin_string)
        self.xmin_string_entry.grid(row=crow, column=1,columnspan=1,padx=5, pady=1,sticky=tk.N)  
        self.xmin_string_entry.config(state = 'disabled')   
     
        self.ymin_string=tk.StringVar()  
        self.ymin_string.set('')  
        self.ymin_string_entry=tk.Entry(top, width = 12,textvariable=self.ymin_string)
        self.ymin_string_entry.grid(row=crow, column=2,columnspan=1,padx=5, pady=1,sticky=tk.N)          
        self.ymin_string_entry.config(state = 'disabled')           
        
        
        self.Lbgrid = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbgrid.insert(1, "On")
        self.Lbgrid.insert(2, "Off")       
        self.Lbgrid.grid(row=crow, column=3, padx=10, pady=1,sticky=tk.N)
        self.Lbgrid.select_set(0)          
        
        crow=crow+1

        self.hwtext92=tk.Label(top,text='Xmax')
        self.hwtext92.grid(row=crow, column=1, columnspan=1, pady=0,sticky=tk.S)             

        self.hwtext99=tk.Label(top,text='Ymax')
        self.hwtext99.grid(row=crow, column=2, columnspan=1, pady=0,sticky=tk.S)      
         
        crow=crow+1
         
        self.xmax_string=tk.StringVar()  
        self.xmax_string.set('')  
        self.xmax_string_entry=tk.Entry(top, width = 12,textvariable=self.xmax_string)
        self.xmax_string_entry.grid(row=crow, column=1,columnspan=1,padx=5, pady=1,sticky=tk.N)
        self.xmax_string_entry.config(state = 'disabled')             
          
        self.ymax_string=tk.StringVar()  
        self.ymax_string.set('')  
        self.ymax_string_entry=tk.Entry(top, width = 12,textvariable=self.ymax_string)
        self.ymax_string_entry.grid(row=crow, column=2,columnspan=1,padx=5, pady=1,sticky=tk.N)          
        self.ymax_string_entry.config(state = 'disabled')             
          
################################################################################

        crow=crow+1         

        self.button_read1 = tk.Button(top, text="Read Input File 1",command=self.read_data1)
        self.button_read1.config( height = 2, width = 18 )
        self.button_read1.grid(row=crow, column=0,columnspan=1,padx=1, pady=10,sticky=tk.W)   
        
        self.button_read2 = tk.Button(top, text="Read Input File 2",command=self.read_data2)
        self.button_read2.config( height = 2, width = 18 )
        self.button_read2.grid(row=crow, column=1,columnspan=1,padx=1, pady=10,sticky=tk.W) 

        crow=crow+1       
        
        self.button_plot1 = tk.Button(top, text="Plot Curve 1",command=self.plot1)
        self.button_plot1.config( height = 2, width = 18 )
        self.button_plot1.grid(row=crow, column=0,columnspan=1,padx=1, pady=10,sticky=tk.W)         
 
        self.button_plot2 = tk.Button(top, text="Plot Curve 2",command=self.plot2)
        self.button_plot2.config( height = 2, width = 18 )
        self.button_plot2.grid(row=crow, column=1,columnspan=1,padx=1, pady=10,sticky=tk.W)   
        
        self.button_plot12 = tk.Button(top, text="Plot Both Curves",command=self.plot12)
        self.button_plot12.config( height = 2, width = 18 )
        self.button_plot12.grid(row=crow, column=2,columnspan=1,padx=1, pady=10,sticky=tk.W)           
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 18 )
        self.button_quit.grid(row=crow, column=3,columnspan=1, padx=1,pady=10)

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
            
        self.a1,self.b1,self.num1=read_two_columns_from_dialog('Select Input File 1',self.master)
        
        if(self.num1>=1):
            tl2=self.topp
            tkMessageBox.showinfo(" ", "Data File 1 Read",parent=tl2)
        
        
    def read_data2(self):            
            
        self.a2,self.b2,self.num2=read_two_columns_from_dialog('Select Input File 2',self.master)

        if(self.num2>=1):
            tl2=self.topp
            tkMessageBox.showinfo(" ", "Data File 2 Read",parent=tl2)
    
################################################################################
        
    def plot1(self):   
                  
        nleg=1+int(self.Lbleg.curselection()[0])   
        nfn=1+int(self.Lbfn.curselection()[0])   
        ngrid=1+int(self.Lbgrid.curselection()[0])
        nxa=1+int(self.Lbxa.curselection()[0])           
        nya=1+int(self.Lbya.curselection()[0])    
        
        nxlim=1+int(self.Lbxlim.curselection()[0])   
        nylim=1+int(self.Lbylim.curselection()[0])          
         

        nc1=1+int(self.Lbc1.curselection()[0])  

        if(nc1==1):
            s1="k"
        if(nc1==2):
            s1="b"            
        if(nc1==3):
            s1="r"
        if(nc1==4):
            s1="g"        

        plt.ion()        
        plt.close(nfn)
#        plt.gca().set_autoscale_on(False)
        fig2=plt.figure(nfn)
        
        print("start plot")
        
        print(len(self.a1))
        
        if(nleg==1):
            line2,=plt.plot(self.a1, self.b1, color=s1, label=self.t1_string.get())
            plt.legend(loc="upper right")              
        else:    
            line2,=plt.plot(self.a1, self.b1, color=s1)
            
        print("ref 2")    
            
        plt.title(self.t_string.get())       
        plt.xlabel(self.xlabel_string.get())     
        plt.ylabel(self.ylabel_string.get()) 
    
        if(ngrid==1):
            plt.grid(True)
            
        if(nxa==2):
            plt.xscale('log')            

        if(nya==2):
            plt.yscale('log')    
            
        if(ngrid==1):
            plt.grid(True)            

       
        if(nxlim==2):
            x1=float(self.xmin_string.get())
            x2=float(self.xmax_string.get())
            
            if(nxa==2):
                
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
        
        print("end plot")        
        
##############################
        
    def plot2(self):          
        
        nleg=1+int(self.Lbleg.curselection()[0])   
        nfn=1+int(self.Lbfn.curselection()[0])   
        ngrid=1+int(self.Lbgrid.curselection()[0])   
        nxa=1+int(self.Lbxa.curselection()[0])           
        nya=1+int(self.Lbya.curselection()[0])                 

        nxlim=1+int(self.Lbxlim.curselection()[0])   
        nylim=1+int(self.Lbylim.curselection()[0])  

        nc2=1+int(self.Lbc2.curselection()[0]) 

        if(nc2==2):
            s2="k"
        if(nc2==2):
            s2="b"            
        if(nc2==3):
            s2="r"
        if(nc2==4):
            s2="g"
            
        plt.ion()  
        plt.close(nfn)
        plt.figure(nfn)

        if(nleg==1):
            plt.plot(self.a2, self.b2, color=s2, label=self.t2_string.get())
            plt.legend(loc="upper right")   
        else:    
            plt.plot(self.a2, self.b2, color=s2)    

        plt.title(self.t_string.get())       
        plt.xlabel(self.xlabel_string.get())     
        plt.ylabel(self.ylabel_string.get()) 

        if(ngrid==1):
            plt.grid(True)
            
        if(nxa==2):
            plt.xscale('log')            

        if(nya==2):
            plt.yscale('log')    
            
        if(ngrid==1):
            plt.grid(True)   

            
        if(nxlim==2):
            x1=float(self.xmin_string.get())
            x2=float(self.xmax_string.get())
            plt.xlim([x1,x2])
            
        if(nylim==2):
            y1=float(self.ymin_string.get())
            y2=float(self.ymax_string.get())            
            plt.ylim([y1,y2])

##############################
        
    def plot12(self):          
        
        nleg=1+int(self.Lbleg.curselection()[0])   
        nfn=1+int(self.Lbfn.curselection()[0])   
        ngrid=1+int(self.Lbgrid.curselection()[0])  
        nxa=1+int(self.Lbxa.curselection()[0])           
        nya=1+int(self.Lbya.curselection()[0])    
        
        nxlim=1+int(self.Lbxlim.curselection()[0])   
        nylim=1+int(self.Lbylim.curselection()[0])  
        
        nc1=1+int(self.Lbc1.curselection()[0])  
        nc2=1+int(self.Lbc2.curselection()[0])          
        
        if(nc1==1):
            s1="k"
        if(nc1==2):
            s1="b"            
        if(nc1==3):
            s1="r"
        if(nc1==4):
            s1="g"              

        if(nc2==2):
            s2="k"
        if(nc2==2):
            s2="b"            
        if(nc2==3):
            s2="r"
        if(nc2==4):
            s2="g"
            
        plt.ion()          
        plt.close(nfn)
        plt.figure(nfn)
        
        if(nleg==1):
            plt.plot(self.a1, self.b1, color=s1, label=self.t1_string.get())
            plt.plot(self.a2, self.b2, color=s2, label=self.t2_string.get()) 
            plt.legend(loc="upper right")  
        else:    
            plt.plot(self.a1, self.b1, color=s1)
            plt.plot(self.a2, self.b2, color=s2)              

         
        plt.title(self.t_string.get())       
        plt.xlabel(self.xlabel_string.get())     
        plt.ylabel(self.ylabel_string.get()) 
        
        if(ngrid==1):
            plt.grid(True)
            
        if(nxa==2):
            plt.xscale('log')            

        if(nya==2):
            plt.yscale('log')    
            
        if(ngrid==1):
            plt.grid(True)                          

            
        if(nxlim==2):
            x1=float(self.xmin_string.get())
            x2=float(self.xmax_string.get())
            
            if(nxa==2):
                
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
        # xdata, ydata = event.artist.get_data()
        # self.x, self.y = xdata[event.ind], ydata[event.ind]
        self.x, self.y = event.mouseevent.xdata, event.mouseevent.ydata
        if self.x is not None:
            self.annotation.xy = self.x, self.y
            self.annotation.set_text(self.text_template % (self.x, self.y))
            self.annotation.set_visible(True)
            event.canvas.draw()
                