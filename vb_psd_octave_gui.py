########################################################################
# program: vb_psd_octave_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.3
# date: August 85, 2014
# description:  
#              
#  This script converts a PSD to octave format.
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
    

from vb_utilities import read_two_columns_from_dialog

from numpy import array,zeros,log,delete,sqrt,append,int8



import matplotlib.pyplot as plt


###############################################################################

class vb_psd_octave:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.26))
        h = int(2.*(h*0.28))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.fig_num=1

###############################################################################
        
        crow=0
        
        self.hwtext3=tk.Label(top,text='This script converts a PSD into octave format')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='The input file must have two columns: Freq(Hz) & PSD(unit^2/Hz)')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
###############################################################################            
        
        crow=crow+1    
        
        self.hwtext4=tk.Label(top,text='Select Input Type')
        self.hwtext4.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.S)      

        self.hwtext5=tk.Label(top,text='Enter Amplitude Unit')
        self.hwtext5.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)             
        
###############################################################################        
        
        crow=crow+1

        self.Lb1 = tk.Listbox(top,height=7,exportselection=0)

        self.Lb1.insert(1, "Acceleration")
        self.Lb1.insert(2, "Velocity")
        self.Lb1.insert(3, "Displacement")
        self.Lb1.insert(4, "Force")        
        self.Lb1.insert(5, "Pressure")
        self.Lb1.insert(6, "Other")        
        
        self.Lb1.grid(row=crow, column=0, pady=2,sticky=tk.N)
        self.Lb1.select_set(0)        
        
        self.aur=tk.StringVar()  
        self.au_entry=tk.Entry(top, width = 12,textvariable=self.aur)
        self.au_entry.grid(row=crow, column=1, pady=4,sticky=tk.N) 
        self.au_entry.configure(state='normal')
        self.aur.set('G')                    

###############################################################################

        crow=crow+1
        
        self.hwtext4=tk.Label(top,text='Select Octave Format')
        self.hwtext4.grid(row=crow, column=0,columnspan=1, pady=6,sticky=tk.SW)        

        self.hwtextf1=tk.Label(top,text='Min Freq (Hz)')
        self.hwtextf1.grid(row=crow, column=1,padx=5, pady=6,sticky=tk.S)

        self.hwtextf2=tk.Label(top,text='Max Freq (Hz)')
        self.hwtextf2.grid(row=crow, column=2,padx=5, pady=6,sticky=tk.S)
        
###############################################################################

        crow=crow+1        

        self.Lb2 = tk.Listbox(top,height=7,exportselection=0)

        self.Lb2.insert(0, "1")
        self.Lb2.insert(1, "1/3")
        self.Lb2.insert(2, "1/6")
        self.Lb2.insert(3, "1/12")      
        
        self.Lb2.grid(row=crow, column=0, pady=2,sticky=tk.N)
        self.Lb2.select_set(1)        
        
        self.f1r=tk.StringVar()  
        self.f1r.set('')  
        self.f1_entry=tk.Entry(top, width = 9,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=1,padx=5, pady=1,sticky=tk.N)

        self.f2r=tk.StringVar()  
        self.f2r.set('')  
        self.f2_entry=tk.Entry(top, width = 9,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=2,padx=5, pady=1,sticky=tk.N)             

###############################################################################      
        
        crow=crow+1           
                
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 2, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=12)      
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculate)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=1,padx=2, pady=12)         

        self.button_save = tk.Button(top, text="Save PSD", command=self.export_psd)
        self.button_save.config( height = 2, width = 15,state = 'disabled')
        self.button_save.grid(row=crow, column=2,padx=2, pady=12) 
        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=3,padx=2,pady=12)        

###############################################################################

    def read_data(self):            
        """
        a = frequency column
        b = PSD column
        num = number of coordinates
        slope = slope between coordinate pairs    
        """
        
        print (" ")
        print (" The input file must have two columns: freq(Hz) & psd(unit^2/Hz)")

        a,b,num =read_two_columns_from_dialog('Select Input File',self.master)

        print ("\n samples = %d " % num)

        a=array(a)
        b=array(b)
        
        if(a[0]<1.0e-20 or b[0]<1.0e-20):
            a = delete(a, 0)
            b = delete(b, 0)  
            num=num-1
    

        self.nm1=num-1
        self.num=num
        self.a=a
        self.b=b        

        self.s1=(self.aur.get())  
        
        na=1+int(self.Lb1.curselection()[0])
        if(na==1):
            self.out1="Accel (%s^2/Hz)" %self.s1        
        
        if(na==2):
            self.out1="Vel (%s^2/Hz)" %self.s1     
            
        if(na==3):
            self.out1="Disp (%s^2/Hz)" %self.s1     
        
        if(na==4):
            self.out1="Force (%s^2/Hz)" %self.s1            
        
        if(na==5):
            self.out1="Pressure (%s^2/Hz)" %self.s1      
            
        if(na==6):
            self.out1="PSD (%s^2/Hz)" %self.s1                  


