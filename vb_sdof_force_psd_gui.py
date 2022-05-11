########################################################################
# 
# program: vb_sdof_force_psd_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.1
# date: December 11, 2014
# description:  
#    
#  This script calculates the response of an SDOF system to a PSD force input.
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

    

from vb_utilities import read_two_columns_from_dialog

from numpy import array,zeros,log,log10,pi,sqrt,floor,ceil

from vb_utilities import WriteData2,WriteData3

import matplotlib.pyplot as plt


###############################################################################

class vb_sdof_force_psd:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.26))
        h = int(2.*(h*0.28))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        
        self.master.title("vb_sdof_force_psd_gui.py ver 1.1  by Tom Irvine") 
        
        self.f=[]
        self.a=[]
        self.slope=[]
        self.grms_in=0

###############################################################################
        
        crow=0
        
        self.hwtext1=tk.Label(top,text='This script calculates the response of an SDOF system to an applied force PSD.')
        self.hwtext1.grid(row=crow, column=0,columnspan=4, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns: Freq(Hz) & Force(unit^2/Hz)')
        self.hwtext2.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
        crow=crow+1    
        
        self.hwtext3=tk.Label(top,text='Select Output Units')
        self.hwtext3.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)                 
        
        crow=crow+1        
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 20 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=2,sticky=tk.N)
        
        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "lbf, G, in/sec, in")
        self.Lb1.insert(2, "N, G, m/sec, mm")
        self.Lb1.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lb1.select_set(0)  
        self.Lb1.bind('<<ListboxSelect>>',self.unit_option)          
           
        crow=crow+1

        self.hwtext_fn=tk.Label(top,text='Enter Natural Frequency (Hz)')
        self.hwtext_fn.grid(row=crow, column=0, columnspan=1, padx=14, pady=10,sticky=tk.S)

        self.hwtext_Q=tk.Label(top,text='Enter Q')
        self.hwtext_Q.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S)
        
        self.hwtext_fn=tk.Label(top,text='Enter Duration (sec)')
        self.hwtext_fn.grid(row=crow, column=2, columnspan=1, padx=14, pady=10,sticky=tk.S)   
                
        self.mass_text=tk.StringVar()  
        self.mass_text.set('Enter Mass (lbm)')         
        self.hwtext_mass=tk.Label(top,textvariable=self.mass_text)        
        self.hwtext_mass.grid(row=crow, column=3,columnspan=1,padx=15)        
        
        
        crow=crow+1        

        self.fnr=tk.StringVar()  
        self.fnr.set('')  
        self.fn_entry=tk.Entry(top, width = 12,textvariable=self.fnr)
        self.fn_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)  

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 12,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N)    
        
        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 12,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=2,padx=14, pady=1,sticky=tk.N)          

        self.massr=tk.StringVar()  
        self.massr.set('')  
        self.mass_entry=tk.Entry(top, width = 12,textvariable=self.massr)
        self.mass_entry.grid(row=crow, column=3,padx=14, pady=1,sticky=tk.N)   
        
        
        crow=crow+1    
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0, pady=20)   
        

        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 12 )
        self.button_quit.grid(row=crow, column=1,pady=20)    

        self.hwtext_e=tk.Label(top,text='Select Response')
        self.hwtext_e.grid(row=crow, column=2, columnspan=1, padx=14, pady=10,sticky=tk.S)

        crow=crow+1   

        self.Lb2 = tk.Listbox(top,height=7,exportselection=0)
        self.Lb2.insert(1, "Acceleration PSD")
        self.Lb2.insert(2, "Velocity PSD")
        self.Lb2.insert(3, "Displacement PSD")
        self.Lb2.insert(4, "Transmitted Force PSD")        
        self.Lb2.insert(5, "Accelerance FRF")
        self.Lb2.insert(6, "Mobility FRF")
        self.Lb2.insert(7, "Receptance FRF")        
        
    
        self.Lb2.grid(row=crow, column=2, pady=2,sticky=tk.N)
        self.Lb2.select_set(0)  
        self.Lb2.bind('<<ListboxSelect>>',self.unit_option)  

        self.button_export = tk.Button(top, text="Export Response", command=self.export)
        self.button_export.config( height = 2, width = 18,state = 'disabled')
        self.button_export.grid(row=crow, column=3, pady=20,sticky=tk.N) 
        
