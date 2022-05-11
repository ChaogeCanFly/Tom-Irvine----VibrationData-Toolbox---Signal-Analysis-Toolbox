################################################################################
# program: vb_accel_psd_syn_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.2
# date: December 9, 2015
# description:  Synthesize a time history to satisfy an acceleration PSD
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
    
    
from velox_correction import velox_correction

from vb_utilities import read_two_columns_from_dialog,WriteData2 
from vb_utilities import signal_stats,sample_rate_check
  
from numpy import array,zeros,log,log10,pi,sqrt,linspace,round,ceil,interp
from numpy import cos,sin,std,floor,argmax,histogram

import matplotlib.pyplot as plt


from scipy.fftpack import fft,ifft

import random


class vb_accel_psd_syn:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.30))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_accel_psd_syn_gui.py ver 1.2  by Tom Irvine")         
                
        self.fig_num=1                
                
###############################################################################     
     
        crow=0
        
        self.hwtext3=tk.Label(top,text='This script synthesizes a time history for an acceleration PSD.')
        self.hwtext3.grid(row=crow, column=0,columnspan=4, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='The input file must have two columns: Freq(Hz) & Accel(G^2/Hz)')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
        crow=crow+1    
        
        self.hwtext4=tk.Label(top,text='Select Output Units')
        self.hwtext4.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S)                 

        self.hwtext_fn=tk.Label(top,text='Enter Duration (sec)')
        self.hwtext_fn.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S) 
        
        crow=crow+1        
        
        
        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "G, in/sec, in")
        self.Lb1.insert(2, "G, cm/sec, mm")
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
        
        self.button_ex = tk.Button(top, text="Export Accel Time History", command=self.export)
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

            self.acc,self.velox,self.dispx=velox_correction(self.psd_th,self.dt,self.freq_spec[0])


            ratio = self.spec_grms/std(self.psd_th)

            self.psd_th*= ratio
            self.velox*= ratio
            self.dispx*= ratio
            
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
        print (" Maximum:  Freq=%8.4g Hz   Amp=%8.4g G^2/Hz" %(self.freq[idx],self.full[idx]))


###############################################################################

        iunit=int(self.Lb1.curselection()[0])      


        if(iunit==0):     
            pass
        else:    
            self.velox=self.velox*9.81*100./386.  
            self.dispx=self.velox*9.81*1000./386.  
            
###############################################################################

        n=len(self.TT)

        max_lines=400000

        psd_th_store=self.psd_th
        
        arms=std(self.psd_th)        
        
        TT=self.TT
        TTo=self.TT
        psd_th=self.psd_th
        velox=self.velox
        dispx=self.dispx

        if(n>max_lines):
            print (' ')
            K=int(ceil(n/max_lines))
            
            print ('processing acceleration plot data')   # keep TTo
            TT,psd_th=small(TTo,psd_th,K)
            print ('processing velocity plot data')  
            TT,velox=small(TTo,velox,K)
            print ('processing displacement plot data')
            TT,dispx=small(TTo,dispx,K)
            
            print(' ')
            print(' Warning time histories reduced for plots only due to size limit. ')



        string_value1 = "  %6.3g" % arms

        title_string='Acceleration'+string_value1+' GRMS'

        plt.figure(self.fig_num)
        self.fig_num+=1
        plt.plot(TT,psd_th, linewidth=1.0)
        plt.xlabel('Time(sec)')
        plt.ylabel('Accel(G)')
        plt.grid(True)
        plt.title(title_string)
        plt.draw()

        string_value1 = "  %6.3g" % std(self.velox)

        plt.figure(self.fig_num)
        self.fig_num+=1
        plt.plot(TT,velox,linewidth=1.0)
        plt.xlabel('Time(sec)')
        if(iunit==0):             
            plt.ylabel('Vel(in/sec)')
            title_string='Velocity'+string_value1+' (in/sec) RMS'            
        else:
            plt.ylabel('Vel(cm/sec)')  
            title_string='Velocity'+string_value1+' (cm/sec) RMS'             
        
        plt.grid(True)
        plt.title(title_string)
        plt.draw()
              

        string_value1 = "  %6.3g" % std(self.dispx)

        plt.figure(self.fig_num)
        self.fig_num+=1
        plt.plot(TT,dispx,linewidth=1.0)
        plt.xlabel('Time (sec)')
        if(iunit==0):             
            plt.ylabel('Disp (in)')
            title_string='Displacement'+string_value1+' in RMS'            
        else:
            plt.ylabel('Disp (mm)')  
            title_string='Disp'+string_value1+' mm RMS'             
        
        plt.grid(True)
        plt.title(title_string)
        plt.draw()
        
###############################################################################

        plt.figure(self.fig_num)
        self.fig_num+=1
        nbins=31
        hist, bins = histogram(self.psd_th, bins=nbins, density=False)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width) 
        plt.ylabel('Counts')
        plt.xlabel('Accel (G)')
        plt.title('Acceleration Histogram')
        plt.draw()             
        
