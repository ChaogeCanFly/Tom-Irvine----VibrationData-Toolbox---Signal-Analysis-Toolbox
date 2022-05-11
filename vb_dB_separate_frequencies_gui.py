###########################################################################
# program: vb_dB_separate_frequencies_gui.py
# author: Tom Irvine
# version: 1.0
# date: May 29, 2014
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
    
from numpy import log,log10        

###############################################################################

class vb_dB_separate_frequencies:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        

        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.30))
        h = int(2.*(h*0.24))
        self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.title("vb_dB_separate_frequencies_gui.py  ver 1.0  by Tom Irvine")
        
        crow=0
        

        self.hwtext1=tk.Label(top,text='Select Dimension')
        self.hwtext1.grid(row=crow, column=0, columnspan=2, pady=7)   
        
        self.hwtext2=tk.Label(top,text='Select Analysis')
        self.hwtext2.grid(row=crow, column=3, columnspan=1, pady=7)       
        
        crow=crow+1
        
        self.Lb1 = tk.Listbox(top,height=3,width=34,exportselection=0)
        self.Lb1.insert(1, "Shock Response Spectrum (G)")
        self.Lb1.insert(2, "Power Spectral Density (G^2/Hz)")      
        self.Lb1.grid(row=crow, column=0, columnspan=3, pady=4)
        self.Lb1.select_set(0) 
        self.Lb1.bind("<<ListboxSelect>>", self.dimension)          

        self.Lb2 = tk.Listbox(top,height=3,width=50,exportselection=0)
        self.Lb2.insert(1, "Calculate slope between two coordinates")
        self.Lb2.insert(2, "Find new coordinate given slope and one coordinate")
        self.Lb2.insert(3, "Find new coordinate given two coordinates")         
        self.Lb2.grid(row=crow, column=3, columnspan=2, pady=4)
        self.Lb2.select_set(0) 
        self.Lb2.bind("<<ListboxSelect>>", self.analysis)            
        
        crow=crow+1

        self.hwtext3=tk.Label(top,text='Frequency (Hz)')
        self.hwtext3.grid(row=crow, column=0, columnspan=1, pady=7, sticky=tk.E)  
        
        self.a_text=tk.StringVar()  
        self.a_text.set('SRS(G)')         
        self.hwtext5=tk.Label(top,textvariable=self.a_text)
        self.hwtext5.grid(row=crow, column=1, columnspan=1, padx=1, pady=7, sticky=tk.NE)        
        
        
        crow=crow+1       
        
        self.freq1r=tk.StringVar()  
        self.freq1_entry=tk.Entry(top, width = 10,textvariable=self.freq1r)
        self.freq1_entry.grid(row=crow, column=0, pady=2, sticky=tk.NE)

        self.amp1r=tk.StringVar()  
        self.amp1_entry=tk.Entry(top, width = 10,textvariable=self.amp1r)
        self.amp1_entry.grid(row=crow, column=1, pady=2, sticky=tk.NE)         

        self.hwtext7=tk.Label(top,text='Coordinate 1')
        self.hwtext7.grid(row=crow, column=2, columnspan=1, padx=4, pady=2, sticky=tk.NW)  
        
        self.sloper=tk.StringVar()  
        self.slope_entry=tk.Entry(top, width = 10,textvariable=self.sloper)
        self.slope_entry.grid(row=crow, column=3, pady=2, sticky=tk.NE)  
        self.slope_entry.config(state='disabled')          
        
        self.slope_text=tk.StringVar()  
        self.slope_text.set(' ')         
        self.hwtext13=tk.Label(top,textvariable=self.slope_text)
        self.hwtext13.grid(row=crow, column=4, columnspan=3, padx=4, pady=7, sticky=tk.NW)  

        crow=crow+1
        
        self.freq2r=tk.StringVar()  
        self.freq2_entry=tk.Entry(top, width = 10,textvariable=self.freq2r)
        self.freq2_entry.grid(row=crow, column=0, pady=2, sticky=tk.NE)  

        self.amp2r=tk.StringVar()  
        self.amp2_entry=tk.Entry(top, width = 10,textvariable=self.amp2r)
        self.amp2_entry.grid(row=crow, column=1, pady=2, sticky=tk.NE)                  
        
        self.c2_text=tk.StringVar()  
        self.c2_text.set('Coordinate 2')         
        self.hwtext9=tk.Label(top,textvariable=self.c2_text)        
        self.hwtext9.grid(row=crow, column=2, columnspan=1, padx=4, pady=2, sticky=tk.NW)          
        
        self.nfreqr=tk.StringVar()  
        self.nfreq_entry=tk.Entry(top, width = 10,textvariable=self.nfreqr)
        self.nfreq_entry.grid(row=crow, column=3, pady=2,sticky=tk.NE) 
        self.nfreq_entry.config(state='disabled')         

        self.nfreq_text=tk.StringVar()  
        self.nfreq_text.set(' ')         
        self.hwtext15=tk.Label(top,textvariable=self.nfreq_text)
        self.hwtext15.grid(row=crow, column=4, columnspan=3, padx=4, pady=7, sticky=tk.NW)  

        crow=crow+1

        self.hwtext11=tk.Label(top,text='Slope Results')
        self.hwtext11.grid(row=crow, column=0, columnspan=1, pady=16, sticky=tk.S)  
        
        self.new_coord_text=tk.StringVar()  
        self.new_coord_text.set(' ')       
        self.hwtext19=tk.Label(top,textvariable=self.new_coord_text)                
        self.hwtext19.grid(row=crow, column=1, columnspan=1, pady=15, sticky=tk.S) 

         

        crow=crow+1

        self.slope_resultr=tk.StringVar()  
        self.slope_result_entry=tk.Entry(top, width = 18,textvariable=self.slope_resultr)
        self.slope_result_entry.grid(row=crow, column=0, pady=2, sticky=tk.N) 
        self.slope_result_entry.config(state='readonly')   
        
        self.new_coordinate_resultr=tk.StringVar()  
        self.new_coordinate_result_entry=tk.Entry(top, width = 27,textvariable=self.new_coordinate_resultr)
        self.new_coordinate_result_entry.grid(row=crow, column=1, pady=2, sticky=tk.N) 
        self.new_coordinate_result_entry.config(state='readonly')          

        
        crow=crow+1
        
        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 18)
        self.button_calculate.grid(row=crow, column=0,columnspan=1, pady=20) 
                
        root=self.master             

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 18 )
        self.button_quit.grid(row=crow, column=1,columnspan=1, padx=10,pady=20)
 
 
        self.freq1_entry.bind("<Key>", self.callback_clear)
        self.amp1_entry.bind("<Key>", self.callback_clear)
        self.freq2_entry.bind("<Key>", self.callback_clear)
        self.amp2_entry.bind("<Key>", self.callback_clear)
        self.slope_entry.bind("<Key>", self.callback_clear)
        self.nfreq_entry.bind("<Key>", self.callback_clear) 
 
