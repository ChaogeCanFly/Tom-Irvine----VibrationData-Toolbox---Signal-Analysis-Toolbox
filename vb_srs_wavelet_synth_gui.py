###########################################################################
# program: vb_srs_wavelet_synth_wavelet_synth_gui.py
# author: Tom Irvine
# Email: tom@irvinemail.org
# version: 1.0
# date: September 16, 2016
# description:  shock response spectrum damped sine synthesis
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
import time

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

from vb_utilities import WriteData2,WriteData3,WriteData5
from vb_utilities import read_two_columns_from_dialog,SRS_function,DSS_waveform_reconstruction,SRS_coefficients

################################################################################

class vb_srs_wavelet_synth:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        self.master.minsize(750,500)
        self.master.geometry("850x550")

        self.master.title("vb_srs_wavelet_synth_gui.py ver 1.0  by Tom Irvine")         
        
        self.num=0
        self.num_fn=0
        
        
        self.e1=0.
        self.e2=0.
        
        self.a=[]
        self.b=[]
        self.dt=0
        self.sr=0  
        
        self.tt=[]
        self.acc=[]
        self.vel=[]
        self.disp=[]
        self.fn=[]       
        self.pos=[]
        self.neg=[]       
        self.wavelet_table=[]      
        
        self.wavelet_accel=[]

        crow=0
        
        self.hwtext1=tk.Label(top,text='Synthesize a time history to satisfy an SRS specification using a damped sine series with wavelet reconstruction')
        self.hwtext1.grid(row=crow, column=0, columnspan=7, pady=4,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  Natural Frequency (Hz) & SRS (G)')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=3,sticky=tk.W)

        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='The sample rate should be >= 10x max SRS frequency')
        self.hwtext2.grid(row=crow, column=0, columnspan=5, pady=3,sticky=tk.W)       
        
        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='The duration should be > 1/( min SRS frequency)')
        self.hwtext2.grid(row=crow, column=0, columnspan=5, pady=3,sticky=tk.W)             

###############################################################################

        crow=crow+1

        self.button_read = tk.Button(top, text="Read Input File", command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=16,sticky=tk.W)  


###############################################################################

        crow=crow+1

        self.hwtextLbx=tk.Label(top,text='Select Units')
        self.hwtextLbx.grid(row=crow, column=0,padx=3)

        self.hwtextLbx=tk.Label(top,text='Q')
        self.hwtextLbx.grid(row=crow, column=1,padx=5)
        
        self.hwtextLbx=tk.Label(top,text='Max Number of Damped Sine Trials')
        self.hwtextLbx.grid(row=crow, column=2,padx=5)   
        
        self.hwtextLbx=tk.Label(top,text='Number of Wavelets')
        self.hwtextLbx.grid(row=crow, column=3,padx=5)   
        
        self.hwtextLbx=tk.Label(top,text='Trials per Wavelet')
        self.hwtextLbx.grid(row=crow, column=4,padx=5)        

###############################################################################

        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=3,exportselection=0)
        self.Lb1.insert(1, "G, in/sec, in")
        self.Lb1.insert(2, "G, cm/sec, mm")
        self.Lb1.insert(3, "m/sec^2, cm/sec, mm")        
        self.Lb1.grid(row=crow, column=0, pady=1)
        self.Lb1.select_set(0) 

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 5,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=1,sticky=tk.N,pady=1)


        self.ntrialsr=tk.StringVar()  
        self.ntrialsr.set('100')  
        self.ntrials_entry=tk.Entry(top, width = 7,textvariable=self.ntrialsr)
        self.ntrials_entry.grid(row=crow, column=2,sticky=tk.N,pady=1)
        
        
        self.nwaveletsr=tk.StringVar()  
        self.nwaveletsr.set('500')  
        self.nwavelets_entry=tk.Entry(top, width = 7,textvariable=self.nwaveletsr)
        self.nwavelets_entry.grid(row=crow, column=3,sticky=tk.N,pady=1)
        
        
        self.nwtrialsr=tk.StringVar()  
        self.nwtrialsr.set('3000')  
        self.nwtrials_entry=tk.Entry(top, width = 7,textvariable=self.nwtrialsr)
        self.nwtrials_entry.grid(row=crow, column=4,sticky=tk.N,pady=1)

