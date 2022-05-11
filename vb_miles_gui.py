################################################################################
# program: vb_miles_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 23, 2014
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
    

from numpy import pi,sqrt



class vb_miles:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.24))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_miles_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0
        
        self.hwtext1=tk.Label(top,text='Response of an SDOF System to a PSD Base Input')
        self.hwtext1.grid(row=crow, column=0, columnspan=3, pady=12)        
        
        crow=crow+1

        self.hwtext1=tk.Label(top,text='Natural Frequency (Hz)')
        self.hwtext1.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)
        
        self.hwtext2=tk.Label(top,text='Amplification Factor Q')
        self.hwtext2.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.S)             

        self.hwtext3=tk.Label(top,text='Response')
        self.hwtext3.grid(row=crow, column=2, columnspan=1, pady=7,sticky=tk.S)

    

        crow=crow+1
        
        self.fnr=tk.StringVar()  
        self.fnr.set('')  
        self.fn_entry=tk.Entry(top, width = 12,textvariable=self.fnr)
        self.fn_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=3,sticky=tk.N)         

        self.Qr=tk.StringVar()  
        self.Qr.set('')  
        self.Q_entry=tk.Entry(top, width = 12,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=1,columnspan=1,padx=5, pady=3,sticky=tk.N)  
               
        self.textWidget = tk.Text(top, width=35, height = 11,font = "TkDefaultFont 9")
        self.textWidget.grid(row=crow, column=2,columnspan=5, rowspan=3, pady=2)                  
        
        
        crow=crow+1                

        self.hwtext6=tk.Label(top,text='PSD (G^2/Hz)')
        self.hwtext6.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)   

        crow=crow+1   
 
        self.Pr=tk.StringVar()  
        self.Pr.set('')  
        self.P_entry=tk.Entry(top, width = 12,textvariable=self.Pr)
        self.P_entry.grid(row=crow, column=0,columnspan=1,padx=5, pady=3,sticky=tk.N)  
        
        
    
################################################################################

        crow=crow+1         
    
        self.button_calculate = tk.Button(top, text="Calculate",command=self.calculate)
        self.button_calculate.config( height = 2, width = 15, state='normal' )
        self.button_calculate.grid(row=crow, column=0,columnspan=1, padx=2, pady=15)     
  
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=15)
        
               
        self.fn_entry.bind("<Key>", self.callback_clear)  
        self.Q_entry.bind("<Key>", self.callback_clear)          
        self.P_entry.bind("<Key>", self.callback_clear)        
      
################################################################################  


    def callback_clear(self,event):
        
        self.textWidget.delete(1.0, tk.END)     

    def calculate(self):   
        
        fn=float(self.fnr.get())
        Q=float(self.Qr.get())
        P=float(self.Pr.get())       


        miles_acc=sqrt((pi/2.)*P*fn*Q)
        out1= 'Acceleration Response \n'  
        out2= '     = %10.2f GRMS (1 sigma) \n ' %(miles_acc)
        out3= '     = %10.2f G    (3 sigma) \n\n ' %(3.*miles_acc)
	
 
        om = 2.*pi*fn
        om2 = (om**2.)
        miles_rd=miles_acc/om2
        miles_rd=miles_rd*386.
       
        out4= 'Relative Displacement \n '
        out5= '      = %10.3g inch (1 sigma) \n ' %(miles_rd)
        out6= '      = %10.3g inch (3 sigma) \n\n' %(3.*miles_rd)

        miles_rd=miles_rd*25.4

        out7= 'Relative Displacement \n'
        out8= '      = %10.3g mm (1 sigma) \n' %(miles_rd)
        out9= '      = %10.3g mm (3 sigma)   ' %(3.*miles_rd)
  
        self.textWidget.delete(1.0, tk.END)
        
        self.textWidget.insert('1.0',out1)
        self.textWidget.insert('end',out2)
        
        self.textWidget.insert('end',out3)       
        self.textWidget.insert('end',out4)
          
        self.textWidget.insert('end',out5)       
        self.textWidget.insert('end',out6) 
        
        self.textWidget.insert('end',out7)
          
        self.textWidget.insert('end',out8)       
        self.textWidget.insert('end',out9)         
        
################################################################################


def quit(root):
    root.destroy()