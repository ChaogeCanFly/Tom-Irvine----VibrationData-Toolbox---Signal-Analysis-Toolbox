###########################################################################
# program: vb_Doppler_shift_gui.py
# author: Tom Irvine
# version: 1.0
# date: May 23, 2014
# 
###############################################################################

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

###############################################################################

class vb_Doppler_shift:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.22))
        h = int(2.*(h*0.28))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_Doppler_shift_gui.py  ver 1.0  by Tom Irvine")
        
        crow=0
   
        self.hwtext1=tk.Label(top,text='Select Velocity Unit')
        self.hwtext1.grid(row=crow, column=0, padx=4,pady=7)    
      
        
        self.speed_sound_text=tk.StringVar()  
        self.speed_sound_text.set('Speed of Sound (ft/sec)')         
        self.hwtext2=tk.Label(top,textvariable=self.speed_sound_text)
        self.hwtext2.grid(row=crow, column=1, columnspan=1, padx=4, pady=7,sticky=tk.S)           
        
        
   
        crow=crow+1       
        
        self.Lb1 = tk.Listbox(top,height=4,width=28,exportselection=0)
        self.Lb1.insert(1, "ft/sec")
        self.Lb1.insert(2, "mph")
        self.Lb1.insert(3, "m/sec")
        self.Lb1.insert(4, "km/hr")        
        self.Lb1.grid(row=crow, column=0, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lb1.select_set(0)  
        self.Lb1.bind('<<ListboxSelect>>',self.velocity_unit_option)   
   
        self.speed_soundr=tk.StringVar()  
        self.speed_soundr.set('1120')  
        self.speed_sound_entry=tk.Entry(top, width = 8,textvariable=self.speed_soundr)
        self.speed_sound_entry.grid(row=crow, column=1,padx=5, pady=4,sticky=tk.N)               

               
        crow=crow+1          
        
        self.hwtext3=tk.Label(top,text='Calculate')
        self.hwtext3.grid(row=crow, column=0, padx=4,pady=7)    
  

        self.results_text=tk.StringVar()  
        self.results_text.set(' ')         
        self.hwtext5=tk.Label(top,textvariable=self.results_text)
        self.hwtext5.grid(row=crow, column=2, columnspan=2, padx=4, pady=7,sticky=tk.S)            
        

        crow=crow+1  
        
        self.Lb2 = tk.Listbox(top,height=4,width=28,exportselection=0)
        self.Lb2.insert(1, "Apparent Frequency")
        self.Lb2.insert(2, "Source Frequency")
        self.Lb2.insert(3, "Source Velocity")
        self.Lb2.insert(4, "Receiver Velocity")        
        self.Lb2.grid(row=crow, column=0, columnspan=1, padx=10, pady=2,sticky=tk.N)
        self.Lb2.select_set(0)  
        self.Lb2.bind('<<ListboxSelect>>',self.calculate_option) 

        self.resultr=tk.StringVar()  
        self.resultr.set('')  
        self.result_entry=tk.Entry(top, width = 14,textvariable=self.resultr)
        self.result_entry.grid(row=crow, column=2,padx=5, pady=2,sticky=tk.N) 
        self.result_entry.configure(state='readonly')               
               
             
        crow=crow+1               
        
          
        self.source_frequency_text=tk.StringVar()  
        self.source_frequency_text.set(' ')         
        self.hwtext11=tk.Label(top,textvariable=self.source_frequency_text)
        self.hwtext11.grid(row=crow, column=0, columnspan=1, padx=4, pady=7,sticky=tk.S)    
        
        self.apparent_frequency_text=tk.StringVar()  
        self.apparent_frequency_text.set(' ')         
        self.hwtext10=tk.Label(top,textvariable=self.apparent_frequency_text)
        self.hwtext10.grid(row=crow, column=1, columnspan=1, padx=4, pady=7,sticky=tk.S)    

        self.button_go = tk.Button(top, text="Calculate",command=self.analysis_go)
        self.button_go.config( height = 2, width = 15 )
        self.button_go.grid(row=crow, column=2,columnspan=1,padx=12,pady=10)
        
        crow=crow+1
        
        self.source_frequencyr=tk.StringVar()  
        self.source_frequency=tk.Entry(top, width = 8,textvariable=self.source_frequencyr)
        self.source_frequency.grid(row=crow, column=0,padx=5, pady=4,sticky=tk.N) 
        
        self.apparent_frequencyr=tk.StringVar()  
        self.apparent_frequency=tk.Entry(top, width = 8,textvariable=self.apparent_frequencyr)
        self.apparent_frequency.grid(row=crow, column=1,padx=5, pady=4,sticky=tk.N) 
        
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 15 )
        self.button_quit.grid(row=crow, column=2, padx=12,pady=10) 
        

        crow=crow+1

        self.source_velocity_text=tk.StringVar()  
        self.source_velocity_text.set(' ')         
        self.hwtext14=tk.Label(top,textvariable=self.source_velocity_text)
        self.hwtext14.grid(row=crow, column=0, columnspan=1, padx=4, pady=7,sticky=tk.S)    

        self.receiver_velocity_text=tk.StringVar()  
        self.receiver_velocity_text.set(' ')         
        self.hwtext15=tk.Label(top,textvariable=self.receiver_velocity_text)
        self.hwtext15.grid(row=crow, column=1, columnspan=1, padx=4, pady=7,sticky=tk.S)     
        
        crow=crow+1
        
        self.source_velocityr=tk.StringVar()  
        self.source_velocity=tk.Entry(top, width = 8,textvariable=self.source_velocityr)
        self.source_velocity.grid(row=crow, column=0,padx=5, pady=4,sticky=tk.N) 
        
        self.receiver_velocityr=tk.StringVar()  
        self.receiver_velocity=tk.Entry(top, width = 8,textvariable=self.receiver_velocityr)
        self.receiver_velocity.grid(row=crow, column=1,padx=5, pady=4,sticky=tk.N)         
        
        
        self.source_frequency.bind("<Key>", self.callback_clear)
        self.apparent_frequency.bind("<Key>", self.callback_clear) 
        self.source_velocity.bind("<Key>", self.callback_clear)
        self.receiver_velocity.bind("<Key>", self.callback_clear)         
        
        self.change_entry(self)        
        
