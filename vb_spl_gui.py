########################################################################
# program: vb_spl_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.2
# date: September 11, 2013
# description:  
#    
#  Calculate the sound pressure level for a pressure time history
#              
########################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename

           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       

    

from vb_utilities import sample_rate_check,read_two_columns_from_dialog,WriteData2

from math import sqrt,log,log10
from numpy import zeros,mean,round,floor

from scipy.fftpack import fft

import matplotlib.pyplot as plt



###############################################################################

class vb_SPL:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
    
    
    
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.32))
        self.master.geometry("%dx%d+0+0" % (w, h) )       
        
        
        self.master.title("vb_spl_gui.py ver 1.2  by Tom Irvine")  
        
        
        
        self.a=[]
        self.b=[]
        
        self.tim=[]
        self.amp=[]
        
        self.pf=[]
        self.pspl=[]        
        
        self.num=0
        self.dt=0
        self.sr=0

        self.ss=zeros(100,'int')
        self.seg=zeros(100,'int')
        self.i_seg=zeros(100,'int')
        self.ddf=zeros(100,'float')     
        
        self.r_ss=[]
        self.r_seg=[]
        self.r_i_seg=[]
        self.r_ddf=[]
        self.rms=0
        self.freq=[]
        self.full=[]
        self.mH=0
        self.NW=0
        self.mmm=0
        
###############################################################################
        
        crow=0
        
        self.hwtext0=tk.Label(top,text='This script calculates sound pressure level of a time history.')
        self.hwtext0.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.NW)

        crow=crow+1            

        self.hwtext3=tk.Label(top,text='The input file must have two columns: time(sec) & pressure')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.NW)
        
###############################################################################        
        
        crow=crow+1        
        
        self.hwtext4=tk.Label(top,text='Select Amplitude Unit')
        self.hwtext4.grid(row=crow, column=1, padx=15,columnspan=1, pady=10)

        self.hwtext5=tk.Label(top,text='Select Weighting Network')
        self.hwtext5.grid(row=crow, column=2, padx=15,columnspan=1, pady=10)           

###############################################################################

        crow=crow+1

        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=9,sticky=tk.NW)
        
        self.Lbu = tk.Listbox(top,height=4,width=12,exportselection=0)
        self.Lbu.insert(1, "psi")
        self.Lbu.insert(2, "Pa")
        self.Lbu.insert(3, "micro Pa")                
        self.Lbu.grid(row=crow, column=1, padx=15,sticky=tk.N)
        self.Lbu.select_set(0) 
        
        self.Lbw = tk.Listbox(top,height=4,width=6,exportselection=0)
        self.Lbw.insert(1, "none")
        self.Lbw.insert(2, "A")
        self.Lbw.insert(3, "B")  
        self.Lbw.insert(4, "C")               
        self.Lbw.grid(row=crow, column=2, padx=15,sticky=tk.N)
        self.Lbw.select_set(0)  
        
        crow=crow+1

        self.hwtext3b=tk.Label(top,text='Select Duration')
        self.hwtext3b.grid(row=crow, column=0, columnspan=1, pady=7,sticky=tk.S)

        self.hwtextt1=tk.Label(top,text='Start Time (sec)')
        self.hwtextt1.grid(row=crow, column=1,padx=3, pady=12)
        
        self.hwtextt2=tk.Label(top,text='End Time (sec)')
        self.hwtextt2.grid(row=crow, column=2,padx=0, pady=12)    
        
################################################################################

        crow=crow+1        
        
        self.Lb_ws = tk.Listbox(top,height=2,exportselection=0)
        self.Lb_ws.insert(1, "Whole Time History")
        self.Lb_ws.insert(2, "Segment")
        self.Lb_ws.grid(row=crow, column=0,padx=10,sticky=tk.N)
        self.Lb_ws.select_set(0)
        self.Lb_ws.bind('<<ListboxSelect>>',self.time_option)
        
        self.tmir=tk.StringVar()  
        self.tmir.set('')  
        self.tmi_entry=tk.Entry(top, width = 8,textvariable=self.tmir,state = 'disabled')
        self.tmi_entry.grid(row=crow, column=1,padx=3, pady=5,sticky=tk.N)
        self.tmi_entry.bind("<KeyPress>", self.OnKeyPress)
  
        self.tmer=tk.StringVar()  
        self.tmer.set('')         
        self.tme_entry=tk.Entry(top, width = 8,textvariable=self.tmer,state = 'disabled')
        self.tme_entry.grid(row=crow, column=2,padx=0, pady=5,sticky=tk.N)       
        self.tme_entry.bind("<KeyPress>", self.OnKeyPress)   

