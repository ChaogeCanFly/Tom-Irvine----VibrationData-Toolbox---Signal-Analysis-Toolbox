###########################################################################
# program: vb_sine_sweep_gui.py
# author: Tom Irvine
# version: 1.2
# date: May 12, 2014
# 
###############################################################################

from __future__ import print_function

from numpy import sin,log,log10,zeros,ceil,linspace,logspace,pi

import matplotlib.pyplot as plt

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

class vb_sine_sweep:
    def __init__(self,parent):
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.24))
        self.master.geometry("%dx%d+0+0" % (w, h))
        

        self.master.title("vb_sine_sweep.py  ver 1.2  by Tom Irvine")        
        
        crow=0
        
        self.hwtext1=tk.Label(top,text='Sweep Type')
        self.hwtext1.grid(row=crow, column=0, pady=7) 

        self.hwtext2=tk.Label(top,text='Sweep Direction')
        self.hwtext2.grid(row=crow, column=1, pady=7) 

        self.hwtext3=tk.Label(top,text='Number of Coordinates')
        self.hwtext3.grid(row=crow, column=2, pady=7) 

        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=2,width=15,exportselection=0)
        self.Lb1.insert(1, "Log")
        self.Lb1.insert(2, "Linear")      
        self.Lb1.grid(row=crow, column=0, columnspan=1, padx=5, pady=4,sticky=tk.N)
        self.Lb1.select_set(0)    

        self.Lb2 = tk.Listbox(top,height=2,width=15,exportselection=0)
        self.Lb2.insert(1, "upward")
        self.Lb2.insert(2, "downward")      
        self.Lb2.grid(row=crow, column=1, columnspan=1, padx=5, pady=4,sticky=tk.N)
        self.Lb2.select_set(0)  

        self.Lb3 = tk.Listbox(top,height=4,width=5,exportselection=0)
        self.Lb3.insert(1, "2")
        self.Lb3.insert(2, "3")
        self.Lb3.insert(3, "4")
        self.Lb3.insert(4, "5")        
        self.Lb3.grid(row=crow, column=2, columnspan=1, padx=5, pady=4,sticky=tk.N)
        self.Lb3.select_set(0) 

###############################################################################

        crow=crow+1
        
        self.hwtext4=tk.Label(top,text='Coordinates')
        self.hwtext4.grid(row=crow, column=0, pady=7)
        
        crow=crow+1
        
        self.hwtext5=tk.Label(top,text='Freq (Hz)')
        self.hwtext5.grid(row=crow, column=0, pady=7,sticky=tk.E)  
        
        self.hwtext6=tk.Label(top,text='Accel (G)')
        self.hwtext6.grid(row=crow, column=1, pady=7,sticky=tk.W)   

###############################################################################

        crow=crow+1

        self.f1r=tk.StringVar()  
        self.f1_entry=tk.Entry(top, width = 12,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=0,sticky=tk.E) 
        self.f1_entry.configure(state='normal')        

        self.a1r=tk.StringVar()  
        self.a1_entry=tk.Entry(top, width = 12,textvariable=self.a1r)
        self.a1_entry.grid(row=crow, column=1,sticky=tk.W) 
        self.a1_entry.configure(state='normal')

        crow=crow+1
        
        self.f2r=tk.StringVar()  
        self.f2_entry=tk.Entry(top, width = 12,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=0,sticky=tk.E) 
        self.f2_entry.configure(state='normal')        

        self.a2r=tk.StringVar()  
        self.a2_entry=tk.Entry(top, width = 12,textvariable=self.a2r)
        self.a2_entry.grid(row=crow, column=1,sticky=tk.W) 
        self.a2_entry.configure(state='normal')

        crow=crow+1        

        self.f3r=tk.StringVar()  
        self.f3_entry=tk.Entry(top, width = 12,textvariable=self.f3r)
        self.f3_entry.grid(row=crow, column=0,sticky=tk.E) 
        self.f3_entry.configure(state='disabled')        

        self.a3r=tk.StringVar()  
        self.a3_entry=tk.Entry(top, width = 12,textvariable=self.a3r)
        self.a3_entry.grid(row=crow, column=1,sticky=tk.W) 
        self.a3_entry.configure(state='disabled')

        crow=crow+1
        
        self.f4r=tk.StringVar()  
        self.f4_entry=tk.Entry(top, width = 12,textvariable=self.f4r)
        self.f4_entry.grid(row=crow, column=0,sticky=tk.E) 
        self.f4_entry.configure(state='disabled')        

        self.a4r=tk.StringVar()  
        self.a4_entry=tk.Entry(top, width = 12,textvariable=self.a4r)
        self.a4_entry.grid(row=crow, column=1,sticky=tk.W) 
        self.a4_entry.configure(state='disabled')

        crow=crow+1
        
        self.f5r=tk.StringVar()  
        self.f5_entry=tk.Entry(top, width = 12,textvariable=self.f5r)
        self.f5_entry.grid(row=crow, column=0,sticky=tk.E) 
        self.f5_entry.configure(state='disabled')        

        self.a5r=tk.StringVar()  
        self.a5_entry=tk.Entry(top, width = 12,textvariable=self.a5r)
        self.a5_entry.grid(row=crow, column=1,sticky=tk.W) 
        self.a5_entry.configure(state='disabled')
        
        
        self.Lb3.bind("<<ListboxSelect>>", self.callback_coordinates) 