###############################################################################

        crow=crow+1

        self.hwtextf1=tk.Label(top,text='Enter Sample Rate (Hz)')
        self.hwtextf1.grid(row=crow, column=0,padx=5, pady=8)

        self.hwtextf2=tk.Label(top,text='Enter Duration (sec)')
        self.hwtextf2.grid(row=crow, column=1,padx=5, pady=8)

###############################################################################

        crow=crow+1

        self.srr=tk.StringVar()  
        self.srr.set('')  
        self.sr_entry=tk.Entry(top, width = 10,textvariable=self.srr)
        self.sr_entry.grid(row=crow, column=0,padx=5, pady=1)
        self.sr_entry.config(state=tk.DISABLED)

        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 8,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=1,padx=5, pady=1)
        self.dur_entry.config(state=tk.DISABLED)

###############################################################################

        crow=crow+1

        self.button_calculate = tk.Button(top, text="Calculate", command=self.srs_synth_calculation)
        self.button_calculate.config( height = 2, width = 18,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0,columnspan=1,padx=3, pady=20) 
             
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))

        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=3,pady=20)

################################################################################

        crow=crow+1

        self.hwtextext_exsrs=tk.Label(top,text='Export Data')
        self.hwtextext_exsrs.grid(row=crow, column=0,pady=10)  
        self.hwtextext_exsrs.config(state = 'disabled')

################################################################################
    
        crow=crow+1

        self.button_sa = tk.Button(top, text="Acceleration", command=self.export_a)
        self.button_sa.config( height = 2, width = 15,state = 'disabled' )
        self.button_sa.grid(row=crow, column=0,columnspan=1, pady=3, padx=2)  

        self.button_sv = tk.Button(top, text="Velocity", command=self.export_v)
        self.button_sv.config( height = 2, width = 15,state = 'disabled' )
        self.button_sv.grid(row=crow, column=1,columnspan=1, pady=3, padx=2) 

        self.button_sd = tk.Button(top, text="Displacement", command=self.export_d)
        self.button_sd.config( height = 2, width = 15,state = 'disabled' )
        self.button_sd.grid(row=crow, column=2,columnspan=1, pady=3, padx=2) 
        
        self.button_ssrs = tk.Button(top, text="SRS", command=self.export_srs)
        self.button_ssrs.config( height = 2, width = 15,state = 'disabled' )
        self.button_ssrs.grid(row=crow, column=3,columnspan=1, pady=3, padx=2)         

        self.button_swt = tk.Button(top, text="Wavelet Table", command=self.export_wt)
        self.button_swt.config( height = 2, width = 15,state = 'disabled' )
        self.button_swt.grid(row=crow, column=4,columnspan=1, pady=3, padx=2)  
           
