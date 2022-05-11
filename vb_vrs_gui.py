########################################################################
# program: vb_vrs_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.6
# date: October 17, 2014
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

    

    
from vb_utilities import read_two_columns_from_dialog,WriteData2  

from numpy import array,zeros,log,pi,sqrt,floor

from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt


###############################################################################

class vb_VRS:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.20))
        h = int(2.*(h*0.30))
        
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        
        self.master.title("vb_vrs_gui.py ver 1.6  by Tom Irvine") 
        
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
        
        self.hwtext3=tk.Label(top,text='This script calculates the VRS for a PSD base input.')
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

        self.hwtext_Q=tk.Label(top,text='Enter Q')
        self.hwtext_Q.grid(row=crow, column=0, columnspan=1, padx=14, pady=10,sticky=tk.S)
        
        self.hwtext_fn=tk.Label(top,text='Enter Duration (sec)')
        self.hwtext_fn.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S)        
  

        crow=crow+1        
 

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 12,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)    
        
        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 12,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N)  


          
        crow=crow+1

        self.hwtext10=tk.Label(top,text='Minimum Plot Freq (Hz)')
        self.hwtext10.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.S)    

        self.hwtext11=tk.Label(top,text='Maximum Plot Freq (Hz)')
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
        
        self.Lbe = tk.Listbox(top,height=4,exportselection=0)
        self.Lbe.insert(1, "Accel VRS GRMS")
        self.Lbe.insert(2, "Accel VRS 3-sigma")
        self.Lbe.insert(3, "Accel VRS n-sigma")
        self.Lbe.insert(4, "Rel Disp VRS RMS")        
        
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
            WriteData2(self.num_fn,self.ff,self.avrs,output_file)  
            
        if(ne==1):
            WriteData2(self.num_fn,self.ff,self.tsvrs,output_file)  
            
        if(ne==2):    
            WriteData2(self.num_fn,self.ff,self.nvrs,output_file)  
            
        if(ne==3):
            WriteData2(self.num_fn,self.ff,self.rdvrs,output_file)             
            
          
                
    def calculation(self):
        
        
        Q=float(self.Qr.get())
        damp=1./(2.*Q)        

        dur=float(self.durr.get())

        fminp=float(self.fminr.get())
        fmaxp=float(self.fmaxr.get())


        tpi=2*pi

        df= 1/40.


        if( fminp >= 1):
            df =  fminp/40. 

        nif=int(floor((max(self.f)-min(self.f))/df))

        fi=zeros(nif,'f')
        ai=zeros(nif,'f')

        fi[0]=self.f[0]
        ai[0]=self.a[0]
    
        


        fmax=max(self.f)

        m=len(self.f)
        
 
        for i in range (0,int(nif)): 	
            fi[i]=self.f[0]+df*i

            if( fi[i] > fmax ):
                break
    
            iflag=0
    
            for j in range (0,int(m-1)):
		
                if( ( fi[i] >= self.f[j] ) and ( fi[i] <= self.f[j+1] ) and iflag==0  ):
					
                    ai[i]=self.a[j]*( ( fi[i] / self.f[j] )**self.slope[j] )
                    iflag=1
#            print (fi[i],ai[i])

							
# print  ("\n interp df = %10.4g Hz  nif=%d  max(fi)=%8.4g  m=%d\n" %(df,nif,max(fi),m))

###############################################################################


        last=len(fi)
        
        a_vrs=zeros(last,'f')
        rd_vrs=zeros(last,'f')

        fn=zeros(10000,'f')
        
 
        fn[0]=5.
        oct=1./24.
        tpi_sq=tpi**2
        
        print (" ")

        print ("calculating vrs.  Percent complete: ")
        
        nfn=len(fn)
        
        tdamp=2*damp
        tdamp2=tdamp**2.        
   
        kk=0
   
        for i in range(0,int(nfn)):   # natural frequency loop
            if(fn[i] > 10000. ):
                break
                     
            if(fn[i] > 2.*fi[last-1] ):
                break
           
            fn[i+1]= fn[i]*(2.**oct)  
            
            kk+=1

          
        i1=0
        i2=0
        i3=0
        i4=0
        L1=0.2
        L2=0.4
        L3=0.6
        L4=0.8
             

        for i in range(0,int(kk)):   # natural frequency loop

            ratio=float(i)/float(kk)
                      
            
            if(ratio>L1 and i1==0):
                i1=1
                print("%3.0f" %(100*ratio))
                
            if(ratio>L2 and i2==0):
                i2=1
                print("%3.0f" %(100*ratio))
                            
            if(ratio>L3 and i3==0):
                i3=1
                print("%3.0f" %(100*ratio))
                
            if(ratio>L4 and i4==0):
                i4=1
                print("%3.0f" %(100*ratio))
                
