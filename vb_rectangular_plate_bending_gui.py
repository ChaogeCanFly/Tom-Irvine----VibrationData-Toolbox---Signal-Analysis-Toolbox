################################################################################
# program: vb_rectangular_plate_bending_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 10, 2014
# description:  
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

from numpy import pi,sqrt

class vb_rectangular_plate_bending:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.30))
        h = int(2.*(h*0.28))
        self.master.geometry("%dx%d+0+0" % (w, h))        
                
        self.master.title("vb_rectangular_plate_bending_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Rectangular Plate Bending Natural Frequency')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=7,sticky=tk.W)
        
        self.hwtext_tbc=tk.Label(top,text='Top BC')
        self.hwtext_tbc.grid(row=crow, column=3, pady=5,sticky=tk.S)        

###############################################################################

        crow=crow+1
                  
        
        self.Lb_tbc = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lb_tbc.insert(1, "fixed")
        self.Lb_tbc.insert(2, "pinned")
        self.Lb_tbc.insert(3, "free")        
        self.Lb_tbc.grid(row=crow, column=3, columnspan=1, padx=1)
        self.Lb_tbc.select_set(0)         
      
      
###############################################################################

        crow=crow+1

        self.hwtext1=tk.Label(top,text='Select Units')
        self.hwtext1.grid(row=crow, column=0, pady=1,sticky=tk.S)
        
        self.hwtext_lbc=tk.Label(top,text='Select Material')
        self.hwtext_lbc.grid(row=crow, column=1, pady=1,sticky=tk.S)         
        
        self.hwtext_lbc=tk.Label(top,text='Left BC')
        self.hwtext_lbc.grid(row=crow, column=2, pady=1,sticky=tk.S)   


        self.hwtext_rbc=tk.Label(top,text='Right BC')
        self.hwtext_rbc.grid(row=crow, column=4, pady=1,padx=20,sticky=tk.S)            
                
###############################################################################

        crow=crow+1

        self.Lbu = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbu.insert(1, "English")
        self.Lbu.insert(2, "Metric")
        self.Lbu.grid(row=crow, column=0, columnspan=1, pady=1, padx=1,sticky=tk.N)
        self.Lbu.select_set(0)         

        self.Lbm = tk.Listbox(top,height=5,width=12,exportselection=0)
        self.Lbm.insert(1, "Aluminum")
        self.Lbm.insert(2, "Steel")
        self.Lbm.insert(3, "Copper")
        self.Lbm.insert(4, "G10")       
        self.Lbm.insert(5, "Other")          
        self.Lbm.grid(row=crow, column=1, columnspan=1, rowspan=2, pady=1, padx=1,sticky=tk.N)
        self.Lbm.select_set(0)      
    

        self.Lb_lbc = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lb_lbc.insert(1, "fixed")
        self.Lb_lbc.insert(2, "pinned")
        self.Lb_lbc.insert(3, "free")        
        self.Lb_lbc.grid(row=crow, column=2, columnspan=1, pady=1, padx=1,sticky=tk.N)
        self.Lb_lbc.select_set(0)      

        x1=0
        x2=260         
        
        y1=0
        y2=160
        
        w = tk.Canvas(top, width=x2, height=y2)
        w.grid(row=crow, column=3, columnspan=1, rowspan=2, pady=0,sticky=tk.NW)

        w.create_rectangle(x1, y1, x2, y2, fill='brown',outline='black')

        self.Lb_rbc = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lb_rbc.insert(1, "fixed")
        self.Lb_rbc.insert(2, "pinned")
        self.Lb_rbc.insert(3, "free")        
        self.Lb_rbc.grid(row=crow, column=4, columnspan=1, pady=1, padx=20,sticky=tk.N)
        self.Lb_rbc.select_set(0)               
                
############################################################################### 

        crow=crow+1
        
        self.hwtext_EM=tk.Label(top,text='Elastic Modulus (psi)')
        self.hwtext_EM.grid(row=crow, column=0,sticky=tk.N)   

        self.EMr=tk.StringVar()  
        self.EM_entry=tk.Entry(top, width = 12,textvariable=self.EMr)
        self.EM_entry.grid(row=crow, column=0,pady=10) 
        self.EM_entry.configure(state='normal')
        
              
        self.hwtext_width=tk.Label(top,text='Width (in)')
        self.hwtext_width.grid(row=crow, column=2,stick=tk.N) 
        
        self.hwtext_PO=tk.Label(top,text='Poisson Ratio')
        self.hwtext_PO.grid(row=crow, column=1,padx=5,sticky=tk.N)
        
        self.POr=tk.StringVar()  
        self.PO_entry=tk.Entry(top, width = 12,textvariable=self.POr)
        self.PO_entry.grid(row=crow, column=1,pady=10) 
        self.PO_entry.configure(state='normal')      
     
        self.widthr=tk.StringVar()  
        self.width_entry=tk.Entry(top, width = 12,textvariable=self.widthr)
        self.width_entry.grid(row=crow, column=2) 
        self.width_entry.configure(state='normal')   
        
                 
############################################################################### 

        crow=crow+1
        
        crow=crow+1
        
        self.hwtext_MD=tk.Label(top,text='Mass Density (lbm/in^3)')
        self.hwtext_MD.grid(row=crow, column=0, pady=10,sticky=tk.S)  

        self.hwtext_nsm=tk.Label(top,text='Nonstructural Mass (lbm)')
        self.hwtext_nsm.grid(row=crow, column=1,padx=5,pady=10,sticky=tk.S)
        
        self.hwtext_thickness=tk.Label(top,text='Thickness (in)')
        self.hwtext_thickness.grid(row=crow, column=2,pady=10, sticky=tk.S)   
        
        self.hwtext_length=tk.Label(top,text='Length (in)')
        self.hwtext_length.grid(row=crow, column=3,pady=10, sticky=tk.SW)

        self.hwtext_bbc=tk.Label(top,text='Bottom BC')
        self.hwtext_bbc.grid(row=crow, column=3, pady=10,sticky=tk.S)   

        self.hwtext_result=tk.Label(top,text='Result: Natural Freq (Hz)')
        self.hwtext_result.grid(row=crow, column=4, pady=10,sticky=tk.S) 

        
        crow=crow+1
        
        self.MDr=tk.StringVar()  
        self.MD_entry=tk.Entry(top, width = 12,textvariable=self.MDr)
        self.MD_entry.grid(row=crow, column=0,sticky=tk.N) 
        self.MD_entry.configure(state='normal')
        
        self.nsmr=tk.StringVar()  
        self.nsm_entry=tk.Entry(top, width = 12,textvariable=self.nsmr)
        self.nsm_entry.grid(row=crow, column=1,sticky=tk.N)
        self.nsm_entry.configure(state='normal') 
        self.nsmr.set('0')    
        
        self.thicknessr=tk.StringVar()  
        self.thickness_entry=tk.Entry(top, width = 12,textvariable=self.thicknessr)
        self.thickness_entry.grid(row=crow, column=2,pady=1,sticky=tk.N) 
        self.thickness_entry.configure(state='normal')         

        self.lengthr=tk.StringVar()  
        self.length_entry=tk.Entry(top, width = 12,textvariable=self.lengthr)
        self.length_entry.grid(row=crow, column=3,sticky=tk.NW) 
        self.length_entry.configure(state='normal')

        self.Lb_bbc = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lb_bbc.insert(1, "fixed")
        self.Lb_bbc.insert(2, "pinned")
        self.Lb_bbc.insert(3, "free")        
        self.Lb_bbc.grid(row=crow, column=3, columnspan=1, pady=1,sticky=tk.N)
        self.Lb_bbc.select_set(0)           

        self.fnr=tk.StringVar()  
        self.fn_entry=tk.Entry(top, width = 12,textvariable=self.fnr)
        self.fn_entry.grid(row=crow, column=4,sticky=tk.N) 
        self.fn_entry.configure(state='readonly')   
        
        self.hwtext_tmass=tk.Label(top,text='Total Mass (lbm)')
        self.hwtext_tmass.grid(row=crow, column=4, pady=10,sticky=tk.S)
        
        crow=crow+1

        button1=tk.Button(top, text='Perform Analysis', command=self.PerformAnalysis)
        button1.grid(row=crow, column=2, padx=1, pady=10)
        button1.config( height = 2, width = 17 )        
          

        self.tmassr=tk.StringVar()  
        self.tmass_entry=tk.Entry(top, width = 12,textvariable=self.tmassr)
        self.tmass_entry.grid(row=crow, column=4, pady=4,sticky=tk.N) 
        self.tmass_entry.configure(state='readonly')  
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 17 )
        self.button_quit.grid(row=crow, column=3, padx=1,pady=10) 
        
        
        self.Lbu.bind("<<ListboxSelect>>", self.callback_unit)  
        self.Lbm.bind("<<ListboxSelect>>", self.callback_unit) 
        
        self.Lb_bbc.bind("<<ListboxSelect>>", self.callback_unit)  
        self.Lb_tbc.bind("<<ListboxSelect>>", self.callback_unit)  
        self.Lb_lbc.bind("<<ListboxSelect>>", self.callback_unit)  
        self.Lb_rbc.bind("<<ListboxSelect>>", self.callback_unit)          
        
        
        self.EM_entry.bind("<Key>", self.callback_clear)    
        self.MD_entry.bind("<Key>", self.callback_clear)    
        self.PO_entry.bind("<Key>", self.callback_clear)    
        self.width_entry.bind("<Key>", self.callback_clear) 
        self.thickness_entry.bind("<Key>", self.callback_clear) 
        self.length_entry.bind("<Key>", self.callback_clear) 
        self.nsm_entry.bind("<Key>", self.callback_clear)         
        
        self.change_material(self)         
        