###############################################################################

    def callback_clear(self,event):
        self.results_text.set(' ')
        self.resultr.set(' ')              
         
    def calculate_option(self,val):
#        sender=val.widget
        
        self.change_entry(self)

  

    @classmethod
    def change_entry(cls,self):      
        n1=int(self.Lb1.curselection()[0])   
        n2=int(self.Lb2.curselection()[0]) 
        
        self.source_frequency_text.set('Source Frequency (Hz)')
        self.apparent_frequency_text.set('Apparent Frequency (Hz)')
        
        self.source_frequency.configure(state='normal')
        self.apparent_frequency.configure(state='normal')
        self.source_velocity.configure(state='normal')
        self.receiver_velocity.configure(state='normal')        


        if(n1==0):
            self.source_velocity_text.set('Source Velocity (ft/sec)')
            self.receiver_velocity_text.set('Receiver Velocity (ft/sec)')
        
        if(n1==1):
            self.source_velocity_text.set('Source Velocity (mph)')
            self.receiver_velocity_text.set('Receiver Velocity (mph)')

        if(n1==2):
            self.source_velocity_text.set('Source Velocity (m/sec)')
            self.receiver_velocity_text.set('Receiver Velocity (m/sec)')

        if(n1==3):
            self.source_velocity_text.set('Source Velocity (km/hr)')
            self.receiver_velocity_text.set('Receiver Velocity (km/hr)')
        
        
        
        
        if(n2==0):  # apparent frequency
            self.apparent_frequency_text.set(' ')        
            self.apparent_frequency.configure(state='disabled')        

        if(n2==1):  # source frequency
            self.source_frequency_text.set(' ')
            self.source_frequency.configure(state='disabled')            
              
        if(n2==2):  # source velocity
            self.source_velocity_text.set(' ')
            self.source_velocity.configure(state='disabled')            

        if(n2==3):  # receiver velocity
            self.receiver_velocity_text.set(' ')
            self.receiver_velocity.configure(state='disabled')  
            
        self.results_text.set(' ')
        self.resultr.set(' ')                 
            
