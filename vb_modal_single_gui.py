################################################################################
# program: vb_force_psd_syn_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.1
# date: October 21, 2014
# description:  Synthesize a time history to satisfy a force or pressure PSD
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
    
    
from vb_utilities import read_two_columns_from_dialog,WriteData2  

from numpy import array,zeros,log,log10,pi,sqrt,linspace,round,ceil,interp

from numpy import cos,sin,std,floor,argmax,histogram

import matplotlib.pyplot as plt

from vb_utilities import WriteData2,signal_stats,sample_rate_check

from scipy.fftpack import fft,ifft

import random


class vb_force_psd_syn:

    def __init__(self,parent): 
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(700,400)
        self.master.geometry("800x500")
        self.master.title("vb_force_psd_syn_gui.py ver 1.0  by Tom Irvine")         
                
        self.fig_num=1     
        
                
###############################################################################     
     
        crow=0
        
        self.hwtext3=tk.Label(top,text='This script synthesizes a time history for a force or pressure PSD.')
        self.hwtext3.grid(row=crow, column=0,columnspan=4, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='The input file must have two columns: Freq(Hz) & psd(units^2/Hz)')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
        crow=crow+1    
        
        self.hwtext4=tk.Label(top,text='Select Amplitude Type & Units')
        self.hwtext4.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S)                 

        self.hwtext_fn=tk.Label(top,text='Enter Duration (sec)')
        self.hwtext_fn.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S) 
        
        crow=crow+1        
        
        
        self.Lb1 = tk.Listbox(top,height=5,exportselection=0)

        self.Lb1.insert(1, "Force (lbf)")
        self.Lb1.insert(2, "Force (N)")
        self.Lb1.insert(3, "Pressure (psi)")
        self.Lb1.insert(4, "Pressure (Pa)")
        self.Lb1.insert(5, "Other")
        
        self.Lb1.grid(row=crow, column=0, pady=2,sticky=tk.N)
        self.Lb1.select_set(0)  

        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 12,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N)   

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=2,columnspan=1,padx=0,pady=2,sticky=tk.N)
        
        
        crow=crow+1

        self.hwtextadv=tk.Label(top,text='Select Analysis Option')
        self.hwtextadv.grid(row=crow, column=0, pady=10)        

        
        crow=crow+1
        
        myframe=tk.Frame(top)
        myframe.grid(row=crow, column=0,padx=3)
        scrollbar = tk.Scrollbar(myframe) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Lba = tk.Listbox(myframe, width=35, yscrollcommand=scrollbar.set) 
        self.Lba.pack()
        scrollbar.config(command=self.Lba.yview)        
              

        crow=crow+1      

               
        self.button_calculate = tk.Button(top, text="Perform Analysis",command=self.analysis_go)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled' )
        self.button_calculate.grid(row=crow, column=0,columnspan=1,padx=10,pady=10)
        
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=6,pady=10) 
        
        self.button_ex = tk.Button(top, text="Export Time History", command=self.export)
        self.button_ex.config( height = 2, width = 23,state = 'disabled' )
        self.button_ex.grid(row=crow, column=2,columnspan=2, padx=10,pady=3)    
        
        self.button_ex_psd = tk.Button(top, text="Export PSD", command=self.export_psd)
        self.button_ex_psd.config( height = 2, width = 14,state = 'disabled' )
        self.button_ex_psd.grid(row=crow, column=4,columnspan=1, padx=10,pady=3)          
        
###############################################################################
        
    def analysis_go(self):
        
        try:
            n= int(self.Lba.curselection()[0])
        except:    
            tkMessageBox.showwarning("Warning","Select Analysis Option",parent=self.button_calculate)
            return
            

        self.NW=self.r_i_seg[n]
        self.mmm = 2**int(log(float(self.num)/float(self.NW))/log(2))
        
        print (n)
        print (self.r_ddf[n])
        
        self.df=1./(self.mmm*self.dt)
        self.mH=((self.mmm/2)-1)
        
        self.Hanning_initial(self)

