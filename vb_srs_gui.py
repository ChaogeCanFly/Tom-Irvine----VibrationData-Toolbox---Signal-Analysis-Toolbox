###########################################################################
# program: srs_gui.py
# author: Tom Irvine
# Email: tom@irvinemail.org
# version: 1.9
# date: August 7, 2018
# description:  shock response spectrum for base excitation
#
###########################################################################
# 
# Note:  for use within Spyder IDE, set: 
#    
# Run > Configuration > Interpreter >
#    
# Excecute in an external system terminal
#
################################################################################


from __future__ import print_function
    
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
    

import numpy as np

import matplotlib.pyplot as plt

from scipy.signal import lfilter

from vb_utilities import WriteData2,WriteData3,sample_rate_check,\
                                                    read_two_columns_from_dialog

################################################################################

class vb_SRS:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
#        self.master.minsize(600,600)
#        self.master.geometry("600x600")
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.22))
        h = int(2.*(h*0.27))
        self.master.geometry("%dx%d+0+0" % (w, h))
       

        self.master.title("vb_srs_gui.py ver 1.9  by Tom Irvine")         
        
        self.num=0
        self.num_fn=0
        
        self.a=[]
        self.b=[]
        self.dt=0
        self.sr=0  
        self.a_pos=[]
        self.a_neg=[]
        self.a_abs=[]
        self.pv_pos=[]
        self.pv_neg=[]
        self.pv_abs=[]    
        self.rd_pos=[]
        self.rd_neg=[]
        self.rd_abs=[] 
        self.fn=[] 
        self.omega=[]
        self.damp=0        
        
        self.hwtext1=tk.Label(top,text='Shock Response Spectrum for Base Excitation')
        self.hwtext1.grid(row=0, column=0, columnspan=6, pady=10,sticky=tk.W)

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & accel(G)')
        self.hwtext2.grid(row=1, column=0, columnspan=6, pady=10,sticky=tk.W)

###############################################################################

        self.button_read = tk.Button(top, text="Read Input File", command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=2, column=0,columnspan=1, pady=20,sticky=tk.W)  

        self.hwtextQ=tk.Label(top,text='Q=')
        self.hwtextQ.grid(row=2, column=1,padx=1,sticky=tk.E)

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 5,textvariable=self.Qr)
        self.Q_entry.grid(row=2, column=2,sticky=tk.W)

###############################################################################

        self.hwtextLbx=tk.Label(top,text='Select Units')
        self.hwtextLbx.grid(row=3, column=0,padx=3)

        self.hwtextLbx=tk.Label(top,text='SRS Plot Type')
        self.hwtextLbx.grid(row=3, column=1,padx=5)

###############################################################################

        crow=4

        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "G, in/sec, in")
        self.Lb1.insert(2, "G, cm/sec, mm")
        self.Lb1.grid(row=crow, column=0, pady=1)
        self.Lb1.select_set(0) 

        self.Lb2 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb2.insert(1, "Pos & Neg")
        self.Lb2.insert(2, "Absolute")
        self.Lb2.grid(row=crow, column=1,padx=5, pady=1)
        self.Lb2.select_set(0) 

###############################################################################

        crow=5

        self.hwtextf1=tk.Label(top,text='Min Freq (Hz)')
        self.hwtextf1.grid(row=crow, column=0,padx=5, pady=8)

        self.hwtextf2=tk.Label(top,text='Max Freq (Hz)')
        self.hwtextf2.grid(row=crow, column=1,padx=5, pady=8)

###############################################################################

        crow=6

        self.f1r=tk.StringVar()  
        self.f1r.set('')  
        self.f1_entry=tk.Entry(top, width = 8,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=0,padx=5, pady=1)

        self.f2r=tk.StringVar()  
        self.f2r.set('')  
        self.f2_entry=tk.Entry(top, width = 8,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=1,padx=5, pady=1)

###############################################################################

        crow=7

        self.button_calculate = tk.Button(top, text="Calculate", command=self.srs_calculation)
        self.button_calculate.config( height = 2, width = 18,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=1,padx=3, pady=20) 
        
        self.button_tripartite = tk.Button(top, text="Plot Tripartite", command=self.tripartite)
        self.button_tripartite.config( height = 2, width = 18,state = 'disabled')
        self.button_tripartite.grid(row=crow, column=1,columnspan=1,padx=3, pady=20)        
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))

        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=3,pady=20)