###############################################################################

        crow=crow+1  
        
        self.button_process = tk.Button(top, text="Show Processing Options",command=self.processing_options)
        self.button_process.config( height = 2, width = 25,state = 'disabled')
        self.button_process.grid(row=crow, column=0, padx=5, pady=20)

###############################################################################

        
        myframe=tk.Frame(top)
        myframe.grid(row=crow, column=1,columnspan=2,padx=3, pady=20)
        scrollbar = tk.Scrollbar(myframe) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Lba = tk.Listbox(myframe, width=35, yscrollcommand=scrollbar.set) 
        self.Lba.pack()
        scrollbar.config(command=self.Lba.yview)         
        
###############################################################################
        
        crow=crow+1  

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0, pady=20) 
        
        self.button_save = tk.Button(top, text="Save SPL", command=self.export_spl)
        self.button_save.config( height = 2, width = 15,state = 'disabled')
        self.button_save.grid(row=crow, column=1, pady=20) 
        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2, padx=10,pady=20)
        
###############################################################################

    def OnKeyPress(self,event):
        self.button_calculate.config(state = 'disabled')  
        self.Lba.delete(0, tk.END) # clear        
        
###############################################################################
        
    def processing_options(self):
        
        self.button_calculate.config(state = 'normal')          
        self.advise(self)

###############################################################################        

    def time_option(self,val):
        sender=val.widget
        n= int(sender.curselection()[0])
        
        if(n==0):
            self.tme_entry.config(state = 'disabled')         
            self.tmi_entry.config(state = 'disabled')             
        else:
            self.tme_entry.config(state = 'normal')         
            self.tmi_entry.config(state = 'normal')          

