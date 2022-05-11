################################################################################
# program: vb_waterfall_fft_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 2.1
# date: July 23, 2014
# description:  Waterfall FFT
#
################################################################################
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

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename     


import numpy as np

import matplotlib.pyplot as plt

from scipy.fftpack import fft
from vb_utilities import sample_rate_check,read_two_columns_from_dialog


class vb_waterfall_FFT:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
##        self.master.minsize(900,800)
##        self.master.geometry("900x800")
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.26))
        h = int(2.*(h*0.33))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        
        self.master.title("vb_waterfall_fft_gui.py ver 2.1  by Tom Irvine")         
                
        self.sr=0
        self.dt=0
        self.b=[]
        self.a=[]
        
        self.num=0
        
        self.clear_arrays(self)
        

################################################################################        
        
        crow=0

        self.hwtext1=tk.Label(top,text='Waterfall FFT')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.hwtext2=tk.Label(top,text='The input file must have two columns:  time(sec) & amplitude')
        self.hwtext2.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

################################################################################

        crow=crow+1

        self.hwtext3=tk.Label(top,text='Enter Time History Y-axis Label')
        self.hwtext3.grid(row=crow, column=0, pady=7,sticky=tk.E)

        self.y_string=tk.StringVar()  
        self.y_string.set('')  
        self.y_string_entry=tk.Entry(top, width = 26,textvariable=self.y_string)
        self.y_string_entry.grid(row=crow, column=1,columnspan=3,padx=0, pady=7,sticky=tk.W)

################################################################################

        crow=crow+1

        self.hwtext3b=tk.Label(top,text='Select Duration')
        self.hwtext3b.grid(row=crow, column=1, columnspan=1, pady=7,sticky=tk.S)

        self.hwtextt1=tk.Label(top,text='Start Time (sec)')
        self.hwtextt1.grid(row=crow, column=2,padx=3, pady=12)
        
        self.hwtextt2=tk.Label(top,text='End Time (sec)')
        self.hwtextt2.grid(row=crow, column=3,padx=0, pady=12)    
        
################################################################################

        crow=crow+1        
        
        self.button_read = tk.Button(top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,sticky=tk.W)
        
        self.Lb_ws = tk.Listbox(top,height=2,exportselection=0)
        self.Lb_ws.insert(1, "Whole Time History")
        self.Lb_ws.insert(2, "Segment")
        self.Lb_ws.grid(row=crow, column=1,padx=10,sticky=tk.N)
        self.Lb_ws.select_set(0)
        
        self.Lb_ws.bind('<<ListboxSelect>>',self.time_option)
        

        self.tmir=tk.StringVar()  
        self.tmir.set('')  
        self.tmi_entry=tk.Entry(top, width = 8,textvariable=self.tmir,state = 'disabled')
        self.tmi_entry.grid(row=crow, column=2,padx=3, pady=5,sticky=tk.N)
        self.tmi_entry.bind("<KeyPress>", self.OnKeyPress)
 
 
        self.tmer=tk.StringVar()  
        self.tmer.set('')         
        self.tme_entry=tk.Entry(top, width = 8,textvariable=self.tmer,state = 'disabled')
        self.tme_entry.grid(row=crow, column=3,padx=0, pady=5,sticky=tk.N)       
        self.tme_entry.bind("<KeyPress>", self.OnKeyPress)

################################################################################
        
        crow=crow+1

        self.hwtextf1=tk.Label(top,text='Min Freq (Hz)')
        self.hwtextf1.grid(row=crow, column=1,padx=8, pady=9,sticky=tk.S)

        self.hwtextf2=tk.Label(top,text='Max Freq (Hz)')
        self.hwtextf2.grid(row=crow, column=2,padx=1, pady=9,sticky=tk.S)

################################################################################

        crow=crow+1
        
        self.button_process = tk.Button(top, text="Show Processing Options",command=self.processing_options)
        self.button_process.config( height = 2, width = 25,state = 'disabled')
        self.button_process.grid(row=crow, column=0, padx=5, pady=1,sticky=tk.N) 
 
        self.f1r=tk.StringVar()  
        self.f1r.set('')  
        self.f1_entry=tk.Entry(top, width = 8,textvariable=self.f1r)
        self.f1_entry.grid(row=crow, column=1,padx=8, pady=1,sticky=tk.N)

        self.f2r=tk.StringVar()  
        self.f2r.set('')  
        self.f2_entry=tk.Entry(top, width = 8,textvariable=self.f2r)
        self.f2_entry.grid(row=crow, column=2,padx=1, pady=1,sticky=tk.N)
        