################################################################################            

    def read_data(self):            
            
        self.a,self.b,self.num=\
            read_two_columns_from_dialog('Select Acceleration File',self.master)
        
        self.sr_entry.config(state=tk.NORMAL)
        tstring= str(int(round(10*max(self.a))))
        self.srr.set(tstring)     
        
        self.dur_entry.config(state=tk.NORMAL) 
        tstring= str(1.6/min(self.a))               
        self.durr.set(tstring)  
        
        
        plt.ion()
        plt.clf()
        plt.figure(1,figsize=(8,6))

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        
        self.Q=float(self.Qr.get())
        
        title_string= 'Shock Response Spectrum Q='+str(self.Q)     

        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= 'Shock Response Spectrum Q='+str(i)
                break
        
        self.n_input_freq=len(self.a)         
        
        self.f1=self.a[0]
        self.f2=self.a[self.n_input_freq-1]
        
        self.y2= 10**(np.ceil(np.log10(max(self.b))+0.2))
        self.y1= 10**(np.floor(np.log10(min(self.b))))        
      
        plt.grid(True)
        plt.xlabel('Natural Frequency (Hz)')
  
        iunit=int(self.Lb1.curselection()[0])
        
        if(iunit<=1):
            plt.ylabel('Peak Accel (G)')        
        else:
            plt.ylabel('Peak Accel (m/sec^2)')            

        plt.title(title_string)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim([self.f1,self.f2])
        plt.ylim([self.y1,self.y2])
        plt.grid(True,which="major",ls="-")
        plt.grid(True,which="minor",ls="--")   
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        
        time.sleep(2)
        self.button_calculate.config(state = 'normal')  
  
   

    def srs_synth_calculation(self):  

        print("\n beginning calculation... may be slow...\n") 

        fig_num=2

        nwtrials=int(self.nwtrialsr.get())

        ntrials=int(self.ntrialsr.get())
        iamax=ntrials    

        Q=float(self.Qr.get())
        damp=1./(2.*Q)

        sr=float(self.srr.get())
        dur=float(self.durr.get()) 
        duration=dur

     
        dt=1./sr          
        
        nt=int(np.round(dur/dt)) 
        
        octave=(2.**(1./12.))
       
        tpi=2.*np.pi

        FMAX=500  # leave 
        
        errlit=1.0e+90
        syn_error = 1.0e+91

        error_before=1.0e+90
        
        iunit=int(self.Lb1.curselection()[0])   

        f=self.a
        a=self.b
        
        n=self.n_input_freq
        
        ffirst=f[0]
        flast=f[n-1]
        last_f=f[n-1]
        last_a=a[n-1]

        ffmin=ffirst
        ffmax=flast
        
#        srs_spec=np.column_stack((f,a))

        slope=np.zeros(n)

        for i in range(0,(n-1)):    
            slope[i]=np.log(a[i+1]/a[i])/np.log(f[i+1]/f[i])


#        dre=4./f[0]

        first=0

        ns=int(nt)

# number of iterations for inner loop

        ntt=100

# Interpolating reference

        rf=np.zeros(FMAX)
        ra=np.zeros(FMAX)

        rf[0]=f[0]
        ra[0]=a[0]

        for i in range(1,FMAX):

            rf[i]=rf[i-1]*octave

            if( rf[i] == max(f) ):
                break
    
            if( rf[i] > max(f) ):
                rf[i]=max(f)
                break
    

        last=i
  
 #       print("last=%ld" %last)
      
###################################################
        
        for i in range(0,last):   
            
            for j in range(0,n-1):

                if( rf[i] > f[j] and rf[i] <f[j+1]):
                    ra[i]=a[j]*( (rf[i]/f[j])**slope[j] )
                    break
        
                if( rf[i]==f[j]):
                    ra[i]=a[j]
                    break
        
                if( rf[i]==f[j+1]):   
                    ra[i]=a[j+1]
                    break
        
        rf[last-1]=last_f
        ra[last-1]=last_a

        
 #       print("ref 1")

####################################################        

        jkj=1

        best_amp=np.zeros(last)
        best_phase=np.zeros(last)
        best_delay=np.zeros(last)
        best_dampt=np.zeros(last)

 #       freq=rf
        
        omega=tpi*rf
        
        ac,bc=SRS_coefficients(damp,omega,dt)

 #         print("ref 2a")

        iacase=0
        icase=0
        
        start = time.time()   
        
        tx=np.zeros(ns)        
        
        for i in range(0,ns):
            tx[i]=i*dt

        for ia in range(0,ntrials):
            
            if(ia>=1):
                end = time.time()
                elapsed = end - start
            
                time_per_trial=elapsed/(float(ia))
            
                remaining=(ntrials-ia)*time_per_trial            
            
                print(" ")
            
                m, s = divmod(elapsed, 60)
                h, m = divmod(m, 60)
                print("  Elapsed time = %d hr %02d min %02d sec" % (h, m, s))   
                self.e1=elapsed
            
                m, s = divmod(remaining, 60)
                h, m = divmod(m, 60)
                print("Remaining time = %d hr %02d min %02d sec  for phase 1" % (h, m, s))            
            
                print(" ")             
            
 #           print("ref 2b")            
    
            iflag=0

