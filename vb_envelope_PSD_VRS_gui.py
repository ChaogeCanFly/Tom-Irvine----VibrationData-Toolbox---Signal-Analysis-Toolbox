########################################################################
# program: vb_envelope_PSD_VRS_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.6
# date: October 24, 2014
# description:  
#    
#  This script will calculate a vibration response spectrum for a 
#  PSD base input.
#              
########################################################################

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

    
from matplotlib.ticker import ScalarFormatter
    
from vb_utilities import read_two_columns_from_dialog,WriteData2  

from numpy import array,zeros,log,log10,pi,sqrt,floor,round,sort,unique

from numpy.random import random


from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt


###############################################################################

class vb_envelope_PSD_VRS:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_envelope_PSD_VRS_gui.py ver 1.6  by Tom Irvine") 
        
        self.f=[]
        self.a=[]
        self.slope=[]
        self.grms_in=0
        
        self.ff=[]
        self.rdvrs=[]
        self.avrs=[]
        self.tsvrs=[] 
        self.nsvrs=[]
          
        self.num_fn=0
        

###############################################################################
        
        crow=0
        
        self.hwtext3=tk.Label(top,text='This script generates a simplified, optimized PSD to envelope a PSD.')
        self.hwtext3.grid(row=crow, column=0,columnspan=5, pady=6,sticky=tk.W)   

        crow=crow+1        
        
        self.hwtext4=tk.Label(top,text='The script assumes an SDOF response.')
        self.hwtext4.grid(row=crow, column=0,columnspan=5, pady=0,sticky=tk.W)           
        
        crow=crow+1

        self.hwtext5=tk.Label(top,text='The input file must have two columns: Freq(Hz) & Accel(G**2/Hz)')
        self.hwtext5.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
        crow=crow+1    
        
        self.hwtext6=tk.Label(top,text='Select Envelope PSD Type')
        self.hwtext6.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)   
              
        
        crow=crow+1        
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=2,sticky=tk.N)
        
        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "Ramp-Plateau-Ramp")
        self.Lb1.insert(2, "Free Form")
        self.Lb1.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lb1.select_set(0)  
        
           
        crow=crow+1

        self.hwtext_Q=tk.Label(top,text='Enter Q')
        self.hwtext_Q.grid(row=crow, column=0, columnspan=1, padx=14, pady=10,sticky=tk.S)
        
  
        self.hwtext_trials=tk.Label(top,text='Enter Number of Trials')
        self.hwtext_trials.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S) 

        crow=crow+1        
 

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 12,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)    
        

        self.ntrialsr=tk.StringVar()  
        self.ntrialsr.set('500')  
        self.ntrials_entry=tk.Entry(top, width = 12,textvariable=self.ntrialsr)
        self.ntrials_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N) 

          
        crow=crow+1

        self.hwtext10=tk.Label(top,text='Minimum Freq (Hz)')
        self.hwtext10.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.S)    

        self.hwtext11=tk.Label(top,text='Maximum Freq (Hz)')
        self.hwtext11.grid(row=crow, column=1,columnspan=1, pady=10,sticky=tk.S)
 
          
        crow=crow+1

        self.fminr=tk.StringVar()  
        self.fminr.set('')  
        self.fmin_entry=tk.Entry(top, width = 12,textvariable=self.fminr)
        self.fmin_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)  
        
        self.fmaxr=tk.StringVar()  
        self.fmaxr.set('')  
        self.fmax_entry=tk.Entry(top, width = 12,textvariable=self.fmaxr)
        self.fmax_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N)          

######

        
        crow=crow+1    
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0, pady=20)         
        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,pady=20)  
        
        
        crow=crow+1
        
        self.hwtext21=tk.Label(top,text='Select Export Format')
        self.hwtext21.grid(row=crow, column=1,columnspan=1, pady=10,sticky=tk.S) 
        
        crow=crow+1   

        self.button_export = tk.Button(top, text="Export Data", command=self.export)
        self.button_export.config( height = 2, width = 15,state = 'disabled')
        self.button_export.grid(row=crow, column=0, pady=10,sticky=tk.N)   
        
        self.Lbe = tk.Listbox(top,height=2,exportselection=0)
        self.Lbe.insert(1, "PSD Envelope")
        self.Lbe.insert(2, "VRS Envelope")
        
        
        self.Lbe.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lbe.select_set(0)  
        
        
