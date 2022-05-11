################################################################################
# program: vb__Shepard_Tone__gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.0
# date: July 8, 2014
# description:  Generate sine tone
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
    import tkMessageBox
    import ttk    
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    import tkinter.messagebox as tkMessageBox
    import tkinter.ttk as ttk 


from numpy import sin,cos,log,zeros,max,abs,int16

from math import pi

from time import sleep

from vb_utilities import WriteData2

from scipy.io.wavfile import write

import platform

from matplotlib.gridspec import GridSpec


class vb_Shepard_Tone:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.25))
        h = int(2.*(h*0.25))
        self.master.geometry("%dx%d+0+0" % (w, h))   

        self.master.title("vb_Shepard_Tone_gui.py ver 1.0  by Tom Irvine")         
                
        self.TT=[]
        self.a =[]    
        self.np=0                
                
 
        crow=0  
 
        self.hwtext1=tk.Label(top,text='Generate Shepard Tone')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=10,sticky=tk.SW)


        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='Sample Rate')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.S)
        
        self.hwtext2=tk.Label(top,text='Number of Tones')
        self.hwtext2.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.S)
  
        self.hwtext3=tk.Label(top,text='Duration (sec)')
        self.hwtext3.grid(row=crow, column=2, columnspan=1, pady=10,sticky=tk.S)
               

        crow=crow+1
        
        self.Lbsr = tk.Listbox(top,height=5,width=10,exportselection=0)
        self.Lbsr.insert(1, "22050")        
        self.Lbsr.insert(2, "44100")          
        self.Lbsr.grid(row=crow, column=0, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lbsr.select_set(0)     
        
        
        self.Lbnt = tk.Listbox(top,height=5,width=8,exportselection=0)
        self.Lbnt.insert(1, "2")        
        self.Lbnt.insert(2, "3")
        self.Lbnt.insert(3, "4")
        self.Lbnt.insert(4, "5")               
        self.Lbnt.grid(row=crow, column=1, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lbnt.select_set(0)        
  

        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 10,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=2,padx=10, pady=1,sticky=tk.N)

###############################################################################

        crow+=1

        self.hwtext9=tk.Label(top,text='Progress')
        self.hwtext9.grid(row=crow, column=0, columnspan=1, pady=8,sticky=tk.E)
        
        self.pbar = ttk.Progressbar(top, orient='horizontal', mode='determinate')   
        self.pbar.grid(row=crow, column=1,columnspan=2, padx=5, pady=1,sticky=tk.W)

###############################################################################

        crow+=1 

        self.s=tk.StringVar()
        self.hwtext5=tk.Label(top,textvariable=self.s)
        self.hwtext5.grid(row=crow, column=0, columnspan=3, pady=5)        
        
###############################################################################        
        
        crow=crow+1
        
        self.button_calculate = tk.Button(top, text="Generate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 14)
        self.button_calculate.grid(row=crow, column=0,columnspan=1, padx=10,pady=20) 
        
        
        self.button_ex_txt = tk.Button(top, text="Export Time History File", command=self.export_txt)
        self.button_ex_txt.config( height = 2, width = 24,state = 'disabled' )
        self.button_ex_txt.grid(row=crow, column=1,columnspan=2, padx=10,pady=3)         
        
        
        self.button_ex_wav = tk.Button(top, text="Export Wav File", command=self.export_wav)
        self.button_ex_wav.config( height = 2, width = 20,state = 'disabled' )
        self.button_ex_wav.grid(row=crow, column=3,columnspan=1, padx=10,pady=3) 
        
        self.button_play = tk.Button(top, text="Play Wav File", command=self.play_wav)
        self.button_play.config( height = 2, width = 18,state = 'disabled' )
        self.button_play.grid(row=crow, column=4,columnspan=1, padx=10,pady=3)         
        
        
        root=self.master        
        
        crow=crow+1       
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))

        self.button_quit.config( height = 2, width = 12 )
        self.button_quit.grid(row=crow, column=2,columnspan=1, padx=10,pady=20)