################################################################################   
        
        crow=crow+1
        
        self.hwtexto=tk.Label(top,text='Select Overlap')
        self.hwtexto.grid(row=crow, column=2, columnspan=1,padx=10, pady=3,sticky=tk.S)           

################################################################################

        crow=crow+1
        
        myframe=tk.Frame(top)
        myframe.grid(row=crow, column=0,columnspan=2,padx=3)
        scrollbar = tk.Scrollbar(myframe) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Lba = tk.Listbox(myframe, width=50, yscrollcommand=scrollbar.set) 
        self.Lba.pack()
        scrollbar.config(command=self.Lba.yview)
        
        self.Lb_over = tk.Listbox(top,height=2,exportselection=0)
        self.Lb_over.insert(1, "None")
        self.Lb_over.insert(2, "50%")
        self.Lb_over.grid(row=crow, column=2,padx=10, pady=2,sticky=tk.N)
        self.Lb_over.select_set(0) 
                
################################################################################

        crow=crow+1  

        self.button_calculate = tk.Button(top, text="Calculate", command=self.waterfall_FFT_calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=0, pady=15,sticky=tk.S) 
        
        root=self.master  
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=1, padx=10,pady=15,sticky=tk.S)

################################################################################

    def OnKeyPress(self,event):
        self.button_calculate.config(state = 'disabled')  
        self.Lba.delete(0, tk.END) # clear        

################################################################################

    def processing_options(self):
        
        self.button_calculate.config(state = 'normal')          
        self.advise(self)         

################################################################################

    def time_option(self,val):
        sender=val.widget
        n= int(sender.curselection()[0])
        
        if(n==0):
            self.tme_entry.config(state = 'disabled')         
            self.tmi_entry.config(state = 'disabled')             
        else:
            self.tme_entry.config(state = 'normal')         
            self.tmi_entry.config(state = 'normal')  
             
            
################################################################################
            
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
        plt.ylabel(self.y_string.get())  
        plt.title('Time History')
    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.button_process.config(state = 'normal')   
                   
        out1=str('%8.4g' %self.a[0])
        out2=str('%8.4g' %self.a[self.num-1])
        
        self.tmir.set(out1) 
        self.tmer.set(out2)         
        
        
    @classmethod      
    def advise(cls,self):
        
        tmi=float(self.tmir.get()) 
        tme=float(self.tmer.get()) 
        
        self.aa=[]
        self.bb=[]
        
        k=0
        for i in range(0,int(self.num)):
            if(self.a[i]>=tmi and self.a[i]<=tme): 
                self.aa.append(self.a[i])
                self.bb.append(self.b[i])                
                k=k+1
                

        self.aa=np.array(self.aa)
        self.bb=np.array(self.bb)      

        
        self.num=k
        n=len(self.bb)
        
        NC=0
        
        for i in range(0,1000):
    
            nmp = 2**i
   
            if(nmp <= n ):
                self.ss.append(2**i)
                self.seg.append(np.round(n/self.ss[i]))
                self.i_seg.append(np.floor(self.seg[i]))
                tseg=self.dt*self.ss[i]
                self.ddf.append(1./tseg)                
                NC=NC+1
            else:
                break


        t_ss= self.ss[NC+1:0:-1]
        t_seg= self.seg[NC+1:0:-1]
        t_i_seg= self.i_seg[NC+1:0:-1]        
        t_ddf= self.ddf[NC+1:0:-1]          
        
        k=0
        
        
        for i in range(0,int(NC)):
            if( t_seg[i]>0 ):
                out1='seg= %d, sps=%d,  df=%6.3g Hz,  sdof=%d' \
                                       %(t_i_seg[i],t_ss[i],t_ddf[i],2*t_i_seg[i])
                self.Lba.insert(i, out1)

                self.r_ss.append(t_ss[i])
                self.r_seg.append(t_ddf[i])
                self.r_i_seg.append(t_i_seg[i])        
                self.r_ddf.append(t_ddf[i]) 

                k=k+1
                    
            if(i==12):
                break

        self.Lba.select_set(0) 
        
