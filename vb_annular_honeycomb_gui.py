################################################################################
# program: vb_annular_honeycomb_gui.py
# author: Tom Irvine
# version: 1.0
# date: April 9, 2014
# description:  annular, honeycomb sandwich plate bending frequencies
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

from numpy import sqrt,pi,zeros,polyfit


class vb_annular_honeycomb:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.28))
        h = int(2.*(h*0.33))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_annular_honeycomb_gui.py ver 1.0  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext0=tk.Label(top,text='Honeycomb Sandwich annular Plate Bending Natural Frequencies ')
        self.hwtext0.grid(row=crow, column=0, columnspan=3, pady=10,sticky=tk.S)
        
        crow=crow+1        
        
        self.hwtext1=tk.Label(top,text='Select Units')
        self.hwtext1.grid(row=crow, column=0, pady=10,sticky=tk.S)

        self.hwtext2a=tk.Label(top,text='Select Outer BC')
        self.hwtext2a.grid(row=crow, column=1, pady=10,sticky=tk.S) 
        
        self.hwtext2b=tk.Label(top,text='Select Inner BC')
        self.hwtext2b.grid(row=crow, column=2, pady=10,sticky=tk.S)           

###############################################################################

        crow=crow+1
          
        self.Lbu = tk.Listbox(top,height=2,width=10,exportselection=0)
        self.Lbu.insert(1, "English")
        self.Lbu.insert(2, "Metric")
        self.Lbu.grid(row=crow, column=0, columnspan=1, pady=4, padx=10)
        self.Lbu.select_set(0) 

        self.Lbco = tk.Listbox(top,height=3,width=18,exportselection=0)
        self.Lbco.insert(1, "fixed")
        self.Lbco.insert(2, "simply-supported")
        self.Lbco.insert(3, "free")       
        self.Lbco.grid(row=crow, column=1, columnspan=1, pady=4, padx=10)
        self.Lbco.select_set(0)            
          
        self.Lbci = tk.Listbox(top,height=3,width=18,exportselection=0)
        self.Lbci.insert(1, "fixed")
        self.Lbci.insert(2, "simply-supported")
        self.Lbci.insert(3, "free")       
        self.Lbci.grid(row=crow, column=2, columnspan=1, pady=4, padx=10)
        self.Lbci.select_set(0)                
        
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
        
        self.hwtext_OD=tk.Label(top,text='Outer Diameter (in)')
        self.hwtext_OD.grid(row=crow, column=1, pady=10,sticky=tk.S)  
        
        self.hwtext_ID=tk.Label(top,text='Inner Diameter (in)')
        self.hwtext_ID.grid(row=crow, column=2, pady=10,sticky=tk.S)          
        
###############################################################################

        crow=crow+1        

        self.ODr=tk.StringVar()  
        self.OD_entry=tk.Entry(top, width = 12,textvariable=self.ODr)
        self.OD_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.OD_entry.configure(state='normal')      
        
        self.IDr=tk.StringVar()  
        self.ID_entry=tk.Entry(top, width = 12,textvariable=self.IDr)
        self.ID_entry.grid(row=crow, column=2, pady=4,sticky=tk.N) 
        self.ID_entry.configure(state='normal')             

###############################################################################

        crow=crow+1
        
        self.hwtext_E=tk.Label(top,text='Face Sheet Elastic Modulus (psi)')
        self.hwtext_E.grid(row=crow, column=0, pady=10,sticky=tk.S) 
        
        self.hwtext_T_top=tk.Label(top,text='Top Sheet Thickness (in)')
        self.hwtext_T_top.grid(row=crow, column=1, pady=10,sticky=tk.S) 
        
        self.hwtext_rho_cr=tk.Label(top,text='Core Mass Density (lbm/in^3)')
        self.hwtext_rho_cr.grid(row=crow, column=2, pady=10,sticky=tk.S) 
        
        self.hwtext_fn=tk.Label(top,text='Results: Natural Freq (Hz)')
        self.hwtext_fn.grid(row=crow, column=3, padx=5, pady=10,sticky=tk.S) 
        
###############################################################################

        crow=crow+1  
        
        self.Er=tk.StringVar()  
        self.E_entry=tk.Entry(top, width = 12,textvariable=self.Er)
        self.E_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.E_entry.configure(state='normal')  
         
        self.T_top_r=tk.StringVar()  
        self.T_top_entry=tk.Entry(top, width = 12,textvariable=self.T_top_r)
        self.T_top_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.T_top_entry.configure(state='normal')     

        self.rho_cr_r=tk.StringVar()  
        self.rho_cr_entry=tk.Entry(top, width = 12,textvariable=self.rho_cr_r)
        self.rho_cr_entry.grid(row=crow, column=2, pady=4,sticky=tk.N) 
        self.rho_cr_entry.configure(state='normal')
        
        self.textWidget = tk.Text(top, width=10, height = 5,font = "TkDefaultFont 9")
        self.textWidget.grid(row=crow, column=3,columnspan=1, rowspan=2, pady=4,sticky=tk.N)

