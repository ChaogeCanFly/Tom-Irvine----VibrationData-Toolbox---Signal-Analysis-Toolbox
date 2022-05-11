###############################################################################
# program: vibrationdata.py
# author: Tom Irvine
# Email: tom@irvinemail.org
# version: 6.4
# date: September 16, 2016
# description:  multi-function signal analysis program
#
###############################################################################

from __future__ import print_function

import sys


if sys.version_info[0] == 2:
    import Tkinter as tk
    import tkMessageBox
           
if sys.version_info[0] == 3:   
    import tkinter as tk 
    import tkinter.messagebox as tkMessageBox        



import matplotlib.pyplot as plt


import webbrowser

###############################################################################


def quit(root):
    root.destroy()


def visitBlog():
    webbrowser.open('https://vibrationdata.wordpress.com/2014/04/02/python-signal-analysis-package-gui/')

###############################################################################

def SignalAnalysisWindow():

    plt.close("all") 
  
    win = tk.Toplevel()
    
    n=int(Lb1.curselection()[0])   

    m=0 

    if(n==m):
        from vb_statistics_gui import vb_statistics        
        vb_statistics(win)
    m=m+1
    
    if(n==m):
        from vb_trend_removal_scaling_gui import vb_trend_removal_scaling        
        vb_trend_removal_scaling(win)
    m=m+1    
        
    if(n==m):
        from vb_various_filters_gui import vb_various_filters        
        vb_various_filters(win)
    m=m+1       
        
    if(n==m):
        from vb_fourier_gui import vb_Fourier        
        vb_Fourier(win)
    m=m+1
        
    if(n==m): 
        from vb_fft_gui import vb_FFT        
        vb_FFT(win)
    m=m+1
        
    if(n==m): 
        from vb_waterfall_fft_gui import vb_waterfall_FFT        
        vb_waterfall_FFT(win)       
    m=m+1
        
    if(n==m):
        from vb_psd_gui import vb_PSD         
        vb_PSD(win)   
    m=m+1
        
    if(n==m):
        from vb_sdof_response_time_domain_gui import vb_sdof_response_time_domain         
        vb_sdof_response_time_domain(win)
    m=m+1
        
    if(n==m):
        from vb_srs_gui import vb_SRS         
        vb_SRS(win)
    m=m+1
        
    if(n==m):
        from vb_rainflow_gui import vb_rainflow         
        vb_rainflow(win)    
    m=m+1
                
    if(n==m):
        from vb_integrate_differentiate_gui import vb_integrate_differentiate         
        vb_integrate_differentiate(win)  
    m=m+1
        
    
    if(n==m):
        from vb_autocorrelation_gui import vb_autocorrelation         
        vb_autocorrelation(win)             
    m=m+1 

    if(n==m):
        from vb_cross_correlation_gui import vb_cross_correlation         
        vb_cross_correlation(win)             
    m=m+1 
    
    if(n==m):
        from vb_cepstrum_gui import vb_cepstrum         
        vb_cepstrum(win)             
    m=m+1     
    
    if(n==m):
        from vb_spl_gui import vb_SPL         
        vb_SPL(win)             
    m=m+1
        
    if(n==m):
        from vb_sine_curvefit_gui import vb_sine_curvefit         
        vb_sine_curvefit(win)             
    m=m+1       
    
    if(n==m):
        from vb_tvfa_gui import vb_tvfa         
        vb_tvfa(win)             
    m=m+1     
    
###############################################################################
    
def PSDAnalysisWindow():

    plt.close("all")  
    
    win = tk.Toplevel()
    
    n=int(Lb3.curselection()[0])  
    
    m=0 

    if(n==m):
        from vb_psd_rms_gui import vb_psd_rms        
        vb_psd_rms(win)         
    
    m=m+1   

    if(n==m):
        from vb_psd_octave_gui import vb_psd_octave        
        vb_psd_octave(win)         
    
    m=m+1   

    if(n==m):
        from vb_sdof_base_psd_gui import vb_sdof_base_psd        
        vb_sdof_base_psd(win)    
        
    m=m+1   

    if(n==m):
        from vb_sdof_force_psd_gui import vb_sdof_force_psd        
        vb_sdof_force_psd(win)          
    
    m=m+1  

    if(n==m):
        from vb_vrs_gui import vb_VRS        
        vb_VRS(win)    
        
    m=m+1  

    if(n==m):
        from vb_vrs_force_gui import vb_VRS_force        
        vb_VRS_force(win)         
    
    m=m+1      

    if(n==m):
        from vb_accel_psd_syn_gui import vb_accel_psd_syn        
        vb_accel_psd_syn(win)         
    
    m=m+1   
    
    if(n==m):
         
        from vb_force_psd_syn_gui import vb_force_psd_syn        
        vb_force_psd_syn(win)         
    
    m=m+1     

    if(n==m):
        from vb_power_trans_gui import vb_power_trans        
        vb_power_trans(win)         
    
    m=m+1   
    
    if(n==m):
        from vb_envelope_PSD_VRS_gui import vb_envelope_PSD_VRS        
        vb_envelope_PSD_VRS(win)         
    
    m=m+1      