###############################################################################         

    def velocity_unit_option(self,val):
        sender=val.widget
        n= int(sender.curselection()[0])
        
        if(n==0):
            self.speed_sound_text.set('Speed of Sound (ft/sec)')            
            self.speed_soundr.set('1120')  

        if(n==1):
            self.speed_sound_text.set('Speed of Sound (mph)')               
            self.speed_soundr.set('767')  
            
        if(n==2):
            self.speed_sound_text.set('Speed of Sound (m/sec)')               
            self.speed_soundr.set('343')  

        if(n==3):
            self.speed_sound_text.set('Speed of Sound (km/hr)')               
            self.speed_soundr.set('1234')              

        self.change_entry(self)
        
        
        

    def analysis_go(self):

    
        
        c=float(self.speed_soundr.get())
         
    
        n1=int(self.Lb1.curselection()[0])   
        n2=int(self.Lb2.curselection()[0])  
        
        if(n2==0):  # apparent frequency
            self.results_text.set('Results: Apparent Frequency (Hz)')   
            
            fs=float(self.source_frequencyr.get())
            u=float(self.source_velocityr.get())
            v=float(self.receiver_velocityr.get())               
            
            if(abs(u)>=c):
                tkMessageBox.showwarning("warning", "Source velocity must be less than speed of sound.",parent=self.button_go)        
         
            if(abs(v)>=c):
                tkMessageBox.showwarning("warning", "Receiver velocity must be less than speed of sound.",parent=self.button_go)          
            
            if(abs(u)<c and abs(v)<c):
                fa=fs*((c-v)/(c-u))
                buf1 = "%8.4g" %fa                   
                self.resultr.set(buf1) 
           
        if(n2==1):  # source frequency
            self.results_text.set('Results: Source Frequency (Hz)')    
         
            fa=float(self.apparent_frequencyr.get())
            u=float(self.source_velocityr.get())
            v=float(self.receiver_velocityr.get())      
            
            if(abs(u)>=c):
                tkMessageBox.showwarning("warning", "Source velocity must be less than speed of sound.",parent=self.button_go)        
         
            if(abs(v)>=c):
                tkMessageBox.showwarning("warning", "Receiver velocity must be less than speed of sound.",parent=self.button_go)     
         
            if(abs(u)<c and abs(v)<c):
                fs=fa/((c-v)/(c-u))
                buf1 = "%8.4g" %fs                   
                self.resultr.set(buf1)               

        if(n2==2):  # source velocity
            if(n1==0):
                self.results_text.set('Results: Source Velocity (ft/sec)')                  
            if(n1==1):
                self.results_text.set('Results: Source Velocity (mph)')                 
            if(n1==2):
                self.results_text.set('Results: Source Velocity (m/sec)')                 
            if(n1==3):              
                self.results_text.set('Results: Source Velocity (km/sec)') 

            fs=float(self.source_frequencyr.get())
            fa=float(self.apparent_frequencyr.get())
            v=float(self.receiver_velocityr.get())   

            if(abs(v)>=c):
                tkMessageBox.showwarning("warning", "Receiver velocity must be less than speed of sound.")
            else:               
                u=-((fs/fa)*(c-v))+c  
                buf1 = "%8.4g" %u                
                self.resultr.set(buf1)                 
                
        if(n2==3):  # receiver velocity            
            if(n1==0):
                self.results_text.set('Results: Receiver Velocity (ft/sec)')                  
            if(n1==1):
                self.results_text.set('Results: Receiver Velocity (mph)')                 
            if(n1==2):
                self.results_text.set('Results: Receiver Velocity (m/sec)')                 
            if(n1==3):              
                self.results_text.set('Results: Receiver Velocity (km/sec)') 
                

            fs=float(self.source_frequencyr.get())
            fa=float(self.apparent_frequencyr.get())
            u=float(self.source_velocityr.get())
            
            if(abs(u)>=c):
                tkMessageBox.showwarning("warning", "Source velocity must be less than speed of sound.")
            else:                
                v=-((fa/fs)*(c-u))+c
                buf1 = "%8.4g" %v                
                self.resultr.set(buf1) 


    
def quit(root):
    root.destroy()              