#     Calculating damped sine parameters.

            amp,phase,delay,dampt,sss,first=                                  \
            vb_srs_wavelet_synth.DSS_sintime(ns,dt,dur,tpi,ia,iamax,ra,   \
                         omega,last,syn_error,best_amp,best_phase,best_delay, \
                                                              best_dampt,first)
                                                              
                                                              
            if(ia==0):
                store=np.zeros(ns)                                                              
                                                              
 #           print("ref 3")

#   Synthesizing initial time history. 

            acc,sym=vb_srs_wavelet_synth.DSS_th_syn(ns,amp,sss,last)
            
 #           print("ref 4")
            
            nlf=len(ac[:,0])
            
            xmin,xmax,xabs=SRS_function(nlf,acc,ac,bc)
            
 #           print("ref 5")            
            
 #            for ik in range(0,len(xmax)):
 #                print("%ld  max=%8.4g  min=%8.4g " %(ik,xmax[ik],xmin[ik]))                
            
                       
            
            for ijk in range(0,ntt):   
                
            
                for i in range(0,last-1):
                    
                    xx = (xmax[i] + abs(xmin[i]))/2. 

                    if(xx <1.0e-90):
                        iflag=1
            
                    amp[i]=amp[i]*((ra[i]/xx)**0.25)
        
                if(iflag==1):
                    break
                
#                print(" max abs amp =%8.4g" % max(abs(amp)))
                
#                print("ref 6") 
        
                sym,acc=vb_srs_wavelet_synth.DSS_scale_th(ns,last,acc,amp,sss)
                
#                print("ref 7  %ld" %ijk) 

                nk=int(np.round(0.9*ns))
                LLL=ns-nk-1
                
                        
                for i in range(nk,ns):
                    x=(i-nk)
                    acc[i]*=(1.-(float(x)/float(LLL)))
        
                acc[ns-1]=0.         
        
                fper=3.
                fper=fper/100.

                n=ns

                na=int(np.round(fper*n))
#                        nb=n-na
#                        delta=n-nb

#                print("ref 8  %ld  na=%ld" %(ijk,na)) 

                for i in range(1,na+1):
                    arg=np.pi*(( float(i-1)/float(na-1) )+1.) 
                    acc[i]*=0.5*(1.+(np.cos(arg)))

 #                print("ref 8  %ld" % ijk) 
                
                xmin,xmax,xabs=SRS_function(last,acc,ac,bc)

 #                print("ref 9  %ld" % ijk) 

                syn_error,iflag=vb_srs_wavelet_synth.DSS_srs_error(last,xmax,xmin,ra,iflag)

 #                print("ref 10  %ld" % ijk) 

                if(iflag==1):
                    break
        
                sym= 20*np.log10(abs(max(acc)/min(acc)))
                sym=abs(sym)
                
                        
                if( ((syn_error < errlit) and (sym < 2.5)) or ia==0):
                            
                    iacase =ia
                    icase = ijk

                    errlit = syn_error
#                    symlit = sym