################################################################################

        crow=8

        self.hwtextext_exsrs=tk.Label(top,text='Export SRS Data')
        self.hwtextext_exsrs.grid(row=crow, column=0,pady=10)  
        self.hwtextext_exsrs.config(state = 'disabled')

################################################################################
    
        crow=9

        self.button_sa = tk.Button(top, text="Acceleration", command=self.export_accel)
        self.button_sa.config( height = 2, width = 15,state = 'disabled' )
        self.button_sa.grid(row=crow, column=0,columnspan=1, pady=3, padx=1)  

        self.button_spv = tk.Button(top, text="Pseudo Velocity", command=self.export_pv)
        self.button_spv.config( height = 2, width = 15,state = 'disabled' )
        self.button_spv.grid(row=crow, column=1,columnspan=1, pady=3, padx=1) 

        self.button_srd = tk.Button(top, text="Rel Disp", command=self.export_rd)
        self.button_srd.config( height = 2, width = 15,state = 'disabled' )
        self.button_srd.grid(row=crow, column=2,columnspan=1, pady=3, padx=1) 
            
################################################################################            

    def read_data(self):            
            
        try:    
            self.a,self.b,self.num=\
                read_two_columns_from_dialog('Select Acceleration File',self.master)
        except:
            tkMessageBox.showwarning("Warning","Input file must have two columns with no header lines")
        
        
        dur=self.a[self.num-1]-self.a[0]
        self.dt=dur/float(self.num)
        
        self.sr=1./self.dt
        
        self.sr,self.dt=sample_rate_check(self.a,self.b,self.num,self.sr,self.dt)
        
        plt.ion()
        plt.clf()
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel('Accel (G)')  
        plt.title('Base Input Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')  
        self.button_tripartite.config(state =  'disabled')         
   

    def srs_calculation(self):  

        self.Q=float(self.Qr.get())
        self.damp=1./(2.*self.Q);

        f1=float(self.f1r.get())
        f2=float(self.f2r.get())
           
        oct=1./12.
        
        fmax=min([f2,self.sr/8.])
        
        noct=np.log(fmax/f1)/np.log(2)
        
        self.num_fn=int(np.ceil(noct*12))
        
        self.fn=np.zeros(self.num_fn,'f')
         
        self.fn[0]=f1    
        for j in range(1,int(self.num_fn)):
            self.fn[j]=self.fn[j-1]*(2.**oct)
                    
        self.omega=2*np.pi*self.fn
    

    
        self.a_pos,self.a_neg,self.a_abs= \
               vb_SRS.accel_SRS(self.b,self.num_fn,self.omega,self.damp,self.dt) 
               
        nLb1= int(self.Lb1.curselection()[0])              
        
        self.rd_pos,self.rd_neg,self.rd_abs,self.pv_pos,self.pv_neg,self.pv_abs=\
               self.rd_SRS(self.b,self.num_fn,self.omega,self.damp,self.dt,nLb1)        
        
           
        n= int(self.Lb2.curselection()[0]) 

        plt.ion()
        plt.close(2)
        plt.figure(2)
        
        if(n==0):    
            plt.plot(self.fn, self.a_pos, label="positive")
            plt.plot(self.fn, self.a_neg, label="negative")
            plt.legend(loc="upper left")      
        else:
            plt.plot(self.fn, self.a_abs, linewidth=1.0,color='b')        
   
        astr='Acceleration'
    
        title_string= astr + ' Shock Response Spectrum Q='+str(self.Q)     
   
        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= astr +' Shock Response Spectrum Q='+str(i)
                break
       
        plt.grid(True)
        plt.xlabel('Natural Frequency (Hz)')
        plt.ylabel('Peak Accel (G)')   
        
        plt.title(title_string)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim([f1,f2])
        plt.grid(True,which="major",ls="-")
        plt.grid(True,which="minor",ls="--")          
            
        plt.draw()
    
        m= int(self.Lb1.curselection()[0])

        self.unit=m
    
        plt.ion()
        plt.close(3)
        plt.figure(3)

        if(n==0):    
            plt.plot(self.fn, self.pv_pos, label="positive")
            plt.plot(self.fn, self.pv_neg, label="negative")
            plt.legend(loc="upper left")      
        else:
            plt.plot(self.fn, self.pv_abs, linewidth=1.0,color='b')        # disregard error
   
        astr='Pseudo Velocity'
    
        title_string= astr + ' Shock Response Spectrum Q='+str(self.Q)     
   
        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= astr +' Shock Response Spectrum Q='+str(i)
                break
       
        plt.grid(True)
        plt.xlabel('Natural Frequency (Hz)')
    
        if(m==0):
            plt.ylabel('Peak Vel (in/sec)') 
        else:
            plt.ylabel('Peak Vel (cm/sec)') 
        
        plt.title(title_string)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim([f1,f2])
        plt.grid(True,which="major",ls="-")
        plt.grid(True,which="minor",ls="--")          
            
        plt.draw()    
    
        plt.ion()
        plt.close(4)
        plt.figure(4)

        if(n==0):    
            plt.plot(self.fn, self.rd_pos, label="positive")
            plt.plot(self.fn, self.rd_neg, label="negative")
            plt.legend(loc="upper right")      
        else:
            plt.plot(self.fn, self.rd_abs, linewidth=1.0,color='b')   
   
        astr='Relative Displacement'
    
        title_string= astr + ' Shock Response Spectrum Q='+str(self.Q)     
   
        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= astr +' Shock Response Spectrum Q='+str(i)
                break
       
        plt.grid(True)
        plt.xlabel('Natural Frequency (Hz)')
    
        if(m==0):
            plt.ylabel('Peak Rel Disp (in)') 
        else:
            plt.ylabel('Peak Rel Disp (mm)') 
        
        plt.title(title_string)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim([f1,f2])
        plt.grid(True,which="major",ls="-")
        plt.grid(True,which="minor",ls="--")  
            
        plt.draw()    

        self.hwtextext_exsrs.config(state = 'normal')
        self.button_sa.config(state = 'normal')
        self.button_spv.config(state = 'normal')    
        self.button_srd.config(state = 'normal')

        self.button_tripartite.config(state = 'normal') 

