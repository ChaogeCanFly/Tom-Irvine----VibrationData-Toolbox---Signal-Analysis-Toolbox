########################################################################
# program: vb_vrs_force_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.1
# date: December 12, 2014
# description:  
#    
#  This script will calculate a vibration response spectrum for an 
#  an applied force PSD.
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

from numpy import array,zeros,log,log10,pi,sqrt,floor,ceil

from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt


###############################################################################

class vb_VRS_force:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        
        self.master.title("vb_vrs_force_gui.py ver 1.1  by Tom Irvine") 
        
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
        
        self.hwtext3=tk.Label(top,text='This script calculates the VRS for an applied force PSD.')
        self.hwtext3.grid(row=crow, column=0,columnspan=4, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='The input file must have two columns: Freq(Hz) & Force(units^2/Hz)')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
        crow=crow+1    
        
        self.hwtext4=tk.Label(top,text='Select Output Units')
        self.hwtext4.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)                 
        
        crow=crow+1        
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=2,sticky=tk.N)
        
        self.Lb1 = tk.Listbox(top,height=3,width=23,exportselection=0)
        self.Lb1.insert(1, "lbf, G, in/sec, in")
        self.Lb1.insert(2, "N, G, m/sec, mm")
        self.Lb1.insert(3, "N, m/sec^2, m/sec, mm")       
        self.Lb1.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lb1.select_set(0)  
        self.Lb1.bind('<<ListboxSelect>>',self.unit_option)          
           
        crow=crow+1

        self.hwtext_Q=tk.Label(top,text='Enter Q')
        self.hwtext_Q.grid(row=crow, column=0, columnspan=1, padx=14, pady=10,sticky=tk.S)
        
        self.hwtext_fn=tk.Label(top,text='Enter Duration (sec)')
        self.hwtext_fn.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S)        
  

        self.mass_text=tk.StringVar()  
        self.mass_text.set('Enter Mass (lbm)')         
        self.hwtext_mass=tk.Label(top,textvariable=self.mass_text)
        self.hwtext_mass.grid(row=crow, column=2, columnspan=1, padx=14, pady=10,sticky=tk.S)  


        crow=crow+1        
 

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 12,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)    
        
        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 12,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N)  

        self.massr=tk.StringVar()  
        self.massr.set('')  
        self.mass_entry=tk.Entry(top, width = 12,textvariable=self.massr)
        self.mass_entry.grid(row=crow, column=2,padx=14, pady=1,sticky=tk.N)

          
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
        
        self.hwtext22=tk.Label(top,text='Export Metric')
        self.hwtext22.grid(row=crow, column=2,columnspan=1, pady=10,sticky=tk.S)        
        
        crow=crow+1   

        self.button_export = tk.Button(top, text="Export Data", command=self.export)
        self.button_export.config( height = 2, width = 15,state = 'disabled')
        self.button_export.grid(row=crow, column=0, pady=10,sticky=tk.N)   
        
        self.Lbe = tk.Listbox(top,height=4,width=20,exportselection=0)
        self.Lbe.insert(1, "Acceleration")
        self.Lbe.insert(2, "Velocity")
        self.Lbe.insert(3, "Displacement")
        self.Lbe.insert(4, "Transmitted Force")        
        
        self.Lbe.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lbe.select_set(0)  
        
    
        
        self.Lbf = tk.Listbox(top,height=4,width=20,exportselection=0)
        self.Lbf.insert(1, "1-sigma")
        self.Lbf.insert(2, "3-sigma")
        self.Lbf.insert(3, "peak")      
        
        self.Lbf.grid(row=crow, column=2, pady=2,sticky=tk.N)
        self.Lbf.select_set(0)          
        