###############################################################################

    def read_data(self):            
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

        nm1=num-1

        self.inslope =zeros(nm1,'f')


        ra=0

        for i in range (0,int(nm1)):
#
            s=log(a[i+1]/a[i])/log(f[i+1]/f[i])
        
            self.inslope[i]=s
            
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
 
        print (" Acceleration ")
        print ("   Overall = %10.3g GRMS" % rms)
        print ("           = %10.3g 3-sigma" % three_rms)
        
        self.grms_in=rms
        self.f=f
        self.a=a
        
        self.button_calculate.config(state = 'normal')
        
        plt.ion()
        plt.clf()
        plt.close(1)
        plt.figure(1)     
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
                                
###############################################################################
                
    def export(self):
        
        root=self.master    
        ne= int(self.Lbe.curselection()[0]) 

        output_file_path = asksaveasfilename(parent=root,title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n') 

        if(ne==0):
            num=len(self.xf)
            WriteData2(num,self.xf,self.xapsd,output_file)  
            
        if(ne==1):
            num=len(self.f_ref)
            WriteData2(num,self.f_ref,self.xvrs,output_file)  
            
            
                
    def calculation(self):
        
        plt.close(2)
        plt.close(3)
        plt.close(4)        
        
        self.Q=float(self.Qr.get())
        self.dam=1./(2.*self.Q)        
        
        ntrials=float(self.ntrialsr.get())

        fminp=float(self.fminr.get())
        fmaxp=float(self.fmaxr.get())
        
        self.f1=fminp
        self.f2=fmaxp

        self.net=1+int(self.Lb1.curselection()[0]) 

###############################################################################
  
        MAX=20000
        MAX2=100000
 
# nbreak   number of breakpoints
# ntrials  number of trails
# ntrials2
# nref    number of reference coordinates
#
        self.record = 1.0e+90
        self.grmslow=1.0e+50
        self.vrmslow=1.0e+50
        self.drmslow=1.0e+50
#
# f_ref[MAX]    reference natural frequency
# a_ref[MAX]    reference vrs(GRMS)
#
# fin[MAX]      input frequency
# psdin[MAX]    input PSD
# inslope[MAX]  input slope
#
# interp_psdin[MAX] interpolated input PSD
#
# f_sam[MAX]    frequency of sample breakpoint
# apsd_sam[MAX] acceleration PSD amplitude of sample breakpoint
# slope[MAX]
#
# f_samfine[MAX]    frequency of sample breakpoint, interpolated
# apsd_samfine[MAX] acceleration PSD of sample breakpoint, interpolated  
#
##        
 
        self.goal=3  # Minimize: acceleration, velocty, displacement  
  
  
        if(ntrials>MAX2):
            ntrials=MAX2
            
        self.nbreak=4  # number of breakpoints
 
  
        self.slope=zeros(self.nbreak,'f')
        self.xf=zeros(self.nbreak,'f')
        self.xapsd=zeros(self.nbreak,'f')

   
##        ic=1  # constrain slope   

        self.slopec = 12.  # 12 db/octave         
  
        self.slopec=(self.slopec/10.)/log10(2.)

        if(self.net==1):     # ramp-plateau-ramp
            self.initial=1   # constrain initial slope to be positive
            self.final=1     # constrain final slope to be negative
        else:           # free-form
            self.initial=2
            self.final=2    

#
        ocn=1./48.
#
#
        self.octave=-1.+(2.**ocn)  
#  
  
#        ffmin=self.f1
        ffmax=self.f2

        if(ffmax<=1000):
            ffmax=1000
 
        if(ffmax>1000 and ffmax<=2000):
            ffmax=2000
  

        self.fin=self.f
        self.psdin=self.a  
  

        if( min(self.psdin) <= 0. ):
            tkMessageBox.showinfo("Warning"," Input error:  each PSD amplitude must be > 0.",parent=self.button_calculate) 
            return                        
            

        if( min(self.fin) < 0. ):
            tkMessageBox.showinfo("Warning"," Input error:  each frequency must be > 0.",parent=self.button_calculate)              
            return
  
        if(self.fin[0]<1.0e-04):
            self.fin[0]=1.0e-04

# Interpolate Input PSD
#
        if( self.f1 < self.fin[0] ): 
                self.f1 = self.fin[0] 
#
        self.f_ref=[]
#
        self.f_ref.append(self.f1)
#
        for i in range(1,MAX):
#   
            self.f_ref.append(self.f_ref[i-1]*(2.**ocn))
#
            if( self.f_ref[i] >= self.f2 ):
                self.f_ref[i]=self.f2
                break
        
        
        print(' length f_ref = %d ' %len(self.f_ref))        
        
#
        self.interp_psdin=[]
        
        self.interp_psdin.append(self.psdin[0])        
        
       
        for i in range(1,len(self.f_ref)):
            
            for j in range(0,(len(self.fin)-1)):
            
                if( self.f_ref[i] >= self.fin[j] and self.f_ref[i] <= self.fin[j+1] ):   
                    
                    self.interp_psdin.append( self.psdin[j]*((self.f_ref[i]/self.fin[j])**self.inslope[j]) )
    
        
        self.nref=len(self.f_ref)
        
        if( self.nref > len(self.interp_psdin) ):
            self.nref = len(self.interp_psdin)
            
#        print('**  nref=%d ** ' %self.nref)    


#        interpolated_PSD=[self.f_ref, self.interp_psdin]
# [a_ref]=env_make_input_vrs(interp_psdin,nref,f_ref,self.octave,dam);


        self.env_make_input_vrs(self)

#    input_vrs=[f_ref a_ref];


###############################################################################

        for self.ik in range(0,int(ntrials)):      
#        
            if(random()>0.5 or self.ik<20):
#      
            # Generate the sample psd
            
                if(self.net==2):  # free
                    self.env_generate_sample_psd(self)
                
                else: 
                    self.env_generate_sample_psd_plateau(self)
                    
                print('\n Phase 1, Trial %d, PSD Coordinates \n' %self.ik)    
                
            else:
#
                if(self.net==2): # free
                    self.env_generate_sample_psd2(self)
                else:
                    self.env_generate_sample_psd2_plateau(self)  
                    
                print('\n Phase 2, Trial %d, PSD Coordinates \n' %self.ik)                     

            self.common_coordinates_finish(self)
            
    
            self.env_interp_sam(self)            

            self.vrs_samfine=zeros(self.nref,'f')
            
            self.env_vrs_sample(self)
            
            self.env_compare_rms(self)            
            
            self.scale=(self.scale**2.)
            self.apsd_sam=self.apsd_sam*self.scale
            
            self.env_grms_sam(self)
            self.env_vrms_sam(self)
            self.env_drms_sam(self)             

            self.env_checklow(self)  

            if(self.iflag==1):
#           
               if(self.drms<self.drmslow):
                   self.drmslow=self.drms
           
               if(self.vrms<self.vrmslow):
                   self.vrmslow=self.vrms
           
               if(self.grms<self.grmslow):
                   self.grmslow=self.grms          
#           
               drmsp=self.drms
               vrmsp=self.vrms
               grmsp=self.grms
#
#               ikbest=self.ik          
#               nnn=self.ntrials
#
               self.xf=self.f_sam
               self.xapsd=self.apsd_sam             
#
               self.xslope=self.slope
#       
               
            print('   Trial: drms=%10.4g  vrms=%10.4g  grms=%10.4g ' %(self.drms,self.vrms,self.grms)) 
            print('  Record: drms=%10.4g  vrms=%10.4g  grms=%10.4g \n'%(drmsp,vrmsp,grmsp))                


        self.env_interp_best(self)
        self.env_vrs_best(self)

        print('\n Optimum Case \n')
        
        print('  Freq (Hz)   PSD(G^2/Hz)')
        
        for i in range(0,self.nbreak):
            print(' %8.2f \t %8.4g ' %(self.xf[i],self.xapsd[i])) 
            
        
    
        print('\n drms=%10.4g  vrms=%10.4g  grms=%10.4g ' %(drmsp,vrmsp,grmsp))
        
        self.grmsp=grmsp
    
###############################################################################  
        
        self.button_export.config(state = 'normal')        
        
        
        f1=self.f1
        f2=self.f2


        plt.figure(2)     

        plt.plot(self.f,self.a,label='Input '+str("%6.3g" %self.grms_in)+' GRMS')
        plt.plot(self.xf,self.xapsd,label='Envelope '+str("%6.3g" %self.grmsp)+' GRMS')
        
        title_string='Power Spectral Density   '+str("%6.3g" %self.grms_in)+' GRMS Overall '
        plt.title(title_string)
        plt.ylabel(' Accel (G^2/Hz)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.legend(loc="upper right")  
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        
        
        if(abs(f1-10)<0.5 and abs(f2-2000)<4):
            
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(f1,f2))    
              
            extraticks=[10,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks) 

        
        if(abs(f1-20)<0.5 and abs(f2-2000)<4):
            
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(f1,f2))    
              
            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                
        
        
        plt.xlim([f1,f2])                
        
        plt.show()



        plt.figure(3)     
        plt.plot(self.f_ref,self.a_ref,label='Input')
        plt.plot(self.f_ref,self.xvrs,label='Envelope')
        title_string='Vibration Response Spectra   Q='+str("%g" %self.Q)
        plt.title(title_string)
        plt.ylabel(' Accel (GRMS)')
        plt.xlabel(' Natural Frequency (Hz) ')
        plt.grid(which='both')
        plt.legend(loc="upper right")  
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        

        if(abs(f1-10)<0.5 and abs(f2-2000)<4):
            
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(f1,f2))    
              
            extraticks=[10,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks) 

        
        if(abs(f1-20)<0.5 and abs(f2-2000)<4):
            
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(f1,f2))    
              
            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                
        
        
        plt.xlim([f1,f2])               
        
        
        plt.show()


        print ("\n Calculation complete.  View Plots.")