###############################################################################

    def calculation(self):     
        
        dur=float(self.durr.get())

        nsr=int(self.Lbsr.curselection()[0])   
        number_tones=2+int(self.Lbnt.curselection()[0])   

        if nsr==1:
            self.sr=22050               
        else: 
            self.sr=44100
         
        dt=1./self.sr
     
        nt=int(self.sr*dur)


        f1 = 27.5                   # starting freq (Hz)
        f2 = (2.**number_tones)*f1  # ending freq (Hz)

        cycles=1

        oct=log(f2/f1)/log(2.)     # number of octaves
        
        ntimes = nt*cycles

        tpi=2.*pi

        rate=oct/dur

        LLL=int(float(ntimes)/25.)

#        print (" ")
#        print (" progress ")
#        print ("0   1   2   3   4   5   6   7   8   9   10")


        self.pbar['value'] = 0
        self.pbar['maximum'] = ntimes


        self.a=zeros(nt,'f')
        self.arg=zeros(nt,'f') 
        self.freq=zeros(nt,'f')        
        self.TT=zeros(nt,'f')
           
        arg=zeros(number_tones,'f')
        key=zeros(number_tones,'f')
        noc=zeros(number_tones,'f')
        amp=zeros(number_tones,'f')          


        for i in range (0,number_tones):
            noc[i]=2**(i-1)

        fspan=f2-f1
        theta_coefficient=tpi/(rate*log(2.))


        for i in range (0,ntimes):

            t=i*dt
            self.TT[i]=t

            
        ijk=0            
            
        for i in range (0,ntimes):            
              
            ijk+=1              
              
            if(ijk==LLL):
#                stdout.write("*")
                ijk=0
                self.pbar['value'] = i
                self.pbar.update()  #this works
                sleep(0.1)
                self.pbar.update_idletasks()
            
            
            W=-1.+2**(rate*self.TT[i])

            arg[0]=f1*W

            for j in range (0,number_tones):
                if(key[j]==0):
                    arg[j]=arg[0]*noc[j]       
                else:
                    W=-1.+2**(rate*self.TT[i-key[j]])
                    arg[j]=f1*W    
         
    
            for j in range (0,number_tones):
                fspectral=noc[j]*f1*(2**(rate*self.TT[i-key[j]]))
                delta=(fspectral-f1)/fspan
                amp[j]=(1-cos(tpi*delta))

                if(fspectral>f2):
                    key[j]=i
                    noc[j]=1
        
            theta=theta_coefficient*arg

            self.a[i]=sum(amp*sin(theta))

        self.a[0]=0.



        maxdata=max(abs(self.a))

        data=self.a/maxdata

        self.scaled = int16(data * 32767)
        
        self.a=self.scaled
        self.np=ntimes
        

        self.button_ex_txt.config(state = 'normal' )
        self.button_ex_wav.config(state = 'normal' )
       
        tkMessageBox.showwarning("Note", "Generation Complete",parent=self.button_calculate)        
        

    def export_txt(self):
        output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n')     
        WriteData2(self.np,self.TT,self.a,output_file)


    def export_wav(self):
        output_file_path = asksaveasfilename(parent=self.master,title="Enter the wav filename: ",filetypes=[("wav files","*.wav")])           
        self.output_file = output_file_path.rstrip('\n')
        write(self.output_file, self.sr, self.scaled)
        self.button_play.config(state = 'normal' ) 


    def play_wav(self):
       
        if platform.system() == 'Windows':
            import winsound
            winsound.PlaySound(self.output_file, winsound.SND_FILENAME)
    
        if platform.system() == 'Linux':

# Install python-pygame from the Ubuntu Software Center
            import pygame,time
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
            print ("Mixer settings", pygame.mixer.get_init())
            print ("Mixer channels", pygame.mixer.get_num_channels())
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play(0)
            while pygame.mixer.music.get_busy():
                pass
            time.sleep(1) 
   
    



def quit(root):
    root.destroy()        