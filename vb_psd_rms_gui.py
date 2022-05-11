########################################################################
# program: vb_psd_rms_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.7
# date: January 27, 2015
# description:  
#              
#  This script calculates the overall level of a PSD.
#
########################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename
    from ttk import Treeview
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    from tkinter.ttk import Treeview
    

from vb_utilities import read_two_columns_from_dialog,loglog_plot
from vb_utilities import spectral_moments_constant_df,interpolate_psd

from numpy import array,zeros,log,pi,sqrt,delete


###############################################################################

class vb_psd_rms:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.19))
        h = int(2.*(h*0.30))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_psd_rms_gui.py ver 1.7  by Tom Irvine")  


###############################################################################
        
        crow=0
        
        self.hwtext3=tk.Label(top,text='This script calculates the overall level of a PSD.')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='The input file must have two columns: Freq(Hz) & Accel(G^2/Hz)')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
        crow=crow+1    
        
        self.hwtext4=tk.Label(top,text='Select Output Units')
        self.hwtext4.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)                 
        
        crow=crow+1        
        
        self.acc_psdutton_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.acc_psdutton_read.config( height = 3, width = 15 )
        self.acc_psdutton_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=2,sticky=tk.N)
        
        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "G, in/sec, in")
        self.Lb1.insert(2, "G, m/sec, mm")
        self.Lb1.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lb1.select_set(0)        
        
        crow=crow+1

        self.hwtext5=tk.Label(top,text='Results, Overall Levels')
        self.hwtext5.grid(row=crow, column=0,columnspan=2, pady=20,sticky=tk.S)        
        
        crow=crow+1          
                
        self.tree = Treeview(top,selectmode="extended",columns=("A","B"),height=6)
        self.tree.grid(row=crow, column=0,columnspan=2, padx=10,pady=1,sticky=tk.N)

        self.tree.heading('#0', text='') 
        self.tree.heading('A', text='Parameter')          
        self.tree.heading('B', text='Value')
        
        self.tree.column('#0',minwidth=0,width=1)
        self.tree.column('A',minwidth=0,width=90, stretch=tk.YES)        
        self.tree.column('B',minwidth=0,width=140)           

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

        crow=crow+1
        
        root=self.master  
        
        self.acc_psdutton_replot=tk.Button(top, text="Replot", command=self.plot_psd_replot)
        self.acc_psdutton_replot.config( height = 2, width = 15 )
        self.acc_psdutton_replot.grid(row=crow, column=0,pady=8,sticky=tk.S)          
        
        self.acc_psdutton_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.acc_psdutton_quit.config( height = 2, width = 15 )
        self.acc_psdutton_quit.grid(row=crow, column=1,pady=8,sticky=tk.S)  


###############################################################################


    def plot_psd_replot(self):
        self.plot_psd_m(self)
        

    @classmethod    
    def plot_psd_m(cls,self):
        
        
        if not self.fminr.get(): #do something
            self.f1=min(self.freq)         
        else:
            fminp=float(self.fminr.get())
            self.f1=fminp        

        if not self.fmaxr.get(): #do something
            self.f2=max(self.freq)         
        else:
            fmaxp=float(self.fmaxr.get())
            self.f2=fmaxp   
                

        xlab='Frequency (Hz)' 
    
        
        fig_num=1    
        
        
#       Displacement

        if(self.iunit==0):
            title_string='Displacement PSD   '+str("%6.3g" %self.drms)+' in RMS Overall '
            
            ylab='Disp (in^2/Hz)'            
            
        else:
            title_string='Displacement PSD   '+str("%6.3g" %self.drms)+' mm RMS Overall '

            ylab='Disp (in^2/Hz)'  


        fig_num=loglog_plot(self.freq,self.vpsd,xlab,ylab,self.f1,self.f2,title_string,fig_num)         
        
        
#       Velocity

        if(self.iunit==0):
            title_string='Velocity PSD   '+str("%6.3g" %self.vrms)+' in/sec RMS Overall '
            
            ylab='Vel ((in/sec)^2/Hz)'            
            
        else:
            title_string='Velocity PSD   '+str("%6.3g" %self.vrms)+' m/sec RMS Overall '

            ylab='Vel ((m/sec)^2/Hz)'  


        fig_num=loglog_plot(self.freq,self.vpsd,xlab,ylab,self.f1,self.f2,title_string,fig_num) 
                
#       acceleration        
        
        ylab='Accel (G^2/Hz)'
        
        title_string='Acceleration PSD   '+str("%6.3g" %self.grms)+' GRMS Overall '
        
        fig_num=loglog_plot(self.freq,self.acc_psd,xlab,ylab,self.f1,self.f2,title_string,fig_num)        
        




###############################################################################

    def read_data(self):            
        """
        a = frequency column
        b = PSD column
        num = number of coordinates
        slope = slope between coordinate pairs    
        """
        
        map(self.tree.delete, self.tree.get_children())        
        
        print (" ")
        print (" The input file must have two columns: freq(Hz) & accel(G^2/Hz)")

        a,b,num =read_two_columns_from_dialog('Select Input File',self.master)

        print ("\n samples = %d " % num)

        a=array(a)
        b=array(b)
        
        if(a[0]<1.0e-20 or b[0]<1.0e-20):
            a = delete(a, 0)
            b = delete(b, 0)  
            num=num-1
    

        nm1=num-1

        slope =zeros(nm1,'f')


        ra=0

        for i in range (0,int(nm1)):
