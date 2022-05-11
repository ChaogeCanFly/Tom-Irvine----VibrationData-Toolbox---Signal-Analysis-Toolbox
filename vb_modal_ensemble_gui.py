################################################################################
# program: vb_modal_ensemble_frf_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.0
# date: November 13, 2014
# description:  Calculate the frf from a force and response time history
#
################################################################################
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
    

from numpy import array,zeros,log,log10,pi,sqrt,linspace,round,floor,ceil,interp

from numpy import mean,pi,cos,sin

from math import atan2

import matplotlib.pyplot as plt

from vb_utilities import WriteData2,WriteData3

from scipy.fftpack import fft

from matplotlib.gridspec import GridSpec


class vb_modal_ensemble_frf:

    def __init__(self,parent,t,c): 
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.top=top
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.26))
        h = int(2.*(h*0.35))
        self.master.geometry("%dx%d+0+0" % (w, h))



        self.master.title("vb_modal_ensemble_frf_gui.py ver 1.0  by Tom Irvine")         
                
        self.fig_num=1    
        
        self.c=c
        self.t=t
        L=len(t)
        Lm1=L-1
        self.dt=(t[Lm1]-t[0])/Lm1
        self.num=L   
        self.sr=1/self.dt
        
################################################################################ 


        self.b=[]
        self.a=[]
 
        self.ss=zeros(100,'int')
        self.seg=zeros(100,'int')
        self.i_seg=zeros(100,'int')
        self.ddf=zeros(100,'float') 
        
        self.r_ss=[]
        self.r_seg=[]
        self.r_i_seg=[]
        self.r_ddf=[]         
        
        self.r_ss=[]
        self.r_seg=[]
        self.r_i_seg=[]
        self.r_ddf=[]
        self.rms=0
        self.freq=[]
        
        self.mH=0
        self.NW=0
        self.mmm=0
     
###############################################################################     
     
        crow=0
        
        self.hwtext1=tk.Label(top,text='Calculate the frf from a force and response time history')
        self.hwtext1.grid(row=crow, column=0,columnspan=4, pady=6,sticky=tk.W)        
        
        
        crow=crow+1    
        
        self.hwtext2=tk.Label(top,text='Select Analysis Option')
        self.hwtext2.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S) 

        self.hwtext3=tk.Label(top,text='Response Type')
        self.hwtext3.grid(row=crow, column=1,columnspan=1, padx=10, pady=6,sticky=tk.S)                 

        self.hwtext4=tk.Label(top,text='Unit')
        self.hwtext4.grid(row=crow, column=2, columnspan=1, padx=4, pady=6,sticky=tk.S) 

###############################################################################
        
        crow=crow+1        
        
        myframe=tk.Frame(top)
        myframe.grid(row=crow, column=0,padx=3)
        scrollbar = tk.Scrollbar(myframe) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Lba = tk.Listbox(myframe, width=35, yscrollcommand=scrollbar.set) 
        self.Lba.pack()
        scrollbar.config(command=self.Lba.yview)        
        
        self.advise(self)
        
        self.Lb1 = tk.Listbox(top,height=3,exportselection=0)
        self.Lb1.grid(row=crow, column=1, columnspan=1, padx=10, pady=10,sticky=tk.N)      
        self.Lb1.insert(1, "Acceleration")
        self.Lb1.insert(2, "Velocity")
        self.Lb1.insert(3, "Displacement")
        self.Lb1.select_set(0)  
        
        self.runitr=tk.StringVar()  
        self.runitr.set('G')  
        self.runit_entry=tk.Entry(top, width = 9,textvariable=self.runitr)
        self.runit_entry.grid(row=crow, column=2,padx=4, pady=1,sticky=tk.N)           
        
