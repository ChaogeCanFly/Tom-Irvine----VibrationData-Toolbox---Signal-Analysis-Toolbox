################################################################################
# program: vb_rainflow_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.5
# date: December 15, 2014
# description:  
#    
#  ASTM E 1049-85 (2005) Rainflow Counting Method
#              
################################################################################

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


from vb_utilities import read_one_column_from_dialog,read_two_columns_from_dialog
                                                    

import numpy as np

import matplotlib.pyplot as plt

import csv

################################################################################

class vb_rainflow:
    def __init__(self,parent): 
        self.master=parent        # store the parent
        self.top = tk.Frame(parent)    # frame for all class widgets
        self.top.pack(side='top')      # pack frame in parent's window

##        self.master.minsize(800,700)
##        self.master.geometry("800x700")
        
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        w = int(2.*(w*0.30))
        h = int(2.*(h*0.35))
        self.master.geometry("%dx%d+0+0" % (w, h))
      
        
        self.master.title("vb_rainflow_gui.py ver 1.5  by Tom Irvine") 
        
        self.num=0
        
        self.crow=0
        
        self.hwtext1=tk.Label(self.top,text='ASTM E 1049-85 (2005) Rainflow Counting Method')
        self.hwtext1.grid(row=self.crow, column=0, columnspan=4, pady=7,sticky=tk.W)

        self.crow=self.crow+1

        self.hwtext2=tk.Label(self.top,text='Select input data format ')
        self.hwtext2.grid(row=self.crow, column=0, columnspan=2, pady=7,sticky=tk.SW)
        
        self.hwtext3=tk.Label(self.top,text='Remove Mean ')
        self.hwtext3.grid(row=self.crow, column=2, columnspan=1, padx=5,pady=7,sticky=tk.S)
        
        self.crow=self.crow+1
        
        self.Lb1 = tk.Listbox(self.top,height=2,exportselection=0)
        self.Lb1.insert(1, "time & amplitude")
        self.Lb1.insert(2, "amplitude")
        self.Lb1.grid(row=self.crow, column=0, pady=4,sticky=tk.W)
        self.Lb1.select_set(0)       
 
        self.Lb2 = tk.Listbox(self.top,height=2,exportselection=0)
        self.Lb2.insert(1, "yes")
        self.Lb2.insert(2, "no")
        self.Lb2.grid(row=self.crow, column=2, padx=5, pady=4,sticky=tk.NW)
        self.Lb2.select_set(0)  
        
        self.crow=self.crow+1
         
        self.button_read = tk.Button(self.top, text="Read Input File",command=self.read_data)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=self.crow, column=0,columnspan=1, pady=10,sticky=tk.W) 
                    
        self.button_calculate = tk.Button(self.top, text="Calculate",command=self.calculate)
        self.button_calculate.config( height = 3, width = 15,state = 'disabled' )
        self.button_calculate.grid(row=self.crow, column=2,columnspan=1, pady=10,sticky=tk.W)
        
        root=self.master  
        
        self.button_quit=tk.Button(self.top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 3, width = 15 )
        self.button_quit.grid(row=self.crow, column=3,columnspan=2, padx=10,pady=20)
               
        self.crow=self.crow+1  
        

        
        self.tree = Treeview(self.top,selectmode="extended",columns=("A","B","C","D","E","F","G"))
        self.tree.grid(row=self.crow, column=0,columnspan=6, padx=10,pady=20)
        
        self.tree.heading('#0', text='') 
        self.tree.heading('A', text='')          
        self.tree.heading('B', text='')
        self.tree.heading('C', text='')
        self.tree.heading('D', text='')
        self.tree.heading('E', text='')
        self.tree.heading('F', text='')
        self.tree.heading('G', text='')   
        
        self.tree.column('#0',minwidth=0,width=1)
        self.tree.column('A',minwidth=0,width=120, stretch=tk.YES)        
        self.tree.column('B',minwidth=0,width=85)        
        self.tree.column('C',minwidth=0,width=80)        
        self.tree.column('D',minwidth=0,width=80)       
        self.tree.column('E',minwidth=0,width=80)        
        self.tree.column('F',minwidth=0,width=80)        
        self.tree.column('G',minwidth=0,width=80) 
        
        self.crow=self.crow+1  

        self.hwtextext_rapv1=tk.Label(self.top,text='Range=peak-valley')
        self.hwtextext_rapv1.grid(row=self.crow, column=0,columnspan=1,pady=10,sticky=tk.W)
        
        self.hwtextext_rapv2=tk.Label(self.top,text='Amplitude=(peak-valley)/2')
        self.hwtextext_rapv2.grid(row=self.crow, column=2,columnspan=1,pady=10,sticky=tk.W)        
        
        self.crow=self.crow+1  

        self.hwtextext_exrf=tk.Label(self.top,text='Export Rainflow Data')
        self.hwtextext_exrf.grid(row=self.crow, column=0,pady=10)  
        self.hwtextext_exrf.config(state = 'disabled')  
        
        self.crow=self.crow+1      

        self.button_rt = tk.Button(self.top, text="Rainflow Table (csv format)", command=self.export_table)
        self.button_rt.config( height = 2, width = 26,state = 'disabled' )
        self.button_rt.grid(row=self.crow, column=0,columnspan=2, pady=3, padx=1)  

        self.button_rc = tk.Button(self.top, text="Range & Cycles", command=self.export_range_cycles)
        self.button_rc.config( height = 2, width = 26,state = 'disabled' )
        self.button_rc.grid(row=self.crow, column=2,columnspan=2, pady=3, padx=4) 

        self.button_ac = tk.Button(self.top, text="Amplitude & Cycles", command=self.export_amp_cycles)
        self.button_ac.config( height = 2, width = 26,state = 'disabled' )
        self.button_ac.grid(row=self.crow, column=4,columnspan=2, pady=3, padx=4)          
        
