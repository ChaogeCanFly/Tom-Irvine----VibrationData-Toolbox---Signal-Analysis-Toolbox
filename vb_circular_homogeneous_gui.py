################################################################################
# program: vb_circular_homogeneous_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 8, 2014
# description:  circular, homogeneous plate bending frequencies
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

from numpy import sqrt,pi,zeros


class vb_circular_homogeneous:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.35))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        
        self.master.title("vb_circular_homogeneous_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext0=tk.Label(top,text='Homogeneous Circular Plate Bending Natural Frequencies ')
        self.hwtext0.grid(row=crow, column=0, columnspan=3, pady=10,sticky=tk.S)
        
        crow=crow+1        
        
        self.hwtext1=tk.Label(top,text='Select Units')
        self.hwtext1.grid(row=crow, column=0, pady=10,sticky=tk.S)

        self.hwtext2=tk.Label(top,text='Select BC')
        self.hwtext2.grid(row=crow, column=1, pady=10,sticky=tk.S)        

###############################################################################

        crow=crow+1
          
        self.Lbu = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbu.insert(1, "English")
        self.Lbu.insert(2, "Metric")
        self.Lbu.grid(row=crow, column=0, columnspan=1, pady=4, padx=10)
        self.Lbu.select_set(0) 

        self.Lbc = tk.Listbox(top,height=3,width=18,exportselection=0)
        self.Lbc.insert(1, "fixed")
        self.Lbc.insert(2, "simply-supported")
        self.Lbc.insert(3, "free")       
        self.Lbc.grid(row=crow, column=1, columnspan=1, pady=4, padx=10)
        self.Lbc.select_set(0)            
          
###############################################################################

        crow=crow+1
        
        self.hwtext3=tk.Label(top,text='Select Material')
        self.hwtext3.grid(row=crow, column=0, pady=10,sticky=tk.S)

        self.hwtext4=tk.Label(top,text='Enter Dimensions')
        self.hwtext4.grid(row=crow, column=1, pady=10,sticky=tk.S)          

###############################################################################

        crow=crow+1
        
        self.Lbm = tk.Listbox(top,height=4,width=12,exportselection=0)
        self.Lbm.insert(1, "Aluminum")
        self.Lbm.insert(2, "Steel")
        self.Lbm.insert(3, "Copper")
        self.Lbm.insert(4, "Other")        
        self.Lbm.grid(row=crow, column=0, columnspan=1, rowspan=2, pady=4, padx=10)
        self.Lbm.select_set(0) 
        
        self.hwtext_diameter=tk.Label(top,text='Diameter (in)')
        self.hwtext_diameter.grid(row=crow, column=1, pady=10,sticky=tk.S)  
        
###############################################################################

        crow=crow+1        

        self.diameterr=tk.StringVar()  
        self.diameter_entry=tk.Entry(top, width = 12,textvariable=self.diameterr)
        self.diameter_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.diameter_entry.configure(state='normal')        

###############################################################################

        crow=crow+1
        
        self.hwtext_E=tk.Label(top,text='Elastic Modulus (psi)')
        self.hwtext_E.grid(row=crow, column=0, pady=10,sticky=tk.S) 
        
        self.hwtext_T=tk.Label(top,text='Thickness (in)')
        self.hwtext_T.grid(row=crow, column=1, pady=10,sticky=tk.S) 
        
        self.hwtext_fn=tk.Label(top,text='Results: Natural Freq (Hz)')
        self.hwtext_fn.grid(row=crow, column=2, pady=10,sticky=tk.S) 
        
###############################################################################

        crow=crow+1  
        
        self.Er=tk.StringVar()  
        self.E_entry=tk.Entry(top, width = 12,textvariable=self.Er)
        self.E_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.E_entry.configure(state='normal')  
         
        self.Tr=tk.StringVar()  
        self.T_entry=tk.Entry(top, width = 12,textvariable=self.Tr)
        self.T_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.T_entry.configure(state='normal')     
        
        self.textWidget = tk.Text(top, width=10, height = 5,font = "TkDefaultFont 9")
        self.textWidget.grid(row=crow, column=2,columnspan=1, rowspan=2, pady=4,sticky=tk.N)

###############################################################################

        crow=crow+1
        
        self.hwtext_rho=tk.Label(top,text='Mass Density (lbm/in^3)')
        self.hwtext_rho.grid(row=crow, column=0, pady=10,sticky=tk.S) 
         
        
###############################################################################

        crow=crow+1        

        self.rhor=tk.StringVar()  
        self.rho_entry=tk.Entry(top, width = 12,textvariable=self.rhor)
        self.rho_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.rho_entry.configure(state='normal')     
                       
###############################################################################

        crow=crow+1
        
        self.hwtext_p=tk.Label(top,text='Poisson Ratio')
        self.hwtext_p.grid(row=crow, column=0, pady=10,sticky=tk.S)    
        
        self.hwtext_nsm=tk.Label(top,text='Nonstructural Mass (lbm)')
        self.hwtext_nsm.grid(row=crow, column=1, pady=10,sticky=tk.S)  

        self.hwtext_tmass=tk.Label(top,text='Total Mass (lbm)')
        self.hwtext_tmass.grid(row=crow, column=2, pady=10,sticky=tk.S)
        
###############################################################################        

        crow=crow+1        

        self.pr=tk.StringVar()  
        self.p_entry=tk.Entry(top, width = 12,textvariable=self.pr)
        self.p_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.p_entry.configure(state='normal')             
        

        self.nsmr=tk.StringVar()  
        self.nsm_entry=tk.Entry(top, width = 12,textvariable=self.nsmr)
        self.nsm_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.nsm_entry.configure(state='normal')         
        self.nsmr.set('0')        

        self.tmassr=tk.StringVar()  
        self.tmass_entry=tk.Entry(top, width = 12,textvariable=self.tmassr)
        self.tmass_entry.grid(row=crow, column=2, pady=4,sticky=tk.N) 
        self.tmass_entry.configure(state='readonly')  

###############################################################################

        crow=crow+1

        button1=tk.Button(top, text='Perform Analysis', command=self.PerformAnalysis)
        button1.grid(row=crow, column=1, padx=10, pady=10)
        button1.config( height = 2, width = 20 )        
          
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 20 )
        self.button_quit.grid(row=crow, column=2, padx=10,pady=10) 
        
        
        self.Lbu.bind("<<ListboxSelect>>", self.callback_unit)  
        self.Lbm.bind("<<ListboxSelect>>", self.callback_unit) 
        self.Lbc.bind("<<ListboxSelect>>", self.callback_clear)
        
        self.E_entry.bind("<Key>", self.callback_clear)    
        self.rho_entry.bind("<Key>", self.callback_clear)    
        self.p_entry.bind("<Key>", self.callback_clear)    
        self.diameter_entry.bind("<Key>", self.callback_clear) 
        self.T_entry.bind("<Key>", self.callback_clear) 
        self.nsm_entry.bind("<Key>", self.callback_clear)         
        
        self.change_material(self) 
        
