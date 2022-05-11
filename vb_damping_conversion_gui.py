###########################################################################
# program: vb_damping_conversion_gui.py
# author: Tom Irvine
# version: 1.2
# date: May 23, 2014
# 
###############################################################################

from __future__ import print_function

from numpy import sin,log,log10,zeros,ceil,linspace,logspace,pi


from vb_utilities import WriteData2
    
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




###############################################################################

class vb_damping_conversion:
    def __init__(self,parent):
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(880,600)
        self.master.geometry("880x600")
        
        self.master.title("vb_damping_conversion.py  ver 1.2  by Tom Irvine")        
        

            
###############################################################################        
        crow=0
        
        self.hwtext1=tk.Label(top,text='Natural Frequency')
        self.hwtext1.grid(row=crow, column=0, pady=7) 

        self.hwtext2=tk.Label(top,text='Freq Unit')
        self.hwtext2.grid(row=crow, column=1, pady=7) 

        self.hwtext3=tk.Label(top,text='Damping Value')
        self.hwtext3.grid(row=crow, column=2, pady=7)         
        
        self.hwtext4=tk.Label(top,text='Damping Unit')
        self.hwtext4.grid(row=crow, column=3, pady=7)          
        
        crow=crow+1  
        
        self.freqr=tk.StringVar()  
        self.freq_entry=tk.Entry(top, width = 12,textvariable=self.freqr)
        self.freq_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.freq_entry.configure(state='normal')            
        self.freqr.set('100')         
        
        self.Lb1 = tk.Listbox(top,height=2,width=15,exportselection=0)
        self.Lb1.insert(1, "Hz")
        self.Lb1.insert(2, "rad/sec")      
        self.Lb1.grid(row=crow, column=1, columnspan=1, padx=5, pady=4,sticky=tk.N)
        self.Lb1.select_set(0)    
        
        self.dampr=tk.StringVar()  
        self.damp_entry=tk.Entry(top, width = 12,textvariable=self.dampr)
        self.damp_entry.grid(row=crow, column=2, pady=4,sticky=tk.N) 
        self.damp_entry.configure(state='normal')  

        self.Lb2 = tk.Listbox(top,height=11,width=35,exportselection=0)
        self.Lb2.insert(1, "quality factor Q")
        self.Lb2.insert(2, "fraction of critical damping [zeta]")     
        self.Lb2.insert(3, "loss factor [eta]")
        self.Lb2.insert(4, "3 dB Bandwidth [delta omega (rad/sec)]")         
        self.Lb2.insert(5, "3 dB Bandwidth [delta f (Hz)]")
        self.Lb2.insert(6, "damping frequency [fd (Hz)]")     
        self.Lb2.insert(7, "decay constant [sigma (1/sec)]")
        self.Lb2.insert(8, "time constant [tau (sec)]")          
        self.Lb2.insert(9, "reverberation time [RT60 (sec)]")
        self.Lb2.insert(10, "decay Rate D (dB/sec)")     
        self.Lb2.insert(11, "logarithmic decrement [delta]")
        self.Lb2.grid(row=crow, column=3, columnspan=2, padx=5, pady=4,sticky=tk.N)
        self.Lb2.select_set(0)          

        crow=crow+1  

        self.hwtext6=tk.Label(top,text='Results: Equivalent Damping Values')
        self.hwtext6.grid(row=crow, column=1,padx=2, pady=4,sticky=tk.W) 
        
        crow=crow+1  

        self.textWidget = tk.Text(top, width=40, height = 16,font = "TkDefaultFont 9")
        self.textWidget.grid(row=crow, column=0,columnspan=3, pady=10)      
        
###############################################################################

        crow=crow+1
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate_main)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=1,padx=2, pady=10,sticky=tk.SW)        

            
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2, padx=2,pady=10,sticky=tk.SW) 


        self.damp_entry.bind("<Key>", self.callback_clear)  
        self.freq_entry.bind("<Key>", self.callback_clear)  
        self.Lb1.bind("<<ListboxSelect>>", self.callback_clear)    
        self.Lb2.bind("<<ListboxSelect>>", self.callback_clear)    