###############################################################################

    def export(self): 
        
        n= int(self.Lb2.curselection()[0])         
        
        num=len(self.fi)
      
      
        if(n<=3):        
        
            output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the response PSD filename")           
            output_file = output_file_path.rstrip('\n')    

            
            if(n==0):
                WriteData2(num,self.fi,self.acceleration_psd,output_file)
            if(n==1):
                WriteData2(num,self.fi,self.velocity_psd,output_file)
            if(n==2):
                WriteData2(num,self.fi,self.displacement_psd,output_file)
            if(n==3):
                WriteData2(num,self.fi,self.tf_psd,output_file)

        else:
            
            output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the frf filename")           
            output_file = output_file_path.rstrip('\n')             
            
            if(n==4):
                WriteData3(num,self.fi,self.accelerance.real,self.accelerance.imag,output_file)
            if(n==5):
                WriteData3(num,self.fi,self.mobility.real,self.mobility.imag,output_file)
            if(n==6):
                WriteData3(num,self.fi,self.receptance.real,self.receptance.imag,output_file)
        

    def read_data(self):            
        """
        f = frequency column
        a = PSD column
        num = number of coordinates
        slope = slope between coordinate pairs    
        """

        print (" ")
        
        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):
            out1='The input file must have two columns: freq(Hz) & force(lbf^2/Hz)'
        else:
            out1='The input file must have two columns: freq(Hz) & force(N^2/Hz)'
        
        f,a,num =read_two_columns_from_dialog(out1,self.master)

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
        
        self.rms=rms
    
        print (" ")
        print (" *** Applied Force PSD *** ")
        print (" ")
 
        if(n1==0): 
 
            print ("   Overall = %10.3g lbf RMS" % rms)
            print ("           = %10.3g 3-sigma" % three_rms)
        
        else:

            print ("   Overall = %10.3g N RMS" % rms)
            print ("           = %10.3g 3-sigma" % three_rms)        
        
        self.force_rms_in=rms
        self.f=f
        self.a=a
        
        self.slope=slope
        
        self.button_calculate.config(state = 'normal') 
        
        plt.ion()
        plt.clf()   
        plt.close(1) 
        plt.figure(1)     
        plt.plot(f,a)
        
        y1=10**int(floor(log10(min(a))))
        y2=10**int(ceil(log10(max(a))))
        
        if(y2==y1):
            y2=10*y1 
            y1=y1/10
        
        plt.ylim([y1,y2])           
        
        nu=int(self.Lb1.curselection()[0])        
        
        if(nu==0):        
            title_string='Power Spectral Density   '+str("%6.3g" %rms)+' lbf RMS Overall '
            plt.ylabel(' Force (lbf^2/Hz)')
        else:
            title_string='Power Spectral Density   '+str("%6.3g" %rms)+' N RMS Overall '
            plt.ylabel(' Force (N^2/Hz)')
            
        
        plt.title(title_string)        
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
                                        
                
###############################################################################
                
    def calculation(self):
        
        tpi=2*pi
        
        n= int(self.Lb1.curselection()[0])
        
        Q=float(self.Qr.get())
        damp=1./(2.*Q)        

        fn=float(self.fnr.get())

        dur=float(self.durr.get())
        
        mass=float(self.massr.get())
        
        if(n==0):
            mass/=386
            
        omegan=tpi*fn
        omegan2=omegan**2              
            
        k=omegan2*mass    