###############################################################################
    
    def calculation(self):    
        
        n=1+int(self.Lb1.curselection()[0])   
        m=1+int(self.Lb2.curselection()[0])  
        
        f1=float(self.freq1r.get())
        amp1=float(self.amp1r.get())       
        

        if(m==1 or m==3):

           f2=float(self.freq2r.get())
           amp2=float(self.amp2r.get()) 
     
           nslope=log(amp2/amp1)/log(f2/f1)
      
           if(n==1):
              dbpo=20*nslope*log10(2) 
           else:        
              dbpo=10*nslope*log10(2)       
      
      
        if(m==2 or m==3):
           new_frequency=float(self.nfreqr.get())
     
    
   
    
        if(m==2):

           dbpo=float(self.sloper.get())

           if(n==1):
               nslope=(dbpo/20)/log10(2)
           else:
               nslope=(dbpo/10)/log10(2)      

           y=amp1*(new_frequency/f1)**(nslope) 
           

        if(m==3):
            y=amp1*(new_frequency/f1)**(nslope) 


        
        if(m==2 or m==3):
            
           if(n==1):
               out2='%g Hz, %8.4g G' %(new_frequency,y)
           else:
               out2='%g Hz, %8.4g G^2/Hz' %(new_frequency,y)
               

           self.new_coordinate_resultr.set(out2)


        out1='%7.3g dB/oct' %dbpo
        self.slope_resultr.set(out1)

###############################################################################    
    
    

    def callback_clear(self,event):
        self.slope_resultr.set(' ')             
        self.new_coordinate_resultr.set(' ')       
    
    
    def dimension(self,event): 
        self.change(self)         
         
    def analysis(self,event): 
        self.change(self)   


    @classmethod
    def change(cls,self):
        
        self.nfreq_text.set(' ')  
        self.slope_text.set(' ')   
        self.new_coord_text.set(' ')
        
        self.c2_text.set('Coordinate 2')  
        
        self.callback_clear(self)        
        
        n1=int(self.Lb1.curselection()[0])   
        n2=int(self.Lb2.curselection()[0])  
        
        if(n2>=1):
            self.new_coord_text.set('New Coordinate Results')

        if(n1==0):
            self.a_text.set('SRS(G)')              
        else:    
            self.a_text.set('PSD(G^2/Hz)')
            
        self.slope_entry.config(state='disabled')   
        self.nfreq_entry.config(state='disabled') 

        self.freq2_entry.config(state='normal')    
        self.amp2_entry.config(state='normal')            
        
        
        if(n2==1):
            self.slope_entry.config(state='normal')   
            self.nfreq_entry.config(state='normal')             

            self.slope_text.set('Enter slope (dB/octave) from lower to higher frequency') 
            self.nfreq_text.set('Enter frequency(Hz) of new coordinate') 
            
            self.freq2_entry.config(state='disabled')    
            self.amp2_entry.config(state='disabled') 

            self.freq2r.set(' ')  
            self.amp2r.set(' ') 

            self.c2_text.set(' ')              

        if(n2==2):
            self.nfreq_entry.config(state='normal') 
            self.nfreq_text.set('Enter frequency(Hz) of new coordinate')                 
            
    
        if(n2==0 or n2==2):
            self.sloper.set(' ')             
            
###############################################################################
    
def quit(root):
    root.destroy()         