###############################################################################
        
    def callback_clear(self,event):
        self.textWidget.delete(1.0, tk.END)        
        
        
    def calculate_main(self):
        
        frequency_unit=1+int(self.Lb1.curselection()[0])
        damping_unit  =1+int(self.Lb2.curselection()[0])        

        frequency=float(self.freqr.get())
        damping=float(self.dampr.get())
        
        tpi=2*pi
 
        if(frequency_unit==1):
            fn=frequency
            om=tpi*fn
        else:
            om=frequency
            fn=om/tpi    

###########################################################################
 
        dd=damping
 
        if(damping_unit==1):  # Q
             Q=dd

        if(damping_unit==2):  # fraction of critical damping
            Q=1/(2*dd)

        if(damping_unit==3):  # loss factor
            Q=1/dd 

        if(damping_unit==4):  # 3 dB Bandwidth delta omega
            Q=om/dd

        if(damping_unit==5):  # 3 dB Bandwidth delta f
            Q=fn/dd 

        if(damping_unit==6):  # damping frequency
            Q=(om/(4*pi))/dd    

        if(damping_unit==7):  # decay constant
            Q=(om/2)/dd   

        if(damping_unit==8):  # time_constant
            Q=dd*om/2

        if(damping_unit==9):  # reverberation time
            Q=dd*om/13.8 

        if(damping_unit==10):  # decay rate
            Q=4.34*om/dd 

        if(damping_unit==11):  # logarithmic decrement
            Q=pi/dd 

###########################################################################
 
        zeta=1/(2*Q)
        loss_factor=1/Q
        three_dB_om=om/Q
        three_dB_f=fn/Q
        fd=(om/(4*pi))/Q
        sigma=(om/2)/Q
        tau=2*Q/om
        RT60=13.8*Q/om
        D=4.34*om/Q
        log_dec=pi/Q
  
###########################################################################
 
        if(damping_unit==1):  # Q
            Q=damping 

        if(damping_unit==2):  # fraction of critical damping
            zeta=damping     

        if(damping_unit==3):  # loss factor
            loss_factor=damping     

        if(damping_unit==4):  # 3 dB Bandwidth delta omega
            three_dB_om=damping

        if(damping_unit==5):  # 3 dB Bandwidth delta f
            three_dB_f=damping 

        if(damping_unit==6):  # damping frequency
            fd=damping 

        if(damping_unit==7):  # decay constant
            sigma=damping 

        if(damping_unit==8):  # time_constant
            tau=damping  

        if(damping_unit==9):  # reverberation time
            RT60=damping 

        if(damping_unit==10):  # decay rate
            D=damping 

        if(damping_unit==11):  # logarithmic decrement
            log_dec=damping 

        
        string1='quality factor Q=%8.4g' %Q
        string2='\nfraction of critical damping [zeta]=%8.4g' %zeta
        string3='\nloss factor [eta]=%8.4g' %loss_factor
        string4='\n\n3 dB Bandwidth [delta omega]=%8.4g rad/sec' %three_dB_om
        string5='\n3 dB Bandwidth [delta f]=%8.4g Hz' %three_dB_f
        string6='\n\ndamping frequency [fd]=%8.4g Hz' %fd
        string7='\ndecay constant [sigma]=%8.4g 1/sec' %sigma
        string8='\n\ntime constant [tau]= %8.4g sec' %tau
        string9='\nreverberation time [RT60]=%8.4g sec' %RT60
        string10='\n\ndecay Rate D=%8.4g dB/sec' %D
        string11='\nlogarithmic decrement [delta]=%8.4g' %log_dec

        self.textWidget.delete(1.0, tk.END)
        
        self.textWidget.insert('1.0',string1)
        self.textWidget.insert('end',string2)
        
        self.textWidget.insert('end',string3)       
        self.textWidget.insert('end',string4)
          
        self.textWidget.insert('end',string5)       
        self.textWidget.insert('end',string6) 
        self.textWidget.insert('end',string7)        
        
        self.textWidget.insert('end',string8)  
        self.textWidget.insert('end',string9)  
        self.textWidget.insert('end',string10)          

        self.textWidget.insert('end',string11)       

###############################################################################

def quit(root):
    root.destroy()                            