###########################################################################
# program: vb_multiple_curves_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.1
# date: October 14, 2014
# description:  power spectral density
#
###########################################################################
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
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    import tkinter.messagebox as tkMessageBox    

from vb_utilities import read_two_columns_from_dialog

from matplotlib.ticker import ScalarFormatter


import matplotlib.pyplot as plt

################################################################################

class vb_multiple_curves:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.30))
        h = int(2.*(h*0.35))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.topp=top

        self.master.title("vb_multiple_curves_gui.py ver 1.0  by Tom Irvine")  
        
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()
        self.var4 = tk.IntVar()           
        
################################################################################

        crow=1

        self.hwtext2=tk.Label(top,\
            text='Each input curve must have two columns')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=8,sticky=tk.W)

################################################################################

        crow=crow+1

        self.button_read1 = tk.Button(top, text="Read Input File 1",command=self.read_data1)
        self.button_read1.config( height = 2, width = 18 )
        self.button_read1.grid(row=crow, column=0,columnspan=1,padx=3, pady=10)   
        
        self.button_read2 = tk.Button(top, text="Read Input File 2",command=self.read_data2)
        self.button_read2.config( height = 2, width = 18 )
        self.button_read2.grid(row=crow, column=1,columnspan=1,padx=3, pady=10) 

        self.button_read3 = tk.Button(top, text="Read Input File 3",command=self.read_data3)
        self.button_read3.config( height = 2, width = 18 )
        self.button_read3.grid(row=crow, column=2,columnspan=1,padx=3, pady=10) 
        
        self.button_read4 = tk.Button(top, text="Read Input File 4",command=self.read_data4)
        self.button_read4.config( height = 2, width = 18 )
        self.button_read4.grid(row=crow, column=3,columnspan=1,padx=3, pady=10)        

        crow=crow+1

        self.hwtext31=tk.Label(top,text='Legend 1')
        self.hwtext31.grid(row=crow, column=0,columnspan=1,padx=3, pady=10) 
        self.hwtext32=tk.Label(top,text='Legend 2')
        self.hwtext32.grid(row=crow, column=1,columnspan=1,padx=3, pady=10) 
        self.hwtext33=tk.Label(top,text='Legend 3')
        self.hwtext33.grid(row=crow, column=2,columnspan=1,padx=3, pady=10) 
        self.hwtext34=tk.Label(top,text='Legend 4')        
        self.hwtext34.grid(row=crow, column=3,columnspan=1,padx=3, pady=10) 

        crow=crow+1
        
        self.L1_string=tk.StringVar()  
        self.L1_string.set('')  
        self.L1_string_entry=tk.Entry(top, width = 26,textvariable=self.L1_string)
        self.L1_string_entry.grid(row=crow, column=0,columnspan=1, pady=5)        
        
        self.L2_string=tk.StringVar()  
        self.L2_string.set('')  
        self.L2_string_entry=tk.Entry(top, width = 26,textvariable=self.L2_string)
        self.L2_string_entry.grid(row=crow, column=1,columnspan=1, pady=5)   
      
        self.L3_string=tk.StringVar()  
        self.L3_string.set('')  
        self.L3_string_entry=tk.Entry(top, width = 26,textvariable=self.L3_string)
        self.L3_string_entry.grid(row=crow, column=2,columnspan=1, pady=5)        
        
        self.L4_string=tk.StringVar()  
        self.L4_string.set('')  
        self.L4_string_entry=tk.Entry(top, width = 26,textvariable=self.L4_string)
        self.L4_string_entry.grid(row=crow, column=3,columnspan=1, pady=5)       
      
      

        crow=crow+1

        self.hwtext41=tk.Label(top,text='Title')
        self.hwtext41.grid(row=crow, column=0, columnspan=1, padx=10, pady=8) 

        self.hwtext42=tk.Label(top,text='X-label')
        self.hwtext42.grid(row=crow, column=1, columnspan=1, padx=10, pady=8) 

        self.hwtext43=tk.Label(top,text='Y-label')
        self.hwtext43.grid(row=crow, column=2, columnspan=1, padx=10, pady=8) 


        crow=crow+1

        self.t_string=tk.StringVar()  
        self.t_string.set('')  
        self.t_string_entry=tk.Entry(top, width = 26,textvariable=self.t_string)
        self.t_string_entry.grid(row=crow, column=0,columnspan=1,padx=10, pady=5)

        self.xlabel_string=tk.StringVar()  
        self.xlabel_string.set('')  
        self.xlabel_string_entry=tk.Entry(top, width = 26,textvariable=self.xlabel_string)
        self.xlabel_string_entry.grid(row=crow, column=1,columnspan=1,padx=10, pady=5)

        self.ylabel_string=tk.StringVar()  
        self.ylabel_string.set('')  
        self.ylabel_string_entry=tk.Entry(top, width = 26,textvariable=self.ylabel_string)
        self.ylabel_string_entry.grid(row=crow, column=2,columnspan=1,padx=10, pady=5)
        
       
        
        crow=crow+1

        self.hwtext74=tk.Label(top,text='Select Curves for Plot')
        self.hwtext74.grid(row=crow, column=0, columnspan=1, padx=10, pady=8) 
        
        self.hwtext52=tk.Label(top,text='X-axis Type')
        self.hwtext52.grid(row=crow, column=1, columnspan=1, padx=10, pady=8) 

        self.hwtext53=tk.Label(top,text='Y-axis Type')
        self.hwtext53.grid(row=crow, column=2, columnspan=1, padx=10, pady=8)         
        
        self.hwtext54=tk.Label(top,text='Legend')
        self.hwtext54.grid(row=crow, column=3, columnspan=1, padx=10, pady=8)         

        crow=crow+1
        
        self.R1 = tk.Radiobutton(top, text="1", variable=self.var1, value=1)
        self.R1.grid(row=crow, column=0, columnspan=1, pady=0)
        
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
        
        
        self.Legend_status = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Legend_status.insert(1, "On")
        self.Legend_status.insert(2, "Off")       
        self.Legend_status.grid(row=crow, column=3, padx=10, pady=1,sticky=tk.N)
        self.Legend_status.select_set(0)        

        crow=crow+1
        
        self.R2 = tk.Radiobutton(top, text="2", variable=self.var2, value=1)        
        self.R2.grid(row=crow, column=0, columnspan=1, pady=0)
        
        self.hwtext62=tk.Label(top,text='X-axis Limits')
        self.hwtext62.grid(row=crow, column=1, columnspan=1, padx=10, pady=8) 

        self.hwtext63=tk.Label(top,text='Y-axis Limits')
        self.hwtext63.grid(row=crow, column=2, columnspan=1, padx=10, pady=8)         

        crow=crow+1
        
        self.R3 = tk.Radiobutton(top, text="3", variable=self.var3, value=1)        
        self.R3.grid(row=crow, column=0, columnspan=1, pady=0)        

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

        crow=crow+1
        
        self.R4 = tk.Radiobutton(top, text="4", variable=self.var4, value=1)
        self.R4.grid(row=crow, column=0, columnspan=1, pady=0)      

        self.hwtext91=tk.Label(top,text='Xmin')
        self.hwtext91.grid(row=crow, column=1, columnspan=1, pady=3,sticky=tk.S)  
        
        self.hwtext97=tk.Label(top,text='Ymin')
        self.hwtext97.grid(row=crow, column=2, columnspan=1, pady=3,sticky=tk.S)  

        crow=crow+1
        
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
        
        crow=crow+1        
        
        self.button_plot = tk.Button(top, text="Plot Curves",command=self.plot)
        self.button_plot.config( height = 2, width = 18 )
        self.button_plot.grid(row=crow, column=1,columnspan=1,padx=3, pady=10,sticky=tk.W)           

        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 18 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=2,pady=10)


        self.Lbxlim.bind("<<ListboxSelect>>", self.callback_limits)    
        self.Lbylim.bind("<<ListboxSelect>>", self.callback_limits)   
                
