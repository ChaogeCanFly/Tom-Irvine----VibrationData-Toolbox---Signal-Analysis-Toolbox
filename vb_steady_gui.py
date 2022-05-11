###############################################################################
# program: vb_steady_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.2
# date: September 11, 2013
# description:
#
#  This script calculates the steady-state response of an SDOF system
#  to sinusoidal excitation
#
###############################################################################

from __future__ import print_function

import sys

if sys.version_info[0] == 2:
    import Tkinter as tk
    from ttk import Treeview
           
if sys.version_info[0] == 3:   
    import tkinter as tk 
    from tkinter.ttk import Treeview
    
from math import pi,sqrt


###############################################################################

class vb_steady:

    def __init__(self,parent):        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_steady_gui.py ver 1.2  by Tom Irvine") 

     
        crow=0

        self.hwtext1=tk.Label(top,text='Steady-state Response of an SDOF System to Sinusoidal Excitation')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=10,sticky=tk.W)
        
###############################################################################

        crow=crow+1

        self.hwtext5=tk.Label(top,text='Select Units')
        self.hwtext5.grid(row=crow, column=0, columnspan=1, pady=10)

        self.hwtext4=tk.Label(top,text='Select Excitation')
        self.hwtext4.grid(row=crow, column=1, columnspan=1, padx=20, pady=10)
        
        self.hwtext6=tk.Label(top,text='Enter Q')
        self.hwtext6.grid(row=crow, column=2, columnspan=1, padx=20, pady=10)
        
###############################################################################

        crow=crow+1
        
        self.Lb_unit = tk.Listbox(top,height=3,width=30,exportselection=0)
        
        self.Lb_unit.insert(1, "lbf, G, in/sec, in")
        self.Lb_unit.insert(2, "N, G, m/sec, mm")        
        self.Lb_unit.insert(3, "N, m/sec^2, m/sec, mm")          
        
        self.Lb_unit.grid(row=crow, column=0, pady=4,sticky=tk.N)
        self.Lb_unit.select_set(0)  
        self.Lb_unit.bind('<<ListboxSelect>>', self.force_accel_change)        


        self.Lb_ex = tk.Listbox(top,height=2,exportselection=0)
        self.Lb_ex.insert(1, "Applied Force")
        self.Lb_ex.insert(2, "Base Excitation")
        self.Lb_ex.grid(row=crow, column=1, padx=20, pady=4,sticky=tk.N)
        self.Lb_ex.select_set(0) 
        self.Lb_ex.bind('<<ListboxSelect>>', self.force_accel_change)         
        
        
        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 5,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=2,sticky=tk.N)
        self.Q_entry.bind("<KeyPress>", self.OnKeyPress)
        
###############################################################################
        
        crow=crow+1

        self.hwtext15=tk.Label(top,text='Enter Natural Frequency (Hz)')
        self.hwtext15.grid(row=crow, column=0, columnspan=1, pady=10)

        self.hwtext14=tk.Label(top,text='Enter Excitation Frequency (Hz)')
        self.hwtext14.grid(row=crow, column=1, columnspan=1, padx=20, pady=10)
                               
        crow=crow+1                               
                               
        self.fnr=tk.StringVar()  
        self.fn_entry=tk.Entry(top, width = 10,textvariable=self.fnr)
        self.fn_entry.grid(row=crow, column=0,sticky=tk.N)   
        self.fn_entry.bind("<KeyPress>", self.OnKeyPress)
        
        self.f_extr=tk.StringVar()  
        self.f_ext_entry=tk.Entry(top, width = 10,textvariable=self.f_extr)
        self.f_ext_entry.grid(row=crow, column=1,sticky=tk.N)  
        self.f_ext_entry.bind("<KeyPress>", self.OnKeyPress)        
        
###############################################################################

        crow=crow+1

        self.amp_text_r=tk.StringVar()    
        self.amp_text_r.set('Enter Applied Force (lbf)')         
        self.hwtext_amp=tk.Label(top,textvariable=self.amp_text_r)
        self.hwtext_amp.grid(row=crow, column=0, columnspan=1, pady=10)
        
        self.mass_text_r=tk.StringVar()    
        self.mass_text_r.set('Enter Mass (lbm)')         
        self.hwtext_mass=tk.Label(top,textvariable=self.mass_text_r)
        self.hwtext_mass.grid(row=crow, column=1, columnspan=1, pady=10)        
        self.hwtext_mass.config(state = 'normal')


        crow=crow+1
        
        self.ampr=tk.StringVar()  
        self.amp_entry=tk.Entry(top, width = 10,textvariable=self.ampr)
        self.amp_entry.grid(row=crow, column=0,sticky=tk.N) 
        self.amp_entry.bind("<KeyPress>", self.OnKeyPress)

        self.massr=tk.StringVar()  
        self.mass_entry=tk.Entry(top, width = 10,textvariable=self.massr)
        self.mass_entry.grid(row=crow, column=1,sticky=tk.N) 
        self.mass_entry.config(state = 'normal')
        self.mass_entry.bind("<KeyPress>", self.OnKeyPress)
        