################################################################################

    @classmethod    
    def accel_SRS(cls,b,num_fn,omega,damp,dt):
        
        a_pos=np.zeros(num_fn,'f')
        a_neg=np.zeros(num_fn,'f')
        a_abs=np.zeros(num_fn,'f')
    
        ac=np.zeros(3)     
        bc=np.zeros(3)

              
        for j in range(0,int(num_fn)):
            
            omegad=omega[j]*np.sqrt(1.-(damp**2))
#
#  bc coefficients are applied to the excitation
            
            E=np.exp(-damp*omega[j]*dt)
            K=omegad*dt
            C=E*np.cos(K)
            S=E*np.sin(K)
            Sp=S/K

   
            ac[0]=1.   
            ac[1]=-2.*C
            ac[2]=+E**2   
        
            bc[0]=1.-Sp
            bc[1]=2.*(Sp-C)
            bc[2]=E**2-Sp
                             
            resp=lfilter(bc, ac, b, axis=-1, zi=None)            
#
            a_pos[j]= max(resp)
            a_neg[j]= abs(min(resp)) 
            a_abs[j]=max(abs(resp))  
            
        return a_pos,a_neg,a_abs    

#        print (" %8.4g  %8.4g " %(fn[j],a_abs[j]))          

    @classmethod  
    def rd_SRS(cls,b,num_fn,omega,damp,dt,n):
        
        rd_pos=np.zeros(num_fn,'f')
        rd_neg=np.zeros(num_fn,'f')
        rd_abs=np.zeros(num_fn,'f')
    
        ac=np.zeros(3)     
        bc=np.zeros(3)   

        for j in range(0,int(num_fn)):
            
            omegad=omega[j]*np.sqrt(1.-(damp**2))            
            
            E =np.exp(  -damp*omega[j]*dt)
            E2=np.exp(-2*damp*omega[j]*dt)
             
            K=omegad*dt
            C=E*np.cos(K)
            S=E*np.sin(K)
        
            ac[0]=1   
            ac[1]=-2*C
            ac[2]=+E**2         
            
            Omr=(omega[j]/omegad)
            Omt=omega[j]*dt
            
            P=2*damp**2-1
            
            b00=2*damp*(C-1)
            b01=S*Omr*P
            b02=Omt
            
            b10=-2*Omt*C
            b11= 2*damp*(1-E2)
            b12=-2*b01   

            b20=(2*damp+Omt)*E2
            b21= b01
            b22=-2*damp*C               
            
            bc[0]=b00+b01+b02
            bc[1]=b10+b11+b12
            bc[2]=b20+b21+b22
            
            bc=-bc/(omega[j]**3*dt)
 