###############################################################################        
        
        crow=crow+1    
        
        self.hwtext5=tk.Label(top,text='Select Input Unit')
        self.hwtext5.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S)
        
        self.hwtext6=tk.Label(top,text='Mean Removal')
        self.hwtext6.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)       
        
        self.hwtext73=tk.Label(top,text='Window')
        self.hwtext73.grid(row=crow, column=2,columnspan=1, pady=6,sticky=tk.S)         
        
        crow=crow+1        
        
        self.Lb2 = tk.Listbox(top,height=2,width=13,exportselection=0)
        self.Lb2.grid(row=crow, column=0, columnspan=1, padx=4, pady=10,sticky=tk.S)        
        self.Lb2.insert(1, "Force (lbf)")
        self.Lb2.insert(2, "Force (N)")
        self.Lb2.select_set(0)  
      
        self.Lb_mr = tk.Listbox(top,height=2,width=6,exportselection=0)
        self.Lb_mr.grid(row=crow, column=1, columnspan=1, padx=4, pady=10,sticky=tk.S)        
        self.Lb_mr.insert(1, "yes")
        self.Lb_mr.insert(2, "no")
        self.Lb_mr.select_set(0)     
        
        self.Lb_win = tk.Listbox(top,height=2,width=12,exportselection=0)
        self.Lb_win.grid(row=crow, column=2, columnspan=1, padx=4, pady=10,sticky=tk.S)        
        self.Lb_win.insert(1, "Rectangular")
        self.Lb_win.insert(2, "Hanning")
        self.Lb_win.select_set(0)         
      
        crow=crow+1    
        
        self.hwtext7=tk.Label(top,text='Plot Frequencies (Hz)')
        self.hwtext7.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.S)      
      
        crow=crow+1    
      
        self.hwtext8=tk.Label(top,text='Minimum')
        self.hwtext8.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S) 
        
        self.hwtext9=tk.Label(top,text='Maximum')
        self.hwtext9.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)       
      
        crow=crow+1   
             
        self.fminr=tk.StringVar()   
        self.fmin_entry=tk.Entry(top, width = 12,textvariable=self.fminr)
        self.fmin_entry.grid(row=crow, column=0,padx=4, pady=1,sticky=tk.N)          
        
        self.fmaxr=tk.StringVar()   
        self.fmax_entry=tk.Entry(top, width = 12,textvariable=self.fmaxr)
        self.fmax_entry.grid(row=crow, column=1,padx=4, pady=1,sticky=tk.N)  


        crow=crow+1    
        
        self.button_calculate = tk.Button(top, text="Calculate FRF", command=self.calculation)
        self.button_calculate.config( height = 2, width = 18)
        self.button_calculate.grid(row=crow, column=0, pady=20)         
        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,pady=20) 
        

        crow=crow+1

        self.hwtextext_exfft=tk.Label(top,text='Export Transfer Function Data')
        self.hwtextext_exfft.grid(row=crow, column=0,columnspan=2,pady=10)  

        crow=crow+1
        
        self.Lbexp = tk.Listbox(top,height=3,width=35,exportselection=0)
        self.Lbexp.grid(row=crow, column=0, columnspan=2, padx=10, pady=10,sticky=tk.N)      
        self.Lbexp.insert(1, "H1: Frequency & Real & Imaginary")
        self.Lbexp.insert(2, "H2: Frequency & Real & Imaginary")
        self.Lbexp.insert(3, "Coherence")        
        self.Lbexp.select_set(0)  
        

        self.button_export = tk.Button(top, text="Export", command=self.export)
        self.button_export.config( height = 2, width = 18,state = 'disabled')
        self.button_export.grid(row=crow, column=2, pady=15)  

        self.button_modal = tk.Button(top, text="Modal Analysis", command=self.modal)
        self.button_modal.config( height = 2, width = 18,state = 'disabled')
        self.button_modal.grid(row=crow, column=3, padx=3,pady=15)            