###############################################################################

        crow=crow+1
        
        self.hwtext11=tk.Label(top,text='Sample Rate (Hz)')
        self.hwtext11.grid(row=crow, column=0, pady=7) 

        self.hwtext12=tk.Label(top,text='Duration (sec)')
        self.hwtext12.grid(row=crow, column=1, pady=7) 

        self.hwtext13=tk.Label(top,text='Number of Octaves')
        self.hwtext13.grid(row=crow, column=2, pady=7)         
        
###############################################################################        

        crow=crow+1
        
        self.SRr=tk.StringVar()  
        self.SR_entry=tk.Entry(top, width = 12,textvariable=self.SRr)
        self.SR_entry.grid(row=crow, column=0) 
        self.SR_entry.configure(state='normal')        

        self.DURr=tk.StringVar()  
        self.dur_entry=tk.Entry(top, width = 12,textvariable=self.DURr)
        self.dur_entry.grid(row=crow, column=1) 
        self.dur_entry.configure(state='normal')        
        
        self.NOCTr=tk.StringVar()  
        self.NOCT_entry=tk.Entry(top, width = 12,textvariable=self.NOCTr)
        self.NOCT_entry.grid(row=crow, column=2) 
        self.NOCT_entry.configure(state='readonly')
        
###############################################################################   

        crow=crow+1
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate_main)
        self.button_calculate.config( height = 2, width = 15)
        self.button_calculate.grid(row=crow, column=0,padx=2, pady=10,sticky=tk.S) 
         
        self.button_sav = tk.Button(top, text="Export Time History", command=self.export_fd)
        self.button_sav.config( height = 2, width = 16,state = 'disabled' )
        self.button_sav.grid(row=crow, column=1, padx=2,pady=10,sticky=tk.S)         

            
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2, padx=2,pady=10,sticky=tk.S) 
        
        
###############################################################################   

    def calculate_main(self):
        
        ntype=1+int(self.Lb1.curselection()[0]) 
        ndir =1+int(self.Lb2.curselection()[0])         
        n3=int(self.Lb3.curselection()[0])         
        
        tmax=float(self.DURr.get())
        sr=float(self.SRr.get())

        dt=1/sr 
        
        n=n3+2
        N=n
        
        freq=zeros(n,'f')
        amp =zeros(n,'f')        
        
        
        freq[0]=float(self.f1r.get())
        amp[0]=float(self.a1r.get())
        
        freq[1]=float(self.f2r.get())
        amp[1]=float(self.a2r.get())
        
        
        if(n>=3):            
            freq[2]=float(self.f3r.get())
            amp[2]=float(self.a3r.get())           
            
        if(n>=4):
            freq[3]=float(self.f4r.get())
            amp[3]=float(self.a4r.get())               
            
        if(n>=5):    
            freq[4]=float(self.f5r.get())
            amp[4]=float(self.a5r.get())  

###

        fff=freq
        aaa=amp

        if(max(fff)>(sr/10.)):
            sr=max(fff)*10
            dt=1/sr
            
            buf1= "%9.6g" %sr  
            self.SRr.set(buf1)  
            
            tkMessageBox.showinfo("Note","Sample Rate Increased")
       
###       
        num=N
        f1 = fff[0]
        f2 = fff[num-1]
        
        ns=int(ceil(tmax*sr))

        oct=log(f2/f1)/log(2.)     
        
        buf1= "%7.3g" %oct  
        self.NOCTr.set(buf1)  
        
        ntimes = ns