###

        df= 0.1/40.


        if(self.f[0] >= 0.1):
            df = self.f[0]/40. 

        nif=int(floor((max(self.f)-min(self.f))/df))

        self.fi=zeros(nif,'f')
        self.ai=zeros(nif,'f')

        self.fi[0]=self.f[0]
        self.ai[0]=self.a[0]

        fmax=max(self.f)

        m=len(self.f)

        inif=int(nif)

        for i in range (0,inif): 	
            self.fi[i]=self.f[0]+df*i

            if( self.fi[i] > fmax ):
                break
    
            iflag=0
    
            for j in range (0,int(m-1)):
		
                if( ( self.fi[i] >= self.f[j] ) and ( self.fi[i] <= self.f[j+1] ) and iflag==0  ):
					
                    self.ai[i]=self.a[j]*( ( self.fi[i] / self.f[j] )**self.slope[j] )
                    iflag=1
#            print (fi[i],ai[i])

							
# print  ("\n interp df = %10.4g Hz  nif=%d  max(fi)=%8.4g  m=%d\n" %(df,nif,max(fi),m))

################################################################################

        
##   Acceleration
        
        self.tf_psd=zeros(inif,'f')
        self.acceleration_psd=zeros(inif,'f')
        self.velocity_psd=zeros(inif,'f')
        self.displacement_psd=zeros(inif,'f')      
        
        self.accelerance=zeros(inif,'complex','f')
        self.mobility=zeros(inif,'complex','f')
        self.receptance=zeros(inif,'complex','f')      
        
        omega=zeros(inif,'f')
 
        num=zeros(inif,'f')            
        den=zeros(inif,'complex','f')            
        
        tdr=2.*damp*omegan

        for j in range (0,inif):
            omega[j]=tpi*self.fi[j]

            num[j]=omegan2/k
            den[j]=omegan2-omega[j]**2+(1j)*omega[j]*tdr 
            
        
        sum=0.

        for j in range (0,inif):

            t= num[j]/den[j]
            
            t=t*(-omega[j]**2)            
            
            self.accelerance[j]=t

            self.acceleration_psd[j]=abs(t**2)*self.ai[j]  

            sum+=self.acceleration_psd[j]   
	
        grms=sqrt(sum*df)


##   Velocity
	
        sum=0. 
 
        for j in range (0,inif):

            t= num[j]/den[j]
            
            t=t*(1j)*omega[j]
            
            self.mobility[j]=t
            
            self.velocity_psd[j]=abs(t**2)*self.ai[j]  

            sum+=self.velocity_psd[j]
   
        vrms=sqrt(sum*df) 
   

##   Displacement
	
        sum=0. 
 
        for j in range (0,inif):

            t= num[j]/den[j]
   
            self.receptance[j]=t   
   
            self.displacement_psd[j]=abs(t**2)*self.ai[j]  

            sum+=self.displacement_psd[j]   
   
        drms=sqrt(sum*df) 
   

##   Transmitted Force
	
        sum=0. 
        
 
        for j in range (0,inif):

            nu=omegan2+(1j)*omega[j]*tdr
            
            t= nu/den[j]
   
            self.tf_psd[j]=abs(t**2)*self.ai[j]  

            sum+=self.tf_psd[j]   
   
        tfrms=sqrt(sum*df) 
        
################################################################################        
   
        for j in range (0,inif):
            
            if(n==0):
                self.acceleration_psd[j]/386**2
            else:
                self.acceleration_psd[j]/9.81**2   
                self.velocity_psd[j]*100**2                 
                self.displacement_psd[j]*1000**2  
                
################################################################################
    
        print ("\n\n ** Output Overall Levels **")	
        
        if(fn>=min(self.f) and fn<=max(self.f)):
            c=sqrt(2*log(fn*dur))
            nnf=c + 0.5772/c                                                               
            print ("\n Maximum expected peak from Rayleigh distribution = %6.2g-sigma" %nnf)          
        
        
################################################################################
              
        
        if(n==0):
            print ("\n Displacement = %12.4g inches RMS" %drms)	
            
            print ("\n Velocity     = %12.4g inch/sec RMS" %vrms) 
                  
            grms/=386            
            
        else:
            drms*=1000
            vrms*=100
            
            print ("\n Displacement = %12.4g mm RMS " %drms)				

            print ("\n Velocity     = %12.4g cm/sec RMS" %vrms)
            
            grms/=9.81            
              
        
        print ("\n Acceleration = %12.4g GRMS  " %grms)
        print ("                  = %12.4g 3-sigma G         " %(3.*grms))

        if(fn>=min(self.f) and fn<=max(self.f)):
            print ("                  = %12.4g %6.2g-sigma G" %(nnf*grms,nnf))
		
  
        if(n==0):
            print ("\n Transmitted Force = %12.4g lbf RMS" %tfrms)	
      
        else:
            print ("\n Transmitted Force = %12.4g N RMS " %tfrms)				

 
  