################################################################################        

    def callback_unit(self,event):
        
        nu=int(self.Lbu.curselection()[0])
        
        if(nu==0):
            self.hwtext_diameter.config(text="Diameter (in)" )
            self.hwtext_T.config(text="Thickness (in)" )
            self.hwtext_E.config(text="Elastic Modulus (psi)" )
            self.hwtext_rho.config(text="Mass Density (lbm/in^3)" )
            self.hwtext_nsm.config(text="Nonstructural Mass (lbm)" )
            self.hwtext_tmass.config(text='Total Mass (lbm)')
        else:    
            self.hwtext_diameter.config(text="Diameter (mm)" )  
            self.hwtext_T.config(text="Thickness (mm)" )            
            self.hwtext_E.config(text="Elastic Modulus (GPa)" )            
            self.hwtext_rho.config(text="Mass Density (kg/m^3)" )            
            self.hwtext_nsm.config(text="Nonstructural Mass (kg)" ) 
            self.hwtext_tmass.config(text='Total Mass (kg)')            
            
        self.callback_clear(self)
        self.change_material(self)         
                       
################################################################################

    @classmethod
    def change_material(cls,self):  
        
        unit=1+int(self.Lbu.curselection()[0])
        material=1+int(self.Lbm.curselection()[0])

        if(unit==1):  # English
        
            if(material==1): # aluminum
                elastic_modulus=1e+007;
                mass_density=0.1;  
      
            if(material==2):  # steel
                elastic_modulus=3e+007;
                mass_density= 0.28;         
    
            if(material==3):  # copper
                elastic_modulus=1.6e+007;
                mass_density=  0.322;
    
        else:                 # metric
        
            if(material==1):  # aluminum
                elastic_modulus=70;
                mass_density=  2700;
    
            if(material==2):  # steel
                elastic_modulus=205;
                mass_density=  7700;        
    
            if(material==3):   # copper
                elastic_modulus=110;
                mass_density=  8900;
    

 
        if(material==1):  # aluminum
             poisson=0.33;  

        if(material==2):  # steel
            poisson=0.30;      

        if(material==3):  # copper
            poisson=0.33; 

        if(material<=3):

            EM="%8.4g" %elastic_modulus
            MD="%8.4g" %mass_density
            PO="%8.4g" %poisson

            self.Er.set(EM) 
            self.rhor.set(MD) 
            self.pr.set(PO) 


    def PerformAnalysis(self):
            
        unit=1+int(self.Lbu.curselection()[0])            
        BC  =1+int(self.Lbc.curselection()[0])

        E=float(self.Er.get())
        rho=float(self.rhor.get())
        mu=float(self.pr.get())
                
        T=float(self.Tr.get())               
        diameter=float(self.diameterr.get())
    
        nsm=float(self.nsmr.get()) 
    
    
        if(unit==1):
            rho=rho/386
            nsm=nsm/386
        else:
            E=E*1.0e+09
            diameter=diameter/1000
            T=T/1000

        tpi=2*pi
 
        r=diameter/2
  
        area=pi*(diameter**2)/4
 
        volume=area*T
 
        total_mass=rho*volume + nsm
        
        tgg=total_mass
        
        if(unit==1):
            tgg=tgg*386
 
        tms="%8.4g" %tgg 
 
        self.tmassr.set(tms)  
 
 
        rho=total_mass/volume
 
        den=12*(rho*T*(1-mu**2))
 
        term=sqrt(E*T**3/den)/(tpi*r**2)
 
        n=3

        fn=zeros(n,'f')
        L=zeros(n,'f')

 
        if(BC==1):  # fixed
            L[0]=10.22
            L[1]=21.26
            L[2]=34.88

        if(BC==2):  # ss
            L[0]=4.977
            L[1]=13.94
            L[2]=25.65

        if(BC==3):  # free
            L[0]=5.253
            L[1]=9.084
            L[2]=12.23    


        for i in range(0,n):
            fn[i]=L[i]*term    
    
        string1='%8.4g' %fn[0]
        string2='\n%8.4g' %fn[1]
        string3='\n%8.4g' %fn[2]

        self.textWidget.delete(1.0, tk.END)
        
        self.textWidget.insert('1.0',string1)
        self.textWidget.insert('end',string2)
        self.textWidget.insert('end',string3)       
        
        print(" ")
        print(" fn (Hz)")
        for i in range(0,n):
            print(" %8.4g" %(fn[i]))    
            
            
    
    def callback_clear(self,event):
        self.textWidget.delete(1.0, tk.END) 
        self.tmassr.set('')   
        
###############################################################################
        
def quit(root):
    root.destroy()                    