###############################################################################   

def SRSAnalysisWindow():

    plt.close("all")  
    
    win = tk.Toplevel()
    
    n=int(Lb4.curselection()[0])  
    
    m=0 

    if(n==m):
        from vb_srs_damped_sine_synth_gui import vb_srs_damped_sine_synth       
        vb_srs_damped_sine_synth(win)         
    
    m=m+1   
    
##    if(n==m):
        
##        tkMessageBox.showwarning("Warning","Function to be Added Soon",parent=self.button_calculate)        
        
#        from vb_srs_wavelet_synth_gui import vb_srs_wavelet_synth       
#        vb_srs_wavelet_synth(win)         
    
    m=m+1      
    
###############################################################################   

def MiscAnalysisWindow():

    plt.close("all")  
    
    win = tk.Toplevel()
    
    n=int(Lb2.curselection()[0])   

    m=0 

    if(n==m):
        from vb_amplitude_conversion_gui import vb_amplitude_conversion        
        vb_amplitude_conversion(win)         

    m=m+1

    if(n==m):
        from vb_sine_sweep_parameters_gui import vb_sine_sweep_parameters        
        vb_sine_sweep_parameters(win)         

    m=m+1
    
    if(n==m):
        from vb_peak_sigma_random_gui import vb_peak_sigma_random        
        vb_peak_sigma_random(win)   
                
    m=m+1

    if(n==m):
        from vb_classical_base_gui import vb_classical_pulse_base        
        vb_classical_pulse_base(win) 
        
    m=m+1

    if(n==m):
        from vb_steady_gui import vb_steady        
        vb_steady(win)         
        
    m=m+1

    if(n==m):
        from vb_generate_gui import vb_generate        
        vb_generate(win)   
               
        
    m=m+1  
      
    if(n==m):
        from vb_structural_dynamics_gui import vb_structural_dynamics        
        vb_structural_dynamics(win)           

    m=m+1  
      
    if(n==m):
        from vb_plot_utilities_gui import vb_plot_utilities        
        vb_plot_utilities(win)        

    m=m+1  
     
    if(n==m):
        from vb_signal_editing_gui import vb_signal_editing      
        vb_signal_editing(win)     

    m=m+1  
     
    if(n==m):
        from vb_rotation_gui import vb_rotation      
        vb_rotation(win)              
                 
    m=m+1  
     
    if(n==m):
        from vb_miles_gui import vb_miles      
        vb_miles(win)     

    m=m+1  
     
    if(n==m):
        from vb_statistical_distributions_gui import vb_statistical_distributions      
        vb_statistical_distributions(win)      

    m=m+1  
     
    if(n==m):
        from vb_Doppler_shift_gui import vb_Doppler_shift      
        vb_Doppler_shift(win)               
        
    m=m+1  
     
    if(n==m):
        from vb_dB_calculations_gui import vb_dB_calculations      
        vb_dB_calculations(win)                
 
    m=m+1  
     
    if(n==m):
        from vb_sound_file_editor_gui import vb_sound_file_editor      
        vb_sound_file_editor(win)   
       

    m=m+1  
     
    if(n==m):
        from vb_modal_frf_gui import vb_modal_frf      
        vb_modal_frf(win)   

    m=m+1  
         
    if(n==m):
        from vb_damping_utilities_gui import vb_damping_utilities      
        vb_damping_utilities(win)      
        
    m=m+1  
         
    if(n==m):
        from vb_wind_waves_gui import vb_wind_waves      
        vb_wind_waves(win)            
        
###############################################################################
    
# create root window

root = tk.Tk()

## root.minsize(1400,750)
## root.geometry("1400x750")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

w = int(2.*(w*0.37))
h = int(2.*(h*0.32))

root.geometry("%dx%d+0+0" % (w, h))


root.title("vibrationdata.py ver 6.3  by Tom Irvine") 

###############################################################################

crow=1

hwtext1=tk.Label(root,text='Multi-function Signal Analysis Script & More')
hwtext1.grid(row=crow, column=0, columnspan=3, padx=8, pady=7,sticky=tk.W)

crow=crow+1

hwtext1=tk.Label(root,text='Note:  for use within Spyder IDE, set: Run > Configuration > Interpreter > Excecute in an external system terminal')
hwtext1.grid(row=crow, column=0, columnspan=3, padx=8, pady=5,sticky=tk.W)

###############################################################################

crow=crow+1

hwtext2=tk.Label(root,text='Select Time History Analysis')
hwtext2.grid(row=crow, column=0, columnspan=1, padx=8, pady=8)

hwtext2=tk.Label(root,text='Select PSD Analysis')
hwtext2.grid(row=crow, column=1, columnspan=1, padx=8, pady=8)

hwtext4=tk.Label(root,text='Select SRS Analysis')
hwtext4.grid(row=crow, column=2, columnspan=1, padx=8, pady=8)

hwtext3=tk.Label(root,text='Select Miscellaneous Analysis')
hwtext3.grid(row=crow, column=3, columnspan=1, padx=8, pady=8)