###############################################################################

    def unit_option(self,val):
        n1=int(self.Lb1.curselection()[0])
        
        if(n1==0):
            self.mass_text.set('Enter Mass (lbm)') 
        else:
            self.mass_text.set('Enter Mass (kg)')  
            
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
    

        nu=int(self.Lb1.curselection()[0])

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
 
        print (" Force ")
        
        if(nu==0):        
        
            print ("   Overall = %10.3g lbf RMS" % rms)
            print ("           = %10.3g 3-sigma" % three_rms)
        
        else:        
    
            print ("   Overall = %10.3g N RMS" % rms)
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
        
        y1=10**int(floor(log10(min(a))))
        y2=10**int(ceil(log10(max(a))))
        
        if(y2==y1):
            y2=10*y1 
            y1=y1/10
        
        plt.ylim([y1,y2])           
        
        
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
                
    def export(self):
        
        root=self.master    
        ne= int(self.Lbe.curselection()[0]) 
        nf= int(self.Lbf.curselection()[0])        

        output_file_path = asksaveasfilename(parent=root,title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n') 

        if(ne==0):
            if(nf==0):
                WriteData2(self.num_fn,self.ff,self.avrs,output_file)  
            if(nf==1):
                WriteData2(self.num_fn,self.ff,self.atsvrs,output_file)  
            if(nf==2):
                WriteData2(self.num_fn,self.ff,self.ansvrs,output_file)                  
            
        if(ne==1):
            if(nf==0):
                WriteData2(self.num_fn,self.ff,self.vvrs,output_file)  
            if(nf==1):
                WriteData2(self.num_fn,self.ff,self.vtsvrs,output_file)  
            if(nf==2):
                WriteData2(self.num_fn,self.ff,self.vnsvrs,output_file)  
            
        if(ne==2):    
            if(nf==0):
                WriteData2(self.num_fn,self.ff,self.dvrs,output_file)  
            if(nf==1):
                WriteData2(self.num_fn,self.ff,self.dtsvrs,output_file)  
            if(nf==2):
                WriteData2(self.num_fn,self.ff,self.dnsvrs,output_file)   
            
        if(ne==3):
            if(nf==0):
                WriteData2(self.num_fn,self.ff,self.tfvrs,output_file)  
            if(nf==1):
                WriteData2(self.num_fn,self.ff,self.tftsvrs,output_file)  
            if(nf==2):
                WriteData2(self.num_fn,self.ff,self.tfnsvrs,output_file)   
                      
            
          
    def calculation(self):
        
        nu=int(self.Lb1.curselection()[0])
        
        masso=self.massr.get()
        
        mass=float(masso)
        

        if(nu==0):
            mass/=386
                   
        
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
        v_vrs=zeros(last,'f')
        d_vrs=zeros(last,'f')
        tf_vrs=zeros(last,'f')        


        fn=zeros(10000,'f')
        
 
        fn[0]=5.
        oct=1./24.
        
        print (" ")

        print ("calculating vrs.  Percent complete: ")
        
        nfn=len(fn)

        kk=0


###############################################################################
   
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

            suma=0.
            sumv=0.
            sumd=0.            
            sumtf=0.
            
            omegan=tpi*fn[i]
            omegan2=omegan**2
            k=omegan2*mass                 
            num=omegan2/k
            
            tdr=2.*damp*omegan

#            print (fn[i],k,mass,tdr)

            for j in range(0,int(last)):

                omega=tpi*fi[j]
                
                den=omegan2-omega**2+(1j)*omega*tdr 
                
                ta= num/den
######
                t=ta*(-omega**2)            
                suma+=abs(t**2)*ai[j]
#####
                t=ta*(1j)*omega
                sumv+=abs(t**2)*ai[j]
######              
                t=ta
                sumd+=abs(t**2)*ai[j]  
######
                numf=omegan2+(1j)*omega*tdr
                t= numf/den
                sumtf+=abs(t**2)*ai[j]  
######                
      
            a_vrs[i]=sqrt(suma*df)
            v_vrs[i]=sqrt(sumv*df)
            d_vrs[i]=sqrt(sumd*df)
            tf_vrs[i]=sqrt(sumtf*df)            
              
        
        ratio=1
        print("%3.0f" %(100*ratio))
        print ("")    
        
###############################################################################

        nn=len(a_vrs) 
        
        ff=[]

        avrs=[]
        atsvrs=[]
        ansvrs=[]        
        
        vvrs=[]
        vtsvrs=[]
        vnsvrs=[]  
        
        dvrs=[]
        dtsvrs=[]
        dnsvrs=[]          
        
        tfvrs=[]
        tftsvrs=[]
        tfnsvrs=[]          
                        
        nu= int(self.Lb1.curselection()[0])        
   
        
        if(nu==0):
            a_vrs/=386
        
        if(nu==1):
            a_vrs/=9.81
            d_vrs*=1000

        if(nu==2):
            d_vrs*=1000


        for i in range(0,int(nn)):

            if(fn[i]>=fminp and fn[i]<=fmaxp):
                ff.append(fn[i])

                c=sqrt(2*log(fn[i]*dur))
                ms=c + 0.5772/c                
                
                avrs.append(a_vrs[i])
                atsvrs.append(3*a_vrs[i])
                ansvrs.append(ms*a_vrs[i])
                
                vvrs.append(v_vrs[i])
                vtsvrs.append(3*v_vrs[i])
                vnsvrs.append(ms*v_vrs[i])
                
                dvrs.append(d_vrs[i])
                dtsvrs.append(3*d_vrs[i])
                dnsvrs.append(ms*d_vrs[i])

                tfvrs.append(tf_vrs[i])
                tftsvrs.append(3*tf_vrs[i])
                tfnsvrs.append(ms*tf_vrs[i])                

###############################################################################
            
        plt.close(2)        
        plt.figure(2)        

        plt.plot(ff,ansvrs,label='peak')
        plt.plot(ff,atsvrs,label='3-sigma')
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
         
        if(nu==0):
            title_string= title_string+' mass='+masso+' lbm'
        else:
            title_string= title_string+' mass='+masso+' kg'

            
#
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')

        if(nu<=1):
            plt.ylabel('Accel (G)')
        else:    
            plt.ylabel('Accel (m/sec^2)')
            

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

        plt.plot(ff,vnsvrs,label='peak')
        plt.plot(ff,vtsvrs,label='3-sigma')
        plt.plot(ff,vvrs,label='1-sigma')

        
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
#
        Q=1/(2*damp)
        title_string= 'Velocity Vibration Response Spectrum Q='+str(Q)
#
        for i in range(1,200):
            if(Q==float(i)):
                title_string= 'Velocity Vibration Response Spectrum Q='+str(i)
                break
#
                
        if(nu==0):
            title_string= title_string+' mass='+masso+' lbm'
        else:
            title_string= title_string+' mass='+masso+' kg'

                
                
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')

        if(nu==0):
            plt.ylabel('Vel (in/sec)')
        else:    
            plt.ylabel('Vel (m/sec)')
            

        plt.grid(True, which="both")
    
        plt.legend(loc="upper right") 
            
        if(fminp==20 and fmaxp==2000):
                
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(fminp,fmaxp))    
              
            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                              
            
        plt.xlim([fminp,fmaxp])    
    
        plt.draw()