###############################################################################

    @classmethod
    def env_interp_best(cls,self):
        
        self.xffine=zeros(self.nref,'f')
        self.xapsdfine=zeros(self.nref,'f')
        
        self.xffine[0]=self.xf[0]
        self.xapsdfine[0]=self.xapsd[0]


        for i in range(0,(self.nbreak-1)):
            
            self.xslope[i]=log(self.xapsd[i+1]/self.xapsd[i])/log(self.xf[i+1]/self.xf[i])
    

        for i in range(0,self.nref):
    
            self.xffine[i]=self.f_ref[i]
 
            for j in range(0,(self.nbreak-1)):
        
                if( ( self.xffine[i] >= self.xf[j] ) and  ( self.xffine[i] <= self.xf[j+1] )  ):
                    
                    self.xapsdfine[i]=self.xapsd[j]*( ( self.xffine[i] / self.xf[j] )**self.xslope[j] )
                    break
                    
        
###############################################################################
        
    @classmethod
    def env_vrs_best(cls,self):

        self.xvrs=zeros(self.nref,'f')
        
        for i in range(0,self.nref):
#    
            sum=0.
# 
            for j in range(0,self.nref):
#        
              # f_ref[i] is the natural frequency
              # f_ref[j] is the forcing frequency
#
                rho=self.f_ref[j]/self.f_ref[i]              
                tdr=2.*self.dam*rho
