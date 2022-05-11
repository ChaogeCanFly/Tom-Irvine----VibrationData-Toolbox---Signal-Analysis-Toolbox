########################################################################
# 
# program: vb_sdof_base_psd_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.8
# date: Januar 28, 2015
# description:  
#    
#  This script calculates the response of an SDOF system to a PSD base input.
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

from vb_utilities import WriteData2
from vb_utilities import spectral_moments_constant_df

import matplotlib.pyplot as plt

from matplotlib.ticker import ScalarFormatter



###############################################################################

class vb_sdof_base_psd:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.18))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        
        self.master.title("vb_sdof_base_psd_gui.py ver 1.8  by Tom Irvine") 
        
        self.f=[]
        self.a=[]
        self.slope=[]
        self.grms_in=0

###############################################################################
        
        crow=0
        
        self.hwtext3=tk.Label(top,text='This script calculates the response of an SDOF system to a PSD base input.')
        self.hwtext3.grid(row=crow, column=0,columnspan=4, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='The input file must have two columns: Freq(Hz) & Accel(G^2/Hz)')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
        crow=crow+1    
        
        self.hwtext4=tk.Label(top,text='Select Output Units')
        self.hwtext4.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)                 
        
        crow=crow+1        
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=2,sticky=tk.N)
        
        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "G, in/sec, in")
        self.Lb1.insert(2, "G, m/sec, mm")
        self.Lb1.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lb1.select_set(0)  
        
           
        crow=crow+1

        self.hwtext_fn=tk.Label(top,text='Enter Natural Frequency (Hz)')
        self.hwtext_fn.grid(row=crow, column=0, columnspan=1, padx=14, pady=10,sticky=tk.S)

        self.hwtext_Q=tk.Label(top,text='Enter Q')
        self.hwtext_Q.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S)
        
        self.hwtext_fn=tk.Label(top,text='Enter Duration (sec)')
        self.hwtext_fn.grid(row=crow, column=2, columnspan=1, padx=14, pady=10,sticky=tk.S)        
        
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
        
        
        crow=crow+1    
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0, pady=20)   
        
        self.button_export = tk.Button(top, text="Export Response PSD", command=self.export)
        self.button_export.config( height = 2, width = 22,state = 'disabled')
        self.button_export.grid(row=crow, column=1, pady=20)          
        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 12 )
        self.button_quit.grid(row=crow, column=2,pady=20)    
        
###############################################################################

    def export(self): 
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the response acceleration PSD filename")           
        output_file = output_file_path.rstrip('\n')    

        num=len(self.fi)

        WriteData2(num,self.fi,self.aa_psd,output_file)


        

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
     
        av=av*386**2
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
        
        self.slope=slope
        
        self.button_calculate.config(state = 'normal') 
                
###############################################################################
                
    def calculation(self):
        
        n= int(self.Lb1.curselection()[0])
        
        Q=float(self.Qr.get())
        damp=1./(2.*Q)        

        fn=float(self.fnr.get())

        dur=float(self.durr.get())

###

        tpi=2*pi

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

        for i in range (0,int(nif)): 	
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

##   Absolute Acceleration

        self.aa_psd=zeros(nif,'f')
        self.trans=zeros(nif,'f')        

        sum=0.

        for j in range (0,int(nif)):

            rho=self.fi[j]/fn
            tdr=2.*damp*rho
        
            c1=tdr**2
            c2=(1-rho**2)**2
    
            t= (1.+ c1 ) / ( c2 + c1 )
            
            self.trans[j]=t

            self.aa_psd[j]=t*self.ai[j]
            sum+=self.aa_psd[j]
	
        grms=sqrt(sum*df)

        grms_out=grms


        m0,m1,m2,m4,vo,vp = spectral_moments_constant_df(self.fi,self.aa_psd,df)  

##   Absolute Displacement
	
        sum=0. 
 
        for j in range (0,int(nif)):

            rho=self.fi[j]/fn
            tdr=2.*damp*rho
        
            c1=tdr**2
            c2=(1-rho**2)**2

            t= (1.+ c1 ) / ( c2 + c1 )
   
            sum+=t*self.ai[j]*df/pow( (tpi*self.fi[j]),4.)   
   
            drms=sqrt(sum)*386.   
   
      
   
##   Relative Displacement

        sum=0.

        for j in range (0,int(nif)):

            rho=self.fi[j]/fn
            tdr=2.*damp*rho

            c1= pow( ( pow(fn,2.)-pow(self.fi[j],2.) ),2. )
            c2= pow( ( 2.*damp*fn*self.fi[j]),2.)

            t= 1. / ( c2 + c1 )

            sum+=t*self.ai[j]*df
		
            rrms=sqrt(sum)*386./pow(tpi,2.)