###############################################################################

crow=crow+1

Lb1 = tk.Listbox(root,height=19,width=36,exportselection=0)
Lb1.insert(1, "Statistics")
Lb1.insert(2, "Trend Removal & Scaling")
Lb1.insert(3, "Filters, Various")
Lb1.insert(4, "Fourier Transform")
Lb1.insert(5, "FFT")
Lb1.insert(6, "Waterfall FFT")
Lb1.insert(7, "PSD")
Lb1.insert(8, "SDOF Response, Base Input & Force")
Lb1.insert(9, "SRS")
Lb1.insert(10, "Rainflow Cycle Counting")
Lb1.insert(11, "Integrate & Differentiate")
Lb1.insert(12, "Autocorrelation")
Lb1.insert(13, "Cross-correlation")
Lb1.insert(14, "Cepstrum & Auto Cepstrum")
Lb1.insert(15, "Sound Pressure Level")
Lb1.insert(16, "Sine & Damped Sine Curve-fit")
Lb1.insert(17, "Time Varying Freq & Amp")
Lb1.grid(row=crow, column=0, padx=16, pady=4,sticky=tk.NE)
Lb1.select_set(0) 

Lb3 = tk.Listbox(root,height=11,width=41,exportselection=0)
Lb3.insert(1, "Overall RMS")
Lb3.insert(2, "Convert to Octave Format")
Lb3.insert(3, "SDOF Response to Base Input")
Lb3.insert(4, "SDOF Response to Applied Force")
Lb3.insert(5, "Vibration Response Spectrum, Base Input")
Lb3.insert(6, "Vibration Response Spectrum, Applied Force")
Lb3.insert(7, "Acceleration PSD Time History Synthesis")
Lb3.insert(8, "Force or Pressure PSD Time History Synthesis")
Lb3.insert(9, "Power Transmissibilty from two PSDs")
Lb3.insert(10, "Envelope PSD via VRS")
Lb3.grid(row=crow, column=1, columnspan=1, padx=8, pady=4,sticky=tk.N)
Lb3.select_set(0)

Lb4 = tk.Listbox(root,height=2,width=26,exportselection=0)
Lb4.insert(1, "Damped Sine Synthesis")
# Lb4.insert(2, "Wavelet Synthesis")
Lb4.grid(row=crow, column=2, columnspan=1, padx=8, pady=4,sticky=tk.N)
Lb4.select_set(0)


Lb2 = tk.Listbox(root,height=19,width=48,exportselection=0)
Lb2.insert(1, "Amplitude Conversion Utilities")
Lb2.insert(2, "Sine Sweep Parameters")
Lb2.insert(3, "SDOF Response: Peak Sigma for Random Base Input")
Lb2.insert(4, "SDOF Response to Classical Pulse Base Input")
Lb2.insert(5, "SDOF Steady-State Response to Sine Excitation")
Lb2.insert(6, "Generate Signal")
Lb2.insert(7, "Structural Dynamics")
Lb2.insert(8, "Plot Utilities")
Lb2.insert(9, "Signal Editing Utilities")
Lb2.insert(10, "Rotation")
Lb2.insert(11, "Miles Equation")
Lb2.insert(12, "Statistical Distributions")
Lb2.insert(13, "Doppler Shift")
Lb2.insert(14, "dB Calculations for log-log Plots")
Lb2.insert(15, "Sound File Editor")
Lb2.insert(16, "Modal FRF")
Lb2.insert(17, "Damping Utilities")
Lb2.insert(18, "Wind & Waves")
Lb2.grid(row=crow, column=3, columnspan=3, padx=8, pady=4,sticky=tk.NW)
Lb2.select_set(0)

###############################################################################

crow=crow+1

button1=tk.Button(root, text='Perform Signal Analysis', command=SignalAnalysisWindow)
button1.grid(row=crow, column=0, padx=8, pady=10)
button1.config( height = 2, width = 30 )

button3=tk.Button(root, text='Perform PSD Analysis', command=PSDAnalysisWindow)
button3.grid(row=crow, column=1, padx=8, pady=10)
button3.config( height = 2, width = 20 )

button4=tk.Button(root, text='Perform SRS Analysis', command=SRSAnalysisWindow)
button4.grid(row=crow, column=2, padx=8, pady=10)
button4.config( height = 2, width = 20 )

button2=tk.Button(root, text='Perform Miscellaneous Analysis', command=MiscAnalysisWindow)
button2.grid(row=crow, column=3, padx=8, pady=10)
button2.config( height = 2, width = 30 )

crow=crow+1

button3=tk.Button(root, text='Visit Python Blog', command=visitBlog)
button3.grid(row=crow, column=0, padx=8, pady=10)
button3.config( height = 2, width = 15 )


button_quit=tk.Button(root, text="Quit", command=lambda root=root:quit(root))
button_quit.config( height = 1, width = 10 )
button_quit.grid(row=crow, column=1, padx=3,pady=10)


###############################################################################

# start event-loop

root.mainloop()