#
                tden=((1.-(rho**2))**2)+ (tdr**2)
                tnum=1.+(tdr**2)
#
                trans=tnum/tden
#
                dfi=self.f_ref[j]*self.octave
# 
                sum=sum+trans*self.xapsdfine[j]*dfi
#
            sum=sqrt(sum)
            self.xvrs[i]=sum

###############################################################################

    @classmethod
    def env_checklow(cls,self):

        self.iflag=0

        if(self.goal==1):
            if( (self.grms < self.grmslow)):       
                self.iflag=1
       
        if(self.goal==2): 
            if( (self.vrms < self.vrmslow) and (self.grms < self.grmslow)):
                self.iflag=1
       
        if(self.goal==3):
           if( (self.drms*self.vrms*self.grms) < self.record ):
               self.record=(self.drms*self.vrms*self.grms)
               self.iflag=1

        if(self.goal==4):
           if( (self.drms < self.drmslow) and (self.grms < self.grmslow)):
               self.iflag=1
       
        if(self.goal==5): 
           if( (self.drms < self.drmslow)):
             self.iflag=1

###############################################################################

    @classmethod
    def env_grms_sam(cls,self):

        ra=0.
        self.grms=0.
        s=zeros((self.nbreak-1),'f')
    
        for i in range(0,(self.nbreak-1)):

            s[i]=log( self.apsd_sam[i+1]/self.apsd_sam[i] )/log( self.f_sam[i+1]/self.f_sam[i] )

            if(s[i] < -1.0001 or  s[i] > -0.9999 ):
                 ra=ra+ ( self.apsd_sam[i+1] * self.f_sam[i+1]- self.apsd_sam[i]*self.f_sam[i])/( s[i]+1.)
            else:
                 ra=ra+ self.apsd_sam[i]*self.f_sam[i]*log( self.f_sam[i+1]/self.f_sam[i])
              
        self.grms=sqrt(ra)
          