###############################################################################

    @classmethod      
    def advise(cls,self):
        
        self.Lba.delete(0, tk.END) # clear

        n=self.num
        
        NC=0
        
        
        for i in range(1,1000):
    
            nmp = 2**(i-1)
   
            if(nmp <= n ):
                self.ss[i] = 2**(i-1)
                self.seg[i] = round(n/self.ss[i])
                self.i_seg[i] = floor(self.seg[i])
                tseg=self.dt*self.ss[i]
                self.ddf[i]=1./tseg                
                NC=NC+1
            else:
                break
            
            
        t_ss= self.ss[NC+1:0:-1]
        t_seg= self.seg[NC+1:0:-1]
        t_i_seg= self.i_seg[NC+1:0:-1]        
        t_ddf= self.ddf[NC+1:0:-1]          
        
        k=0
        
        nL=int(self.sr/4.)
        
        for i in range(0,int(NC)):
            if( t_seg[i]>0 and t_ddf[i]< nL ):
                out1='sps=%d,  df=%6.3g Hz,  sdof=%d' \
                                       %(t_ss[i],t_ddf[i],2*t_i_seg[i])
                                       
                print(out1)
                       
                self.Lba.insert(i, out1)

                self.r_ss.append(t_ss[i])
                self.r_seg.append(t_ddf[i])
                self.r_i_seg.append(t_i_seg[i])        
                self.r_ddf.append(t_ddf[i]) 

                k=k+1
                    
            
        self.kmax=len(self.r_ss)    

        self.Lba.select_set(0)    
        
###############################################################################
        
    def calculation(self):
      
        nLb1= int(self.Lb1.curselection()[0])  # avd         
        nLb2= int(self.Lb2.curselection()[0])  # force unit                      
    
#       self.t=self.t        
        self.a=self.c[:,0]
        self.b=self.c[:,1]

### 

        if(nLb2==0):
            YF='Force (lbf)'
            FU='lbf'
        else:
            YF='Force (N)'
            FU='N'        
  
### 
      
        if(nLb1==0):
            YR1='Acceleration'

        if(nLb1==1):
            YR1='Velocity'

        if(nLb1==2):
            YR1='Displacement'          
      
### 

        YU=self.runitr.get()
                           
###    

        YR2='('+YU+')'

        YR= YR1+YR2
### 

        self.dur=self.num*self.dt

##
        
#        YS=YU

        trans_label= YR1+'/Force ('+YU+'/'+FU+')'

        try:
            n= int(self.Lba.curselection()[0])
        except:    
            tkMessageBox.showwarning("Warning","Select Analysis Option",parent=self.button_calculate)
            return


        print('n=%d kmax=%d' %(n,self.kmax))    

        if(n>=0 and n<self.kmax):
            pass
        else:
            tkMessageBox.showwarning("Warning","Select Analysis Option",parent=self.button_calculate)
            return
        
        mr_choice=int(self.Lb_mr.curselection()[0])
        h_choice =int(self.Lb_win.curselection()[0])        
        

        self.NW=self.r_i_seg[n]
        self.mmm = 2**int(log(float(self.num)/float(self.NW))/log(2.))
        
        print (n)
        print (self.r_ddf[n])
        
        self.df=1./(self.mmm*self.dt)
        self.mH=((self.mmm/2)-1)
        
        if h_choice==1:
            H=self.Hanning_initial(self.mmm)
            
        print (" ")
        print ("     number of segments   NW= %d " %self.NW)
        print ("       samples/segments  mmm= %d " %self.mmm)
        print (" half samples/segment-1   mH=%d  " %self.mH)
        print (" ")
        print ("        df=%6.3f Hz" %self.df)

#        

        if len(self.fmaxr.get()) == 0:
            sr=1/self.dt
            nyf=sr/2.
            self.max=nyf
        else:
            self.fmax=float(self.fmaxr.get())            

#

        if len(self.fminr.get()) == 0:
            self.fmin=0
        else:
            self.fmin=float(self.fminr.get())  

