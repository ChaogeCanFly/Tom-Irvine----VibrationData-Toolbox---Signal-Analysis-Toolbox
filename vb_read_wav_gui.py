################################################################################
# program: vb_read_wav_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.0
# date: July 17, 2014
# description:  Read, play & export wav file
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
import platform
import os

import numpy as np
import matplotlib.pyplot as plt


if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename,askopenfilename    
    import tkMessageBox
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename,askopenfilename     
    import tkinter.messagebox as tkMessageBox


from vb_utilities import WriteData2
from scipy.io.wavfile import read

###############################################################################

def normalize_demean(v):
    
    v=np.array(v)

    n=len(v) 

    av=float(np.mean(v))

    w=np.zeros(n,'f')    
    
    w=v-av 
        
    norm=float(max(abs(w)))    
        
    return w/norm
        


class vb_read_wav:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        self.top = tk.Frame(parent)    # frame for all class widgets
        self.top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.16))
        h = int(2.*(h*0.19))
        self.master.geometry("%dx%d+0+0" % (w, h))   

        self.master.title("vb_read_wav_gui.py ver 1.0  by Tom Irvine")         
                
        crow=0        
        
        self.button_read = tk.Button(self.top, text="Read wav File", command=self.read_wav)
        self.button_read.config( height = 2, width = 16 )
        self.button_read.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.N)  

        crow=crow+1  

        self.button_play = tk.Button(self.top, text="Play wav File", command=self.play_wav)
        self.button_play.config( height = 2, width = 16,state = 'disabled' )
        self.button_play.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.N)  

        crow=crow+1  

        self.button_export = tk.Button(self.top, text="Export Text File", command=self.export_txt)
        self.button_export.config( height = 2, width = 16,state = 'disabled' )
        self.button_export.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.N)  

      
        crow=crow+1  

        self.button_calculate_FFT = tk.Button(self.top, text="Calculate FFT", command=self.calculate_FFT)
        self.button_calculate_FFT.config( height = 2, width = 16,state = 'disabled' )
        self.button_calculate_FFT.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.N)  
        
        
      
        root=self.master        
        
        crow=crow+1       
        
        self.button_quit=tk.Button(self.top, text="Quit", command=lambda root=root:quit(root))

        self.button_quit.config( height = 2, width = 16 )
        self.button_quit.grid(row=crow, column=0,columnspan=1,pady=10)
        
###############################################################################

    def calculate_FFT(self):

        win = tk.Toplevel()

        from vb_fft_gui import vb_FFT        
        vb_FFT(win)        



###############################################################################

    def read_wav(self):
        
        label="Enter the input wav filename: "
        
        input_file_path = askopenfilename(parent=self.master,title=label,filetypes=[("wav files","*.wav")])

        self.file_path = input_file_path.rstrip('\n')

#
        if not os.path.exists(self.file_path):
            print ("This file doesn't exist")
            return
 #
        if os.path.exists(self.file_path):
            self.rate,self.data=read(self.file_path)    

###############################################################################

        self.nad=self.data.ndim
       
        dt=1/float(self.rate)

        if(self.nad==1):
            self.num=self.data.shape[0]
            
        if(self.nad==2):
            self.num=self.data.shape[0]
            self.nr=self.data.shape[1]

        self.t=np.linspace(0,(self.num-1)*dt,self.num)  

        print (' ')
        print ('lines read = %d' %self.num)

        print (' ')
        print ('sample rate = %d' %self.rate)

########

        plt.ion()
        plt.figure(1)
        
        if(self.nad==1):
            
            v=np.zeros(self.num,'f')

            v=self.data.astype(float)
 
            self.dataf=normalize_demean(v)            
            
            plt.plot(self.t, self.dataf, linewidth=1.0)
              
        
        if(self.nad==2):
            
            self.dataf=np.zeros([self.num,2],'f')
            
            v1=np.zeros(self.num,'f')
            v2=np.zeros(self.num,'f') 
            
            v1=self.data[:,0].astype(float)
            v2=self.data[:,1].astype(float)
 
 
            self.dataf[:,0]=normalize_demean(v1)
            self.dataf[:,1]=normalize_demean(v2)
            
            plt.plot(self.t, self.dataf[:,0], linewidth=1.0)
            plt.plot(self.t, self.dataf[:,1], linewidth=1.0)
            
            plt.xlabel('Time (sec)')
            plt.title('Time History')  
            plt.grid(True)
            plt.draw()    
             
        
        self.button_play.config( height = 2, width = 16,state = 'normal' )        
        self.button_export.config( height = 2, width = 16,state = 'normal' )
              
###############################################################################       
              
    def export_txt(self):
        
        if(self.nad==1):
            output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename")           
            output_file = output_file_path.rstrip('\n')              
            WriteData2(self.num,self.t,self.dataf,output_file)
        else:    
            output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename for channel 1")           
            output_file = output_file_path.rstrip('\n')              
            WriteData2(self.num,self.t,self.dataf[:,0],output_file)            
            
            output_file_path = asksaveasfilename(parent=self.master,\
                                    title="Enter the output filename for channel 2")           
            output_file = output_file_path.rstrip('\n')              
            WriteData2(self.num,self.t,self.dataf[:,1],output_file)             

        self.button_calculate_FFT.config( height = 2, width = 16,state = 'normal' )

###############################################################################

    def play_wav(self):
       
        if platform.system() == 'Windows':
            import winsound
            winsound.PlaySound(self.file_path, winsound.SND_FILENAME)
    
        if platform.system() == 'Linux':

# Install python-pygame from the Ubuntu Software Center
            import pygame,time
            pygame.mixer.init(frequency=self.rate, size=-16, channels=self.nad)
            print ("Mixer settings", pygame.mixer.get_init())
            print ("Mixer channels", pygame.mixer.get_num_channels())
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play(0)
            while pygame.mixer.music.get_busy():
                pass
            time.sleep(1) 
   
###############################################################################
    
def quit(root):
    root.destroy()        