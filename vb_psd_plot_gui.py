########################################################################
# program: vb_psd_plot_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.4
# date: August 15, 2014
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
    

from vb_utilities import read_two_columns_from_dialog

from numpy import array,zeros,log,delete,sqrt



import matplotlib.pyplot as plt


###############################################################################

class vb_psd_plot:
    
    def __init__(self,parent):    
        
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window


        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.22))
        h = int(2.*(h*0.22))
        self.master.geometry("%dx%d+0+0" % (w, h))


        self.master.title("vb_psd_plot_gui.py ver 1.4  by Tom Irvine")  


###############################################################################
        
        crow=0
        
        self.hwtext3=tk.Label(top,text='This script calculates the overall level of a PSD.')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)        
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='The input file must have two columns: Freq(Hz) & PSD(unit^2/Hz)')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)
        
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
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=15)

        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1,pady=15)        

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

        

        rms=sqrt(ra)
        three_rms=3*rms
        
        na=1+int(self.Lb1.curselection()[0])
    
        print (" ")
        print (" *** Input PSD *** ")
        print (" ")
 
        print ("   Overall = %10.3g RMS" % rms)
        print ("           = %10.3g 3-sigma" % three_rms)

                
###############################################################################

        print (" ")
        print (" view plot ")
        
        s1=(self.aur.get())  

        plt.ion()
        plt.close(1)
        plt.figure(1)     
        plt.plot(a,b)
        title_string='Power Spectral Density   '+str("%6.3g %s" %(rms,s1))+' RMS Overall '
        plt.title(title_string)
        
        if(na==1):
            out1="Accel (%s^2/Hz)" %s1        
        
        if(na==2):
            out1="Vel (%s^2/Hz)" %s1     
            
        if(na==3):
            out1="Disp (%s^2/Hz)" %s1     
        
        if(na==4):
            out1="Force (%s^2/Hz)" %s1            
        
        if(na==5):
            out1="Pressure (%s^2/Hz)" %s1      
            
        if(na==6):
            out1="PSD (%s^2/Hz)" %s1                  
        
        
        plt.ylabel(out1)
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()

###############################################################################        

        return a,b,rms,num,slope

###############################################################################
              
def quit(root):
    root.destroy()
                       
###############################################################################