###############################################################################

        crow=crow+1

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0, pady=20) 

        root=self.master 
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=10,pady=20)
        
        
        crow=crow+1  
        
        self.hwtext_results=tk.Label(top,text='Results')
        self.hwtext_results.grid(row=crow, column=0, columnspan=1, pady=12)   
        
        crow=crow+1          
        
        self.tree = Treeview(top,selectmode="extended",columns=("A","B"),height=4)
        self.tree.grid(row=crow, column=0,columnspan=2, padx=10,pady=1,sticky=tk.NW)

        self.tree.heading('#0', text='') 
        self.tree.heading('A', text='Parameter')          
        self.tree.heading('B', text='Value')
        
        self.tree.column('#0',minwidth=0,width=1)
        self.tree.column('A',minwidth=0,width=170, stretch=tk.YES)        
        self.tree.column('B',minwidth=0,width=85)                   
        

###############################################################################

    def calculate(self):
        
        x=self.tree.get_children()
        
        for i in range (0,len(x)):
            self.tree.delete(x[i])

        nfa_choice=int(self.Lb_ex.curselection()[0])
        nun_choice=int(self.Lb_unit.curselection()[0])
        
        fn= float(self.fnr.get())   
        freq= float(self.f_extr.get())  
        amp= float(self.ampr.get())  
        Q= float(self.Qr.get())
        damp=1/(2*Q)

        rho=freq/fn
        omegan=2*pi*fn 
        omega=2*pi*freq          
        
        den=omegan**2-omega**2 + (2*damp*omegan*omega)*1j        

        rel_disp=0
        
        
        if(nfa_choice==0):      # force
       
            force=amp        
       
            mass= float(self.massr.get())  
            
            if(nun_choice==0):
                mass/=386
                
            stiff=mass*omegan**2
            
            if(nun_choice==0):
                print('\n  stiffness= %8.4g lbf/in \n' %stiff)
            else:
                print('\n  stiffness= %8.4g N/m \n' %stiff)                
            
            
            disp=force*(1/stiff)*omegan**2/den
            velox=omega*disp*1j
            accel=-omega**2*disp
    
            term=2*damp*rho
 
            num=sqrt(1+term**2)
            den=sqrt((1-rho**2)**2+term**2)
    
            transmitted_force=force*num/den  
            
            A3="%8.4g" %abs(transmitted_force)  

            if(nun_choice==0):
                L3='Transmitted Force (lbf)'
            if(nun_choice==1):            
                L3='Transmitted Force (N)'                
            if(nun_choice==2):
                L3='Transmitted Force (N)'                   
                
        else:

            base_accel=amp
            
            if(nun_choice==0):            
                base_accel=base_accel*386    
            
            if(nun_choice==1):        
                base_accel=base_accel*9.81        
        
            num=omegan**2+(1j)*2*damp*omega*omegan
    
            accel=base_accel*num/den
            velox=accel/((1j)*omega)    
            disp=accel/(-omega**2)
            rel_disp=-base_accel/den              

            if(nun_choice==0):
                L3='Relative Displacement (in)'
            if(nun_choice==1):            
                L3='Relative Displacement (mm)'                
            if(nun_choice==2):
                L3='Relative Displacement (mm)'
            
##########            
            
        if(nun_choice==0):
            L0='Acceleration (G)'
            L1='Velocity (in/sec)'
            L2='Displacement (in)'
        if(nun_choice==1):            
            L0='Acceleration (G)'
            L1='Velocity (m/sec)'
            L2='Displacement (mm)'                
        if(nun_choice==2):
            L0='Acceleration (m/sec^2)'
            L1='Velocity (m/sec)'
            L2='Displacement (mm)'
                
                
        if(nun_choice==0):
            accel/=386
        if(nun_choice==1):                
            accel/=9.81
            disp*=1000
            rel_disp*=1000                
        if(nun_choice==2):                  
            disp*=1000 
            rel_disp*=1000  
            
            
        A0="%8.4g" %abs(accel)
        A1="%8.4g" %abs(velox)
        A2="%8.4g" %abs(disp)       

        if(nfa_choice==1):
            A3="%8.4g" %abs(rel_disp )
        
        
        self.tree.insert('', 'end', values=(L0,A0))        
        self.tree.insert('', 'end', values=(L1,A1))   
        self.tree.insert('', 'end', values=(L2,A2))      
        self.tree.insert('', 'end', values=(L3,A3))   
    
        print ("%s %s" %(L0,A0))     
        print ("%s %s" %(L1,A1))   
        print ("%s %s" %(L2,A2))   
        print ("%s %s" %(L3,A3))   
        
    
    def force_accel_change(self,val):
        
        map(self.tree.delete, self.tree.get_children())

        nfa_choice=int(self.Lb_ex.curselection()[0])
        nun_choice=int(self.Lb_unit.curselection()[0])   

        if(nfa_choice==0):      # force
            self.hwtext_mass.config(state = 'normal')     
            self.mass_entry.config(state = 'normal')            
            if(nun_choice==0):  #   Engish
                self.amp_text_r.set('Enter Applied Force (lbf)')
                self.mass_text_r.set('Enter Mass (lbm)')  
            else:               #   metric
                self.amp_text_r.set('Enter Applied Force (N)')
                self.mass_text_r.set('Enter Mass (kg)')                  
        else:
            self.hwtext_mass.config(state = 'disabled')   # accel
            self.mass_entry.config(state = 'disabled')    

            self.massr.set(' ')              
            
            if(nun_choice<=1):  #   English 
                self.amp_text_r.set('Enter Base Accel (G)')                
            else:               #   metric
                self.amp_text_r.set('Enter Base Accel (m/sec^2)')
                
                
    def OnKeyPress(self,event):
         map(self.tree.delete, self.tree.get_children())
         
###############################################################################

def quit(root):
    root.destroy()    