################################################################################
# program: vb_beam_bending_gui.py
# author: Tom Irvine
# version: 1.2
# date: December 5, 2014
# description:  beam bending natural frequencies & mode shapes
#               
################################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    import tkinter.messagebox as tkMessageBox
        
import matplotlib.pyplot as plt

from numpy import sin,cos,sinh,cosh,sqrt,pi,zeros,ones


class vb_beam_bending:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.32))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_beam_bending_gui.py ver 1.1  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Select Left BC')
        self.hwtext1.grid(row=crow, column=0, pady=10,sticky=tk.SE)

        self.hwtext2=tk.Label(top,text='Select Right BC')
        self.hwtext2.grid(row=crow, column=4, pady=10,sticky=tk.SW)

###############################################################################

        crow=crow+1
        
        self.Lb1 = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lb1.insert(1, "Fixed")
        self.Lb1.insert(2, "Pinned")
        self.Lb1.insert(3, "Free")
        self.Lb1.grid(row=crow, column=0, columnspan=1, padx=2,sticky=tk.NE)
        self.Lb1.select_set(0)                
        
        
        w = tk.Canvas(top, width=230, height=72)
        w.grid(row=crow, column=1, columnspan=3,padx=5)
        
        x1=0
        x2=230         

        w.create_rectangle(x1, 42, x2, 44, fill="black")        
        w.create_rectangle(x1, 36, x2, 42, fill="brown")
        
        w.create_rectangle(x1, 34, x2, 36, fill="black")
        w.create_rectangle(x1, 10, x2, 34, fill="brown")
        w.create_rectangle(x1, 8, x2, 10, fill="black")        

        w.create_rectangle(x1, 2, x2, 8, fill="brown")        
        w.create_rectangle(x1, 0, x2, 2, fill="black")       
        
        self.Lb2 = tk.Listbox(top,height=3,width=10,exportselection=0)
        self.Lb2.insert(1, "Fixed")
        self.Lb2.insert(2, "Pinned")
        self.Lb2.insert(3, "Free")
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

        self.hwtext5=tk.Label(top,text='Select Cross Section')
        self.hwtext5.grid(row=crow, column=0, pady=10)
        
        self.hwtext6=tk.Label(top,text='Select Material')
        self.hwtext6.grid(row=crow, column=1, pady=10)     
        
        self.hwtext6=tk.Label(top,text='Natural Frequencies (Hz)')
        self.hwtext6.grid(row=crow, column=2, pady=10) 
        
###############################################################################

        crow=crow+1

        self.Lbcs = tk.Listbox(top,height=4,width=20,exportselection=0)
        self.Lbcs.insert(1, "Rectangular")
        self.Lbcs.insert(2, "Pipe")
        self.Lbcs.insert(3, "Solid Cylinder")
        self.Lbcs.insert(4, "Other")        
        self.Lbcs.grid(row=crow, column=0, pady=1, padx=5,sticky=tk.N)
        self.Lbcs.select_set(0)   

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

        self.hwtext7=tk.Label(top,text='Thickness (inch)')
        self.hwtext7.grid(row=crow, column=0, pady=5)
        
        self.hwtext8=tk.Label(top,text='Elastic Modulus (lbf/in^2)')
        self.hwtext8.grid(row=crow, column=1, columnspan=1,pady=5)   
        
###############################################################################
        
        crow=crow+1

        self.cs1r=tk.StringVar()  
        self.cs1_entry=tk.Entry(top, width = 12,textvariable=self.cs1r)
        self.cs1_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.cs1_entry.configure(state='normal')  

        self.mat1r=tk.StringVar()  
        self.mat1_entry=tk.Entry(top, width = 12,textvariable=self.mat1r)
        self.mat1_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.mat1_entry.configure(state='normal')  
        self.mat1r.set('1.0e+07') 
        
        
###############################################################################

        crow=crow+1

        self.hwtext9=tk.Label(top,text='Width (inch)')
        self.hwtext9.grid(row=crow, column=0, pady=10)
        
        self.hwtext10=tk.Label(top,text='Mass Density (lbm/in^3)')
        self.hwtext10.grid(row=crow, column=1, columnspan=1, pady=5)          