#                    print("\n %ld %ld  best= %8.4g  sym= %8.4g" %(ia,ijk,syn_error,sym))
            
                    for k in range(0,last-1):                                
                                
                        best_amp[k]=amp[k]
                        best_phase[k]=phase[k]
                        best_dampt[k]= dampt[k]
                        best_delay[k]=delay[k]
            
                        store=acc
        
                print(" %ld %ld  error= %8.4g   best= %8.4g  " %(ia,ijk,syn_error,errlit))

                if(ijk>8 and syn_error > error_before):  
                    break
        
                if(ijk>8 and sym>3.0):  
                    break
                
                if(ijk>2 and syn_error> 7.0*errlit):
                    break                     
                
                if(ijk>4 and syn_error> 5.0*errlit):
                    break                    
                
                if(ijk>6 and syn_error> 4.0*errlit):
                    break                   
                
                if(ijk>8 and syn_error> 3.0*errlit):
                    break                
                
                if(ijk>10 and syn_error> 2.0*errlit):
                    break
  
                if(ijk>20 and syn_error> 1.5*errlit):
                    break              
           
                if(ijk>1 and syn_error > 1.0e+90):
                   break
        
                error_before=syn_error
                
            if(errlit<0.35 and ia>5):
                break
        
            if(jkj==1):
                jkj=2
            else:
                jkj=1


        print(" \n\n Best case is %ld %ld " %(iacase,icase))

        self.wavelet_accel=vb_srs_wavelet_synth.add_pre_shock(store,dur,dt)
      
      
###############################################################################
      
        xmin,xmax,xabs=SRS_function(last,self.wavelet_accel[:,1],ac,bc)

        plt.close(fig_num)
        plt.figure(fig_num,figsize=(8,6))
        fig_num+=1

        w=2.**(0.5)

        MM=len(self.b)
        
        tol1=np.zeros(MM)      # must do the long way
        tol2=np.zeros(MM)
        
        for i in range(0,MM):
            bb=float(self.b[i])
            tol1[i]=w*bb
            tol2[i]=bb/w

        plt.plot(self.a, self.b, linewidth=1.0,color='k',label="Spec and +/- 3dB Tol")        # disregard error
        plt.plot(self.a, tol1, linewidth=1.0,color='k')  
        plt.plot(self.a, tol2, linewidth=1.0,color='k')          
        
        fn=omega[0:last]/tpi
        
        print("l fn %8.4g" %(len(fn)))   
        print("xmax %8.4g" %(len(xmax))) 
        
        plt.plot(fn,xmax,color='b',label="Pos Synthesis")
        plt.plot(fn,xmin,color='g',label="Neg Synthesis")  
        plt.legend(loc="upper left")  
       
        plt.grid(True)
        
        self.Q=float(self.Qr.get())
        
        title_string= 'Shock Response Spectrum Q='+str(self.Q)     

        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= 'Shock Response Spectrum Q='+str(i)
                break
        
        self.n_input_freq=len(self.a)         
        
        self.f1=self.a[0]
        self.f2=self.a[self.n_input_freq-1]
        
        self.y2= 10**(np.ceil(np.log10(max(self.b))+0.2))
        self.y1= 10**(np.floor(np.log10(min(self.b))))        
      
        plt.grid(True)
        plt.xlabel('Natural Frequency (Hz)')
  
        iunit=int(self.Lb1.curselection()[0])
        
        if(iunit<=1):
            plt.ylabel('Peak Accel (G)')        
        else:
            plt.ylabel('Peak Accel (m/sec^2)')            

        plt.title(title_string)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim([self.f1,self.f2])
        plt.ylim([self.y1,self.y2])
        plt.grid(True,which="major",ls="-")
        plt.grid(True,which="minor",ls="--")   
    
        plt.draw()         
        
###############################################################################        
        
        t=self.wavelet_accel[:,0] 

        
        ds_temp=(self.wavelet_accel[:,1])*1.  # keep this to avoid serious error

        
        freq=rf
        nfr=len(freq)
                
# waveform reconstruction        
                
        nwavelets=int(self.nwaveletsr.get())        
        