################################################################################

    @classmethod 
    def clear_arrays(cls,self):  

        self.aa=[]
        self.bb=[]
        
        self.ss=[]
        self.seg=[]
        self.i_seg=[]
        self.ddf=[]       
        
        
        self.r_ss=[]
        self.r_seg=[]
        self.r_i_seg=[]
        self.r_ddf=[]         
        
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

        
################################################################################        
        
    def waterfall_FFT_calculation(self):       
       
        s1=self.f1r.get()
        s2=self.f2r.get()
       
        
        if len(s1) == 0:  # empty!
            self.f1r.set('0')                           
            minf=0        
        else:
            minf=float(s1)
            
        if len(s2) == 0:  # empty!
            nyq=self.sr/2.  
            snq=('%8.4g' %nyq)
            self.f2r.set(snq)                           
            maxf=nyq        
        else:
            maxf=float(s2)            
            
            
        
        tmi=float(self.tmir.get()) 
        tme=float(self.tmer.get())         

        if tmi<self.aa[0]:
            tmi=self.aa[0]

#        tme=float(self.tmer.get()) 


        dtmin=1e+50
        dtmax=0

        for i in range(1, int(self.num-1)):
            if (self.aa[i]-self.aa[i-1])<dtmin:
                dtmin=self.aa[i]-self.aa[i-1];
            if (self.aa[i]-self.aa[i-1])>dtmax:
                dtmax=self.aa[i]-self.aa[i-1];

        print ("  dtmin = %8.4g sec" % dtmin)
        print ("     dt = %8.4g sec" % self.dt)
        print ("  dtmax = %8.4g sec \n" % dtmax)

        print ("  srmax = %8.4g samples/sec" % float(1/dtmin))
        print ("     sr = %8.4g samples/sec" % self.sr)
        print ("  srmin = %8.4g samples/sec" % float(1/dtmax))
        
        FL=0.98*self.sr/2.        
        
        if(maxf>FL):
            maxf=FL

        self.aa=np.array(self.aa)
        self.bb=np.array(self.bb)

        self.bb-=sum(self.bb)/len(self.bb)  # demean
        

        n= int(self.Lba.curselection()[0]) 
        
#        print (n)
                

        self.NW=self.r_i_seg[n]
#        self.mmm = 2**int(np.log(float(self.num)/float(self.NW))/np.log(2))
 
        self.mmm= self.r_ss[n]
       
        self.md2=self.mmm/2
        

#        print (self.r_ddf[n])
        
        self.df=1./(self.mmm*self.dt)
        self.mH=((self.mmm/2)-1)
 
        io=int(self.Lb_over.curselection()[0]) 

        freq=np.zeros(self.md2,'f')

        for i in range (0,int(self.md2)): 
            freq[i]=i*self.df
            if freq[i]>maxf:
                break

        self.mk=i

        t1=tmi+(self.dt*self.mmm)

        if io==0:
            time_a=np.zeros(self.NW,'f')
            time_a[0]=t1
    
            for i in range(1,int(self.NW)):
                time_a[i]=time_a[i-1]+self.dt*self.mmm
    
        else:
            self.NW=2*self.NW-1
            time_a=np.zeros(self.NW,'f')
            time_a[0]=t1     
            self.dt=self.dt/2
            for i in range(1,int(self.NW)):
                time_a[i]=time_a[i-1]+self.dt*self.mmm
  
################################################################################                
#
#   waterfall_FFT_core
#

        freq_p=[]

        for k in range(0,int(self.mk)):
                          
            if freq[k]>=minf and freq[k]<=maxf:
                freq_p.append(freq[k])

        freq_p=np.array(freq_p)
        
        nfreq=len(freq_p)
        
        last_freq=nfreq-1        
        
        self.mk=nfreq
        

###############################################################################
        
        LF=len(freq)        
        
        store=np.zeros((self.NW,LF),'f')
        store_p=np.zeros((self.NW,self.mk),'f')    
    
        
        jk=0
        