#   absolute acceleration

            fn2=fn[i]**2.

            suma=0.
            sumr=0.

            for j in range(0,int(last)):

                rho = fi[j]/fn[i]
                tdr=tdamp*rho

                c1= tdr** 2.
                c2= (1.- (rho**2.))** 2.

                suma+= ai[j]*(1.+ c1 ) / ( c2 + c1 )             
             
                fi2=fi[j]**2.              
             
                c1= (fn2-fi2)**2.
                c2= tdamp2*fn2*fi2

                sumr+= ai[j]/ ( c2 + c1 ) 


            rd_vrs[i]=sqrt(sumr*df)/tpi_sq       
            a_vrs[i]=sqrt(suma*df)
              
        
        ratio=1
        print("%3.0f" %(100*ratio))
        print ("")    
###############################################################################

        nn=len(a_vrs) 
        
        ff=[]
        avrs=[]
        tsvrs=[]
        nsvrs=[]
        rdvrs=[]


        nu= int(self.Lb1.curselection()[0])        
   
        
        if(nu==0):
            rd_vrs*=386
        else:
            rd_vrs*=9.81*1000


        for i in range(0,int(nn)):

            if(fn[i]>=fminp and fn[i]<=fmaxp):
                ff.append(fn[i])
                avrs.append(a_vrs[i])
                tsvrs.append(3*a_vrs[i])
                c=sqrt(2*log(fn[i]*dur))
                ms=c + 0.5772/c
                nsvrs.append(ms*a_vrs[i])
                rdvrs.append(rd_vrs[i])
            
        plt.close(2)        
        plt.figure(2)        

        plt.plot(ff,nsvrs,label='peak')
        plt.plot(ff,tsvrs,label='3-sigma')
        plt.plot(ff,avrs,label='1-sigma')

        
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
#
        Q=1/(2*damp)
        title_string= 'Acceleration Vibration Response Spectrum Q='+str(Q)
#
        for i in range(1,200):
            if(Q==float(i)):
                title_string= 'Acceleration Vibration Response Spectrum Q='+str(i)
                break
#
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')
        plt.ylabel('Accel (G)')
        plt.grid(True, which="both")
    
        plt.legend(loc="upper left") 
            
        if(fminp==20 and fmaxp==2000):
                
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(fminp,fmaxp))    
              
            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                              
            
        plt.xlim([fminp,fmaxp])    
    
        plt.draw()


###############################################################################

        plt.close(3)
        plt.figure(3)        

        plt.plot(ff,rdvrs)
        
        if(nu==0):
            plt.ylabel('Rel Disp (inch RMS)')
        else:
            plt.ylabel('Rel Disp (mm RMS)')      

                    
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
#
        Q=1/(2*damp)
        title_string= 'Relative Displacement Vibration Response Spectrum Q='+str(Q)
#
        for i in range(1,200):
            if(Q==float(i)):
                title_string= 'Relative Displacement Vibration Response Spectrum Q='+str(i)
                break
#
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')        

        plt.grid(True, which="both")
        
        if(fminp==20 and fmaxp==2000):
                
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(fminp,fmaxp))    
              
            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                              
            
        plt.xlim([fminp,fmaxp])          
        
        plt.draw()      
        
        
        self.ff=ff
        self.rdvrs=rdvrs
        self.avrs=avrs
        self.tsvrs=tsvrs
        self.nsvrs=nsvrs        
        
        self.num_fn=len(ff)
        
        self.button_export.config(state = 'normal')        

        print ("Calculation complete.  View Plots.")

###############################################################################
                      
def quit(root):
    root.destroy()
                       
###############################################################################