#        cycles=0.

        tpi=2.*pi        

        if(ntype==2):        # linear
            rate=(f2-f1)/tmax
        else:                # log
            rate=oct/tmax

        maxn=20000000

        if(ntimes>maxn):
            ntimes=maxn
            tmax=ntimes*dt   
            
            tkMessageBox.showwarning("Warning","Time history truncated")            

    
        self.TT=linspace(0,tmax,ntimes) 
        
        self.TT=self.TT-self.TT[0]

        a = zeros(ntimes,'f')
        arg = zeros(ntimes,'f')
        freq = zeros(ntimes,'f')

        if(ntype==2):  # linear
#
# 0.5 factor is necessary to obtain correct number of cycles for linear case.
#
#           fspectral= (     rate*t ) + f1
#        
            fmax=0.5*(f2-f1)+f1
            freq=linspace(f1,fmax,ntimes)     
#
        else:  # log
#  
#           fspectral = f1*pow(2.,rate*t)
#
            for i in range(0,ntimes):
                arg[i]=-1.+2**(rate*self.TT[i])        

###

        if(ntype==2):           # linear
            arg=tpi*freq*self.TT
        else:                   # log
            arg=tpi*f1*arg/(rate*log(2)) 

        ntimes=len(a)

        if(ntype==2):           # linear
            spectral=linspace(f1,f2,ntimes) 
        else: 
            f1=log10(f1)
            f2=log10(f2)
            spectral=logspace(f1,f2,ntimes)         

###

        limit=len(fff)-1;
        amplitude=zeros(ntimes,'f')
        
        for i in range(0,ntimes):
            for j in range(0,limit):
                if(fff[j]<=spectral[i] and fff[j+1]>=spectral[i]):

                    if(aaa[j]==a[j-1]):
                        amplitude[i]=aaa[j]
                        break                        
                    else:    
                        x=spectral[i]-fff[j]
                        L=fff[j+1]-fff[j]
                        c2=x/L
                        c1=1-x/L
                        amplitude[i]=c1*aaa[j]+c2*aaa[j+1]
                        break

###

        self.a=sin(arg)

        self.a[0]=0.
        self.a=self.a*amplitude
#        self.TT=self.TT-self.TT[0]
   
        if(ndir==2):             # reverse order
            self.a=self.a[::-1] 
        
###
        
        self.button_sav.config(state = 'normal')


        plt.ion()
        plt.clf()   
        plt.figure(1)
        
        n=len(self.a)
        
        if(n<=500000):

            plt.plot(self.TT, self.a, linewidth=1.0,color='b')     # disregard error
       
        else:
            
            win = tk.Toplevel()
            from vb_plot_large_data_array_gui import vb_plot_large_data_array        
            vb_plot_large_data_array(win,self.TT,self.a,'Time (sec)','Accel (G)','Sine Sweep Time History',1)   
        
#            tkMessageBox.showinfo("Note"," Plot large data set with * due to Matplotlib limitations. \n Zoom function is ineffective.")
#            plt.plot(self.TT, self.a,'b*')     # disregard error            
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel('Accel (G)')  
        plt.title('Sine Sweep Time History')
    
        plt.draw()          
        
###############################################################################   
        
    def callback_coordinates(self,event):
        self.f3_entry.configure(state='disabled')
        self.a3_entry.configure(state='disabled')
        self.f4_entry.configure(state='disabled')
        self.a4_entry.configure(state='disabled')
        self.f5_entry.configure(state='disabled')
        self.a5_entry.configure(state='disabled')   
        
        n=int(self.Lb3.curselection()[0])
        
        n=n+2
        
        if(n>=3):
            self.f3_entry.configure(state='normal')
            self.a3_entry.configure(state='normal')
            
        if(n>=4):
            self.f4_entry.configure(state='normal')
            self.a4_entry.configure(state='normal')            
            
        if(n>=5):    
            self.f5_entry.configure(state='normal')
            self.a5_entry.configure(state='normal')
         
         
###############################################################################
    
    def export_fd(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output time history filename: ")       
        output_file = output_file_path.rstrip('\n')
        self.num=len(self.TT)
        WriteData2(self.num,self.TT,self.a,output_file)          

###############################################################################

def quit(root):
    root.destroy()                    