###############################################################################

        crow=crow+1
        
        self.hwtext_rho_fc=tk.Label(top,text='Face Sheet Mass Density (lbm/in^3)')
        self.hwtext_rho_fc.grid(row=crow, column=0, pady=10,sticky=tk.S) 
        
        self.hwtext_T_core=tk.Label(top,text='Core Thickness (in)')
        self.hwtext_T_core.grid(row=crow, column=1, pady=10,sticky=tk.S) 
         
        self.hwtext_nsm=tk.Label(top,text='Nonstructural Mass (lbm)')
        self.hwtext_nsm.grid(row=crow, column=2, pady=10,sticky=tk.S)           
        
###############################################################################

        crow=crow+1        

        self.rho_fc_r=tk.StringVar()  
        self.rho_fc_entry=tk.Entry(top, width = 12,textvariable=self.rho_fc_r)
        self.rho_fc_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.rho_fc_entry.configure(state='normal')     

        self.T_core_r=tk.StringVar()  
        self.T_core_entry=tk.Entry(top, width = 12,textvariable=self.T_core_r)
        self.T_core_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.T_core_entry.configure(state='normal') 

        self.nsmr=tk.StringVar()  
        self.nsm_entry=tk.Entry(top, width = 12,textvariable=self.nsmr)
        self.nsm_entry.grid(row=crow, column=2, pady=4,sticky=tk.N) 
        self.nsm_entry.configure(state='normal')         
        self.nsmr.set('0') 
                       
###############################################################################

        crow=crow+1
        
        self.hwtext_p=tk.Label(top,text='Face Sheet Poisson Ratio')
        self.hwtext_p.grid(row=crow, column=0, pady=10,sticky=tk.S)    
        
        self.hwtext_T_bot=tk.Label(top,text='Bottom Sheet Thickness (in)')
        self.hwtext_T_bot.grid(row=crow, column=1, pady=10,sticky=tk.S) 

        self.hwtext_tmass=tk.Label(top,text='Total Mass (lbm)')
        self.hwtext_tmass.grid(row=crow, column=2, pady=10,sticky=tk.S)
        
###############################################################################        

        crow=crow+1        

        self.pr=tk.StringVar()  
        self.p_entry=tk.Entry(top, width = 12,textvariable=self.pr)
        self.p_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.p_entry.configure(state='normal')             
               
        self.T_bot_r=tk.StringVar()  
        self.T_bot_entry=tk.Entry(top, width = 12,textvariable=self.T_bot_r)
        self.T_bot_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.T_bot_entry.configure(state='normal')                

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
        self.Lbco.bind("<<ListboxSelect>>", self.callback_clear)
        self.Lbci.bind("<<ListboxSelect>>", self.callback_clear)        
        
        
        self.E_entry.bind("<Key>", self.callback_clear)    
        self.rho_fc_entry.bind("<Key>", self.callback_clear) 
        self.rho_cr_entry.bind("<Key>", self.callback_clear)            
        self.p_entry.bind("<Key>", self.callback_clear)    
        self.OD_entry.bind("<Key>", self.callback_clear) 
        self.ID_entry.bind("<Key>", self.callback_clear)         
        self.T_top_entry.bind("<Key>", self.callback_clear) 
        self.nsm_entry.bind("<Key>", self.callback_clear)         
        
        self.change_material(self) 
        
################################################################################        

    def callback_unit(self,event):
        
        nu=int(self.Lbu.curselection()[0])
        
        if(nu==0):
            self.hwtext_OD.config(text="Outer Diameter (in)" )
            self.hwtext_ID.config(text="Inner Diameter (in)" )            
            self.hwtext_T_top.config(text="Top Sheet Thickness (in)" )
            self.hwtext_T_core.config(text="Core Thickness (in)" )
            self.hwtext_T_bot.config(text="Top Sheet Thickness (in)" )            
            self.hwtext_E.config(text="Bottom Sheet Elastic Modulus (psi)" )
            self.hwtext_rho_fc.config(text="Face Sheet Mass Density (lbm/in^3)" )
            self.hwtext_rho_cr.config(text="Face Sheet Mass Density (lbm/in^3)" )            
            self.hwtext_nsm.config(text="Nonstructural Mass (lbm)" )
            self.hwtext_tmass.config(text='Total Mass (lbm)')
        else:    
            self.hwtext_OD.config(text="Outer Diameter (mm)" )  
            self.hwtext_ID.config(text="Inner Diameter (mm)" )             
            self.hwtext_T_top.config(text="Top Sheet Thickness (mm)" )  
            self.hwtext_T_core.config(text="Core Thickness (mm)" )              
            self.hwtext_T_bot.config(text="Bottom Sheet Thickness (mm)" )              
            self.hwtext_E.config(text="Face Sheet Elastic Modulus (GPa)" )            
            self.hwtext_rho_fc.config(text="Face Sheet Mass Density (kg/m^3)" )       
            self.hwtext_rho_cr.config(text="Face Sheet Mass Density (kg/m^3)" )            
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
            self.rho_fc_r.set(MD) 
            self.pr.set(PO) 


    def PerformAnalysis(self):
            
        unit=1+int(self.Lbu.curselection()[0])            
        outer_BC  =1+int(self.Lbco.curselection()[0])
        inner_BC  =1+int(self.Lbci.curselection()[0])

        E=float(self.Er.get())
        rho_fc=float(self.rho_fc_r.get())
        rho_cr=float(self.rho_cr_r.get())        
        mu=float(self.pr.get())
                
        t1=float(self.T_top_r.get())     
        hc=float(self.T_core_r.get())  
        t2=float(self.T_bot_r.get())  
          
        OD=float(self.ODr.get())
        ID=float(self.IDr.get())        
    
        nsm=float(self.nsmr.get()) 
    
    
        if(unit==1):
            rho_fc=rho_fc/386
            rho_cr=rho_cr/386            
            nsm=nsm/386
        else:
            E=E*1.0e+09
            OD=OD/1000
            ID=ID/1000
            t1=t1/1000
            hc=hc/1000
            t2=t2/1000            