###############################################################################

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
        
###############################################################################

    def plot(self):
        
        nxlim=1+int(self.Lbxlim.curselection()[0])   
        nylim=1+int(self.Lbylim.curselection()[0])         
        
        p1=self.var1.get()
        p2=self.var2.get()
        p3=self.var3.get()
        p4=self.var4.get()
    

        if(p1==0 and p2==0 and p3==0 and p4==0):
            tkMessageBox.showinfo("Warning", "Select one or more curves",parent=self.button_plot)
            return            
                    
###############################################################################
                    
        plt.ion()          
        plt.close(1)
        plt.figure(1)        
        
        if not self.L1_string.get(): #do something
            L1_s=' '
        else:
            L1_s=self.L1_string.get()
 
        if not self.L2_string.get(): #do something
            L2_s=' '
        else:
            L2_s=self.L2_string.get()
   
        if not self.L3_string.get(): #do something
            L3_s=' '
        else:
            L3_s=self.L3_string.get()    
        
        if not self.L4_string.get(): #do something
            L4_s=' '
        else:
            L4_s=self.L4_string.get()            
        
###############################################################################
        
        
        if(p1==1):
            plt.plot(self.a1, self.b1, label=L1_s)

        if(p2==1):
            plt.plot(self.a2, self.b2, label=L2_s)
        
        if(p3==1):
            plt.plot(self.a3, self.b3, label=L3_s)      

        if(p4==1):
            plt.plot(self.a4, self.b4, label=L4_s)      
          
###############################################################################

        if not self.t_string.get(): #do something
             plt.title('  ')           
        else:
            plt.title(self.t_string.get())  
            
        if not self.xlabel_string.get(): #do something
            plt.xlabel('   ')             
        else:
            plt.xlabel(self.xlabel_string.get())  
                         
        if not self.ylabel_string.get(): #do something
            plt.xlabel('   ')           
        else:
            plt.ylabel(self.ylabel_string.get())  
      

###############################################################################

        nxa=1+int(self.Lbxa.curselection()[0])           
        nya=1+int(self.Lbya.curselection()[0])
         
        if(nxa==2):
            plt.xscale('log')            

        if(nya==2):
            plt.yscale('log')    

        nl=1+int(self.Legend_status.curselection()[0])

        if(nl==1):
            plt.legend(loc="upper right")  


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
            
            
        plt.grid(True)    
        
###############################################################################

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


    def read_data3(self):            
            
        self.a3,self.b3,self.num3=read_two_columns_from_dialog('Select Input File 3',self.master)
        
        if(self.num3>=1):
            tl2=self.topp
            tkMessageBox.showinfo(" ", "Data File 3 Read",parent=tl2)
        
        
    def read_data4(self):            
            
        self.a4,self.b4,self.num4=read_two_columns_from_dialog('Select Input File 4',self.master)

        if(self.num4>=1):
            tl2=self.topp
            tkMessageBox.showinfo(" ", "Data File 4 Read",parent=tl2)    


################################################################################

def quit(root):
    root.destroy()