###############################################################################

        slope =zeros(self.nm1,'f')

        ra=0

        for i in range (0,int(self.nm1)):
#
            s=log(self.b[i+1]/self.b[i])/log(self.a[i+1]/self.a[i])
        
            slope[i]=s
#
            if s < -1.0001 or s > -0.9999:
                ra+= ( self.b[i+1] * self.a[i+1]- self.b[i]*self.a[i])/( s+1.)
            else:
                ra+= self.b[i]*self.a[i]*log( self.a[i+1]/self.a[i])
                
        rms=sqrt(ra)        

       
        plt.ion()
        plt.clf()   
        
        plt.figure(self.fig_num)     
        self.fig_num+=1
        plt.plot(self.a,self.b)
        title_string='Power Spectral Density   '+str("%6.3g %s" %(rms,self.s1))+' RMS Overall '
        plt.title(title_string)
        plt.ylabel(self.out1)   
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')

        if (self.f1r.get() and self.f2r.get()):
            f1=float(self.f1r.get())
            f2=float(self.f2r.get()) 
            plt.xlim([f1,f2])


        plt.show()    

        self.button_calculate.config(state = 'normal')        
        self.convert_octave_band(self)        
        
###############################################################################
        
    def calculate(self):             
        self.convert_octave_band(self)

###############################################################################

    @classmethod  
    def convert_octave_band(cls,self):


        nb=int(self.Lb2.curselection()[0])
        
        print(nb)

        fl,fc,fu=vb_psd_octave.octave_bands(nb)

        num_fc=len(fc)   
 
 #       print("\n ref 2 \n")
       
 #       for i in range(0,num_fc):
 #           print('%g %g %g' %(fl[i],fc[i],fu[i]))

###############################################################################
        
     
        
        print(' ')
        print('  counts...')
        
        ssum=zeros(num_fc,'f')
        count=zeros(num_fc,'f')
              
        
        
        self.ossum=[]
        self.ff=[]

        for k in range(0,self.num):
        
            for i in range(0,num_fc):
		
                if( self.a[k]>= fl[i] and self.a[k] < fu[i]):

        	         ssum[i]=ssum[i] + self.b[k]
		         count[i]=count[i] + 1.

###############################################################################

#        print("\n ref 4 \n")
       
#        for i in range(0,num_fc):
#            print('%8.4g %8.4g %8.4g' %(fc[i],ssum[i],count[i]))
            
            

        
        for i in range (0,num_fc-1):
	
            iflag=0
        
            if( fl[i] > self.a[self.num-1]):
		     break
		
            if(iflag==0):
               if(count[i]>=1. and count[i+1]>=2.):
                   iflag=1
            

            if(iflag==1 and ssum[i] > 1.0e-20): 
                self.ossum.append(ssum[i]/count[i])
                self.ff.append(fc[i])
 
 

        self.ff=array(self.ff)
        self.ossum=array(self.ossum)


#        print("\n ref 5 \n")
       
#        for i in range(0,len(self.ff)):
#            print('%8.4g %8.4g' %(self.ff[i],self.ossum[i]))
            


        rb=0

        for i in range (0,len(self.ff)-1):
#
            s=log(self.ossum[i+1]/self.ossum[i])/log(self.ff[i+1]/self.ff[i])

#
            if s < -1.0001 or s > -0.9999:
                rb+= ( self.ossum[i+1] * self.ff[i+1]- self.ossum[i]*self.ff[i])/( s+1.)
            else:
                rb+= self.ossum[i]*self.ff[i]*log( self.ff[i+1]/self.ff[i])
                
        rms2=sqrt(rb)     


        self.button_save.config(state = 'normal')

###############################################################################

        print (" ")
        print (" view plots ")
    
        
###############################################################################

        plt.figure(self.fig_num)
        self.fig_num=self.fig_num+1
        plt.plot(self.ff,self.ossum)

        if(nb==0):        
            title_string='Full Octave PSD '+str("%6.3g %s" %(rms2,self.s1))+' RMS Overall '
        if(nb==1):        
            title_string='One-Third Octave PSD '+str("%6.3g %s" %(rms2,self.s1))+' RMS Overall '
        if(nb==2):        
            title_string='One-Sixth Octave PSD '+str("%6.3g %s" %(rms2,self.s1))+' RMS Overall '
        if(nb==3):        
            title_string='One-Twelfth Octave PSD '+str("%6.3g %s" %(rms2,self.s1))+' RMS Overall '            

        plt.title(title_string)
        plt.ylabel(self.out1)   
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('octave_power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')

        if (self.f1r.get() and self.f2r.get()):
            f1=float(self.f1r.get())
            f2=float(self.f2r.get()) 
            plt.xlim([f1,f2])

        plt.show()                
        
        