###############################################################################

    @classmethod
    def env_vrms_sam(cls,self):
        
        tpi=2*pi

        ra=0.
          
        vpsd_sam=zeros(self.nbreak,'f')
           
        conv=(386.**2.)/(tpi**2.)

        self.vrms=0.

        s=zeros((self.nbreak-1),'f')
      
        for i in range(0,self.nbreak):
            vpsd_sam[i]=self.apsd_sam[i]*conv/(self.f_sam[i]**2.)
          

        for i in range(0,(self.nbreak-1)):

            s[i]=log( vpsd_sam[i+1]/vpsd_sam[i] )/log( self.f_sam[i+1]/self.f_sam[i] )

            if(s[i] < -1.0001 or  s[i] > -0.9999 ):
                 ra=ra+ ( vpsd_sam[i+1] * self.f_sam[i+1]- vpsd_sam[i]*self.f_sam[i])/( s[i]+1.)
            else:
                 ra=ra+ vpsd_sam[i]*self.f_sam[i]*log( self.f_sam[i+1]/self.f_sam[i])
              
          
        self.vrms=sqrt(ra)

 ###############################################################################

    @classmethod
    def env_drms_sam(cls,self):       

        tpi=2*pi
           
        ra=0.

        dpsd_sam=zeros(self.nbreak,'f')

        conv=(386.**2.)/(tpi**4.)

        self.drms=0.
        s=zeros((self.nbreak-1),'f')
   
        for i in range(0,self.nbreak):
            dpsd_sam[i]=self.apsd_sam[i]*conv/(self.f_sam[i]**4.)
          

        for i in range(0,(self.nbreak-1)):
          
            s[i]=log( dpsd_sam[i+1]/dpsd_sam[i] )/log( self.f_sam[i+1]/self.f_sam[i] )
 
            if(s[i] < -1.0001 or  s[i] > -0.9999 ):
              
                ra=ra+ ( dpsd_sam[i+1] * self.f_sam[i+1]- dpsd_sam[i]*self.f_sam[i])/( s[i]+1.)
 
            else:
                ra=ra+ dpsd_sam[i]*self.f_sam[i]*log( self.f_sam[i+1]/self.f_sam[i])
 
            
        self.drms=sqrt(ra)

###############################################################################

    @classmethod
    def env_compare_rms(cls,self):
        
        self.scale=0.

        for i in range(0,self.nref):
            
            if( self.vrs_samfine[i] < 1.0e-30):
                print('\n Error:  vrs_samfine[%d])=%10.4g ' %(i,self.vrs_samfine[i]))
                return
            
            if(  (self.a_ref[i]/self.vrs_samfine[i]) > self.scale ):
                self.scale=(self.a_ref[i]/self.vrs_samfine[i])
                    
################################################################################

    @classmethod
    def env_vrs_sample(cls,self):

       for i in range(0,self.nref):
  
          sum=0.

          for j in range(0,self.nref):
       
              # f_ref[i] is the natural frequency
              # f_ref[j] is the forcing frequency

              rho=self.f_ref[j]/self.f_ref[i]              
              tdr=2.*self.dam*rho

              tden=((1.-(rho**2))**2)+ (tdr**2)
              tnum=1.+(tdr**2)

              trans=tnum/tden

              dfi=self.f_ref[j]*self.octave

              sum=sum+trans*self.apsd_samfine[j]*dfi

              if(dfi<1.0e-20):
                   print(' Error: dfi=%12.4g \n' %dfi)
                   return
  
              if(trans<1.0e-30):
                   print(' Error: trans=%12.4g \n' %trans)
                   return

              if(self.apsd_samfine[j]<1.0e-30):
                   print(' Error: self.apsd_samfine[%d]=%12.4g \n' %(j,self.apsd_samfine[j]))           
                   return           
           
          if(sum<1.0e-30):
               print(' Error: sum=%12.4g \n' %sum)
               return           
           
          qsum=sqrt(sum)
       
          self.vrs_samfine[i]=qsum
    