#        acceleration,velocity,displacement,srs_syn,srs_syn_abs,wavelet_table,te2=\
#        vb_srs_wavelet_synth.vibrationdata_DSS_waveform_reconstruction(t,\
#              self.wavelet_accel,dt,first,freq,ffmin,ffmax,damp,iunit,nt,nfr,ac,bc,duration,nwavelets,nwtrials)

        acceleration,velocity,displacement,srs_syn,srs_syn_abs,wavelet_table,te2=\
        DSS_waveform_reconstruction(t,ds_temp,dt,first,freq,\
                                    ffmin,ffmax,omega,damp,iunit,nt,nfr,ac,bc,\
                                                   duration,nwavelets,nwtrials)

#        plt.figure(fig_num,figsize=(8,6.5))
#        fig_num+=1
#        plt.plot(self.wavelet_accel[:,0],self.wavelet_accel[:,1], linewidth=1.0,color='g')




##################

        self.tt=acceleration[:,0]
        self.acc=acceleration[:,1]
        self.vel=velocity[:,1]
        self.disp=displacement[:,1]
        self.fn=srs_syn[:,0]
        self.pos=srs_syn[:,1]
        self.neg=srs_syn[:,2]
        self.wavelet_table=wavelet_table

################## 

        print("\n generating plots ") 


        plt.ion()
        plt.close(fig_num)
        plt.figure(fig_num,figsize=(8,6.5))
        fig_num+=1
        plt.subplot(211)
        plt.plot(self.wavelet_accel[:,0],self.wavelet_accel[:,1], linewidth=1.0,color='b')
        title_string= 'Damped Sine Time History'     
        plt.title(title_string)
        plt.grid(True)
        
        plt.xlabel('Time (sec)') 
        if(iunit<=1):
            plt.ylabel('Accel (G)')        
        else:
            plt.ylabel('Accel (m/sec^2)')          
            
#        print(acceleration.shape)

        plt.subplot(212)
        plt.plot(acceleration[:,0],acceleration[:,1], linewidth=1.0,color='b') 
        title_string= 'Damped Sine Time History with Wavelet Reconstruction'     
        plt.title(title_string)
        plt.grid(True)

        plt.xlabel('Time (sec)') 
        if(iunit<=1):
            plt.ylabel('Accel (G)')        
        else:
            plt.ylabel('Accel (m/sec^2)')  
        
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)         
        plt.draw()
        

################## 
 
        plt.close(fig_num)
        plt.figure(fig_num,figsize=(8,6))
        fig_num+=1
        
        print(" max abs %8.4g " %max(srs_syn_abs[:,1]))

        w=2.**(0.5)

        MM=len(self.b)
        
        tol1=np.zeros(MM)      # must do the long way
        tol2=np.zeros(MM)
        
        for i in range(0,MM):
            bb=float(self.b[i])
            tol1[i]=w*bb
            tol2[i]=bb/w

        plt.plot(self.a, self.b, linewidth=1.0,color='k',label="Spec and +/- 3dB Tol")        # disregard error
        plt.plot(self.a, tol1, linewidth=1.0,color='k')  
        plt.plot(self.a, tol2, linewidth=1.0,color='k')          
        
        plt.plot(srs_syn[:,0],srs_syn[:,1],color='b',label="Pos Synthesis")
        plt.plot(srs_syn[:,0],srs_syn[:,2],color='g',label="Neg Synthesis")  
        plt.legend(loc="upper left")  
       
        plt.grid(True)
        
        self.Q=float(self.Qr.get())
        
        title_string= 'Shock Response Spectrum Q='+str(self.Q)     

        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= 'Shock Response Spectrum Q='+str(i)
                break
        
        self.n_input_freq=len(self.a)         
        
        self.f1=self.a[0]
        self.f2=self.a[self.n_input_freq-1]
        
        self.y2= 10**(np.ceil(np.log10(max(self.b))+0.2))
        self.y1= 10**(np.floor(np.log10(min(self.b))))        
      
        plt.grid(True)
        plt.xlabel('Natural Frequency (Hz)')
  
        iunit=int(self.Lb1.curselection()[0])
        
        if(iunit<=1):
            plt.ylabel('Peak Accel (G)')        
        else:
            plt.ylabel('Peak Accel (m/sec^2)')            

        plt.title(title_string)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim([self.f1,self.f2])
        plt.ylim([self.y1,self.y2])
        plt.grid(True,which="major",ls="-")
        plt.grid(True,which="minor",ls="--")   
    
        plt.draw()        
        
        self.hwtextext_exsrs.config(state = 'normal')
        self.button_sa.config( height = 2, width = 15,state = 'normal' )
        self.button_sv.config( height = 2, width = 15,state = 'normal' )
        self.button_sd.config( height = 2, width = 15,state = 'normal' )
        self.button_ssrs.config( height = 2, width = 15,state = 'normal' )
        self.button_swt.config( height = 2, width = 15,state = 'normal' )
                      
        print(" plots complete ") 
        
        ttee=float(0.)
        ttee=float(self.e1)+float(te2)
        m, s = divmod(ttee, 60)
        h, m = divmod(m, 60)
        print("\n Total time = %d hr %02d min %02d sec" % (h, m, s))  