################################################################################

    def export_table(self):
        output_file_path = asksaveasfilename(parent=self.master,title="Enter the Rainflow Table Comma-Delimited filename")           
        output_file = output_file_path.rstrip('\n')
        
        header=(['Range(units)','Cycle Count','Ave Amp','Max Amp','Ave Mean','Min Valley','Max Peak'])

        with open(output_file, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            
            for i in range (13,0,-1):            
                
                s1="%8.2f to %8.2f" %(self.L[i],self.L[i+1])
                s2="%8.1f" %self.C[i]
                s3="%6.4g" %self.AverageAmp[i]
                s4="%6.4g" %self.MaxAmp[i]
                s5="%6.4g" %self.AverageMean[i]
                s6="%6.4g" %self.MinValley[i]
                s7="%6.4g" %self.MaxPeak[i]

                mat=([s1,s2,s3,s4,s5,s6,s7])
                writer.writerow(mat)



    def export_range_cycles(self):
        output_file_path = asksaveasfilename(parent=self.master,title="Enter the Range & Cycles filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2B(self.kv,self.B,output_file)
        
    def export_amp_cycles(self):
        output_file_path = asksaveasfilename(parent=self.master,title="Enter the Amplitude & Cycles filename")           
        output_file = output_file_path.rstrip('\n')    
        WriteData2B(self.kv,self.B/2,output_file)        

################################################################################

    @classmethod 
    def find_points(cls,self):
        y=self.b
        k=0
        self.a[0]=y[0]

        k=1

        for i in range (1,int(self.num-1)):
            
            slope1=(  y[i]-y[i-1])
            slope2=(y[i+1]-y[i])

            if((slope1*slope2)<=0 and abs(slope1)>0):
                self.a[k]=y[i]
                k+=1
                     
        self.last_a=k        
        self.hold=self.last_a        
        self.a[k]=y[self.num-1]

################################################################################        
        
    @classmethod         
    def count_cycles(cls,self):    
    
        i=0
        j=1

        self.sum=0
        self.kv=0

        self.ymax=-1.0e+20

        print (" ")
# print (" last_a=%d " %last_a)


        aa=self.a.tolist()

        nkv=0

        print ("\n percent completed \n")

        while(1):
    
    
            Y=abs(aa[i]-aa[i+1])
            X=abs(aa[j]-aa[j+1])
    
##    print (" i=%d j=%d last_a=%d  X=%8.4g  Y=%8.4g " %(i,j,last_a,X,Y)

            if(X>=Y and Y>0):		
                if(Y>self.ymax):
                    self.ymax=Y
             
                if(i==0):		
                    self.sum+=0.5
                    self.B[self.kv][3]=aa[i+1]
                    self.B[self.kv][2]=aa[i]
                    self.B[self.kv][1]=0.5
                    self.B[self.kv][0]=Y
                    self.kv+=1
                    aa.pop(i)
                    self.last_a-=1
                    i=0
                    j=1    
                
                else:      
                    self.sum+=1
                    self.B[self.kv][3]=aa[i+1]
                    self.B[self.kv][2]=aa[i]
                    self.B[self.kv][1]=1.
                    self.B[self.kv][0]=Y
                    self.kv+=1	
                    
                    aa.pop(i+1)
                    aa.pop(i)                
                
                    i=0
                    j=1

                    self.last_a-=2
            
                    nkv+=1

                    if(nkv==3000):
                        pr=(self.sum/(self.hold/2))*100.
                        print (" %8.4g " %pr)
                        nkv=0
              	    
            else:
                i+=1
                j+=1
                
            if((j+1)>self.last_a):
                break                
 
 
        for i in range (0,int(self.last_a)):
	
            Y=(abs(aa[i]-aa[i+1]))

##    print ("i=%d  kv=%d  Y=%g " %(i,kv,Y)

            if(Y>0):
		
                self.sum+=0.5
                self.B[self.kv][3]=aa[i+1]
                self.B[self.kv][2]=aa[i]
                self.B[self.kv][1]=0.5
                self.B[self.kv][0]=Y
        
                self.kv+=1
		
                if(Y>self.ymax):
                    self.ymax=Y
 
        print (" ymax=%8.4g " %self.ymax)

################################################################################

    @classmethod 
    def rainflow_bins(cls,self):

        self.L=np.zeros(15,'f')
        self.C=np.zeros(15,'f')

        self.AverageMean=np.zeros(15,'f')
        self.MaxPeak=np.zeros(15,'f')
        self.MinValley=np.zeros(15,'f')
        self.MaxAmp=np.zeros(15,'f')
        self.AverageAmp=np.zeros(15,'f')

        self.L[1]=0
        self.L[2]=2.5
        self.L[3]=5
        self.L[4]=10
        self.L[5]=15
        self.L[6]=20
        self.L[7]=30
        self.L[8]=40
        self.L[9]=50
        self.L[10]=60
        self.L[11]=70
        self.L[12]=80
        self.L[13]=90
        self.L[14]=100

        for ijk in range (1,15):
    
            self.L[ijk]*=self.ymax/100.
    
            self.MaxPeak[ijk]=-1.0e+20
            self.MinValley[ijk]= 1.0e+20

            self.MaxAmp[ijk]=-1.0e+20

        self.kv-=1

        for i in range (0,int(self.kv+1)):
            Y=self.B[i][0]
     
##     print ("i=%d  Y=%g " %(i,Y)
     
            for ijk in range (13,0,-1):
         
                 if(Y>=self.L[ijk] and Y<=self.L[ijk+1]):         
                     self.C[ijk]+=self.B[i][1]
            
                     self.AverageMean[ijk]+=self.B[i][1]*(self.B[i][3]+self.B[i][2])*0.5  # weighted average    

                     if(self.B[i][3]>self.MaxPeak[ijk]):
                         self.MaxPeak[ijk]=self.B[i][3]
            
                     if(self.B[i][2]>self.MaxPeak[ijk]):
                         self.MaxPeak[ijk]=self.B[i][2]
            
                     if(self.B[i][3]<self.MinValley[ijk]):
                         self.MinValley[ijk]=self.B[i][3]
            
                     if(self.B[i][2]<self.MinValley[ijk]):
                         self.MinValley[ijk]=self.B[i][2]
            
                     if(Y>self.MaxAmp[ijk]):
                         self.MaxAmp[ijk]=Y
            
                     self.AverageAmp[ijk]+=self.B[i][1]*Y*0.5

                     break

        for ijk in range (1,15):

            if(self.C[ijk]>0):
                self.AverageMean[ijk]/=self.C[ijk]
                self.AverageAmp[ijk]/=self.C[ijk]
      
            if(self.C[ijk]<0.5):
                self.AverageMean[ijk]=0.    
                self.AverageAmp[ijk]=0.       
                self.MaxPeak[ijk]=0.            
                self.MinValley[ijk]=0.         
                self.MaxAmp[ijk]=0.            
        
        self.MaxAmp[ijk]/=2.
# 
        self.tree.heading('A', text='Range (units)')
        self.tree.heading('B', text='Cycle Count')
        self.tree.heading('C', text='Ave Amp')
        self.tree.heading('D', text='Max Amp')
        self.tree.heading('E', text='Ave Mean')
        self.tree.heading('F', text='Min Valley')
        self.tree.heading('G', text='Max Peak')
             
        self.hwtextext_exrf.config(state = 'normal')               
        self.button_rt.config( height = 2, width = 26,state = 'normal' )
        self.button_ac.config( height = 2, width = 26,state = 'normal' )    
        self.button_rc.config( height = 2, width = 26,state = 'normal' )     
    
        print (" ")
        print (" Amplitude = (peak-valley)/2  ")

#        outfile.write('\n  Amplitude = (peak-valley)/2 \n\n')

#*****************************************************************************

        print (" ")
        print ("          Range            Cycle       Ave      Max     Ave     Min       Max")
        print ("         (units)           Counts      Amp      Amp     Mean    Valley    Peak ")


        for i in range (13,0,-1):
            print ("  %8.2f to %8.2f\t%8.1f\t%6.4g\t%6.4g\t%6.4g\t%6.4g\t %6.4g "\
            %(self.L[i],self.L[i+1],self.C[i],self.AverageAmp[i],self.MaxAmp[i],\
                       self.AverageMean[i],self.MinValley[i],self.MaxPeak[i]))
                
                                
            s0="%8.2f to %8.2f" %(self.L[i],self.L[i+1])
               
            s1="%8.1f" %self.C[i]
            
            s2="%6.4g" %self.AverageAmp[i]
             
            s3="%6.4g" %self.MaxAmp[i]
            
            s4="%6.4g" %self.AverageMean[i]
              
            s5="%6.4g" %self.MinValley[i]
         
            s6="%6.4g" %self.MaxPeak[i]

            self.tree.insert('', 'end', values=(s0,s1,s2,s3,s4,s5,s6))
           
            

        sh=self.hold
        sn=self.num
        sy=self.ymax
        ss=self.sum

        print ("\n\n Total Cycles = %g  hold=%d  NP=%d ymax=%g\n" %(ss,sh,sn,sy))
                
#############################################################################

    def calculate(self):
        # remove mean
        imr=int(self.Lb2.curselection()[0])
        
        if(imr==0):
            self.b-=np.mean(self.b)          

        self.b=np.array(self.b)
        
################################################################################

        self.a=np.zeros(self.num,'f')
        self.B=np.zeros((self.num,4),'f')

        self.find_points(self)
        self.count_cycles(self)   
        self.rainflow_bins(self)
        
################################################################################                

    def read_data(self):
        icf=int(self.Lb1.curselection()[0])
        
        plt.ion()
        plt.clf()        
        
        if(icf==1):  # single column
            self.b,self.num=read_one_column_from_dialog('Select Input File',self.master)
            plt.figure(1)
            plt.plot(self.b, linewidth=1.0,color='b')            
        else:        # two columns
            self.a,self.b,self.num=read_two_columns_from_dialog('Select Input File',self.master)
            plt.figure(1)
            plt.plot(self.a, self.b, linewidth=1.0,color='b')
            plt.xlabel('Time (sec)')
 
 
        plt.grid(True)        
        plt.ylabel('Amplitude')        
        plt.title('Time History')    
        plt.draw()

        print ("\n samples = %d " % self.num)
        
        self.button_calculate.config(state = 'normal')

        self.tree.heading('A', text='')          
        self.tree.heading('B', text='')
        self.tree.heading('C', text='')
        self.tree.heading('D', text='')
        self.tree.heading('E', text='')
        self.tree.heading('F', text='')
        self.tree.heading('G', text='')    

        self.hwtextext_exrf.config(state = 'disabled')               
        self.button_rt.config(state = 'disabled' )
        self.button_ac.config(state = 'disabled' )             
        self.button_rc.config(state = 'disabled' )  
        
################################################################################

def WriteData2B(nn,bb,output_file_path):
    """
    Write two columns of data to an external ASCII text file
    """
    output_file = output_file_path.rstrip('\n')
    outfile = open(output_file,"w")
    for i in range (0, int(nn)):
        outfile.write(' %10.6e \t %8.4e \n' %  (bb[i][0],bb[i][1]))
    outfile.close()

################################################################################

def quit(root):
    root.destroy()
    