################################################################################        

    def callback_unit(self,event):
        
        nu=int(self.Lbu.curselection()[0])
        
        if(nu==0):
            self.hwtext_width.config(text="Width (in)" )
            self.hwtext_thickness.config(text="Thickness (in)" )               
            self.hwtext_length.config(text="Length (in)" )            
            self.hwtext_EM.config(text="Elastic Modulus (psi)" )
            self.hwtext_MD.config(text="Mass Density (lbm/in^3)" )
            self.hwtext_nsm.config(text="Nonstructural Mass (lbm)" )
            self.hwtext_tmass.config(text='Total Mass (lbm)')
        else:    
            self.hwtext_width.config(text="Width (mm)" )
            self.hwtext_thickness.config(text="Thickness (mm)" )               
            self.hwtext_length.config(text="Length (mm)" )         
            self.hwtext_EM.config(text="Elastic Modulus (GPa)" )            
            self.hwtext_MD.config(text="Mass Density (kg/m^3)" )            
            self.hwtext_nsm.config(text="Nonstructural Mass (kg)" ) 
            self.hwtext_tmass.config(text='Total Mass (kg)')            
            
        self.callback_clear(self)
        self.change_material(self)  
        
###############################################################################

    @classmethod
    def change_material(cls,self):  
        
        unit=1+int(self.Lbu.curselection()[0])
        material=1+int(self.Lbm.curselection()[0])

        if(unit==1):  # English
        
            if(material==1): # aluminum
                elastic_modulus=1e+007
                mass_density=0.1  
      
            if(material==2):  # steel
                elastic_modulus=3e+007
                mass_density= 0.28         
    
            if(material==3):  # copper
                elastic_modulus=1.6e+007
                mass_density=  0.322
                
            if(material==4):  # G10
                elastic_modulus=2.7e+06
                mass_density=0.065                 
    
        else:                 # metric
        
            if(material==1):  # aluminum
                elastic_modulus=70
                mass_density=  2700
    
            if(material==2):  # steel
                elastic_modulus=205
                mass_density=  7700        
    
            if(material==3):   # copper
                elastic_modulus=110;
                mass_density=  8900
    
            if(material==4):  # G10
                elastic_modulus=18.6
                mass_density=1800      
                
 
        if(material==1):  # aluminum
             poisson=0.33  

        if(material==2):  # steel
            poisson=0.30      

        if(material==3):  # copper
            poisson=0.33 
            
        if(material==4):  # copper
            poisson=0.12             

        if(material<=4):

            EM="%8.4g" %elastic_modulus
            MD="%8.4g" %mass_density
            PO="%8.4g" %poisson

            self.EMr.set(EM) 
            self.MDr.set(MD) 
            self.POr.set(PO) 
        
        