#            
        self.full=zeros(self.mH,'f')    
        self.mag_seg=zeros(self.mH,'f')     

        nov=0

        CPSD=zeros(self.mmm,dtype=complex) 
        PSD_A=zeros(self.mmm,dtype=complex) 
        PSD_B=zeros(self.mmm,dtype=complex)
        H1=zeros(self.mmm,dtype=complex)
        H2=zeros(self.mmm,dtype=complex)

        for ijk in range(0,(2*self.NW-1)):
            
            amp_seg_A=zeros(self.mmm,'f')            
            amp_seg_A[0:self.mmm]=self.a[(0+nov):(self.mmm+nov)]    

            amp_seg_B=zeros(self.mmm,'f')            
            amp_seg_B[0:self.mmm]=self.b[(0+nov):(self.mmm+nov)]  

            nov=nov+int(self.mmm/2)
    
            if mr_choice==0 or h_choice==1:
                amp_seg_A-=mean(amp_seg_A)
                amp_seg_B-=mean(amp_seg_B)
        
            if h_choice==1:
                amp_seg_A*=H
                amp_seg_B*=H

            complex_FFT_A = array(fft(amp_seg_A))
            complex_FFT_B = array(fft(amp_seg_B))
            
            GFX=complex_FFT_A.conjugate()*complex_FFT_B
            GXF=complex_FFT_B.conjugate()*complex_FFT_A

            GFF=complex_FFT_A.conjugate()*complex_FFT_A            
            GXX=complex_FFT_B.conjugate()*complex_FFT_B            

            CPSD+=  GFX/self.df
            PSD_A+= GFF/self.df
            PSD_B+= GXX/self.df

            
            H1L=GFX/GFF
            H2L=GXX/GXF            

            H1+=H1L
            H2+=H2L
            
    
        den=(2*self.NW-1)
        CPSD/=den
        PSD_A/=den
        PSD_B/=den
        H1/=den
        H2/=den             
            
        CPSD_mag=abs(CPSD)           
        H1_mag=abs(H1)
        H2_mag=abs(H2)
        
        CPSD_phase=zeros(self.mmm,'f')
        H1_phase=zeros(self.mmm,'f')
        H2_phase=zeros(self.mmm,'f')        
        
        for i in range(0,self.mmm):
            CPSD_phase[i]=(180/pi)*atan2(CPSD[i].imag,CPSD[i].real)    
            H1_phase[i]=(180/pi)*atan2(H1[i].imag,H1[i].real)
            H2_phase[i]=(180/pi)*atan2(H2[i].imag,H2[i].real)

        
        mH=self.mH        
        
        fffmax=(mH)*self.df
        self.freq=linspace(0,fffmax,mH)

        CPSD_m=zeros(mH,'f')
#        CPSD_p=zeros(mH,'f')        
        self.H1_m=zeros(mH,'f')
        self.H1_p=zeros(mH,'f')
        self.H2_m=zeros(mH,'f')
        self.H2_p=zeros(mH,'f')
        self.ff=zeros(mH,'f')



        CPSD_m[0]=CPSD_mag[0]
        CPSD_m[1:mH]=2*CPSD_mag[1:mH]
#        CPSD_p=CPSD_phase[0:mH]        
        
        self.H1_m[0]=H1_mag[0]
        self.H1_m[1:mH]=2*H1_mag[1:mH]
        self.H1_p=H1_phase[0:mH]

        self.H2_m[0]=H2_mag[0]
        self.H2_m[1:mH]=2*H2_mag[1:mH]
        self.H2_p=H2_phase[0:mH]        
        
        self.COH=zeros(mH,'f')
        self.H1_real=zeros(mH,'f')
        self.H1_imag=zeros(mH,'f')
        self.H2_real=zeros(mH,'f')
        self.H2_imag=zeros(mH,'f')        
        
        self.ff=zeros(mH,'f')
        
        for i in range(0,mH):
       
            self.COH[i]=abs(CPSD_mag[i]**2/( PSD_A[i]*PSD_B[i] ))

            self.H1_real[i]=H1[i].real
            self.H1_imag[i]=H1[i].imag 
            self.H2_real[i]=H2[i].real
            self.H2_imag[i]=H2[i].imag   
            
            self.ff[i]=i*self.df

###############################################################################

        self.button_export.config( state = 'normal')     
        self.button_modal.config( state='normal')        
        
###############################################################################

        plt.ion()
        plt.close(1)
        plt.figure(1)
        
        plt.plot(self.t, self.a, linewidth=1.0,color='b')        # disregard error
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(YF)        
        plt.title('Force Signal')
        
        
        plt.close(2)
        plt.figure(2)   
        
        plt.plot(self.t, self.b, linewidth=1.0,color='b')        # disregard error
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(YR)        
        plt.title('Response Signal')        

