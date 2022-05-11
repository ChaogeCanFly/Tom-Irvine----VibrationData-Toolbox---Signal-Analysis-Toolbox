################################################################################
# program: vb_rod_longitudinal_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 8, 2014
# description:  longitudinal natural frequencies of a rod 
#               
################################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
        
import matplotlib.pyplot as plt

from numpy import sin,cos,sinh,cosh,sqrt,pi,zeros,ones


class vb_rod_longitudinal:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.32))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_rod_longitudinal_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Select Left BC')
        self.hwtext1.grid(row=crow, column=0, pady=10,sticky=tk.SE)

        self.hwtext2=tk.Label(top,text='Select Right BC')
        self.hwtext2.grid(row=crow, column=4, pady=10,sticky=tk.SW)

###############################################################################

        crow=crow+1
        
        self.Lb1 = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lb1.insert(1, "Fixed")
        self.Lb1.insert(2, "Free")
        self.Lb1.grid(row=crow, column=0, columnspan=1, padx=2,sticky=tk.NE)
        self.Lb1.select_set(0)                
        
        
        w = tk.Canvas(top, width=230, height=26)
        w.grid(row=crow, column=1, columnspan=3,padx=5)
        
        x1=0
        x2=230         
        
        w.create_rectangle(x1, 24, x2, 26, fill="black")
        w.create_rectangle(x1, 10, x2, 24, fill="brown")
        w.create_rectangle(x1, 8, x2, 10, fill="black")            
        
        self.Lb2 = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lb2.insert(1, "Fixed")
        self.Lb2.insert(2, "Free")
        self.Lb2.grid(row=crow, column=4, columnspan=1, padx=2,sticky=tk.NW)
        self.Lb2.select_set(0)            
        
###############################################################################

        crow=crow+1

        self.hwtext3=tk.Label(top,text='Select Units')
        self.hwtext3.grid(row=crow, column=0, pady=10)
        
        self.hwtext4=tk.Label(top,text='Enter Length (in)')
        self.hwtext4.grid(row=crow, column=1, pady=10)
        

###############################################################################

        crow=crow+1

        self.Lbu = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbu.insert(1, "English")
        self.Lbu.insert(2, "Metric")
        self.Lbu.grid(row=crow, column=0, columnspan=1, pady=4, padx=10)
        self.Lbu.select_set(0)    
        
        self.lengthr=tk.StringVar()  
        self.length_entry=tk.Entry(top, width = 12,textvariable=self.lengthr)
        self.length_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.length_entry.configure(state='normal')            
       
        
###############################################################################

        crow=crow+1


        self.hwtext6=tk.Label(top,text='Select Material')
        self.hwtext6.grid(row=crow, column=1, pady=10)     
        
        self.hwtext6=tk.Label(top,text='Natural Frequencies (Hz)')
        self.hwtext6.grid(row=crow, column=2, pady=10) 
        
###############################################################################

        crow=crow+1

        self.Lbmat = tk.Listbox(top,height=6,width=20,exportselection=0)
        self.Lbmat.insert(1, "Aluminum")
        self.Lbmat.insert(2, "Steel")
        self.Lbmat.insert(3, "Copper")
        self.Lbmat.insert(4, "G10")  
        self.Lbmat.insert(5, "PVC")
        self.Lbmat.insert(6, "Other")          
        self.Lbmat.grid(row=crow, column=1, pady=1, padx=5,sticky=tk.N)
        self.Lbmat.select_set(0)           

        self.textWidget = tk.Text(top, width=10, height = 5,font = "TkDefaultFont 9")
        self.textWidget.grid(row=crow, column=2,columnspan=1, pady=10,sticky=tk.N)
        

###############################################################################

        crow=crow+1
        
        self.hwtext8=tk.Label(top,text='Elastic Modulus (lbf/in^2)')
        self.hwtext8.grid(row=crow, column=1, columnspan=1,pady=5)   
        
###############################################################################
        
        crow=crow+1 

        self.mat1r=tk.StringVar()  
        self.mat1_entry=tk.Entry(top, width = 12,textvariable=self.mat1r)
        self.mat1_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.mat1_entry.configure(state='normal')  
        self.mat1r.set('1.0e+07') 
        
        
###############################################################################

        crow=crow+1
        
        self.hwtext10=tk.Label(top,text='Mass Density (lbm/in^3)')
        self.hwtext10.grid(row=crow, column=1, columnspan=1, pady=5)          


###############################################################################
        
        crow=crow+1

        self.mat2r=tk.StringVar()  
        self.mat2_entry=tk.Entry(top, width = 12,textvariable=self.mat2r)
        self.mat2_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.mat2_entry.configure(state='normal')          
        self.mat2r.set('0.1') 
        
###############################################################################
        
        crow=crow+1

        button1=tk.Button(top, text='Perform Analysis', command=self.PerformAnalysis)
        button1.grid(row=crow, column=1, padx=10, pady=10)
        button1.config( height = 2, width = 20 )        
          
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 20 )
        self.button_quit.grid(row=crow, column=2, padx=10,pady=10) 
        
        
        self.Lb1.bind("<<ListboxSelect>>", self.callback_clear)    
        self.Lb2.bind("<<ListboxSelect>>", self.callback_clear)        
        
        self.Lbu.bind("<<ListboxSelect>>", self.callback_unit)           
        self.Lbmat.bind("<<ListboxSelect>>", self.callback_material)  
        
        self.length_entry.bind("<Key>", self.callback_clear)          
  
        self.mat1_entry.bind("<Key>", self.callback_clear)    
        self.mat2_entry.bind("<Key>", self.callback_clear)    
        