###############################################################################

    @classmethod    
    def octave_bands(cls,nb):

        if(nb==0):  # 1
        	oex=1./2.
        if(nb==1):  # 1/3
		oex=1./6.        
        if(nb==2):  # 1/6
		oex=1./12.
        if(nb==3):  # 1/12        
		oex=1./24.

        fc = array([])

        if(nb==0):
            fc = append(fc, 2.)
            fc = append(fc, 4.)
            fc = append(fc, 8.)
            fc = append(fc, 16.)
            fc = append(fc, 31.5)
            fc = append(fc, 63.)
            fc = append(fc, 125.)
            fc = append(fc, 250.)
            fc = append(fc, 500.)
            fc = append(fc, 1000.)       
            fc = append(fc, 2000.)   
            fc = append(fc, 4000.)   
            fc = append(fc, 8000.)   
            fc = append(fc, 16000.)               
          
        if(nb>=1):
            fc = append(fc, 2.5)
            fc = append(fc, 3.15)
            fc = append(fc, 4.)
            fc = append(fc, 5.)
            fc = append(fc, 6.3)
            fc = append(fc, 8.)
            fc = append(fc, 10.)
            fc = append(fc, 12.5)
            fc = append(fc, 16.)
            fc = append(fc, 20.)       
            fc = append(fc, 25.)   
            fc = append(fc, 31.5)   
            fc = append(fc, 40.)   
            fc = append(fc, 50.)  
            fc = append(fc, 63.)
            fc = append(fc, 80.)
            fc = append(fc, 100.)
            fc = append(fc, 125.)
            fc = append(fc, 160.)
            fc = append(fc, 200.)
            fc = append(fc, 250.)
            fc = append(fc, 315.)
            fc = append(fc, 400.)
            fc = append(fc, 500.)       
            fc = append(fc, 630.)   
            fc = append(fc, 800.)   
            fc = append(fc, 1000.)   
            fc = append(fc, 1250.)  
            fc = append(fc, 1600.)
            fc = append(fc, 2000.)
            fc = append(fc, 2500.)
            fc = append(fc, 3150.)
            fc = append(fc, 4000.)
            fc = append(fc, 5000.)
            fc = append(fc, 6300.)
            fc = append(fc, 8000.)
            fc = append(fc, 10000.)
            fc = append(fc, 12500.)       
            fc = append(fc, 16000.)   
            fc = append(fc, 20000.)   
            
    
            
        if(nb>=2):       
          
          
            fcc = []
          
            n=len(fc)
            
            for i in range(1,n):
                fcc.append(fc[i-1])
                a=sqrt(fc[i-1]*fc[i])
                fcc.append(a)

          
            fcc.append(fc[n-1])
          
          
        if(nb==3):       
          
            fccc = []
          
            n=len(fcc)
            
            for i in range(1,n):
                fccc.append(fcc[i-1])
                a=sqrt(fcc[i-1]*fcc[i])
                fccc.append(a)          

            fccc.append(fcc[n-1])
###          
          
        if(nb<=1):
            freq=fc
 
        if(nb==2):
            freq=array(fcc)
            
        if(nb==3):
            freq=array(fccc)       
            

        fl=[]
        fu=[]             
        
        n=len(freq)

        for i in range(0,n):
            
		fl.append(freq[i]/(2.**oex))

     
        for i in range(0,n-1):
  
		fu.append(fl[i+1])	
      
        fu.append(freq[n-1]*(2.**oex))


        fl=array(fl)
        fu=array(fu)


#        for i in range(0,n):            
#            print(" %8.4g %8.4g %8.4g " %(fl[i],freq[i],fu[i]))
            
        return fl,freq,fu        
        
    
###############################################################################
            
    def export_psd(self):
        output_file_path = asksaveasfilename(parent=self.master,title="Enter the PSD filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2(len(self.ff),self.ff,self.ossum,output_file)
            
###############################################################################
    
def WriteData2(nn,aa,bb,output_file_path):
    """
    Write two columns of data to an external ASCII text file
    """
    output_file = output_file_path.rstrip('\n')
    outfile = open(output_file,"w")
    for i in range (0, int(nn)):
        outfile.write(' %10.6e \t %8.4e \n' %  (aa[i],bb[i]))
    outfile.close()   
          
def quit(root):
    root.destroy()
                       
###############################################################################