#
            s=log(b[i+1]/b[i])/log(a[i+1]/a[i])
        
            slope[i]=s
#
            if s < -1.0001 or s > -0.9999:
                ra+= ( b[i+1] * a[i+1]- b[i]*a[i])/( s+1.)
            else:
                ra+= b[i]*a[i]*log( a[i+1]/a[i])

        omega=2*pi*a

##
        df=0.1
        
        aint,bint=interpolate_psd(a,b,slope,df)

        m0,m1,m2,m4,vo,vp = spectral_moments_constant_df(aint,bint,df)

##
        bv=zeros(num,'f') 
        bd=zeros(num,'f') 
        
        vpsd=zeros(num,'f')
        dpsd=zeros(num,'f')        
        
        
        for i in range (0,int(num)):         
            bv[i]=b[i]/omega[i]**2
            bd[i]=b[i]/omega[i]**4               
               
        bv=bv*386**2        
        vpsd=bv
        
        bd=bd*386**2        
        dpsd=bd        
        
        
        rv=0        


        for i in range (0,int(nm1)):
#
            s=log(bv[i+1]/bv[i])/log(a[i+1]/a[i])
#
            if s < -1.0001 or s > -0.9999:
                vv= ( bv[i+1] * a[i+1]- bv[i]*a[i])/( s+1.)
                rv+=vv 
            else:
                vv=  bv[i]*a[i]*log( a[i+1]/a[i])
                rv+= vv
                
              
     
        rd=0

        for i in range (0,int(nm1)):
#
            s=log(bd[i+1]/bd[i])/log(a[i+1]/a[i])
#
            if s < -1.0001 or s > -0.9999:
                rd+= ( bd[i+1] * a[i+1]- bd[i]*a[i])/( s+1.)
            else:
                rd+= bd[i]*a[i]*log( a[i+1]/a[i])         


        m=int(self.Lb1.curselection()[0])
        

        rms=sqrt(ra)
        three_rms=3*rms
    
        print (" ")
        print (" *** Input PSD *** ")
        print (" ")
 
        print (" Acceleration ")
        print ("   Overall = %10.3g GRMS" % rms)
        print ("           = %10.3g 3-sigma" % three_rms)

        grms=rms

        vrms=sqrt(rv)

        if(m==1):
            scale=(9.81/386.)             
            vrms=scale*vrms
            vpsd=scale**2*vpsd
            

        

        vthree_rms=3*vrms

        print (" ")
        print (" Velocity ") 

        if(m==0):
            print ("   Overall = %10.3g in/sec rms" % vrms)
            print ("           = %10.3g in/sec 3-sigma" % vthree_rms)
        else:
            print ("   Overall = %10.3g m/sec rms" % vrms)
            print ("           = %10.3g m/sec 3-sigma" % vthree_rms)            


        drms=sqrt(rd)

        if(m==1):
            scale=(9.81/386.)*1000
            drms=scale*drms
            dpsd=scale**2*dpsd
            

        dthree_rms=3*drms

        print (" ")
        print (" Displacement ") 
        
        if(m==0):
            print ("   Overall = %10.3g in rms" % drms)
            print ("           = %10.3g in 3-sigma" % dthree_rms)
        else:
            print ("   Overall = %10.3g mm rms" % drms)
            print ("           = %10.3g mm 3-sigma" % dthree_rms)           
        
########
        

        s0='Acceleration'
        s1="%8.3g GRMS" %grms
        self.tree.insert('', 'end', values=(s0,s1))
        
        s0=' '
        s1="%8.3g 3-sigma" %three_rms
        self.tree.insert('', 'end', values=(s0,s1))
     
                
        s0='Velocity'
        if(m==0):
            s1="%8.3g in/sec rms" %vrms
        else:
            s1="%8.3g m/sec rms" %vrms
        self.tree.insert('', 'end', values=(s0,s1))
             
                
        s0=' '
        if(m==0):
            s1="%8.3g in/sec 3-sigma" %vthree_rms
        else:
            s1="%8.3g m/sec 3-sigma" %vthree_rms
        self.tree.insert('', 'end', values=(s0,s1))
 

        s0='Displacement'
        if(m==0):
            s1="%8.3g in rms" %drms
        else:
            s1="%8.3g mm rms" %drms
        self.tree.insert('', 'end', values=(s0,s1))
     
                
        s0=' '
        if(m==0):
            s1="%8.3g in 3-sigma" %dthree_rms
        else:
            s1="%8.3g mm 3-sigma" %dthree_rms
        self.tree.insert('', 'end', values=(s0,s1))
        
        
        print('\n Rate of Up-zero crossings = %7.4g Hz' %vo)
        print('             Rate of peaks = %7.4g Hz' %vp)        
        
      
        self.iunit=m      
      
        self.freq=a
        self.acc_psd=b
        self.grms=rms
        
        self.vrms=vrms
        self.vpsd=vpsd

        self.drms=drms
        self.dpsd=dpsd


        self.plot_psd_m(self)
        
        
###############################################################################
    
###############################################################################
              
def quit(root):
    root.destroy()
                       
###############################################################################