###############################################################################

        plt.close(4)        
        plt.figure(4)        

        plt.plot(ff,dnsvrs,label='peak')
        plt.plot(ff,dtsvrs,label='3-sigma')
        plt.plot(ff,dvrs,label='1-sigma')

        
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
#
        Q=1/(2*damp)
        title_string= 'Displacement Vibration Response Spectrum Q='+str(Q)
#
        for i in range(1,200):
            if(Q==float(i)):
                title_string= 'Displacement Vibration Response Spectrum Q='+str(i)
                break
#
        if(nu==0):
            title_string= title_string+' mass='+masso+' lbm'
        else:
            title_string= title_string+' mass='+masso+' kg'                
                
                
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')

        if(nu==0):
            plt.ylabel('Disp (in)')
        else:    
            plt.ylabel('Disp (mm)')
            

        plt.grid(True, which="both")
    
        plt.legend(loc="upper right") 
            
        if(fminp==20 and fmaxp==2000):
                
            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(fminp,fmaxp))    
              
            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                              
            
        plt.xlim([fminp,fmaxp])    
    
        plt.draw()

###############################################################################

        plt.close(5)        
        plt.figure(5)        

        plt.plot(ff,tfnsvrs,label='peak')
        plt.plot(ff,tftsvrs,label='3-sigma')
        plt.plot(ff,tfvrs,label='1-sigma')

        
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
#
        Q=1/(2*damp)
        title_string= 'Transmitted Force Vibration Response Spectrum Q='+str(Q)
#
        for i in range(1,200):
            if(Q==float(i)):
                title_string= 'Transmitted Force Vibration Response Spectrum Q='+str(i)
                break
#
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')

        if(nu==0):
            plt.ylabel('Force (lbf)')
        else:    
            plt.ylabel('Force (N)')
            

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
        
        self.ff=ff
               
        self.avrs=avrs
        self.atsvrs=atsvrs
        self.ansvrs=ansvrs        
        
        self.vvrs=vvrs
        self.vtsvrs=vtsvrs
        self.vnsvrs=vnsvrs  
        
        self.dvrs=dvrs
        self.dtsvrs=dtsvrs
        self.dnsvrs=dnsvrs          
        
        self.tfvrs=tfvrs
        self.tftsvrs=tftsvrs
        self.tfnsvrs=tfnsvrs
         
        
        self.num_fn=len(ff)
        
        self.button_export.config(state = 'normal')  

        print ("Calculation complete.  View Plots.")

###############################################################################
                      
def quit(root):
    root.destroy()
                       
###############################################################################