##

        print(" hc=%8.4g t1=%8.4g t2=%8.4g" %(hc,t1,t2))  

        h=hc+(0.5)*(t1+t2)
        
        print(" h=%8.4g " %h)        

        num=t1*t2*h**2
        den=t1+t2
        
        print(" num=%8.4g " %num)
        print(" den=%8.4g " %den)

        D=(E/(1-mu**2))*num/den

        print(" D=%8.4g " %D)

        tpi=2*pi

        r=OD/2


        area=pi*(OD**2-ID**2)/4

        rho_area=rho_fc*(t1+t2) + rho_cr*hc + nsm/area;

        total_mass=rho_area*area

        term=sqrt(D/rho_area)/(tpi*r**2)
        
        print(" term=%8.4g " %term)

        
        tgg=total_mass
        
        if(unit==1):
            tgg=tgg*386
 
        tms="%8.4g" %tgg 
 
        self.tmassr.set(tms)  

##
 
        x=zeros(4,'f')
        y1=zeros(4,'f')
        y2=zeros(4,'f')

        x=[ 0.1, 0.3, 0.5, 0.7 ]

        if(outer_BC==1 and inner_BC==1):  # fixed-fixed
            y1=[ 27.3,  45.2,  89.2,  248]
            y2=[ 28.4,  45.6,  90.2,  249 ]


        if(outer_BC==1 and inner_BC==2):  # fixed-ss
            y1=[ 22.6,  33.7,  63.9,  175] 
            y2=[ 25.1,  35.8,  65.4,  175 ]


        if(outer_BC==1 and inner_BC==3):  # fixed-free
            y1=[ 10.2,  11.4,   17.7,  43.1]
            y2=[ 21.1,  19.5,   22.1,  45.3 ]


        if(outer_BC==2 and inner_BC==1):  # ss-fixed
            y1=[ 17.8,  29.9,  59.8,   168]
            y2=[ 19.0,  31.4,  61.0,   170]
 

        if(outer_BC==2 and inner_BC==2):  # ss-ss
            y1=[ 14.5,  21.1,   40.0,  110]  
            y2=[ 16.7,  23.3,   41.8,  112]


        if(outer_BC==2 and inner_BC==3):  # ss-free
            y1=[ 4.86,  4.66,   5.07,   6.94] 
            y2=[ 13.9,  12.8,   11.6,  13.3 ]


        if(outer_BC==3 and inner_BC==1):  # free-fixed
            y1=[ 4.23,    6.66,   13.0,   37.0] 
            y2=[ 3.14,    6.33,   13.3,   37.5]


        if(outer_BC==3 and inner_BC==2):  # free-ss
            y1=[ 3.45,   3.42,    4.11,    6.18] 
            y2=[ 2.30,   3.32,    4.86,    8.34]


        if(outer_BC==3 and inner_BC==3):  # free-free
            y1=[ 5.30,  4.91,   4.28,  3.57] 
            y2=[ 8.77,  8.36,   9.32,  13.2]


        iflag=0

        z=ID/OD

        if(z>=1):
            iflag=1
            tk.tkMessageBox.showinfo("Warning", "Switch inner & outer diameters")


        if(z<0.1):
            iflag=2
            tk.tkMessageBox.showinfo("Warning", "Calculation unavialable for diameter ratio <0.1")            

##
        if(iflag==0):
            
            n=2 

            fn=zeros(n,'f')            

            p = polyfit(x,y1,3)
            L=p[0]*z**3+p[1]*z**2+p[2]*z+p[3]        
            fn[0]=L*term

            p = polyfit(x,y2,3)            
            L=p[0]*z**3+p[1]*z**2+p[2]*z+p[3]            
            fn[1]=L*term            

            
            fn.sort()       


    
            string1='%8.4g' %fn[0]
            string2='\n%8.4g' %fn[1]

            self.textWidget.delete(1.0, tk.END)
        
            self.textWidget.insert('1.0',string1)
            self.textWidget.insert('end',string2)     
        
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