###############################################################################
        
        crow=crow+1

        self.cs2r=tk.StringVar()  
        self.cs2_entry=tk.Entry(top, width = 12,textvariable=self.cs2r)
        self.cs2_entry.grid(row=crow, column=0, pady=4,sticky=tk.N) 
        self.cs2_entry.configure(state='normal')  

        self.mat2r=tk.StringVar()  
        self.mat2_entry=tk.Entry(top, width = 12,textvariable=self.mat2r)
        self.mat2_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.mat2_entry.configure(state='normal')          
        self.mat2r.set('0.1') 
        
###############################################################################
        
        crow=crow+1

        button1=tk.Button(top, text='Perform Analysis', command=self.PerformAnalysis)
        button1.grid(row=crow, column=0, padx=10, pady=10)
        button1.config( height = 2, width = 20 )        
          
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 20 )
        self.button_quit.grid(row=crow, column=1, padx=10,pady=10) 
        
        
        self.Lb1.bind("<<ListboxSelect>>", self.callback_clear)    
        self.Lb2.bind("<<ListboxSelect>>", self.callback_clear)        
        
        self.Lbu.bind("<<ListboxSelect>>", self.callback_unit)  
        self.Lbcs.bind("<<ListboxSelect>>", self.callback_cross_section)          
        self.Lbmat.bind("<<ListboxSelect>>", self.callback_material)  
        
        self.length_entry.bind("<Key>", self.callback_clear)          

        self.cs1_entry.bind("<Key>", self.callback_clear)    
        self.cs2_entry.bind("<Key>", self.callback_clear)    
        self.mat1_entry.bind("<Key>", self.callback_clear)    
        self.mat2_entry.bind("<Key>", self.callback_clear)    
        
################################################################################
    
    def callback_clear(self,event):
        self.textWidget.delete(1.0, tk.END)     
    
    
    @classmethod
    def change_cross_section(cls,self):
        
        self.cs2_entry.configure(state='normal') 
        
        nu=int(self.Lbu.curselection()[0])
        ncs=int(self.Lbcs.curselection()[0])            

        if(ncs==0):
            if(nu==0):
                self.hwtext7.config(text="Thickness (in)" )
                self.hwtext9.config(text="Width (in)" )
            else:
                self.hwtext7.config(text="Thickness (mm)" )
                self.hwtext9.config(text="Width (mm)" )

        if(ncs==1):
            if(nu==0):
                self.hwtext7.config(text="Outer Diameter (in)" )
                self.hwtext9.config(text="Wall Thickness (in)" )
            else:
                self.hwtext7.config(text="Outer Diameter (mm)" )
                self.hwtext9.config(text="Wall Thickness (mm)" )    
            
        if(ncs==2):
            self.cs2_entry.configure(state='readonly')
            self.cs2r.set(' ')               
            
            if(nu==0):
                self.hwtext7.config(text="Diameter (in)" )
                self.hwtext9.config(text=" " )
            else:
                self.hwtext7.config(text="Diameter (mm)" )
                self.hwtext9.config(text=" " )            
            
        if(ncs==3):
            if(nu==0):
                self.hwtext7.config(text="Area (in^2)")
                self.hwtext9.config(text="Area MOI (in^4)")
            else:
                self.hwtext7.config(text="Area (mm^2)")
                self.hwtext9.config(text="Area MOI (mm^4)")  

    
    def callback_cross_section(self,event):
        
        self.change_cross_section(self)
        self.callback_clear(self)
                       
    def callback_material(self,event):
        
        self.change_material(self)                         
        self.callback_clear(self)
        
        
    def callback_unit(self,event):
        
        nu=int(self.Lbu.curselection()[0])
        
        if(nu==0):
            self.hwtext4.config(text="Enter Length (in)" )
        else:    
            self.hwtext4.config(text="Enter Length (m)" )        
            
        self.change_cross_section(self)   
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
        ncs=1+int(self.Lbcs.curselection()[0])  
      
        
        LBC=1+int(self.Lb1.curselection()[0]) 
        RBC=1+int(self.Lb2.curselection()[0]) 

        E=float(self.mat1r.get())
        rho=float(self.mat2r.get())

                
        if len(self.lengthr.get()) == 0:
            tkMessageBox.showinfo("Note", "Enter Length")
            return

        L=float(self.lengthr.get())

        iflag=0

        if((LBC==2 and RBC==3) or (LBC==3 and RBC==2)): # pinned-free
            # case unavailable
            iflag=1

        if(L>1.0e-20 and L<1.0e+20):
            pass
        else:
            iflag=2


        thick=0
        width=0
        diameter=0
        wall_thick=0
        

        if(ncs==1):
            thick=float(self.cs1r.get())
            width=float(self.cs2r.get())
            
        if(ncs==2):
            diameter=float(self.cs1r.get())
            wall_thick=float(self.cs2r.get())            
            
        if(ncs==3):
            diameter=float(self.cs1r.get())
    
        if(ncs==4):
            area=float(self.cs1r.get())
            MOI=float(self.cs2r.get())       
    
 
        if(nu==1): # English
            rho=rho/386
    
        if(nu==2): # metric
            E=E*1.0e+09
            thick=thick/1000
            width=width/1000
            diameter=diameter/1000
            wall_thick=wall_thick/1000
    
    
        if(ncs==1): # rectangular
            area=thick*width
            MOI=(1./12.)*width*thick**3

    
        if(ncs==2): # pipe
            ID=diameter-2*wall_thick
            area=pi*(diameter**2-ID**2)/4.
            MOI=pi*(diameter**4-ID**4)/64.
    
        if(ncs==3): # solid cylinder
            area=pi*diameter**2/4.
            MOI=pi*diameter**4/64. 
    
        rho=rho*area   # mass per unit length
    
        mass=rho*L
        
        print(" ")
        print(" mass = %8.4g " %(mass))