################################################################################
    
    def callback_clear(self,event):
        self.textWidget.delete(1.0, tk.END)     
    
    
                       
    def callback_material(self,event):
        
        self.change_material(self)                         
        self.callback_clear(self)
        
        
    def callback_unit(self,event):
        
        nu=int(self.Lbu.curselection()[0])
        
        if(nu==0):
            self.hwtext4.config(text="Enter Length (in)" )
        else:    
            self.hwtext4.config(text="Enter Length (m)" )        
            
        self.change_material(self) 
        
#########
        
    @classmethod
    def change_material(cls,self):  
        
        nu=int(self.Lbu.curselection()[0])
        nmat=int(self.Lbmat.curselection()[0])        
        
        if(nmat==0):   # aluminum
            if(nu==0): 
                self.mat1r.set('1e+007')
                self.mat2r.set('0.1')
            else:
                self.mat1r.set('70')
                self.mat2r.set('2700')                

        if(nmat==1):   # steel
            if(nu==0):
                self.mat1r.set('3e+007')
                self.mat2r.set('0.28')
            else:
                self.mat1r.set('205')
                self.mat2r.set('7700')
            
        if(nmat==2):   # copper
            if(nu==0):
                self.mat1r.set('1.6e+007')
                self.mat2r.set('0.322')
            else:
                self.mat1r.set('110')
                self.mat2r.set('8900')
            
        if(nmat==3):   # G10
            if(nu==0):
                self.mat1r.set('2.7e+006')
                self.mat2r.set('0.065')
            else:
                self.mat1r.set('18.6')
                self.mat2r.set('1800')
                            
        if(nmat==4):   # PVC
            if(nu==0):
                self.mat1r.set('3.5e+005')
                self.mat2r.set('0.052')
            else:
                self.mat1r.set('24.1')
                self.mat2r.set('1440')
            
        if(nmat==5):  # other pass
            if(nu==0):
                pass
            else:
                pass             
        
#########        

        nmat=int(self.Lbmat.curselection()[0])   

        if(nu==0):
            self.hwtext8.config(text="Elastic Modulus (lbf/in^2)" )
            self.hwtext10.config(text="Mass Density (lbm/in^3)" )            
        else:
            self.hwtext8.config(text="Elastic Modulus (GPa)" )
            self.hwtext10.config(text="Mass Density (kg/m^3)" )              
                       
################################################################################

    def PerformAnalysis(self):
        
        n=4
        
        fn=zeros(n,'f')
        root=zeros(n,'f')
        beta=zeros(n,'f')            


        nu=1+int(self.Lbu.curselection()[0])
#        nmat=1+int(self.Lbmat.curselection()[0]) 
      
        
        LBC=1+int(self.Lb1.curselection()[0]) 
        RBC=1+int(self.Lb2.curselection()[0]) 

        E=float(self.mat1r.get())
        rho=float(self.mat2r.get())
        L=float(self.lengthr.get())

        iflag=0

        if((LBC==2 and RBC==3) or (LBC==3 and RBC==2)): # pinned-free
            # case unavailable
            iflag=1

        if(L>1.0e-20 and L<1.0e+20):
            pass
        else:
            iflag=2
       
 
        if(nu==1): # English
            rho=rho/386
    
        if(nu==2): # metric
            E=E*1.0e+09
 
        
###

        m=4

        tpi=2*pi
 
        c=sqrt(E/rho)
        term=pi*c/L
 
 
        if((LBC==1 and RBC==1) or (LBC==2 and RBC==2)):  # fixed-fixed or free-free
            for n in range(0,4):
                nn=n+1
                omega=nn*term
                fn[n]=omega/tpi
   

 
        if((LBC==1 and RBC==2) or (LBC==2 and RBC==1)): # fixed-free
            for n in range(0,4):
                nn=n+1
                omega=((2*nn-1)/2)*term
                fn[n]=omega/tpi
 
 
           
        if(iflag==1):
            tk.tkMessageBox.showinfo("Warning:", "case unavailable")
    
        if(iflag==2):
            tk.tkMessageBox.showinfo("Error:", "length erorr")


        string1='%8.4g' %fn[0]
        string2='\n%8.4g' %fn[1]
        string3='\n%8.4g' %fn[2]
        string4='\n%8.4g' %fn[3]

        self.textWidget.delete(1.0, tk.END)
        
        self.textWidget.insert('1.0',string1)
        self.textWidget.insert('end',string2)
        
        self.textWidget.insert('end',string3)       
        self.textWidget.insert('end',string4)
        
        print(" ")
        print(" fn (Hz)")
        for i in range(0,m):
            print(" %8.4g" %(fn[i]))
            
        print(" ")
        
        if(nu==1): # English
            print(" Speed of sound = %8.4g in/sec" %c)    
        else:
            print(" Speed of sound = %8.4g m/sec" %c)                

###############################################################################
        
def quit(root):
    root.destroy()                    