################## 

        ttt=acceleration[:,0]

        
        plt.close(fig_num)
        plt.figure(fig_num,figsize=(8,8))
        fig_num+=1

        plt.subplot(311)
        plt.plot(ttt,acceleration[:,1], linewidth=1.0,color='b')
        title_string= 'Acceleration Wavelet Reconstruction'     
        plt.title(title_string)
        plt.grid(True)
        
        plt.xlabel('Time (sec)') 
        if(iunit<=1):
            plt.ylabel('Accel (G)')        
        else:
            plt.ylabel('Accel (m/sec^2)')          
            
            
        plt.subplot(312)
        plt.plot(ttt,velocity[:,1], linewidth=1.0,color='b') 
        title_string= 'Velocity'     
        plt.title(title_string)
        plt.grid(True)

        plt.xlabel('Time (sec)') 
        if(iunit<=0):
            plt.ylabel('Vel (in/sec)')        
        else:
            plt.ylabel('Vel (m/sec)')  
            
            
        plt.subplot(313)
        plt.plot(ttt,displacement[:,1], linewidth=1.0,color='b') 
        title_string= 'Displacement'     
        plt.title(title_string)
        plt.grid(True)

        plt.xlabel('Time (sec)') 
        if(iunit<=0):
            plt.ylabel('Disp (in)')        
        else:
            plt.ylabel('Disp (cm/sec)')  
         
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0) 

        plt.draw()
               
   
###############################################################################
   

  
###############################################################################

    @classmethod
    def add_pre_shock(cls,store,dur,dt):

        nm=len(store)

        tstart=dur/20.

        npre=int(round(tstart/dt))

        ntotal=nm+npre

        tt=np.zeros([ntotal,1])
        temp=np.zeros([ntotal,1])

        ijk=1

        for i in range(0,ntotal):
            
            tt[i]=-tstart+(i-1)*dt
            if(i>npre):
                temp[i]=store[ijk]
                ijk=ijk+1

        acceleration=np.column_stack((tt,temp))

        return acceleration

###############################################################################

    @classmethod
    def DSS_srs_error(cls,last,xmax,xmin,ra,iflag):
    
        error=0.

        for i in range(0,last):
            if( xmax[i] <=0 or xmin[i] <=0):
                iflag=1
                error=1.0e+99
                break
       
        db=abs(20.*np.log10(xmin[i]/ra[i]))

        if(db>error):      
           error=db
          
        db=abs(20.*np.log10(xmax[i]/ra[i]))

        if(db>error):
                error=db    
    
        return error,iflag

###############################################################################

    @classmethod
    def DSS_scale_th(cls,ns,last,acc,amp,sss):

        for j in range(0,ns):
 
            acc[j]= sum(amp[0:last]*sss[0:last,j])

        big=max(acc)
        small=min(acc)
        
#        print("big=%8.4g  small=%8.4g " % (big,small))

        acc[0]=0.

        sym = abs(20*np.log10( big/abs(small)))

