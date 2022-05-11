##########################################################################
# program: vb_sine_amplitude_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.2
# date: September 11, 2013
# description:  Sine amplitude conversion utility
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

class vb_sine_amplitude:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.32))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_sine_amplitude_gui.py ver 1.2  by Tom Irvine")         

        
        self.iflag=0
        
        crow=0
        
        self.hwtext1=tk.Label(top,text='Sine Amplitude Conversion Utility')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='Select Input')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.E)       
        
        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=4,width=30,exportselection=0)
        self.Lb1.insert(1, "Displacement (peak-to-peak)")
        self.Lb1.insert(2, "Displacement (zero-to-peak)")
        self.Lb1.insert(3, "Velocity (zero-to-peak)")
        self.Lb1.insert(4, "Acceleration (zero-to-peak)")        
        self.Lb1.grid(row=crow, column=0, columnspan=2, pady=4)
        self.Lb1.select_set(0) 
        self.Lb1.bind("<<ListboxSelect>>", self.OnKeyPress)        

        crow=crow+1
        
        self.hwtext_freq=tk.Label(top,text='Enter Frequency (Hz)')
        self.hwtext_freq.grid(row=crow, column=0, columnspan=6, pady=12,sticky=tk.W) 
 
        self.amp_text=tk.StringVar()  
        self.amp_text.set('Enter Displacement (peak-to-peak)')         
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
                
        self.tree = Treeview(top,selectmode="extended",columns=("A","B"),height=5)
        self.tree.grid(row=crow, column=0,columnspan=2, padx=10,pady=1,sticky=tk.NW)

        self.tree.heading('#0', text='') 
        self.tree.heading('A', text='Parameter')          
        self.tree.heading('B', text='Value')
        
        self.tree.column('#0',minwidth=0,width=1)
        self.tree.column('A',minwidth=0,width=170, stretch=tk.YES)        
        self.tree.column('B',minwidth=0,width=85)              


################################################################################

    def OnKeyPress(self,event):
        self.Lb2.delete(0, tk.END)

        n=1+int(self.Lb1.curselection()[0]) 

        s1='Enter Displacement (peak-to-peak)'
        s2='Enter Displacement (zero-to-peak)'
        s3='Enter Velocity'
        s4='Enter Acceleration'


        if(n==1 or n==2):
            str1='inch'
            str2='mm'

        if(n==1):
            self.amp_text.set(s1)

        if(n==2):
            self.amp_text.set(s2)

        if(n==3):
            self.amp_text.set(s3)
            str1='inch/sec'
            str2='m/sec'

        if(n==4):
            self.amp_text.set(s4)
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

        dzp_in=0
        dzp_mm=0
        dpp_in=0
        dpp_mm=0        

        if(n==1):
#
           if(m==1):  # inch input
               dpp_in=amp
               dpp_mm=amp*mm_per_in       
           else:
               dpp_mm=amp
               dpp_in=amp*in_per_mm     
   
#
           dzp_in=dpp_in/2
           dzp_mm=dpp_mm/2

        if(n==2):

           if(m==1):  # inch input
               dzp_in=amp
               dzp_mm=amp*mm_per_in       
           else:
               dzp_mm=amp
               dzp_in=amp*in_per_mm     
   
        if(n==3):

           if(m==1):  # in/sec input
               v_ips=amp
               v_mps=amp*m_per_in  

           else:  # m/sec
              v_mps=amp 
              v_ips=amp*in_per_m

           dzp_in=v_ips/omega
           dzp_mm=(v_mps/omega)*1000
           
        if(n==4):

           if(m==1):  # G input
             a_g=amp
             a_mps2=amp*9.81 

           else:  # m/sec
             a_mps2=amp 
             a_g=amp/9.81
   
           dzp_in=(a_g/om2)*386
           dzp_mm=(a_mps2/om2)*1000

        if(n!=1):
           dpp_in=dzp_in*2
           dpp_mm=dzp_mm*2

        if(n!=3):
           v_ips=omega*dzp_in
           v_mps=omega*(dzp_mm)/1000

        if(n!=4):
           a_g=om2*dzp_in/386
           a_mps2=om2*dzp_mm/1000

        print ("\n")

        s0='Frequency'
        s1="%8.4g Hz" %freq
        self.tree.insert('', 'end', values=(s0,s1))
        print (s0,s1)

        s0='Displacement (peak-to-peak)'
        if(m==1):
            s1="%8.4g in" %dpp_in
        else:
            s1="%8.4g mm" %dpp_mm
        self.tree.insert('', 'end', values=(s0,s1))
        print (s0,s1)
        
        s0='Displacement (zero-to-peak)'
        if(m==1):
            s1="%8.4g in" %dzp_in
        else:
            s1="%8.4g mm" %dzp_mm
        self.tree.insert('', 'end', values=(s0,s1))
        print (s0,s1)
        
        s0='Velocity (zero-to-peak)'
        if(m==1):
            s1="%8.4g in/sec" %v_ips
        else:
            s1="%8.4g m/sec" %v_mps
        self.tree.insert('', 'end', values=(s0,s1))
        print (s0,s1)
            
        s0='Accel (zero-to-peak)'
        if(n==3 and m==2):
            s1="%8.4g m/sec^2" %a_mps2
        else:
            s1="%8.4g G" %a_g            
        self.tree.insert('', 'end', values=(s0,s1))    
        print (s0,s1)

        self.iflag=1        
            
###############################################################################
           

def quit(root):
    root.destroy()    