#        print(' mmm=%d  NW=%d  len(bb)=%d   ' %(self.mmm,self.NW,len(self.bb)))
    
        for ij in range(0,int(self.NW)):

            sa=np.zeros(self.mmm,'f')
            

            if io==0:   
                for k in range(0,int(self.mmm)):
#                    print (" %d %d %d" %(self.mmm,len(self.b),jk)                    
                    sa[k]=self.bb[jk]
                    jk=jk+1
            
            else:
                for k in range(0,int(self.mmm)):
                    sa[k]=self.bb[jk]
                    jk=jk+1
            
                jk=jk-self.mmm/2
        

            Y= fft(sa,self.mmm)
        

            j=0
            
#            print(' mk=%d ' %self.mk)            
            
            for k in range(0,LF):
            
#                ym= 2.*abs(Y[k])/self.mmm        
            
                if k==0:
                    store[ij][k] = abs(Y[0])/self.mmm           
                else:    
                    store[ij][k] =2.*abs(Y[k])/self.mmm    
            
                if freq[k]>maxf:
                    break
            
                if freq[k]>=minf and freq[k]<=maxf and j<self.mk:
#                    print('j=%d k=%d LF=%d ij=%d' %(j,k,LF,ij))
                    store_p[ij][j]=store[ij][k]
#                    print('%8.4g %8.4g' %(freq[k],store_p[ij][j]))
                
                    last_freq=j    
                    j=j+1
                
        self.mk=last_freq+1
    

        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        from matplotlib.colors import colorConverter

        plt.close(2)
        fig = plt.figure(2)
        ax = fig.gca(projection='3d')

#        cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)

        verts = []

        ys=np.zeros(self.mk,'f')
        zs=np.zeros(self.mk,'f')

        maxz=0

        for i in range(0,int(self.NW)):
            for j in range(0,int(self.mk)):
                zs[j] = store_p[i][j]
        
                if zs[j]>maxz:
                    maxz=zs[j]
        
            for j in range(0,int(self.mk)):        
                ys[j]=time_a[i]
      

            zs[0]=0
            zs[int(self.mk)-1]=0
      
            verts.append(list(zip(freq_p, ys, zs)))

        ax.add_collection3d(Poly3DCollection(verts, facecolors = 'r'))

        ax.view_init(elev=45, azim=-100)

        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Time (sec)')
        ax.set_zlabel('Magnitude')

        if(minf<=5):
            minf=0
        
        ax.set_xlim3d(minf, maxf)
        
        ax.set_ylim3d(tmi,tme)        

        ax.set_zlim3d(0, maxz)
        
################################################################################

        from matplotlib import cm  
        from numpy import meshgrid  
       
        plt.close(3)       
        fig=plt.figure(3)

        X,Y = meshgrid(freq_p,time_a)

        ax = fig.gca(projection='3d')
        
        surf = ax.plot_surface(X, Y, store_p, rstride=1, cstride=1, cmap=cm.jet,
            linewidth=0, antialiased=False)

#        ax.set_xlim3d(minf, maxf)
        ax.set_zlim3d(0, maxz)

        ax.view_init(elev=45, azim=-100)

        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Time (sec)')
        ax.set_zlabel('Magnitude ')
        
################################################################################        

        plt.close(4)
        fig=plt.figure(4)

        X,Y = meshgrid(freq_p,time_a)

        ax = fig.gca(projection='3d')
        
        surf = ax.plot_surface(X, Y, store_p, rstride=1, cstride=1, cmap=cm.jet,
            linewidth=0, antialiased=False)

#        ax.set_xlim3d(minf, maxf)
      

        ax.set_zlim3d(0, maxz)
        
        ax.set_zticks((0, maxz))
        ax.set_zticklabels((' ',' '))                  

        ax.view_init(elev=89.9, azim=-90.1)

        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Time (sec)')

################################################################################

        self.clear_arrays(self)
        
        self.Lba.delete(0, tk.END)
        
        self.button_calculate.config(state = 'disabled')
            
################################################################################

        print ('View Plots')
        print ('Manually resize 3D plots. ')
        print ('Change view azimuth and elevation as desired.') 
        print (' ')
        print ('Then save image. ')
        print (' ')
        print ('Call *.png image into image editor to crop.')

        plt.show()     
                                               
################################################################################
       
       
def quit(root):
    root.destroy()
     