###############################################################################
        
    def export_spl(self):
        output_file_path = asksaveasfilename(parent=self.master,title="Enter the SPL filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2(len(self.pf),self.pf,self.pspl,output_file)    
        
###############################################################################

    @classmethod      
    def advise(cls,self):
        
        tmi=float(self.tmir.get()) 
        tme=float(self.tmer.get()) 
        
        k=0
        for i in range(0,self.num):
            if(self.a[i]>=tmi and self.a[i]<=tme):             
                k=k+1
                

        self.aa=self.a[0:k-1]
        self.bb=self.b[0:k-1]         

        
        self.num=k
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
        
        for i in range(0,NC):
            if( t_seg[i]>0 ):
                out1='sps=%d,  df=%6.3g Hz,  sdof=%d' \
                                       %(t_ss[i],t_ddf[i],2*t_i_seg[i])
                self.Lba.insert(i, out1)

                self.r_ss.append(t_ss[i])
                self.r_seg.append(t_ddf[i])
                self.r_i_seg.append(t_i_seg[i])        
                self.r_ddf.append(t_ddf[i]) 

                k=k+1
                    
            if(i==12):
                break

        self.Lba.select_set(0) 
        
###############################################################################        

    def calculation(self):
        nu= int(self.Lbu.curselection()[0])
        
        if(nu==0):
            p_unit='psi'
            ref = 2.9e-09
                
        if(nu==1):            
            p_unit='Pa'
            ref = 20.e-06
            
        if(nu==2):
            p_unit='micro Pa'    
            ref = 20.      
            
        plt.close(1)
        plt.figure(1)

        plt.plot(self.a, self.b, linewidth=1.0,color='b')        # disregard error
       
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel(p_unit)  
        plt.title('Input Time History') 
        
        st=float(self.tmir.get()) 
        te=float(self.tmer.get())                 


        j=1
        jfirst=0
        jlast=self.num
        
        for i in range (0,self.num):
            if(self.a[i]<st):
                jfirst=i
    
            if(self.a[i]>te):
                jlast=i
                break
    
        self.tim=self.a[jfirst:jlast]
        self.amp=self.b[jfirst:jlast]

        n=len(self.tim)   
   
        print (" ")
        print (" Time history length = %d " %n)

        mu=mean(self.amp)
        self.amp=self.amp-mu 
        
        n= int(self.Lba.curselection()[0])
                
        NW=self.r_i_seg[n]
        mmm = 2**int(log(float(self.num)/float(NW))/log(2))
        df=1./(mmm*self.dt)
        
        
        tmi=self.tim[0]
        
        io=2   # 50% overlapp

        mk,freq,time_a,dt,NW=vb_SPL.FFT_time_freq_set(mmm,NW,self.dt,df,tmi,io)                
        
        store,store_p,freq_p,max_a,max_f=vb_SPL.FFT_core_seg(NW,mmm,mk,freq,self.amp,io)        
        
        store=store.T

        imax=store.shape[0]
        jmax=store.shape[1]

#        print (" store  imax=%d  jmax=%d  " %(imax,jmax))

        full=zeros(imax,'f')

        for i in range(0,imax):
 
            ms=0 
    
            for j in range (0,jmax):
                
                ms+=0.5*store[i,j]**2
         
        
            full[i]=sqrt(2.)*sqrt(ms/jmax)    # rms

    
        fl,fc,fu,imax=vb_SPL.one_third_octave_frequencies()


        band_rms=vb_SPL.convert_FFT_to_one_third(freq,fl,fu,full)    


        splevel,oaspl=vb_SPL.convert_one_third_octave_mag_to_dB(band_rms,ref)

        self.pf,self.pspl,oaspl=vb_SPL.trim_acoustic_SPL(fc,splevel,ref) 

        nw= int(self.Lbw.curselection()[0])

        imax=len(self.pf)

        if(nw==0):
            p_rms = ref*(10**(oaspl/20.))
            print ('  pressure in air = %8.4g %s rms  \n' %(p_rms,p_unit))            
        else:
            self.pf,self.pspl,oaspl,scale_label=vb_SPL.acoustic_weighting(self.pf,self.pspl,imax,ref,nw)
            
        print ('\n OASPL = %8.4g dB  ref 20 micro Pa \n' %oaspl)


        plt.close(2) 
        plt.figure(2)    
        plt.plot(self.pf,self.pspl)
        plt.xlabel('Center Frequency (Hz)')    
        plt.ylabel('SPL (dB)')
        plt.grid(True)

        if(nw==0):
            out7= 'One-Third Octave SPL   OASPL=%7.4g dB  Ref= 20 micro Pa' %oaspl
        else:
            out7= 'One-Third Octave SPL %s-scale  OASPL=%7.4g dB  Ref= 20 micro Pa' %(scale_label,oaspl)        
    
        plt.title(out7)
        plt.xscale('log')
        plt.draw()    
        plt.show()

        self.button_save.config(state='normal')

###############################################################################

    @classmethod  
    def acoustic_weighting(cls,pf,pspl,imax,ref,iscale): 
    
        fw,aw,bw,cw=vb_SPL.SPL_weights()    


        if(iscale==1):
            ww=aw
            scale_label='A'

        if(iscale==2):
            ww=bw
            scale_label='B'    

        if(iscale==3):
            ww=cw
            scale_label='C'    

        wmax=len(fw)

        js=1

        k=0

        ms=0
    
        ft=[]
        pt=[]

        for i in range (0,imax):
            for j in range(js,wmax):
        
                dff=abs(log(pf[i]/fw[j])/log(2))

                if( dff < 0.1 ):
                    ft.append(pf[i])
                    pt.append(pspl[i]+ww[j])

                    bs=ref*10**(pt[k]/20)
                    ms=ms+bs**2

                    k=k+1
                    js=j
                    break
        
        ms=sqrt(ms)

        oaspl = 20*log10(ms/ref)

        pf=[]
        pspl=[]

        pf=ft
        pspl=pt

        return pf,pspl,oaspl,scale_label            
            
###############################################################################
            
    @classmethod                
    def one_third_octave_frequencies(cls):
    
        fc=[]

# 0 to 9

        fc.append(0.02)   
        fc.append(0.025)  
        fc.append(0.0315)  
        fc.append(0.04)
        fc.append(0.05)
        fc.append(0.063)
        fc.append(0.08)
        fc.append(0.1)
        fc.append(0.125)
        fc.append(0.16)

        i=0
        while(1):
            fc.append(10*fc[i])
            if(fc[i+10]>=20000):
                break
    
            i=i+1


        imax=len(fc)

        fl=zeros(imax,'f')
        fu=zeros(imax,'f')

        for i in range (0,imax):
            fl[i]=fc[i]/(2**(1./6.))

        for i in range (0,(imax-1)):
            fu[i]=fl[i+1]

        fu[imax-1]= fc[imax-1]*(2**(1/6))

        return fl,fc,fu,imax

###############################################################################
                    
    def read_data(self):            
            
        self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
        
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
##        plt.ylabel(self.y_string.get())  
        plt.title('Pressure Time History')        

        self.button_process.config(state = 'normal')   
                   
        out1=str('%8.4g' %self.a[0])
        out2=str('%8.4g' %self.a[self.num-1])
        
        self.tmir.set(out1) 
        self.tmer.set(out2)    
        
###############################################################################
        
    @classmethod              
    def SPL_weights(cls):
    
        fw=zeros(34,'f')
        aw=zeros(34,'f')
        bw=zeros(34,'f')
        cw=zeros(34,'f')
    
        fw[0]=10.
        aw[0]=-70.4
        bw[0]=-38.2
        cw[0]=-14.3

        fw[1]=12.5
        aw[1]=-63.4
        bw[1]=-33.2
        cw[1]=-11.2

        fw[2]=16.
        aw[2]=-56.7
        bw[2]=-28.5
        cw[2]=-8.5

        fw[3]=20.
        aw[3]=-50.5
        bw[3]=-24.2
        cw[3]=-6.2

        fw[4]=25.
        aw[4]=-44.7
        bw[4]=-20.4
        cw[4]=-4.4

        fw[5]=31.5
        aw[5]=-39.4
        bw[5]=-17.1
        cw[5]=-3.0

        fw[6]=40.
        aw[6]=-34.6
        bw[6]=-14.2
        cw[6]=-2.0

        fw[7]=50.
        aw[7]=-30.2
        bw[7]=-11.6
        cw[7]=-1.3

        fw[8]=63.
        aw[8]=-26.2
        bw[8]=-9.3
        cw[8]=-0.8

        fw[9]=80.
        aw[9]=-22.5
        bw[9]=-7.4
        cw[9]=-0.5

        fw[10]=100.
        aw[10]=-19.1
        bw[10]=-5.6
        cw[10]=-0.3

        fw[11]=125.
        aw[11]=-16.1
        bw[11]=-4.4
        cw[11]=-0.2

        fw[12]=160.
        aw[12]=-13.4
        bw[12]=-3.0
        cw[12]=-0.1

        fw[13]=200.
        aw[13]=-10.9
        bw[13]=-2.0
        cw[13]=0.

        fw[14]=250.
        aw[14]=-8.6
        bw[14]=-1.3
        cw[14]=0.

        fw[15]=315.
        aw[15]=-6.6
        bw[15]=-0.8
        cw[15]=0.

        fw[16]=400.
        aw[16]=-4.8
        bw[16]=-0.5
        cw[16]=0.

        fw[17]=500.
        aw[17]=-3.2
        bw[17]=-0.3
        cw[17]=0.

        fw[18]=630.
        aw[18]=-1.9
        bw[18]=-0.1
        cw[18]=0.

        fw[19]=800.
        aw[19]=-0.8
        bw[19]=0.
        cw[19]=0.
        
        fw[20]=1000.
        aw[20]=0.
        bw[20]=0.
        cw[20]=0.
        
        fw[21]=1250.
        aw[21]=0.6
        bw[21]=0.
        cw[21]=0.

        fw[22]=1600.
        aw[22]=1.0
        bw[22]=0.
        cw[22]=-0.1

        fw[23]=2000.
        aw[23]=1.2
        bw[23]=-0.1
        cw[23]=-0.2

        fw[24]=2500.
        aw[24]=1.3
        bw[24]=-0.2
        cw[24]=-0.3

        fw[25]=3150.
        aw[25]=1.2
        bw[25]=-0.4
        cw[25]=-0.5

        fw[26]=4000.
        aw[26]=1.0
        bw[26]=-0.7
        cw[26]=-0.8

        fw[27]=5000.
        aw[27]=0.5
        bw[27]=-1.2
        cw[27]=-1.3

        fw[28]=6300.
        aw[28]=-0.1
        bw[28]=-1.9
        cw[28]=-2.0

        fw[29]=8000.
        aw[29]=-1.1
        bw[29]=-2.9
        cw[29]=-3.0

        fw[30]=10000.
        aw[30]=-2.5
        bw[30]=-4.3
        cw[30]=-4.4
        
        fw[31]=12500.
        aw[31]=-4.3
        bw[31]=-6.1
        cw[31]=-6.2

        fw[32]=16000.
        aw[32]=-6.6
        bw[32]=-8.4
        cw[32]=-4.4

        fw[33]=20000.
        aw[33]=-9.3
        bw[33]=-11.1
        cw[33]=-11
    
        return fw,aw,bw,cw            
  
###############################################################################
  
    @classmethod    
    def convert_FFT_to_one_third(cls,freq,fl,fu,full):

        jmax=len(fu)

        band_rms=zeros(jmax,'f')

        rms=full/sqrt(2)

        imax=len(rms)
    
#    print (" jmax=%d  imax=%d " %(jmax,imax))
    
#     for i in range (0,imax):
#         print ("@@@ i=%d  rms=%8.4g" %(i,rms[i]))



        istart=1

        for j in range (0,jmax):
            for i in range (istart,imax):
                if( freq[i]>= fl[j] and freq[i] <= fu[j]):
#                 print (" i=%d j=%d fl=%8.4g  freq=%8.4g  fu=%8.4g  " %(i,j,fl[j],freq[i],fu[j]))
                    band_rms[j]+= (rms[i])**2
        
                if(freq[i]>fu[j]):
                    istart=i
                    break
        
            band_rms[j]=sqrt(band_rms[j])    

        return band_rms
    
###############################################################################

    @classmethod    
    def convert_one_third_octave_mag_to_dB(cls,band_rms,ref):    

        imax=len(band_rms)

        splevel=zeros(imax,'f')

        ms=0.

        for j in range(0,imax):
#         print (" %d  band_rms=%8.4g " %(j,band_rms[j]))
            if(band_rms[j]>1.0e-12):
                ms+=(band_rms[j])**2
                splevel[j]=20*log10(band_rms[j]/ref)

        ms=sqrt(ms)

        oaspl = 20*log10(ms/ref)

        return splevel,oaspl
    
###############################################################################

    @classmethod       
    def trim_acoustic_SPL(cls,fc,splevel,ref):    

        k=0

        ms=0 

        imax=len(splevel)
    
        pf=[]
        pspl=[]
    
#     print ("** imax=%d" %imax)

        for i in range (0,imax):
#         print (" %d  spl=%8.4g  fc=%8.4g " %(i,splevel[i],fc[i]))
            if(splevel[i]>0.0001 and fc[i]>9):
                pf.append(fc[i])
                pspl.append(splevel[i])

                bs=ref*10**(pspl[k]/20)
                ms+=bs**2

                k+=1

        ms=sqrt(ms)
        oaspl = 20*log10(ms/ref)

        return pf,pspl,oaspl

###############################################################################
 
    @classmethod      
    def FFT_time_freq_set(cls,mmm,NW,dt,df,tmi,io):

        sr=1/dt
        maxf=sr/2

        md2=int(mmm/2)
        freq=zeros(md2,'f')


    
        for i in range (1,md2):
            freq[i]=(i-1)*df
            if(freq[i]>maxf):
                freq.pop[i]
                break


        mk=len(freq)
        t1=tmi+(dt*mmm)

        if(io==1):
            time_a=zeros(NW,'f')
            time_a[0]=t1 
            for i in range (2,NW):
                time_a[i]=time_a[i-1]+dt*mmm
        else:
            NW=2*NW-1
            time_a=zeros(NW,'f')
            time_a[0]=t1     
            dt=dt/2
                    
            for i in range (2,NW):
                time_a[i]=time_a[i-1]+dt*mmm


        return mk,freq,time_a,dt,NW    

###############################################################################

    @classmethod 
    def FFT_core_seg(cls,NW,mmm,mk,freq,amp,io):

        store=zeros([NW,mk],'f')
        store_p=zeros([NW,mk],'f')
    
        max_a=zeros(NW,'f')
        max_f=zeros(NW,'f')
    
        sa=zeros(mmm,'f')

        minf=0

        jk=0
    
        for ij in range (0,NW):
        
            sa=[]

            max_a[ij]=0.
            max_f[ij]=0.
        
            if(io==1):   
                for k in range (0,mmm):
                    sa.append(amp[jk])
                    jk=jk+1
            
            else:
                for k in range (0,mmm):
                    sa.append(amp[jk])
                    jk=jk+1
            
                jk=jk-int(mmm/2)
        

            Y=[]
        
            Y= fft(sa,mmm)

            store[ij,0] = abs(Y[0])/mmm 
   
            j=0
        
            freq_p=[]
        
            for k in range (1,mk):
                store[ij,k] =2.*abs(Y[k])/mmm
            
                if(freq[k]>=minf):
                    store_p[ij,j]=store[ij,k]
                    freq_p.append(freq[k])
                
                    if(store_p[ij,j]>max_a[ij]):
                        max_a[ij]=store_p[ij,j]
                        max_f[ij]=freq_p[j]
                
                    j=j+1

        return store,store_p,freq_p,max_a,max_f
        
###############################################################################
              
def quit(root):
    root.destroy()
                       
###############################################################################