########################################################################

        print (" ")
        print ("     number of segments   NW= %d " %self.NW)
        print ("       samples/segments  mmm= %d " %self.mmm)
        print (" half samples/segment-1   mH=%d  " %self.mH)
        print (" ")
        print ("        df=%6.3f Hz" %self.df)

        maxf=(self.mH-1)*self.df

        self.Hanning_initial(self)

        self.freq=zeros(self.mH,'f')
        self.freq=linspace(0,maxf,self.mH)

        self.delta=self.freq_spec[0]/30
        
        self.full=zeros(self.mH,'f')
        self.mag_seg=zeros(self.mH,'f') 

        self.amp_seg=zeros(self.mmm,'f')

#######################################################################3333==========

        tpi=2*pi

        nnt=3

        print (" Velocity correction")


        for kvn in range (0,nnt):

#            self.acc,self.velox,self.dispx=velox_correction(self.psd_th,self.dt,self.freq_spec[0])

            ratio = self.spec_RMS/std(self.psd_th)

            self.psd_th*= ratio
            
            self.psd_core(self)

            MK=len(self.psd_th)
            self.tim=linspace(0,MK*self.dt,MK)
    
# low frequency correction    

            self.psd1=0
    
            for i in range (0,len(self.freq)):
 #       print " %8.4g  %8.4g " %(freq[i],freq_spec[0])
                if( self.freq[i]<=self.freq_spec[0] and self.freq_spec[0]<=self.freq[i+1] ):
                    x=self.freq_spec[0]-self.freq[i]
                    c2=x/(self.freq[i+1]-self.freq[i])
                    c1=1-c2
                    self.psd1= c1*self.full[i] +c2*self.full[i+1]
                    break
        
        
#     print "\n @@ kvn=%d  psd1=%8.4g  amp_spec=%8.4g  " %(kvn,psd1,amp_spec[0])      
        

            if(self.psd1<self.amp_spec[0]):
                ca=sqrt(2)*sqrt(self.amp_spec[0]*self.df-self.psd1*self.df)

                print ("kvn=%d    ca=%9.5g " %(kvn,ca))
        
                pha=tpi*random.random()

                fff=self.freq_spec[0]+(-0.5+random.random())*self.delta

                if(kvn==0):
                    fff=self.freq_spec[0]           
        
                if(kvn==1):
                    fff=self.freq_spec[0]+self.delta/2
               
                if(kvn==2):
                   fff=self.freq_spec[0]-self.delta/2
        
                self.psd_th+=ca*sin(tpi*fff*self.tim+pha)
    

################################################################################

        tempf=self.freq[0:self.mH-1]
        tempa=self.full[0:self.mH-1]
        self.freq=tempf
        self.full=tempa

        rms=sqrt(self.ms*self.df)
        three_rms=3*rms

        print (" ")
        print (" Overall RMS = %10.3g " % rms)
        print (" Three Sigma = %10.3g " % three_rms)

        idx = argmax(self.full)

        print (" ")
        print (" Maximum:  Freq=%8.4g Hz   Amp=%8.4g unit^2/Hz" %(self.freq[idx],self.full[idx]))
            
###############################################################################

        n=len(self.TT)

        max_lines=400000

        if(n>max_lines):
            print (' ')
            K=int(ceil(n/max_lines))
            TTo=self.TT
            print ('processing plot data')
            self.TT,self.psd_th=small(TTo,self.psd_th,K)


        arms=std(self.psd_th)

        string_value1 = "  %6.3g" % arms
        
        self.iunit=int(self.Lb1.curselection()[0])  
        if(self.iunit==0):
            self.title_string='Force'+string_value1+' lbf RMS'
            self.ypsd_string='Force (lbf^2/Hz)'
            self.yth_string='Force (lbf)'
        if(self.iunit==1):
            self.title_string='Force'+string_value1+' N RMS'
            self.ypsd_string='Force (N^2/Hz)'
            self.yth_string='Force (N)'            
        if(self.iunit==2):
            self.title_string='Pressure'+string_value1+' psi RMS'
            self.ypsd_string='Pressure (psi^2/Hz)'
            self.yth_string='Pressure (psi)'             
        if(self.iunit==3):
            self.title_string='Pressure'+string_value1+' Pa RMS'
            self.ypsd_string='Pressure (Pa^2/Hz)'  
            self.yth_string='Pressure (Pa)'                
        if(self.iunit==4):
            self.title_string=''+string_value1+' RMS'
            self.ypsd_string='unit^2/Hz'
            self.yth_string='Amplitude'           
        
        
        plt.close(self.fig_num)        
        plt.figure(self.fig_num)
        self.fig_num+=1
        plt.plot(self.TT,self.psd_th, linewidth=1.0)
        plt.xlabel('Time(sec)')
        plt.ylabel(self.yth_string)
        plt.grid(True)
        plt.title(self.title_string)
        plt.draw()

     