###############################################################################

    def PerformAnalysis(self):

        unit=1+int(self.Lbu.curselection()[0])
            
        topBC    =1+int(self.Lb_tbc.curselection()[0])
        rightBC  =1+int(self.Lb_rbc.curselection()[0])
        bottomBC =1+int(self.Lb_bbc.curselection()[0])
        leftBC   =1+int(self.Lb_lbc.curselection()[0])
        

        E=float(self.EMr.get())
        rho=float(self.MDr.get())
        mu=float(self.POr.get())
                        
        L=float(self.lengthr.get())
        W=float(self.widthr.get())    
        thick=float(self.thicknessr.get())    
    
        nsm=float(self.nsmr.get()) 
        
        if(unit==2):
            rho=rho/(1000**3)
    
        mass=L*W*thick*rho+nsm
    
        if(unit==1):
            mass=mass/386
        else:
            L=L/1000
            W=W/1000
            thick=thick/1000
            E=E*1e+09

###

        tgg=mass
        
        if(unit==1):
            tgg=tgg*386
 
        tms="%8.4g" %tgg 
 
        self.tmassr.set(tms)  

###

        area=L*W
        rhos=mass/area
 
        D=E*thick**3/(12*(1.-mu**2))
#        Drho=D/rhos
 
        sqDrho=sqrt(D/rhos)
 
        a=L
        b=W
 
        a2=a**2
        a4=a**4
 
        b2=b**2
        b4=b**4
 
        a2b2=a**2*b**2
  
        iflag=0
   
