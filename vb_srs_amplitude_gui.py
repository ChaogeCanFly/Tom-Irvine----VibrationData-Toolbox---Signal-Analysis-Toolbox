##########################################################################
# program: vb_srs_amplitude_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.1
# date: February 20, 2015
# description:  srs amplitude conversion utility
#               
###############################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename
    from ttk import Treeview
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    from tkinter.ttk import Treeview

import numpy as np



###############################################################################

class vb_srs_amplitude:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))
                
        
        self.master.title("vb_srs_amplitude_gui.py ver 1.1  by Tom Irvine")         

        
        self.iflag=0
        
        crow=0
        
        self.hwtext1=tk.Label(top,text='SRS Amplitude Conversion Utility')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='Select Input')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.E)       
        
        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=4,width=30,exportselection=0)
        self.Lb1.insert(1, "Relative Displacement")
        self.Lb1.insert(2, "Pseudo Velocity")
        self.Lb1.insert(3, "Absolute Acceleration")
        self.Lb1.grid(row=crow, column=0, columnspan=2, pady=4)
        self.Lb1.select_set(0) 
        self.Lb1.bind("<<ListboxSelect>>", self.OnKeyPress)        

        crow=crow+1
        
        self.hwtext_freq=tk.Label(top,text='Enter Frequency (Hz)')
        self.hwtext_freq.grid(row=crow, column=0, columnspan=6, pady=12,sticky=tk.W) 
 
        self.amp_text=tk.StringVar()  
        self.amp_text.set('Enter Displacement (zero-to-peak)')         
        self.hwtext_amp=tk.Label(top,textvariable=self.amp_text)
        self.hwtext_amp.grid(row=crow, column=1, columnspan=6, padx=40, pady=12,sticky=tk.S)          
             
        crow=crow+1             

        self.fnr=tk.StringVar()  
        self.fnr.set('')  
        self.fn_entry=tk.Entry(top, width = 12,textvariable=self.fnr)
        self.fn_entry.grid(row=crow, column=0,padx=5, pady=1,sticky=tk.N)  

        self.ampr=tk.StringVar()  
        self.ampr.set('')  
        self.amp_entry=tk.Entry(top, width = 12,textvariable=self.ampr)
        self.amp_entry.grid(row=crow, column=1,padx=20, pady=1,sticky=tk.NE)
        
        self.Lb2 = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lb2.insert(1, "inch")
        self.Lb2.insert(2, "mm")
        self.Lb2.grid(row=crow, column=2, columnspan=1, padx=1,pady=1,sticky=tk.NW)
        self.Lb2.select_set(0)        
        
        crow=crow+1    
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 
                
        root=self.master             

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=20)
        
        crow=crow+1  
        
        self.hwtext_results=tk.Label(top,text='Results')
        self.hwtext_results.grid(row=crow, column=0, columnspan=2, pady=12) 

        crow=crow+1          
                
        self.tree = Treeview(top,selectmode="extended",columns=("A","B"),height=4)
        self.tree.grid(row=crow, column=0,columnspan=2, padx=10,pady=1,sticky=tk.NW)

        self.tree.heading('#0', text='') 
        self.tree.heading('A', text='Parameter')          
        self.tree.heading('B', text='Value')
        
        self.tree.column('#0',minwidth=0,width=1)
        self.tree.column('A',minwidth=0,width=170, stretch=tk.YES)        
        self.tree.column('B',minwidth=0,width=95)              


################################################################################

    def OnKeyPress(self,event):
        self.Lb2.delete(0, tk.END)

        n=1+int(self.Lb1.curselection()[0]) 

        s1='Enter Relative Displacement '
        s2='Enter Pseudo Velocity '
        s3='Enter Acceleration'


        if(n==1):
            self.amp_text.set(s1)
            str1='inch'
            str2='mm'            

        if(n==2):
            self.amp_text.set(s2)
            str1='in/sec'
            str2='m/sec'

        if(n==3):
            self.amp_text.set(s3)
            str1='G'
            str2='m/sec^2'



        self.Lb2.insert(1, str1)
        self.Lb2.insert(2, str2)
        self.Lb2.select_set(0) 
          
###############################################################################        

    def calculation(self):
        
        x=self.tree.get_children()
        
        for i in range (0,len(x)):
            self.tree.delete(x[i])
                
#        map(self.tree.delete, self.tree.get_children())

        n=1+int(self.Lb1.curselection()[0]) 
        m=1+int(self.Lb2.curselection()[0])         

        freq= float(self.fnr.get())   
        amp= float(self.ampr.get())        
        
        omega=2*np.pi*freq
        om2=omega**2     
        
        mm_per_in=25.4
        in_per_mm=1/mm_per_in

        m_per_in=mm_per_in/1000
        in_per_m=1/m_per_in

        rd_in=0
        rd_mm=0
    

        if(n==1):
#
           if(m==1):  # inch input
               rd_in=amp
               rd_mm=amp*mm_per_in       
           else:
               rd_mm=amp
               rd_in=amp*in_per_mm   
               
           pv_ips=rd_in*omega
           pv_mps=rd_mm*omega/1000
           
           a_G=rd_in*om2/386
           a_mps2=rd_mm*om2/(1000)
           
        if(n==2):

           if(m==1):  # in/sec input
               pv_ips=amp
               pv_mps=amp*m_per_in  

           else:  # m/sec
              pv_mps=amp 
              pv_ips=amp*in_per_m

           rd_in=pv_ips/omega
           rd_mm=1000*pv_mps/omega           
               
           a_G=pv_ips*omega/386
           a_mps2=pv_mps*omega
    
         
        if(n==3):

           if(m==1):  # G input
             a_G=amp
             a_mps2=amp*9.81 

           else:  # m/sec
             a_mps2=amp 
             a_G=amp/9.81
    
           pv_ips=386*a_G/omega
           pv_mps=a_mps2/omega 

           rd_in=386*a_G/om2
           rd_mm=1000*a_mps2/om2 
   
    
        print ("\n")

        s0='Frequency'
        s1="%8.4g Hz" %freq
        self.tree.insert('', 'end', values=(s0,s1))
        print (s0,s1)

        s0='Relative Displacement'
        if(m==1):
            s1="%8.4g in" %rd_in
        else:
            s1="%8.4g mm" %rd_mm
        self.tree.insert('', 'end', values=(s0,s1))
        print (s0,s1)
        
        
        s0='Pseudo Velocity'
        if(m==1):
            s1="%8.4g in/sec" %pv_ips
        else:
            s1="%8.4g m/sec" %pv_mps
        self.tree.insert('', 'end', values=(s0,s1))
        print (s0,s1)
            
        s0='Acceleration'
        if(m==1):
            s1="%8.4g G" %a_G
        else:
            s1="%8.4g m/sec^2" %a_mps2            
        self.tree.insert('', 'end', values=(s0,s1))    
        print (s0,s1)

        self.iflag=1        
            
###############################################################################
           

def quit(root):
    root.destroy()    