###############################################################################

        plt.close(self.fig_num) 
        plt.figure(self.fig_num)
        self.fig_num+=1
        nbins=31
        hist, bins = histogram(self.psd_th, bins=nbins, density=False)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width) 
        plt.ylabel('Counts')
        plt.xlabel(self.ypsd_string)
        plt.title('Histogram')
        plt.draw()             
        
###############################################################################

        plt.close(self.fig_num) 
        plt.figure(self.fig_num)
        self.fig_num+=1        
        
        out1='Synth'+str("%6.3g" %arms+' RMS')
        out2='Spec'+str("%6.3g" %self.spec_RMS+' RMS')
        
        plt.plot(self.freq,self.full, color='b',label=out1)
        plt.plot(self.freq_spec, self.amp_spec, color='r',label=out2)
        plt.plot(self.freq_spec, self.amp_spec*sqrt(2),color='k',label='+/-1.5 dB') 
        plt.plot(self.freq_spec, self.amp_spec/sqrt(2),color='k') 
        
        plt.legend(loc="upper right")           
        
        
        title_string='Power Spectral Density'
        plt.title(title_string)
        plt.ylabel(self.ypsd_string)
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        y1=10**int(floor(log10(min(self.amp_spec))))
        y2=10**int(ceil(log10(max(self.amp_spec))))
        plt.ylim([y1,y2])
        x1=10**int(floor(log10(min(self.freq_spec))))
        x2=10**int(ceil(log10(max(self.freq_spec))))
        plt.xlim([x1,x2])       
        plt.show()        
        
        self.button_ex.config( state = 'normal' )
        self.button_ex_psd.config( state = 'normal' )
        
        print(' View Plots ')
        
###############################################################################

    @classmethod	
    def magnitude_resolve(cls,self):
#
        mHm1=self.mH-1
        z=zeros(self.mH,'f')
        self.mag_seg=zeros(self.mH,'f')
#
#     for i in range (0,mH):
#       z[i]=sqrt(Y.real[i]**2+Y.imag[i]**2)
#
        z=abs(self.Y)/float(self.mmm)
#
        self.mag_seg[0]=z[0]**2
#
        self.mag_seg[1:mHm1]=((2*z[1:mHm1])**2)/2
#


########################################################################

    @classmethod	
    def Hanning_initial(cls,self):
        self.H=zeros(self.mmm,'f')
        tpi=2*pi
        alpha=linspace(0,tpi,self.mmm)
        ae=sqrt(8./3.)
        self.H=ae*0.5*(1.-cos(alpha))


########################################################################

    @classmethod	
    def psd_core(cls,self):
        
        self.full=zeros(self.mH,'f')
        self.mag_seg=zeros(self.mH,'f')
        self.amp_seg=zeros(self.mmm,'f')
        
        den=self.df*(2*self.NW-1)

        nov=0
        
        for ijk in range (1,int(2*self.NW)):

            self.amp_seg[0:self.mmm]=self.psd_th[(0+nov):(self.mmm+nov)]

            nov=nov+int(self.mmm/2)

            mean = sum(self.amp_seg)/float(self.mmm)
            self.amp_seg-=mean

            self.amp_seg*=self.H

            self.Y = fft(self.amp_seg)

            self.magnitude_resolve(self)

            self.full+=self.mag_seg

        self.full/=den

        self.ms=sum(self.full)