#        print("sym=%8.4g" %sym)
        
        return sym,acc

###############################################################################
   
    
###############################################################################    

    @classmethod    
    def DSS_th_syn(cls,ns,amp,sss,last):
        
        acc=np.zeros(ns)
        

        for j in range(0,ns):

            acc[j]=sum(amp[0:last]*sss[0:last,j])   

#            if(j<300):
#                print(" acc[%ld]=%8.4g" % (j,acc[j] ))     
            
        acc[0]=0.
        
        big=max(acc)
        small=min(acc)

        sym = abs(20*np.log10( big/abs(small)))

        if(sym ==0):
            print("  error: sym=%8.4g ",sym)     

#       for ik in range(0,last):
#           print(" amp[%ld]=%8.4g" % (ik,amp[ik]))

#        print(" max acc =%8.4g" % big )           
 #       print(" min acc =%8.4g" % small) 
        
 #       plt.figure(2)
 #       plt.plot(acc, linewidth=1.0,color='b')    
               
        return acc,sym

###############################################################################

    @classmethod    
    def DSS_sintime(cls,ns,dt,dur,tpi,ia,iamax,ra,omega,last,syn_error, \
                          best_amp,best_phase,best_delay,best_dampt,first):
        
        amp=np.zeros(last)
        phase=np.zeros(last)
        delay=np.zeros(last)
        dampt=np.zeros(last)
        sss=np.zeros([last,ns])

        if( (ia < 12 ) or np.random.rand()<0.5):
    
            for i in range(0,last):
       
                amp[i]=(ra[i]/10.)
                
                if(np.random.rand()<0.5):
                    amp[i]=-amp[i]
            
                phase[i]=0

                delay[i] = first + 0.020*dur*np.random.rand()
                dampt[i] = 0.003 + 0.035*np.random.rand()
        
    
        else:
    
            for i in range(0,last):

                amp[i]=     best_amp[i]*(0.99+0.02*np.random.rand())
                phase[i]= best_phase[i]*(0.99+0.02*np.random.rand())
                delay[i]= best_delay[i]*(1.0+0.02*np.random.rand())

                if(delay[i] > 0.015*dur):
                    delay[i]=0.015*dur
            
                dampt[i]= best_dampt[i]*(0.99+0.02*np.random.rand())

        tv=np.linspace(0,dur,num=ns)

        for k in range(0,last):
            
            index1=int(np.floor(delay[k]/dur))*ns
    
            ft=omega[k]*(tv[index1:ns]-delay[k])
            sss[k,index1:ns]=np.exp(-dampt[k]*ft)*np.sin(ft)   
            ft=None
           
        return amp,phase,delay,dampt,sss,first

################################################################################
    
    def export_a(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the acceleration time history filename")           
        output_file = output_file_path.rstrip('\n')    
       
        num=len(self.tt)
        WriteData2(num,self.tt,self.acc,output_file)

    def export_v(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the velocity time history filename")           
        output_file = output_file_path.rstrip('\n')    

        num=len(self.tt)        
        WriteData2(num,self.tt,self.vel,output_file)
        
    def export_d(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the displacement time history filename")           
        output_file = output_file_path.rstrip('\n')    
        
        num=len(self.tt)        
        WriteData2(num,self.tt,self.disp,output_file)       
        
    def export_srs(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the SRS filename")           
        output_file = output_file_path.rstrip('\n')    
        
        num=len(self.fn)
        WriteData3(num,self.fn,self.pos,self.neg,output_file)       
       
       
    def export_wt(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the wavelet table filename")           
        output_file = output_file_path.rstrip('\n')    
        
        num=len(self.wavelet_table[:,0])
        WriteData5(num,\
                   self.wavelet_table[:,0],\
                   self.wavelet_table[:,1],\
                   self.wavelet_table[:,2],\
                   self.wavelet_table[:,3],\
                   self.wavelet_table[:,4],output_file)

            
################################################################################

def quit(root):
    root.destroy()