#
        sq_mass=sqrt(mass)
#
        EI_term = sqrt(E*MOI/rho)
               
###

        root=zeros(n,'f')
 
        if((LBC==1 and RBC==1)or((LBC==3 and RBC==3))): # fixed-fixed or free-free
            root[0]=4.73004
            root[1]=7.8532
            root[2]=10.9956
            root[3]=14.13717

        if((LBC==1 and RBC==2) or (LBC==2 and RBC==1)): # fixed-pinned
            root[0]=3.9266
            root[1]=7.0686
            root[2]=10.2102
            root[3]=13.3518

        if((LBC==1 and RBC==3) or (LBC==3 and RBC==1)): # fixed-free
            root[0]=1.87510
            root[1]=4.69409
            root[2]=7.85476
            root[3]=10.99554

        if(LBC==2 and RBC==2): # pinned-pinned
#            print(" pinned-pinned")
#            print(" n=%d" %n)
            for i in range(0,n):
                j=i+1
                root[i]=j*pi
#                print(" r=%8.4g" %root[i])                
###        
    
        for i in range(0,n):
            beta[i]=root[i]/L
            omegan=beta[i]**2*EI_term
            fn[i]=omegan/(2*pi)            
#            print(" b=%8.4g  pi=%8.4g  EI_term=%8.4g" %(beta[i],pi,EI_term))       
 
 
        print(" ")
        print("    root     beta ")
        for i in range(0,n):
            print(" %8.4g  %8.4g" %(root[i],beta[i]))
        
##############
        
        C=zeros(n,'f')
    
        part=zeros(n,'f')
#   
        if(LBC==1 and RBC==1): # fixed-fixed
            for i in range(0,n):
                bL=root[i]
                C[i]=(sinh(bL)+sin(bL))/(cosh(bL)-cos(bL))
                arg=root[i]
                p2=(sinh(arg)-sin(arg))-C[i]*(cosh(arg)+cos(arg))
                arg=0
                p1=(sinh(arg)-sin(arg))-C[i]*(cosh(arg)+cos(arg))
                part[i]=(p2-p1)/beta[i]
        