# ac same as acceleration case                       
            
            resp=lfilter(bc, ac, b, axis=-1, zi=None) 
        
            rd_pos[j]= max(resp)
            rd_neg[j]= abs(min(resp))   
            rd_abs[j]=max(abs(resp))

        pv_pos=omega*rd_pos
        pv_neg=omega*rd_neg
        pv_abs=omega*rd_abs

        if(n==0):
            pv_scale=386.
            rd_scale=386.
        else:
            pv_scale=9.81*100
            rd_scale=9.81*1000
                
        rd_pos*=rd_scale
        rd_neg*=rd_scale
        rd_abs*=rd_scale
    
        pv_pos*=pv_scale
        pv_neg*=pv_scale
        pv_abs*=pv_scale    
    
        return rd_pos,rd_neg,rd_abs,pv_pos,pv_neg,pv_abs 
   
################################################################################
    
    def export_accel(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the acceleration SRS filename")           
        output_file = output_file_path.rstrip('\n')    
        n= int(self.Lb2.curselection()[0])   
 
        if(n==0):
            WriteData3(self.num_fn,self.fn,self.a_pos,self.a_neg,output_file)        
        else:
            WriteData2(self.num_fn,self.fn,self.a_abs,output_file)

    def export_pv(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                 title="Enter the pseudo velocity SRS filename")           
        output_file = output_file_path.rstrip('\n')    
        n= int(self.Lb2.curselection()[0])   
        if(n==0):
            WriteData3(self.num_fn,self.fn,self.pv_pos,self.pv_neg,output_file)        
        else:
            WriteData2(self.num_fn,self.fn,self.pv_abs,output_file)

    def export_rd(self):    
        output_file_path = asksaveasfilename(parent=self.master,\
                           title="Enter the relative displacement SRS filename")           
        output_file = output_file_path.rstrip('\n')    
        n= int(self.Lb2.curselection()[0])   
        if(n==0):
            WriteData3(self.num_fn,self.fn,self.rd_pos,self.rd_neg,output_file)        
        else:
            WriteData2(self.num_fn,self.fn,self.rd_abs,output_file)
            
################################################################################
            
    def tripartite(self):

        m=self.unit
        

        f1=float(self.f1r.get())
        f2=float(self.f2r.get())



        plt.close(5)
        plt.figure(5)
                 
        n= int(self.Lb2.curselection()[0])
        
        if(n==0):    
            plt.plot(self.fn, self.pv_pos, label="positive")
            plt.plot(self.fn, self.pv_neg, label="negative")
            plt.legend(loc="upper right")      
        else:
            plt.plot(self.fn, self.pv_abs, linewidth=1.0,color='b')        # disregard error
   
        astr='Pseudo Velocity'
    
        title_string= astr + ' SRS Q='+str(self.Q)     
   
        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= astr +' SRS Q='+str(i)
                break
       
        plt.grid(True,which="major",ls="-")
        plt.grid(True,which="minor",ls="--")        
        
        
        plt.xlabel('Natural Frequency (Hz)')
    
        if(m==0):
            plt.ylabel('Peak Vel (in/sec)') 
        else:
            plt.ylabel('Peak Vel (cm/sec)') 
        
        plt.title(title_string)
        plt.xscale('log')
        plt.yscale('log')
            
###            
        srs_max=max(max(self.pv_pos),max(self.pv_neg))
        srs_min=min(min(self.pv_pos),min(self.pv_neg))

        fmin=self.fn[0]
        fmax=max(self.fn)
        
        fmax= 10**(np.ceil(np.log10(fmax)));
        fmin= 10**(np.floor(np.log10(fmin))); 
    
        ymax= 10**(np.ceil(np.log10(srs_max)+0.2));
        ymin= 10**(np.floor(np.log10(srs_min)));

#


#  
        nxd=np.ceil(np.log10(fmax/fmin))
        nyd=np.ceil(np.log10(ymax/ymin))

        if(nxd<nyd):
            ymin=ymax/(10**nxd)   
    
        if(nyd<nxd):
            ymax=ymin*(10**nxd)     



    
#
        v = [fmin, fmax, ymin, ymax]
        plt.axis(v)
#
#  Acceleration Limits
#
        aa=np.zeros(2,'f')
        bb=np.zeros(2,'f')
#
        if(self.unit==0):
            scale=386.
        else:
            scale=9.81*100

        f1=fmin
        v2=ymin
#
        for jk in range (-5,5):
            for k in range (1,10):  
                amp=k*10**(jk)
                v1=amp*scale/(2*np.pi*fmin)
                f2=amp*scale/(2*np.pi*v2)
                aa[0]=f1
                aa[1]=f2
                bb[0]=v1
                bb[1]=v2
                plt.plot(aa,bb,'k--',linewidth=0.25)
#
#
#  Displacement Limits
#
        aa=np.zeros(2,'f')
        bb=np.zeros(2,'f')
#
        f1=fmin
        f2=fmax
#
        for jk in range (-8,5):
            for k in range (1,10):  
                amp=k*10**(jk)
                v1=amp*(2*np.pi*fmin)
                v2=amp*(2*np.pi*fmax)
                aa[0]=f1
                aa[1]=f2
                bb[0]=v1
                bb[1]=v2
                plt.plot(aa,bb,'k--',linewidth=0.25)
#
        plt.savefig('srs_plot')
# 
        plt.legend(bbox_to_anchor=(1.1, 1.05))
#
        theta=-45;
#      
        if nxd==nyd:
            theta=-37

# if nxd==2 and nyd==3:
#     theta=-29
  
# if nxd==3 and nyd==2:
#     theta=-48.5
    
# if nxd==3 and nyd==4:
#     theta=-34
        
        amax=ymax*(2*np.pi*fmin)/scale
        amin=ymin*(2*np.pi*fmin)/scale

        aamax=ymax*(2*np.pi*fmax)/scale

        k=0

        if(amin<=0.01 and amax>=0.01):
            plt.text(fmin,0.012*scale/(2*np.pi*fmin),'0.01 G',fontsize=12,rotation=theta)
            k+=1
        
        if(amin<=0.1 and amax>=0.1):   
            plt.text(fmin,0.12*scale/(2*np.pi*fmin),'0.1 G',fontsize=12,rotation=theta)
            k+=1        
         
        if(amin<=1 and amax>=1):
            plt.text(fmin,1.2*scale/(2*np.pi*fmin),'1 G',fontsize=12,rotation=theta) 
            k+=1         
          
        if(amin<=10 and amax>=10): 
            plt.text(fmin,12*scale/(2*np.pi*fmin),'10 G',fontsize=12,rotation=theta) 
            k+=1        
          
        if(amin<=100 and amax>=100):
            plt.text(fmin,120*scale/(2*np.pi*fmin),'100 G',fontsize=12,rotation=theta) 
            k+=1      
          
        if(amin<=1000 and amax>=1000): 
            plt.text(fmin,1200*scale/(2*np.pi*fmin),'1K G',fontsize=12,rotation=theta)
            k+=1        
          
        if(amin<=10000 and amax>=10000):   
            plt.text(fmin,12000*scale/(2*np.pi*fmin),'10K G',fontsize=12,rotation=theta) 
            k+=1     
          
        if(amin<=100000 and amax>=100000):
            plt.text(fmin,120000*scale/(2*np.pi*fmin),'100K G',fontsize=12,rotation=theta)
            k+=1

#        
        if(amax<=0.01 and 0.01<aamax):
            plt.text(0.012*scale/(2*np.pi*ymax),0.9*ymax,'0.01 G',fontsize=12,rotation=theta) 
            k+=1   
        
        if(amax<=0.1 and 0.1<aamax):
            plt.text(0.12*scale/(2*np.pi*ymax),0.9*ymax,'0.1 G',fontsize=12,rotation=theta)
            k+=1   
    
        if(amax<=1 and 1<aamax):
            plt.text(1.2*scale/(2*np.pi*ymax),0.9*ymax,'1 G',fontsize=12,rotation=theta)             
            k+=1   
        
        if(amax<=10 and 10<aamax):
            plt.text(12*scale/(2*np.pi*ymax),0.9*ymax,'10 G',fontsize=12,rotation=theta)
            k+=1                  
        
        if(amax<=100 and 100<aamax):
            plt.text(120*scale/(2*np.pi*ymax),0.9*ymax,'100 G',fontsize=12,rotation=theta)   
            k+=1               
          
        if(amax<=1000 and 1000<aamax):
            plt.text(1200*scale/(2*np.pi*ymax),0.9*ymax,'1K G',fontsize=12,rotation=theta)  
            k+=1                
       
        if(amax<=10000 and 10000<aamax):
            plt.text(12000*scale/(2*np.pi*ymax),0.9*ymax,'10K G',fontsize=12,rotation=theta)   
            k+=1               
        
        if(amax<=100000 and 100000<aamax):
            plt.text(120000*scale/(2*np.pi*ymax),0.9*ymax,'100K G',fontsize=12,rotation=theta) 
            k+=1                  


#
        dmax=ymax/(2*np.pi*fmax)
        dmin=ymin/(2*np.pi*fmax)

        tpfmax=2*np.pi*fmax

        if(nyd==2):
            fmax32=0.64*fmax
        else:
            fmax32=0.32*fmax        
    
 
        tpfmax*=1.9

        theta=-theta
        
        if(self.unit==0):
            ds='in'
#            vs='in/sec'
        else:
            ds='mm'
#            vs='cm/sec'
        

        if(dmin<=10 and dmax>=10):
            plt.text(fmax32,4*tpfmax,'10 ' +str("%s" %ds),fontsize=12,rotation=theta)  
        
        if(dmin<=1 and dmax>=1):
            plt.text(fmax32,0.4*tpfmax,'1 ' +str("%s" %ds),fontsize=12,rotation=theta)           
        
        if(dmin<=0.1 and dmax>=0.1):
            plt.text(fmax32,0.04*tpfmax,'0.1 ' +str("%s" %ds),fontsize=12,rotation=theta) 
           
        if(dmin<=0.01 and dmax>=0.01):
            plt.text(fmax32,0.004*tpfmax,'0.01 ' +str("%s" %ds),fontsize=12,rotation=theta)               
        
        if(dmin<=0.001 and dmax>=0.001):
            plt.text(fmax32,0.0004*tpfmax,'0.001 ' +str("%s" %ds),fontsize=12,rotation=theta)             
        
        if(dmin<=0.0001 and dmax>=0.0001):
            plt.text(fmax32,0.00004*tpfmax,'0.0001 ' +str("%s" %ds),fontsize=12,rotation=theta)                 

        ddmax=ymax/(2*np.pi*fmin)
        ddmin=ymax/(2*np.pi*fmax)

        if(self.unit==0):
            b=0.8
        else:    
            b=0.56
            
        sc=0.9    


        if(ddmin<=0.01 and 0.01<ddmax):
            plt.text(b*ymax/(2*np.pi*0.01),sc*ymax,'0.01 ' +str("%s" %ds),fontsize=12,rotation=theta) 
 
        if(ddmin<=0.1 and 0.1<ddmax):
            plt.text(b*ymax/(2*np.pi*0.1),sc*ymax,'0.1 ' +str("%s" %ds),fontsize=12,rotation=theta)
    
        if(ddmin<=1 and 1<ddmax):
            plt.text(b*ymax/(2*np.pi*1),sc*ymax,'1 ' +str("%s" %ds),fontsize=12,rotation=theta)
    
        if(ddmin<=10 and 10<ddmax):
            plt.text(b*ymax/(2*np.pi*10),sc*ymax,'10 ' +str("%s" %ds),fontsize=12,rotation=theta)
    
        if(ddmin<=100 and 100<ddmax):
            plt.text(b*ymax/(2*np.pi*100),sc*ymax,'100 ' +str("%s" %ds),fontsize=12,rotation=theta)  
            
 
#*******************************************************************************   

            
###            
        plt.draw()
        
        self.button_tripartite.config(state =  'disabled')    
                     
################################################################################

def quit(root):
    root.destroy()