###############################################################################

    def read_data(self):            
        
        self.iunit=int(self.Lb1.curselection()[0])  

        if(self.iunit==0):
            self.ypsd_string='Force (lbf^2/Hz)'
            self.yth_string='Force (lbf)'
        if(self.iunit==1):
            self.ypsd_string='Force (N^2/Hz)'
            self.yth_string='Force (N)'            
        if(self.iunit==2):
            self.ypsd_string='Pressure (psi^2/Hz)'
            self.yth_string='Pressure (psi)'             
        if(self.iunit==3):
            self.ypsd_string='Pressure (Pa^2/Hz)'  
            self.yth_string='Pressure (Pa)'                
        if(self.iunit==4):
            self.ypsd_string='unit^2/Hz'
            self.yth_string='Amplitude'         
        
        if not self.durr.get(): #do something
            tkMessageBox.showinfo("Warning", "Enter duration",parent=self.button_read)
            return


        self.tmax =float(self.durr.get())        
        
        
        """
        f = frequency column
        a = PSD column
        num = number of coordinates
        slope = slope between coordinate pairs    
        """
        
        print (" ")
        print (" The input file must have two columns: freq(Hz) & psd(unit^2/Hz)")

        f,a,num =read_two_columns_from_dialog('Select Input File',self.master)

        print ("\n samples = %d " % num)

        f=array(f)
        a=array(a)
    

        nm1=num-1

        slope =zeros(nm1,'f')


        ra=0

        for i in range (0,int(nm1)):
#
            s=log(a[i+1]/a[i])/log(f[i+1]/f[i])
        
            slope[i]=s
#
            if s < -1.0001 or s > -0.9999:
                ra+= ( a[i+1] * f[i+1]- a[i]*f[i])/( s+1.)
            else:
                ra+= a[i]*f[i]*log( f[i+1]/f[i])

  
        rms=sqrt(ra)
        three_rms=3*rms
    
        print (" ")
        print (" *** Input PSD *** ")
        print (" ")
        print ("   Overall = %10.3g RMS" % rms)
        print ("           = %10.3g 3-sigma" % three_rms)


        
        self.RMS_in=rms
        self.f=f
        self.a=a

        self.rms=rms
        self.freq_spec=f
        self.amp_spec=a
        self.num=num        
        self.slope=slope
        
        self.button_calculate.config(state = 'normal')
        
        self.spec_RMS=rms         
        
        plt.ion()
        plt.clf()   
        plt.close(self.fig_num) 
        plt.figure(self.fig_num)
        self.fig_num+=1        
        plt.plot(f,a)
        title_string='Power Spectral Density   '+str("%6.3g" %rms)+' RMS Overall '
        plt.title(title_string)
        plt.ylabel(self.ypsd_string)
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
        
        self.white_noise(self)
        self.calculate_fft(self)
        self.apply_spec(self)
        self.calculate_invfft(self)
        self.advise(self)
        
        self.button_calculate.config( state = 'normal' )
    
###############################################################################

    @classmethod
    def advise(cls,self):    

        self.Lba.delete(0, tk.END) # clear
        
        n=self.num

        self.ss=zeros(n)
        self.seg=zeros(n,'f')
        self.i_seg=zeros(n)
        self.ddf=zeros(n,'f')

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


        self.r_ss=[]
        self.r_seg=[]
        self.r_i_seg=[]        
        self.r_ddf=[]

        
        k=0
        
        nL=int(self.sr/4.)
        
        for i in range(0,int(NC)):
            if( t_seg[i]>0 and t_ddf[i]< nL ):
                out1='sps=%d,  df=%6.3g Hz,  sdof=%d' \
                                       %(t_ss[i],t_ddf[i],2*t_i_seg[i])
                                       
 #               print(out1)
                       
                self.Lba.insert(i, out1)

                self.r_ss.append(t_ss[i])
                self.r_seg.append(t_ddf[i])
                self.r_i_seg.append(t_i_seg[i])        
                self.r_ddf.append(t_ddf[i]) 

                k=k+1
                                
        self.kmax=len(self.r_ss)    

        self.Lba.select_set(0)         
            
###############################################################################

    @classmethod
    def calculate_invfft(cls,self):
        
        print (" Calculating inverse FFT ")

        YI = ifft(self.Y)

        print (" YIR")

        YIR = YI.real

        print (" psd_th")


        self.psd_th = YIR[0:self.np]

        self.np = len(self.psd_th)

        self.TT = linspace(0, (self.np - 1) * self.dt, self.np)

        print (" ")
        print ("num_fft=%d " %self.num_fft)
        print ("np=%d      " %self.np)

        stddev = std(self.psd_th)

        self.psd_th *= (self.spec_RMS / stddev)