###############################################################################

        plt.figure(self.fig_num)
        self.fig_num+=1        
        
        out1='Synth'+str("%6.3g" %arms+' GRMS')
        out2='Spec'+str("%6.3g" %self.spec_grms+' GRMS')
        
        plt.plot(self.freq,self.full, color='b',label=out1)
        plt.plot(self.freq_spec, self.amp_spec, color='r',label=out2)
        plt.plot(self.freq_spec, self.amp_spec*sqrt(2),color='k',label='+/-1.5 dB') 
        plt.plot(self.freq_spec, self.amp_spec/sqrt(2),color='k') 
        
        plt.legend(loc="upper right")           
        
        
        title_string='Acceleration Power Spectral Density'
        plt.title(title_string)
        plt.ylabel(' Accel (G^2/Hz)')
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
        print (" The input file must have two columns: freq(Hz) & accel(G^2/Hz)")

        f,a,num =read_two_columns_from_dialog('Select Input File',self.master)

        print ("\n samples = %d " % num)

        f=array(f)
        a=array(a)
    
        self.maxf=max(f)

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

        omega=2*pi*a

        av=zeros(num,'f') 
        ad=zeros(num,'f') 
        
        for i in range (0,int(num)):         
            av[i]=a[i]/omega[i]**2
            
        
        rv=0

        for i in range (0,int(nm1)):
#
            s=log(av[i+1]/av[i])/log(f[i+1]/f[i])
#
            if s < -1.0001 or s > -0.9999:
                rv+= ( av[i+1] * f[i+1]- av[i]*f[i])/( s+1.)
            else:
                rv+= av[i]*f[i]*log( f[i+1]/f[i])         
         
        
        for i in range (0,int(num)):         
            ad[i]=av[i]/omega[i]**2
     
        rd=0

        for i in range (0,int(nm1)):
#
            s=log(ad[i+1]/ad[i])/log(f[i+1]/f[i])
#
            if s < -1.0001 or s > -0.9999:
                rd+= ( ad[i+1] * f[i+1]- ad[i]*f[i])/( s+1.)
            else:
                rd+= ad[i]*f[i]*log( f[i+1]/f[i])         

        
        rms=sqrt(ra)
        three_rms=3*rms
    
        print (" ")
        print (" *** Input PSD *** ")
        print (" ")
 
        print (" Acceleration ")
        print ("   Overall = %10.3g GRMS" % rms)
        print ("           = %10.3g 3-sigma" % three_rms)
        
        self.grms_in=rms
        self.f=f
        self.a=a

        self.rms=rms
        self.freq_spec=f
        self.amp_spec=a
        self.num=num        
        self.slope=slope
        
        self.button_calculate.config(state = 'normal')
        
        self.spec_grms=rms         
        
        plt.ion()
        plt.clf()   
        plt.figure(self.fig_num)
        self.fig_num+=1        
        plt.plot(f,a)
        title_string='Power Spectral Density   '+str("%6.3g" %rms)+' GRMS Overall '
        plt.title(title_string)
        plt.ylabel(' Accel (G^2/Hz)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
        
        self.advise(self)        
        self.white_noise(self)
        self.calculate_fft(self)
        self.apply_spec(self)
        self.calculate_invfft(self)
        
        
        self.button_calculate.config( state = 'normal' )
    
###############################################################################

    @classmethod
    def advise(cls,self):    

        self.Lba.delete(0, tk.END) # clear
        
        n=1        
        
        while(1):
            n=n*2
            nf=floor(log(n)/log(2.))
            n=2**nf
            
            self.dt=self.tmax/float(n-1)
            self.sr=1/self.dt
            
            if(self.sr>=10*self.maxf):
                break
              
        n=int(n)               
              
        self.number_points=n    
            
        self.ss=zeros(n)
        self.seg=zeros(n,'f')
        self.i_seg=zeros(n)
        self.ddf=zeros(n,'f')

        NC=0
        
        for i in range(1,1000):
    
            nmp = 2**(i-1)
   
            if(nmp <= n ):
                self.ss[i] = nmp
                self.seg[i] = round(n/float(nmp))
                self.i_seg[i] = floor(self.seg[i])
                
                tseg=self.dt*nmp
                self.ddf[i]=1./tseg

#                print(' nmp=%d  ddf=%8.4g  dt=%8.4g  ss=%8.4g  tseg=%8.4g   ' %(nmp,self.ddf[i],self.dt,self.ss[i],tseg)) 
                
                NC=NC+1
            else:
                break
              
#        print(' *** ')      

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

        self.psd_th *= (self.spec_grms / stddev)

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

        sr = fmax * 16.
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
            p=int(floor((i+i+k+1)/2))

        else:     

                
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
    