###

# case 1:  pinned-pinned-free-free
        if( (leftBC==3 and topBC==3 and rightBC==2 and bottomBC==2)or\
            (leftBC==2 and topBC==2 and rightBC==3 and bottomBC==3)or\
            (leftBC==2 and topBC==3 and rightBC==3 and bottomBC==2)or\
            (leftBC==3 and topBC==2 and rightBC==2 and bottomBC==3)):
                fn=(pi/11)*sqDrho*( (1/a2) + (1/b2) )
                iflag=1

 
# case 2:  pinned-pinned-free-pinned
        if( (leftBC==2 and topBC==2 and rightBC==3 and bottomBC==2)or\
            (leftBC==3 and topBC==2 and rightBC==2 and bottomBC==2)):
            fn=(pi/2)*sqDrho*( (1/(4*a2)) + (1/b2) )
            iflag=1

# case 3:  pinned-pinned-pinned-pinned
        if( leftBC==2 and topBC==2 and rightBC==2 and bottomBC==2):
            fn=(pi/2)*sqDrho*( (1/a2) + (1/b2) )
            iflag=1

# case 4:  fixed-fixed-free-free
        if( (leftBC==3 and topBC==3 and rightBC==1 and bottomBC==1)or\
            (leftBC==1 and topBC==1 and rightBC==3 and bottomBC==3)or\
            (leftBC==1 and topBC==3 and rightBC==3 and bottomBC==1)or\
            (leftBC==3 and topBC==1 and rightBC==1 and bottomBC==3)):
            fn=(pi/5.42)*sqDrho*sqrt( (1/a4) + (3.2/a2b2)+ (1/b4) )
            iflag=1

# case 5:  fixed-fixed-fixed-free
        if( (leftBC==1 and topBC==1 and rightBC==3 and bottomBC==1)or\
            (leftBC==3 and topBC==1 and rightBC==1 and bottomBC==1)):
            fn=(pi/3)*sqDrho*sqrt( (0.75/a4) + (2/a2b2)+ (12/b4) )
            iflag=1

# case 6:  fixed-fixed-fixed-fixed
        if(leftBC==1 and topBC==1 and rightBC==1 and bottomBC==1):
            fn=(pi/1.5)*sqDrho*sqrt( (3/a4) + (2/a2b2) + (3/b4) )
            iflag=1

# case 7:  fixed-pinned-fixed-pinned
        if(leftBC==1 and topBC==2 and rightBC==1 and bottomBC==2):
            fn=(pi/3.46)*sqDrho*sqrt( (16/a4) + (8/a2b2) + (3/b4) )
            iflag=1

# case 8:  free-free-free-free
        if( leftBC==3 and topBC==3 and rightBC==3 and bottomBC==3):
            fn=(pi/2)*sqDrho*sqrt( 2.08/a2b2 )
            iflag=1

# case 9:  fixed-free-free-free
        if( (leftBC==1 and topBC==3 and rightBC==3 and bottomBC==3)or\
            (leftBC==3 and topBC==3 and rightBC==1 and bottomBC==3)):  
            fn=(0.56/a2)*sqDrho
            iflag=1

# case 10:  fixed-free-fixed-free
        if( leftBC==1 and topBC==3 and rightBC==1 and bottomBC==3): 
             fn=(3.55/a2)*sqDrho
             iflag=1

