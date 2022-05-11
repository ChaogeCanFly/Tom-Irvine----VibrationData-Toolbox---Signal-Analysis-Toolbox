################################################################################
# program: vb_plot_utilities_gui.py
# author: Tom Irvine
# version: 1.2
# date: October 13, 2014
#
################################################################################

from __future__ import print_function
    
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
        

import matplotlib.pyplot as plt


class vb_plot_utilities:

    def __init__(self,parent): 
        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.18))
        h = int(2.*(h*0.21))
        self.master.geometry("%dx%d+0+0" % (w, h))

        
        self.master.title("vb_plot_utilities_gui.py ver 1.2  by Tom Irvine")    
        
################################################################################

        crow=0

        self.hwtext1=tk.Label(top,text='Select Analysis')
        self.hwtext1.grid(row=crow, column=0, columnspan=6, pady=7,sticky=tk.W)

        crow=crow+1

        self.Lb3 = tk.Listbox(top,height=11,width=40,exportselection=0)
        self.Lb3.insert(1, "Time History")        
        self.Lb3.insert(2, "Two Time Histories, Scatter Plot")
        self.Lb3.insert(3, "PSD")       
        self.Lb3.insert(4, "SRS")
        self.Lb3.insert(5, "SPL")
        self.Lb3.insert(6, "Fourier Transform: magnitude & phase")
        self.Lb3.insert(7, "Fourier Transform: real & imaginary")
        self.Lb3.insert(8, "Nyquist & Nichols Plots")
        self.Lb3.insert(9, "Two Curves & Miscellaneous")
        self.Lb3.insert(10, "Multiple Curves")        
        
        self.Lb3.grid(row=crow, column=0, columnspan=1, padx=10, pady=4,sticky=tk.N)
        self.Lb3.select_set(0)
        

        crow=crow+1

        button1=tk.Button(top, text='Perform Analysis', command=self.PerformAnalysis)
        button1.grid(row=crow, column=0, padx=10, pady=10)
        button1.config( height = 2, width = 30 )        
        
        crow=crow+1        
        
        root=self.master        
        
        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 30 )
        self.button_quit.grid(row=crow, column=0, padx=10,pady=10) 
        
################################################################################

    def PerformAnalysis(self):

        plt.close("all") 
  
        win = tk.Toplevel()
    
        n=int(self.Lb3.curselection()[0])   

        m=0 
        
        if(n==m):
            from vb_time_history_plot_gui import vb_time_history_plot         
            vb_time_history_plot(win)
            
        m=m+1        

        if(n==m):
            from vb_scatter_plot_gui import vb_scatter_plot        
            vb_scatter_plot(win)
            
        m=m+1
        
        if(n==m):
            from vb_psd_plot_gui import vb_psd_plot         
            vb_psd_plot(win)
            
        m=m+1
    
        if(n==m):
            from vb_srs_plot_gui import vb_srs_plot        
            vb_srs_plot(win)
            
        m=m+1    
        
        if(n==m):
            from vb_spl_plot_gui import vb_spl_plot        
            vb_spl_plot(win)
            
        m=m+1       
    
        if(n==m):
            from vb_ft_mp_plot_gui import vb_ft_mp_plot        
            vb_ft_mp_plot(win)
    
        m=m+1   
 
    
        if(n==m):
            from vb_ft_ri_plot_gui import vb_ft_ri_plot        
            vb_ft_ri_plot(win)
    
        m=m+1   
        
    
        if(n==m):
            from vb_nyquist_nichols_plots_gui import vb_nyquist_nichols_plots        
            vb_nyquist_nichols_plots(win)
    
        m=m+1   

    
        if(n==m):
            from vb_two_curves_plots_gui import vb_two_curves_plots        
            vb_two_curves_plots(win)
    
        m=m+1           
        
        if(n==m):
            from vb_multiple_curves_gui import vb_multiple_curves       
            vb_multiple_curves(win)
    
        m=m+1  
      

###############################################################################
        
def quit(root):
    root.destroy()                    