###############################################################################

    @classmethod
    def env_interp_sam(cls,self):
        
        self.apsd_samfine=zeros(self.nref,'f')
        self.f_samfine=self.f_ref

        self.slope=zeros(self.nbreak-1,'f')

        for i in range (0,(self.nbreak-1)):
            self.slope[i]=log(self.apsd_sam[i+1]/self.apsd_sam[i])/log(self.f_sam[i+1]/self.f_sam[i])
    

        for i in range(0,self.nref):

            for j in range(0,(self.nbreak-1)):
       
                if( ( self.f_samfine[i] >= self.f_sam[j] ) and  ( self.f_samfine[i] <= self.f_sam[j+1] )  ):      
                    self.apsd_samfine[i]=self.apsd_sam[j]*( ( self.f_samfine[i] / self.f_sam[j] )**self.slope[j] )
                    break 
                
###############################################################################        

    @classmethod
    def common_coordinates_finish(cls,self):
#
    # absolute slopes are limited to self.slopec
#
        for i in range(0,(self.nbreak-1)):
            
            fr=self.f_sam[i+1]/self.f_sam[i]
            sss=0.
            sss=log(self.apsd_sam[i+1]/self.apsd_sam[i])/log(fr)
            
            
            if(self.net==2):  
            
                if(sss > self.slopec):
                    self.apsd_sam[i+1]=self.apsd_sam[i]*(fr**self.slopec)
        
                if(sss < -self.slopec):
                    self.apsd_sam[i+1]=self.apsd_sam[i]*(fr**(-self.slopec))
                

        self.f_sam[0]=self.f1
        self.f_sam[self.nbreak-1]=self.f2
#
        self.f_sam=sort(self.f_sam)
        
        for i in range(0,self.nbreak):
            print(' %8.2f \t %8.4g ' %(self.f_sam[i],self.apsd_sam[i]))    


###############################################################################
    
    @classmethod
    def check_frequencies(cls,self):

        self.f_sam=sort(self.f_sam)         
    
        ialarm = 0
#        fnum = (self.f_ref(nref)-self.f_ref[0])/200.
#
        for i in range(0,self.nbreak-1):
#
            if (  abs( log(self.f_sam[i+1]/self.f_sam[i])/log(2.) ) < 1 ):
                ialarm = 1
                break
#    
        if(ialarm == 1 ):
#
            df=(self.f_ref[self.nref-1]-self.f_ref[0])/(self.nref-1)
#    
            for i in range(1,self.nbreak):
                self.f_sam[i]=self.f_sam[i-1]+df
        
        self.f_sam[self.nbreak-1]=self.f_ref[self.nref-1]
        self.f_sam=sort(self.f_sam)

###############################################################################

    @classmethod
    def amin_check(cls,self):
        
        amin=1.0e-12
#
        for i in range(0,self.nbreak):
#    
            if(self.apsd_sam[i] < amin):
                self.apsd_sam[i]=amin
            
            if(self.apsd_sam[i] > (1./amin)):
              self.apsd_sam[i]=(1./amin)    


###############################################################################

    @classmethod
    def env_generate_sample_psd2_plateau(cls,self):
#
        self.f_sam=zeros(self.nbreak,'f')     # leave here
        self.apsd_sam=zeros(self.nbreak,'f')
        
        self.f_sam[0]=self.f1
        self.f_sam[self.nbreak-1]=self.f2      
#
        if( random()>0.2):
            bbb=(random())**3.
        else:
            bbb=0.1*random()
    
#
        aaa=1.-bbb/2.
#  
        for i in range(0,self.nbreak):
            self.f_sam[i]=self.xf[i]*(aaa+bbb*random())    
#   
#######
#
# check frequencies for adequate spacing
#         
        self.check_frequencies(self)
#
######
#
       # generate some random number for amplitude
#
        bbb=(random())**3.
#
        aaa=1.-bbb/2.
#
        for i in range(0,self.nbreak):
#       
            self.apsd_sam[i]=self.xapsd[i]*(aaa+bbb*random())
#
            if(self.apsd_sam[i]>2000.):
#           
                print(' Error: %d  %8.4g  %8.4g \n',i,self.apsd_sam[i],self.xapsd[i])
       
#     
        self.apsd_sam[2]=self.apsd_sam[1]        

###############################################################################

    @classmethod
    def env_generate_sample_psd2(cls,self):
#
        self.f_sam=zeros(self.nbreak,'f')     # leave here
        self.apsd_sam=zeros(self.nbreak,'f')
        
        self.f_sam[0]=self.f1
        self.f_sam[self.nbreak-1]=self.f2        
    
#   
        if( random()>0.2):
            bbb=(random())**3.
        else:
            bbb=0.1*random()
    
        aaa=1.-bbb/2.