################################################################################

        plt.close(2)
        plt.figure(2)     

        if(n==0):
            out1="Force (lbf^2/Hz)"        
            out_app="Applied %6.2g lbf rms" %self.rms
            out_trans="Transmitted %6.3g lbf rms" %tfrms            
        else:
            out1="Force (N^2/Hz)"
            out_app="Applied %6.2g N rms" %self.rms
            out_trans="Transmitted %6.3g N rms" %tfrms    

        plt.plot(self.fi,self.ai,label=out_app)
        plt.plot(self.fi,self.tf_psd,label=out_trans)
        
        title_string='Force Power Spectral Density   '
        plt.title(title_string)
        
         
        plt.legend(loc="upper right")

        y1=10**int(floor(log10(min(self.tf_psd))))
        y2=10**int(ceil(log10(max(self.tf_psd))))
        
        if(y1<y2*1.0e-05):
            y1=y2*1.0e-05
            
        y2=y2*10    
        
        plt.ylim([y1,y2])               
            
        plt.ylabel(out1)
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
        
##########
        
        plt.close(3)
        plt.figure(3)  
        
        plt.plot(self.fi,self.acceleration_psd)          

        title_string='Acceleration Power Spectral Density  %6.3g GRMS ' %grms 
        plt.title(title_string)
        
        y1=10**int(floor(log10(min(self.acceleration_psd))))
        y2=10**int(ceil(log10(max(self.acceleration_psd))))
        
        if(y1<y2*1.0e-05):
            y1=y2*1.0e-05  
            
        plt.ylim([y1,y2])             
            
        plt.ylabel('Accel (G^2/Hz)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
        
##########
        
        plt.close(4)
        plt.figure(4)   
        
        plt.plot(self.fi,self.velocity_psd)        

        y1=10**int(floor(log10(min(self.velocity_psd))))
        y2=10**int(ceil(log10(max(self.velocity_psd))))
        
        if(y1<y2*1.0e-05):
            y1=y2*1.0e-05  

        plt.ylim([y1,y2])

        if(n==0):
            title_string='Velocity Power Spectral Density  %6.3g ips RMS ' %vrms 
            plt.ylabel('Vel (ips^2/Hz)')
        else:
            title_string='Velocity Power Spectral Density  %6.3g (cm/sec) RMS ' %vrms 
            plt.ylabel('Vel ((cm/sec)^2/Hz)')        
        
        plt.title(title_string)
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()       
        
##########
        
        plt.close(5)
        plt.figure(5)   
        
        plt.plot(self.fi,self.displacement_psd)        

        y1=10**int(floor(log10(min(self.displacement_psd))))
        y2=10**int(ceil(log10(max(self.displacement_psd))))

        print(y1,y2)

        if(y1<y2*1.0e-05):
            y1=y2*1.0e-05  
              

        plt.ylim([y1,y2])

        if(n==0):
            title_string='Displacement Power Spectral Density  %6.3g inch RMS ' %drms 
            plt.ylabel('Disp (inch^2/Hz)')
        else:
            title_string='Displacement Power Spectral Density  %6.3g mm RMS ' %vrms 
            plt.ylabel('Disp (mm^2/Hz)')        
        
        plt.title(title_string)
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()              

##########        

        print (" ")
        print (" view plots ")

        self.button_export.config(state = 'normal')

###############################################################################

    def unit_option(self,val):
        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):
            self.mass_text.set('Enter Mass (lbm)') 
        else:
            self.mass_text.set('Enter Mass (kg)')   

###############################################################################
                      
def quit(root):
    root.destroy()
                       
###############################################################################