#        ModeShape=@(arg,Co)((cosh(arg)-cos(arg))-Co*(sinh(arg)-sin(arg)))
        
            ModeShape = lambda arg,Co: ((cosh(arg)-cos(arg))-Co*(sinh(arg)-sin(arg)))        
        
            part=part*sqrt(mass/L**2)
    
#    
        if((LBC==1 and RBC==2) or (LBC==2 and RBC==1)): # fixed-pinned
 
            for i in range(0,n):
                C[i]=-(sinh(root[i])+sin(root[i]))/(cosh(root[i])+cos(root[i]))
                arg=root[i]
                p2=(cosh(arg)+cos(arg))-C[i]*(sinh(arg)-sin(arg))
                arg=0
                p1=(cosh(arg)+cos(arg))-C[i]*(sinh(arg)-sin(arg))
                part[i]=(p2-p1)/beta[i]
              
#        ModeShape=@(arg,Co)((sinh(arg)-sin(arg))+Co*(cosh(arg)-cos(arg)))
              
            ModeShape = lambda arg,Co:((sinh(arg)-sin(arg))+Co*(cosh(arg)-cos(arg)))               
              
            part=part*sqrt(mass/L**2)       
    
#   
        if((LBC==1 and RBC==3) or (LBC==3 and RBC==1)): # fixed-free
 
            for i in range(0,n):
                C[i]=-(cos(root[i])+cosh(root[i]))/(sin(root[i])+sinh(root[i]))
                arg=root[i]
                p2=(sinh(arg)-sin(arg))+C[i]*(cosh(arg)+cos(arg))
                arg=0
                p1=(sinh(arg)-sin(arg))+C[i]*(cosh(arg)+cos(arg))
                part[i]=(p2-p1)/beta[i]           
        
#        ModeShape=@(arg,Co)((cosh(arg)-cos(arg))+Co*(sinh(arg)-sin(arg)))
        
            ModeShape = lambda arg,Co:((cosh(arg)-cos(arg))+Co*(sinh(arg)-sin(arg)))
        
            part=part*sqrt(mass/L**2)
#    
        if(LBC==2 and RBC==2): # pinned-pinned
            C=ones(n)
#      
            for i in range(0,n):
                j=i+1
                part[i]=(-1/(j*pi))*sqrt(2*mass)*(cos(j*pi)-1)

#        ModeShape=@(arg,Co)(Co*sin(arg))

            ModeShape = lambda arg,Co:(Co*sin(arg))            
            
#    
        if(LBC==3 and RBC==3): # free-free
            for i in range(0,n):
                bL=root[i]
                C[i]=(-cosh(bL)+cos(bL))/(sinh(bL)+sin(bL))

#        ModeShape=@(arg,Co)((sinh(arg)+sin(arg))+Co*(cosh(arg)+cos(arg)))
        
            ModeShape = lambda arg,Co: ((sinh(arg)+sin(arg))+Co*(cosh(arg)+cos(arg)))       
    

        
        if(iflag==1):
            tkMessageBox.showinfo("Warning:", "case unavailable")
            return
    



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
        for i in range(0,n):
            print(" %8.4g" %(fn[i]))
            
         
        print(" ")       
        num=200            
            
        if(iflag !=1):
            dx=L/num
            
            x=zeros(num+1,'f')
            y=zeros(((num+1),n),'f')
            
    
            for i in range(0,num+1):
                x[i]=i*dx
        
                for j in range(0,n):
                    arg=beta[j]*x[i]
                    y[i,j]=ModeShape(arg,C[j])
                    
#                    if(j==0):
#                        print(" x=%8.4f   arg=%8.4f  C=%8.4f  y=%8.4g" %(x[i],arg,C[j],y[i,j]))
        
            for j in range(0,n):
                yy=y[:,j]
                my=max(abs(yy))   
#                print(' %8.4g' %my)
                y[:,j]=yy/my


            for j in range(0,n):
                plt.figure(j+1)
                plt.plot(x, y[:,j], linewidth=1.0)
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.grid('on')
                st=" Mode %d  fn=%8.4g Hz" %(j+1,fn[j])
                plt.title(st)
                plt.draw()

###############################################################################
        
def quit(root):
    root.destroy()                    