#  
        for i in range(0,self.nbreak):
            self.f_sam[i]=self.xf[i]*(aaa+bbb*random())    
#
#########
#
# check frequencies for adequate spacing
#         
        self.check_frequencies(self)    
#
#########
#
       # generate some randomom number for amplitude
#
        bbb=(random())**3.
#
        aaa=1.-bbb/2.
#
        for i in range(0,self.nbreak):
#       
            self.apsd_sam[i]=self.xapsd[i]*(aaa+bbb*random())
#
            if(self.apsd_sam[i]>2000.):
#           
                print(' Error: %d  %8.4g  %8.4g \n',i,self.apsd_sam[i],self.xapsd[i])
        
        self.amin_check(self) 

#
###############################################################################

    @classmethod
    def env_generate_sample_psd_plateau(cls,self):

        self.f_sam=zeros(self.nbreak,'f')     # leave here
        self.apsd_sam=zeros(self.nbreak,'f')
        
        self.f_sam[0]=self.f1
        self.f_sam[self.nbreak-1]=self.f2    

#
# generate some random numbers for frequency
#
        L=len(self.f_ref)
    
        for ijk in range(0,10000):
       
            for i in range(1,self.nbreak):
#         
                index = int(round( self.nref*random()))

                if(index >=L ):
                    index=L-1
            
                if(index < 1):
                    index=1                    
#
#                print(' i=%d  len(f_sam)=%d  index=%d  nbreak=%d L=%d' %(i,len(self.f_sam),index,self.nbreak,L))     
                self.f_sam[i]=self.f_ref[index]
    
#    
            self.f_sam[self.nbreak-1]=self.f2   
#          
# sort the frequencies
#
            self.f_sam=sort(self.f_sam)
#
            self.f_sam=round(self.f_sam)
###            self.f_sam=unique(self.f_sam)   # causes error
#
            nnn=len(self.f_sam)
#    
            if(nnn==self.nbreak):         
#
# check frequencies for adequate spacing
#         
               self.check_frequencies(self)            
         
#
# generate some random numbers for amplitude
#
               for i in range(0,self.nbreak):
                   self.apsd_sam[i]=random()
       
#      
               self.apsd_sam[2]=self.apsd_sam[1]                
               
               self.amin_check(self)      
#

            
#
###############################################################################

    @classmethod    
    def env_generate_sample_psd(cls,self):

        self.f_sam=zeros(self.nbreak,'f')     # leave here
        self.apsd_sam=zeros(self.nbreak,'f')
        
        self.f_sam[0]=self.f1
        self.f_sam[self.nbreak-1]=self.f2    

        
# generate some random numbers for frequency
#
        for ijk in range(0,10000):
       
            for i in range(1,self.nbreak):
#         
                index = int(round( self.nref*random()))

                if(index >= self.nref):
                    index=self.nref-1
            
                if(index < 1):
                    index=1                    
#
                self.f_sam[i]=self.f_ref[index]
    
#    
            self.f_sam[self.nbreak-1]=self.f2   
#          
# sort the frequencies
#
            self.f_sam=sort(self.f_sam)
#
            self.f_sam=round(self.f_sam)
#             self.f_sam=unique(self.f_sam)  # cause error
#
            nnn=len(self.f_sam)
#    
            if(nnn==self.nbreak):         
#
# check frequencies for adequate spacing
#         
               self.check_frequencies(self)            
         
#
# generate some random numbers for amplitude
#
               for i in range(0,self.nbreak):
                   self.apsd_sam[i]=random()
       
#      
               self.amin_check(self)      
#

    
###############################################################################

    @classmethod    
    def env_make_input_vrs(cls,self):
        
        self.a_ref=[]

#
        for i in range(0,self.nref):
#   
            sum=0.
#
            for j in range (0,self.nref):
#       
              # f_ref[i] is the natural frequency
              # f_ref[j] is the forcing frequency
#
                rho=self.f_ref[j]/self.f_ref[i]
#             
                tdr=2.*self.dam*rho
#
                tden=((1.-(rho**2))**2)+(tdr**2)
                tnum=1.+(tdr**2)
#
                trans=tnum/tden
#
                dfi=self.f_ref[j]*self.octave
#
                sum=sum+trans*self.interp_psdin[j]*dfi
#     
        
            sum=sqrt(sum)
            self.a_ref.append(sum)


###############################################################################
                      
def quit(root):
    root.destroy()
                       
###############################################################################