# case 11:  fixed-free-pinned-free
        if( (leftBC==1 and topBC==3 and rightBC==2 and bottomBC==3)or\
            (leftBC==2 and topBC==3 and rightBC==1 and bottomBC==3)):  
             fn=(0.78*pi/a2)*sqDrho
             iflag=1

# case 12:  pinned-free-pinned-free
        if( leftBC==2 and topBC==3 and rightBC==2 and bottomBC==3): 
             fn=(pi/(2*a2))*sqDrho
             iflag=1

# case 13:  fixed-pinned-fixed-free
        if( (leftBC==1 and topBC==2 and rightBC==1 and bottomBC==3)or\
            (leftBC==1 and topBC==3 and rightBC==1 and bottomBC==2)):  
            fn=(pi/1.74)*sqDrho*sqrt((4/a4)+(1/(2*a2b2))+(1/(64*b4)))
            iflag=1
            
# case 14:  fixed-pinned-free-free
        if( (leftBC==1 and topBC==2 and rightBC==3 and bottomBC==3)or\
            (leftBC==1 and topBC==3 and rightBC==3 and bottomBC==2)or\
            (leftBC==3 and topBC==2 and rightBC==1 and bottomBC==3)or\
            (leftBC==3 and topBC==3 and rightBC==1 and bottomBC==2)): 
            fn=(pi/2)*sqDrho*sqrt((0.127/a4)+(0.20/a2b2))
            iflag=1
 
# case 15:  pinned-fixed-pinned-free
        if( (leftBC==2 and topBC==1 and rightBC==2 and bottomBC==3)or\
            (leftBC==2 and topBC==3 and rightBC==2 and bottomBC==1)):  
            fn=(pi/2)*sqDrho*sqrt((1/a4)+(0.608/a2b2)+(0.126/b4))
            iflag=1
     
# case 16:  fixed-fixed-pinned-fixed
        if( (leftBC==2 and topBC==1 and rightBC==1 and bottomBC==1)or\
            (leftBC==1 and topBC==1 and rightBC==2 and bottomBC==1)):  
            fn=(pi/2)*sqDrho*sqrt((2.45/a4)+(2.90/a2b2)+(5.13/b4))
            iflag=1
 
# case 17:  fixed-fixed-free-pinned
        if( (leftBC==1 and topBC==1 and rightBC==3 and bottomBC==2)or\
            (leftBC==1 and topBC==2 and rightBC==3 and bottomBC==1)or\
            (leftBC==3 and topBC==1 and rightBC==1 and bottomBC==2)or\
            (leftBC==3 and topBC==2 and rightBC==1 and bottomBC==1)): 
            fn=(pi/2)*sqDrho*sqrt((0.127/a4)+(0.707/a2b2)+(2.44/b4))
            iflag=1
 
# case 18:  fixed-fixed-pinned-pinned-pinned
        if( (leftBC==2 and topBC==2 and rightBC==1 and bottomBC==1)or\
            (leftBC==1 and topBC==1 and rightBC==2 and bottomBC==2)or\
            (leftBC==1 and topBC==2 and rightBC==2 and bottomBC==1)or\
            (leftBC==2 and topBC==1 and rightBC==1 and bottomBC==2)): 
            fn=(pi/2)*sqDrho*sqrt((2.45/a4)+(2.68/a2b2)+(2.45/b4))
            iflag=1
            
# case 19:  fixed-pinned-pinned-pinned
        if( (leftBC==1 and topBC==2 and rightBC==2 and bottomBC==2)or\
            (leftBC==2 and topBC==2 and rightBC==1 and bottomBC==2)):  
            fn=(pi/2)*sqDrho*sqrt((2.45/a4)+(2.32/a2b2)+(1/b4))
            iflag=1
 
###########################################################################
 
        if(thick>0.5*W or thick>0.5*L):
            tk.tkMessageBox.showinfo("Warning", "thickness is too large")
            iflag=2

        else:

            if(iflag==1):
                buf="%8.4g" %fn
                self.fnr.set(buf)   
            else:
                tk.tkMessageBox.showinfo("Warning", "Case unavailable")
    
###############################################################################    
  
    def callback_clear(self,event):
        self.fnr.set('')  
        self.tmassr.set('')   

###############################################################################
        
def quit(root):
    root.destroy()                    