#### check psd ############################################################

        a=self.TT
        b=self.psd_th

        self.num=len(a)

        sr,dt,mean,sd,rms,skew,kurtosis,dur=signal_stats(a,b,self.num)

        self.sr,self.dt=sample_rate_check(a,b,self.num,sr,dt)
    
###############################################################################

    @classmethod
    def apply_spec(cls,self):

        print (" Apply spec ")

# for j in range(1, m2):
#    Y[j] = sq_spec[j] * YF[j]


        YFn=self.YF[0:self.m2]

        self.Y[0:self.m2]=self.sq_spec*YFn

        self.Y[0]=0.


        print (" Make symmetric")

        for j in range(1, self.m2):
            self.Y[self.num_fft - j] = complex(self.Y[j].real, -self.Y[j].imag)    
    
###############################################################################

    @classmethod
    def calculate_fft(cls,self):
        
        self.num_fft=2

        while(self.num_fft<self.np):
            self.num_fft*=2

        N = self.num_fft
        df = 1. / (N * self.dt)

        self.m2 = int(self.num_fft / 2)

        fft_freq = linspace(0, (self.m2 - 1) * df, self.m2)
#        fft_freq2 = linspace(0, (self.num_fft - 1) * df, self.num_fft)

        self.spec = zeros(self.m2, float)
        self.sq_spec = zeros(self.m2, float)

        print (" Interpolate specification")

        if(fft_freq[0]<=0):
            fft_freq[0]=0.5*fft_freq[1]        
        
        x=log10(fft_freq)    
        xp=log10(self.freq_spec)    
        yp=log10(self.amp_spec)
        
        y=interp(x, xp, yp, left=-10, right=-10)


        self.sq_spec=sqrt(10**y)

# add option for sine tones later

        print (" Calculating FFT ")

        white_trunc=[]
        
               
        for i in range(0,self.num_fft):
            white_trunc.append(self.white[i])


        self.Y = zeros(self.num_fft, complex)

        self.YF = fft(white_trunc)                               
                               
###############################################################################

                               
    @classmethod	
    def white_noise(cls,self):


        fmax = max(self.freq_spec)

        sr = fmax * 20.
        self.dt = 1 / sr

        self.np = int(ceil(self.tmax/self.dt))
        self.np3 = 3 * self.np

        mu = 0.
        sigma = 1.

        print (" Generate white noise")

        self.white=[]
        
        for i in range(0,int(self.np3)):
            self.white.append(random.gauss(mu, sigma))

        print (" End white noise") 
        

###############################################################################

   
    def export(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n') 
        
        
        self.np=len(self.TT)
 
        WriteData2(self.np,self.TT,self.psd_th,output_file)


###############################################################################

   
    def export_psd(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n') 
        
        
        self.np=len(self.freq)
 
        WriteData2(self.np,self.freq,self.full,output_file)
        
        
###############################################################################        

def quit(root):
    root.destroy()        
    
    

###############################################################################    
    
def small(tt,input_matrix,k):
    """
    Return size of array while retaining max and min values
    in each window
    """
    n=len(input_matrix)
    
    if(k<2):
        k=2
      
    iflag=0
    
    i=0
    m=0
    
    B=zeros(n,'f')
    T=zeros(n,'f')
    
    while(iflag==0):
        
#        print i,(i+k+1),n
                
        if((i+k+1)<n):
            a=max(input_matrix[i:i+k+1])
            b=min(input_matrix[i:i+k+1])
            p=floor((i+i+k+1)/2)

        else:     
            if(i<=(n-1)):
                a=max(input_matrix[i:n-1])
                b=min(input_matrix[i:n-1])       
                p=floor((i+n)/2) 
                
            iflag=1

            
        if(p>=n):
            p=n-1
            
        if(i>(n-1)):
            iflag=1
            break
 
        if(m>(n-1)):
            print ('m limit')
            iflag=1
            break
              
        
        B[m]=a
        T[m]=tt[i] 
        m+=1

        
        B[m]=b
        T[m]=tt[p]
  
        m+=1        
            
        i=i+k+2    
    
        

    output_matrix=B[0:m-1]
    TT=T[0:m-1]
    
    return TT,output_matrix    

###############################################################################
    