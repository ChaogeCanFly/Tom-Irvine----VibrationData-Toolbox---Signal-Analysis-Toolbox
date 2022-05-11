################################################################################
# program: vb_sine_tone_gui.py
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
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    import tkinter.messagebox as tkMessageBox


from numpy import sin,linspace,zeros,max,abs,int16

from math import pi


from vb_utilities import WriteData2

from scipy.io.wavfile import write

import platform


class vb_sine_tone:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.24))
        h = int(2.*(h*0.20))
        self.master.geometry("%dx%d+0+0" % (w, h))
        
        self.master.title("vb_sine_tone_gui.py ver 1.0  by Tom Irvine")         
                
        self.TT=[]
        self.a =[]    
        self.np=0                
                
 
        crow=0  
 
        self.hwtext1=tk.Label(top,text='Generate Sine Tone')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=10,sticky=tk.SW)


        crow=crow+1
        
        self.hwtext2=tk.Label(top,text='Frequency (Hz)')
        self.hwtext2.grid(row=crow, column=0, columnspan=1, pady=10,sticky=tk.SW)
        
        self.hwtext2=tk.Label(top,text='Duration (sec)')
        self.hwtext2.grid(row=crow, column=1, columnspan=1, pady=10,sticky=tk.SW)
                 

        crow=crow+1

        self.freqr=tk.StringVar()  
        self.freqr.set('')  
        self.freq_entry=tk.Entry(top, width = 10,textvariable=self.freqr)
        self.freq_entry.grid(row=crow, column=0,padx=10, pady=1,sticky=tk.NW)      

        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 10,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=1,padx=10, pady=1,sticky=tk.NW)

  
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
        
        freq=float(self.freqr.get())
        dur=float(self.durr.get())

        self.sr=44100

        dt=1./self.sr
     
        nt=int(self.sr*dur)

        data=zeros(nt,'f')
        self.a=zeros(nt,'f')        
        self.TT=zeros(nt,'f')
           
        omega=2.*pi*freq

        for i in range (0,nt):
            t=i*dt
            self.TT[i]=t
            data[i]=sin(omega*t)

        maxdata=max(abs(data))

        data=data/maxdata

        self.scaled = int16(data * 32767)
        
        self.a=self.scaled
        self.np=nt
        

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