###############################################################################        

        x1=self.fmin
        x2=self.fmax
 
        y1=-180
        y2= 180
        
###############################################################################            

       
        plt.close(3)
        plt.figure(3)
        gs1 = GridSpec(3, 1)        

 
        plt.subplot(gs1[:-2, :])          
        plt.plot(self.ff,self.H1_p)
        plt.title('H1 Frequency Response Function ') 
        plt.ylabel('Phase (deg)')
        plt.yticks([-180,-90,0,90,180]) 
        plt.xscale('log')
        plt.xlim([x1,x2])
        plt.ylim([y1,y2])  
        plt.grid(b=True, which='major')
        plt.grid(b=True, which='minor')        
        plt.draw()
         
        plt.subplot(gs1[-2:0, :])        
        plt.plot(self.ff,self.H1_m)
        plt.ylabel(trans_label)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim([x1,x2])       
        plt.grid(b=True, which='major')
        plt.grid(b=True, which='minor')        
        plt.draw()

        plt.xlabel('Frequency (Hz)')
        
        
###############################################################################            
       
        plt.close(4)
        plt.figure(4)
        gs1 = GridSpec(3, 1)        
 
        plt.subplot(gs1[:-2, :])          
        plt.plot(self.ff,self.H2_p)
        plt.title('H2 Frequency Response Function ')        
        plt.ylabel('Phase (deg)')
        plt.yticks([-180,-90,0,90,180])
        plt.xscale('log')
        plt.xlim([x1,x2])
        plt.ylim([y1,y2])        
        plt.grid(b=True, which='major')
        plt.grid(b=True, which='minor')        
        plt.draw()
         
        plt.subplot(gs1[-2:0, :])        
        plt.plot(self.ff,self.H2_m)
        plt.ylabel(trans_label)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim([x1,x2])       
        plt.grid(b=True, which='major')
        plt.grid(b=True, which='minor')       
        plt.xlabel('Frequency (Hz)') 
        plt.draw()
        
###############################################################################

        plt.close(5)
        plt.figure(5)        
        plt.plot(self.ff,self.COH)
        plt.title('Coherence ') 
        plt.xlabel('Frequency (Hz)')  
        plt.xscale('log')    
        plt.ylabel('(lamba xy)^2')
        ymin=0.
        ymax=1.
        plt.xlim([x1,x2])      
        plt.ylim([ymin,ymax])  
        plt.grid(b=True, which='major')
        plt.grid(b=True, which='minor')        
        plt.draw()
        
###############################################################################


    @classmethod     
    def Hanning_initial(cls,mmm):
        H=zeros(mmm,'f')
        tpi=2*pi    
        alpha=linspace(0,tpi,mmm)
        ae=sqrt(8./3.)
        H=ae*0.5*(1.-cos(alpha))                
        return H          


###############################################################################

    def modal(self):
        
        win = tk.Toplevel()
        
        from vb_half_power_bandwidth_fc_gui import vb_half_power_bandwidth_fc        
        vb_half_power_bandwidth_fc(win)               

                    
    def export(self):

        m= int(self.Lbexp.curselection()[0])   
        
        n=len(self.ff)
        
        if(m==0):
        
            output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output H1 filename: ")       
            output_file = output_file_path.rstrip('\n')    
        
            WriteData3(n,self.ff,self.H1_real,self.H1_imag,output_file)  
        
        
        if(m==1):
        
            output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output H2 filename: ")       
            output_file = output_file_path.rstrip('\n')    
        
            WriteData3(n,self.ff,self.H2_real,self.H2_imag,output_file)          
        

        if(m==2):
        
            output_file_path = asksaveasfilename(parent=self.master,\
                            title="Enter the output Coherence filename: ")       
            output_file = output_file_path.rstrip('\n')    
        
            WriteData2(n,self.ff,abs(self.COH),output_file) 

 
###############################################################################
                      
def quit(root):
    root.destroy()
                       
###############################################################################  