################################################################################
    
        print ("\n\n ** Output Overall Levels **")	
        
        if(fn>=min(self.f) and fn<=max(self.f)):
            c=sqrt(2*log(fn*dur))
            nnf=c + 0.5772/c                                                               
            print ("\n Maximum expected peak from Rayleigh distribution = %6.2g-sigma" %nnf)          
        
        
        print ("\n Absolute Acceleration = %12.4g GRMS  " %grms)
        print ("                       = %12.4g 3-sigma G         " %(3.*grms))

        if(fn>=min(self.f) and fn<=max(self.f)):
            print ("                       = %12.4g %6.2g-sigma G" %(nnf*grms,nnf))

################################################################################
        
        omegan=tpi*fn        
        
        if(n==0):
            print ("\n Absolute Displacement = %12.4g inches RMS" %drms)	
            
            print ("\n Pseudo Velocity       = %12.4g inch/sec RMS" %(omegan*rrms))
            print ("                       = %12.4g inch/sec 3-sigma " %(omegan*rrms*3.)) 
            
            if(fn>=min(self.f) and fn<=max(self.f)):
                print ("                       = %12.4g %6.2g-sigma inch/sec" \
                                                        %(omegan*nnf*rrms,nnf))
        
            print ("\n Relative Displacement = %12.4g inches RMS" %(rrms))
            print ("                       = %12.4g inches 3-sigma " %(rrms*3.))		
       
                   
        else:
            print ("\n Absolute Displacement = %12.4g mm RMS " %(drms*25.4))				

            print ("\n Pseudo Velocity       = %12.4g cm/sec RMS" %(omegan*rrms*2.54))
            print ("                       = %12.4g cm/sec 3-sigma " %(omegan*rrms*2.54*3))

            if(fn>=min(self.f) and fn<=max(self.f)):
                print ("                       = %12.4g %6.2g-sigma cm/sec" \
                                                   %(omegan*nnf*rrms*2.54,nnf))                

            print ("\n Relative Displacement = %12.4g mm RMS " %(rrms*25.4))
            print ("                       = %12.4g mm 3-sigma " %(rrms*25.4*3.))             

	


        print('\n Acceleration ')
        print('\n Rate of Up-zero crossings = %7.4g Hz' %vo)
        print('             Rate of peaks = %7.4g Hz' %vp)  
	
################################################################################

        print (" ")
        print (" view plots ")

        maxa=max(self.a)
        mina=min(self.a)
        maxp=max(self.aa_psd)
        minp=min(self.aa_psd)


        ymax=10**ceil(log10(maxp))

        if(maxa>maxp):
            ymax=10**ceil(log10(maxa))    


        ymin=10**floor(log10(minp))
        
        if(mina<minp):
            ymin=10**floor(log10(mina))    

        if(ymin<ymax*1.0e-05):
            ymin=ymax*1.0e-05
        
        
        
        self.button_export.config(state = 'normal')

        plt.ion()
        plt.figure(1)     

        input_string='input '+str("%6.3g" %self.grms_in)+' GRMS'
        response_string='response '+str("%6.3g" %grms_out)+' GRMS'

        plt.plot(self.f,self.a,label=input_string)
        plt.plot(self.fi,self.aa_psd,label=response_string)

         
    
        title_string='Power Spectral Density  fn=' + str("%g" %fn)+' Hz  Q=' +str("%g" %Q)

        plt.title(title_string)
        plt.ylabel(' Accel (G^2/Hz)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        plt.legend(loc="upper right") 
        plt.ylim([ymin,10*ymax])
        

        if(min(self.f)==20 and max(self.f)==2000):
            
                
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(20,2000))    
              
            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                
        
            plt.xlim([20,2000])


        plt.show()


###############################################################################

        maxa=max(self.trans)
        mina=min(self.trans)

        ymax=10**ceil(log10(maxa))    
        ymin=10**floor(log10(mina))

        if(ymin<ymax*1.0e-06 and ymin < 0.01):
            ymin=0.01


        plt.figure(2)     

        plt.plot(self.fi,self.trans,label=response_string)

         
        title_string='Power Transmissibility  fn=' + str("%g" %fn)+' Hz  Q=' +str("%g" %Q)

        plt.title(title_string)
        plt.ylabel(' Trans (G^2/G^2)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        plt.ylim([ymin,ymax])

        if(min(self.f)==20 and max(self.f)==2000):
            
                
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(20,2000))    
              
            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                
        
            plt.xlim([20,2000])

        plt.show()


###############################################################################
                      
def quit(root):
    root.destroy()
                       
###############################################################################