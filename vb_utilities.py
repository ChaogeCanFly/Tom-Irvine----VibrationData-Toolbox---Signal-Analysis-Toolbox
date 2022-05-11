################################################################################
# program: vb_utilities.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 2.5
# date: September 12, 2016
# description:  utility functions
#
################################################################################

from __future__ import print_function

import time
import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    from tkFileDialog import askopenfilename 
        
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    from tkinter.filedialog import askopenfilename   


import os
import re
import numpy as np

from scipy import stats

from scipy.fftpack import fft

from scipy.signal import lfilter
from math import pi,cos,sin,tan,sqrt

import matplotlib.pyplot as plt

from matplotlib.ticker import ScalarFormatter

###############################################################################

def loglog_plot(f,a,xlab,ylab,f1,f2,title_string,fig_num):

    plt.ion() 

    plt.close(fig_num)        
    plt.figure(fig_num)            
        
    plt.plot(f,a)
    plt.title(title_string)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.grid(which='both')
    plt.xscale('log')
    plt.yscale('log')
        
    if(abs(f1-10)<0.5 and abs(f2-2000)<4):
            
        ax=plt.gca().xaxis
        ax.set_major_formatter(ScalarFormatter())
        plt.ticklabel_format(style='plain', axis='x', scilimits=(f1,f2))    
              
        extraticks=[10,2000]
        plt.xticks(list(plt.xticks()[0]) + extraticks) 

        
    if(abs(f1-20)<0.5 and abs(f2-2000)<4):
            
        ax=plt.gca().xaxis
        ax.set_major_formatter(ScalarFormatter())
        plt.ticklabel_format(style='plain', axis='x', scilimits=(f1,f2))    
              
        extraticks=[20,2000]
        plt.xticks(list(plt.xticks()[0]) + extraticks)                
        
        
    plt.xlim([f1,f2])        
        
    plt.show()

    fig_num=fig_num+1

    return fig_num

###############################################################################

def interpolate_psd(f,a,s,df):
    
    fmax=max(f)
    
    num=len(f)
    
    i=0
    
    fi=[]
    ai=[]
    
    while(1): 	

        nf=f[0]+df*i
        
        if( nf > fmax ):
            break
        else:
            fi.append(nf)
            i+=1
   
    m=len(fi)
    
    jf=0
    
    for i in range(0,m):
    
        for j in range (jf,num-1):
            
#            print(' i=%d j=%d m=%d num=%d' %(i,j,m,num))
		
            if( ( fi[i] >= f[j] ) and ( fi[i] <= f[j+1] )  ):
                
                q=a[j]*( ( fi[i] / f[j] )**s[j] )
					
                ai.append(q)
                
                jf=j                 
                
                break
    
    return fi,ai
    
###############################################################################    

def spectral_moments_constant_df(fi,aa_psd,df):
    
    m0=0
    m1=0
    m2=0
    m4=0

    for j in range (0,len(fi)):
	
        m0=m0+aa_psd[j]
        m1=m1+aa_psd[j]*fi[j]
        m2=m2+aa_psd[j]*fi[j]**2
        m4=m4+aa_psd[j]*fi[j]**4


    m0=(m0*df)
    m1=(m1*df)
    m2=(m2*df)
    m4=(m4*df)

    vo=sqrt(m2/m0)
    vp=sqrt(m4/m2)

    return m0,m1,m2,m4,vo,vp

###############################################################################

def half_cosine_fade_perc(y,fper):

    fper=fper/100.

    n=len(y)

    na=int(np.ceil(fper*n))
    nb=n-na
    delta=n-1-nb
    
#    print( 'n=%d na=%d nb=%d fper=%g'  %(n,na,nb,fper))

    for i in range(0,na):
        arg=pi*(( (i-1)/float(na-1) )+1) 
        y[i]=y[i]*0.5*(1+(cos(arg)))


    for i in range(nb,n):
        arg=pi*( (i-nb)/float(delta) )
        y[i]=y[i]*(1+cos(arg))*0.5
            
    return y    


###############################################################################

def mean_filter_hpf(num,y,dt,fc):
    sr=1./dt

    n=num
    a=y
    
    a-=np.mean(a)
 
    maxw=np.floor(float(n)/10.)    
    
    q=0.728*(sr/fc)
            
    w= 2*np.floor(q/2.)+1
    
    while(w>maxw):
        w-=2 
    
    if(w<3):
        w=3
 
    k=int(np.floor(float(w-1)/2.))
    

 
    last=n
 
    print("w=%ld last=%ld  k=%ld" %(w,last,k)) 
 
    b=np.zeros(n) 
 
    for i in range(0,last):
 
        ave=0.
        n=0
 
        for j in range ((i-k),(i+k)):
 
            if(j>=0 and j<last ):
 
                ave+=a[j]
                n+=1
        
        if(n>=1):
            b[i]=ave/float(n)
 
    yy=y-b
                
    return yy,b  # hpf

###############################################################################

def integrate_th(num,b,dt):
    
    v=np.zeros(num,'f')    
    
    v[0]=b[0]*dt/2.

    for i in range(1,int(num-1)):
        v[i]=v[i-1]+b[i]*dt
    
    v[num-1]=v[num-2]+b[num-1]*dt/2.
            
    return v        
            
###############################################################################
            
def differentiate_th(num,b,dt):

    ddt=12.*dt
    
    v=np.zeros(num,'f')

    v[0]=( -b[2]+4.*b[1]-3.*b[0] )/(2.*dt)
    v[1]=( -b[3]+4.*b[2]-3.*b[1] )/(2.*dt)

    for i in range (2,int(num-2)):
        v[i]=( -b[i+2] +8.*b[i+1] -8.*b[i-1] +b[i-2] ) / ddt
    
    v[num-2]=( b[num-2]-b[num-4] )/(2.*dt)
    v[num-1]=( b[num-2]-b[num-3] )/dt      

    return v         

###############################################################################

def read_one_column_from_dialog(label,pt):
    """
    Prompt the user for the input filename.
    The input file must have one column.
    The input file may have an arbitrary number of header and blank lines.
    Return the column as array b.
    Return the total numbers of lines as num.
    """

    while(1):

        input_file_path = askopenfilename(parent=pt,title=label)

        file_path = input_file_path.rstrip('\n')
#
        if not os.path.exists(file_path):
            print ("This file doesn't exist")
#
        if os.path.exists(file_path):
            print ("This file exists")
            print (" ")
            infile = open(file_path,"rb")
            lines = infile.readlines()
            infile.close()

            b = []
            num=0
            for line in lines:
#
                if sys.version_info[0] == 3:            
                    line = line.decode(encoding='UTF-8') 
                    
                if re.search(r"(\d+)", line):  # matches a digit
                    iflag=0
                else:
                    iflag=1 # did not find digit
#
                if re.search(r"#", line):
                    iflag=1
#
                if iflag==0:
                    line=line.lower()
                    if re.search(r"([a-d])([f-z])", line):  # ignore header lines
                        iflag=1
                    else:
                        line = line.replace(","," ")
                        b.append(float(line))
                        num=num+1
            break;

            b=np.array(b)

            print ("\n samples = %d " % num)
            
    return b,num

###############################################################################

def read_two_columns_from_dialog(label,pt):
    """
    Read data from file using a dialog box
    """ 
    while(1):

        input_file_path = askopenfilename(parent=pt,title=label)

        file_path = input_file_path.rstrip('\n')
#
        if not os.path.exists(file_path):
            print ("This file doesn't exist")
#
        if os.path.exists(file_path):
            print ("This file exists")
            print (" ")
            infile = open(file_path,"rb")
            lines = infile.readlines()
            infile.close()

            a = []
            b = []
            num=0
            for line in lines:
#
                if sys.version_info[0] == 3:            
                    line = line.decode(encoding='UTF-8') 
            
                if re.search(r"(\d+)", line):  # matches a digit
                    iflag=0
                else:
                    iflag=1 # did not find digit
#
                if re.search(r"#", line):
                    iflag=1
#
                if iflag==0:
                    line=line.lower()
                    if re.search(r"([a-d])([f-z])", line):  # ignore header lines
                        iflag=1
                    else:
                        line = line.replace(","," ")
                        col1,col2=line.split()
                        a.append(float(col1))
                        b.append(float(col2))
                        num=num+1
            break

            a=np.array(a)
            b=np.array(b)

            print ("\n samples = %d " % num)
            
    return a,b,num
    
###############################################################################

def read_three_columns_from_dialog(label,pt):
    """
    Read data from file using a dialog box
    """ 
    while(1):

        input_file_path = askopenfilename(parent=pt,title=label)

        file_path = input_file_path.rstrip('\n')
#
        if not os.path.exists(file_path):
            print ("This file doesn't exist")
#
        if os.path.exists(file_path):
            print ("This file exists")
            print (" ")
            infile = open(file_path,"rb")
            lines = infile.readlines()
            infile.close()

            a = []
            b = []
            c = []
            
            num=0
            for line in lines:
#
                if sys.version_info[0] == 3:            
                    line = line.decode(encoding='UTF-8') 
            
                if re.search(r"(\d+)", line):  # matches a digit
                    iflag=0
                else:
                    iflag=1 # did not find digit
#
                if re.search(r"#", line):
                    iflag=1
#
                if iflag==0:
                    line=line.lower()
                    if re.search(r"([a-d])([f-z])", line):  # ignore header lines
                        iflag=1
                    else:
                        line = line.replace(","," ")
                        col1,col2,col3=line.split()
                        a.append(float(col1))
                        b.append(float(col2))
                        c.append(float(col3))
                        num=num+1
            break

            a=np.array(a)
            b=np.array(b)
            c=np.array(c)            

            print ("\n samples = %d " % num)
            
    return a,b,c,num
    
################################################################################

def sample_rate_check(a,b,num,sr,dt):
    dtmin=1e+50
    dtmax=0

    srmin=1./dt
    srmax=1./dt

    for i in range(1, num-1):
        diffA=a[i]-a[i-1]
        if diffA<dtmin:
            dtmin=diffA
        if diffA>dtmax:
            dtmax=diffA

    print ("  dtmin = %8.4g sec" % dtmin)
    print ("     dt = %8.4g sec" % dt)
    print ("  dtmax = %8.4g sec \n" % dtmax)

    if(dtmin>1.0e-20):    
        srmax=float(1./dtmin)
 
    if(dtmax>1.0e-20):   
        srmin=float(1./dtmax)

    print ("  srmax = %8.4g samples/sec" % srmax)
    print ("     sr = %8.4g samples/sec" % sr)
    print ("  srmin = %8.4g samples/sec" % srmin)

    if((srmax-srmin) > 0.01*sr):
        print(" ")
        print(" Warning: sample rate difference ")
#        sr = None
#        while not sr:
#            try:
#                print(" Enter new sample rate ")
#                s = stdin.readline()
#                sr=float(s)
#                dt=1/sr
#            except ValueError:
#                print ('Invalid Number')
    return sr,dt

################################################################################

def WriteData2(nn,aa,bb,output_file_path):
    """
    Write two columns of data to an external ASCII text file
    """
    output_file = output_file_path.rstrip('\n')
    outfile = open(output_file,"w")
    

    if(len(bb)==len(aa)):
        nn=len(aa)
        
        for i in range (0, nn):
            outfile.write(' %11.7e \t %8.4e \n' %  (aa[i],bb[i]))
        outfile.close()
    else:
        print(' length error' )        

################################################################################

def WriteData3(nn,aa,bb,cc,output_file_path):
    """
    Write three columns of data to an external ASCII text file
    """
    outfile = open(output_file_path,"w")
    for i in range (0, nn):
        outfile.write(' %8.4e \t %8.4e \t %8.4e \n' %  (aa[i],bb[i],cc[i]))
    outfile.close()
    

def WriteData5(nn,aa,bb,cc,dd,ee,output_file_path):
    """
    Write five columns of data to an external ASCII text file
    """
    outfile = open(output_file_path,"w")
    for i in range (0, nn):
        outfile.write(' %8.4e \t %8.4e \t %8.4e \t %8.4e \t %8.4e \n' %  (aa[i],bb[i],cc[i],dd[i],ee[i]))
    outfile.close()    
    
################################################################################    

def signal_stats(a,b,num):
    """
    a is the time column.
    b is the amplitude column.
    num is the number of coordinates
    Return
          sr - sample rate
          dt - time step
        mean - average
          sd - standard deviation
         rms - root mean square
        skew - skewness
    kurtosis - peakedness
         dur - duration
    """
    sr=0.
    dt=0.
    ave=0.
    sd=0.
    rms=0.
    skewness=0.
    kurtosis=0.
    dur=0.    
    
    if(len(b)==0):
        print('\n ** Error: len(b)=0 ** \n')
        return sr,dt,ave,sd,rms,skewness,kurtosis,dur
    
    bmax=max(b)
    bmin=min(b)

    ave = np.mean(b)

    dur = a[num-1]-a[0];

    dt=dur/float(num-1)
    sr=1/dt


    rms=np.sqrt(np.var(b))
    sd=np.std(b)

    skewness=stats.skew(b)
    kurtosis=stats.kurtosis(b,fisher=False)
    
    mb=max([bmax,abs(bmin)])
    
    crest=mb/sd

    print ("\n max = %8.4g  min=%8.4g \n" % (bmax,bmin))

    print ("         mean = %8.4g " % ave)
    print ("      std dev = %8.4g " % sd)
    print ("          rms = %8.4g " % rms)
    print ("     skewness = %8.4g " % skewness)
    print ("     kurtosis = %8.4g " % kurtosis)
    print (" crest factor = %8.4g " % crest)

    print ("\n  start = %8.4g sec  end = %8.4g sec" % (a[0],a[num-1]))
    print ("    dur = %8.4g sec \n" % dur)
    return sr,dt,ave,sd,rms,skewness,kurtosis,dur

###############################################################################

class BUTTERWORTH:

    def __init__(self,l,f,fh,fl,dt,iband,iphase,y):
    
        self.l=l
        self.f=f
        self.freq=f
        self.fh=fh
        self.fl=fl
        self.dt=dt
        self.iband=iband
        self.iphase=iphase
        self.y=y
        
        self.om=0
        
        self.a=np.zeros((4,4),'f')	
        self.b=np.zeros((4,4),'f')
        
        self.alpha=np.zeros(2*self.l,'f')
        
        self.s=(1+1j)*np.zeros(20,'f')
        
        self.ns=len(y)
        
        self.ik=0
        
        self.yt=np.zeros(self.ns,'f')        
        
            
    def Butterworth_filter_main(self):
        

        if(self.iband !=3):
            BUTTERWORTH.coefficients(self)
    
        if(self.iband == 1 or self.iband ==2):
            BUTTERWORTH.applymethod(self)

        if(self.iband == 3):
            self.f=self.fh
            self.freq=self.f
            
            print("\n Step 1")
            self.iband=2
    
            BUTTERWORTH.coefficients(self)
            BUTTERWORTH.applymethod(self)

            self.f=self.fl
            self.freq=self.f

            print("\n Step 2")
            self.iband=1
    
            BUTTERWORTH.coefficients(self)
            BUTTERWORTH.applymethod(self)   
            
        return self.y        
            
    @classmethod    
    def coefficients(cls,self):
    
        self.a=np.zeros((4,4),'f')	
        self.b=np.zeros((4,4),'f')		
    
#*** normalize the frequency ***

        targ=pi*self.f*self.dt   # radians
    
        print (" targ = %8.4g " %targ)
             
        self.om=tan(targ)   
    
        print("   om = %8.4g " %self.om)

#*** solve for the poles *******

        BUTTERWORTH.poles(self)

#*** solve for alpha values ****

        print("\n alpha ")    
    
        self.alpha=np.zeros(2*self.l,'f')
        self.alpha=2*self.s.real
    
##    for i in range(0,len(alpha)):
##        print ("  %5.3f +j %5.3f " %(alpha[i].real,alpha[i].imag))

#*** solve for filter coefficients **

        if( self.iband == 1 ):
            BUTTERWORTH.lco(self)
        else:
            BUTTERWORTH.hco(self)
    
#*** plot digital transfer function **

#    dtrans();

#*** check stability ****************
    
        BUTTERWORTH.stab(self)
    
    
    
    @classmethod
    def applymethod(cls,self):
        
        if(self.iphase==1):
            self.apply(self)
            self.apply(self) 
        else:	
            self.apply(self)
        
    

    @classmethod
    def stage1(cls,self):
             
        self.yt=np.zeros(self.ns,'f')

        bc=self.b[self.ik][0:3]
        ac=self.a[self.ik][0:3]
        ac[0]=1
    
        self.yt=lfilter(bc, ac, self.y, axis=-1, zi=None)      


 
    @classmethod
    def stage2(cls,self):
    
        self.y=np.zeros(self.ns,'f')
    
        bc=self.b[self.ik][0:3]
        ac=self.a[self.ik][0:3]
        ac[0]=1

        self.y=lfilter(bc, ac, self.yt, axis=-1, zi=None)  
    
        
    @classmethod
    def apply(cls,self):
        
        BUTTERWORTH.coefficients(self)
 
    
        if(self.iphase==1):	

            yr=np.zeros(self.ns,'f')
            for i in range(0,int(self.ns)):
                yr[self.ns-1-i]=self.y[i]

            self.y=yr
            

#  cascade stage 1

        print("\n  stage 1")
        self.ik=1
        BUTTERWORTH.stage1(self)

#  cascade stage 2

        print("  stage 2");
        self.ik=2
        BUTTERWORTH.stage2(self);
       
#  cascade stage 3

        print("  stage 3");
        self.ik=3
        BUTTERWORTH.stage1(self);
    
        self.y=self.yt

    

    @classmethod	
    def stab(cls,self):
    
        a1=0
        d1=0 
        d2=0 
        d3=0
        dlit=0

        at1=0
        at2=0
        als=0.5e-06
        h2=0

        als*=6.
    
        print ("\n stability reference threshold= %14.7e " %als)

        for i in range(1,int((self.l/2)+1)):
        
            at1= -self.a[i][1]
            at2= -self.a[i][2]

#       print("\n\n stability coordinates: (%12.7g, %14.7g) ",at1,at2);
        
            h2=at2
 
            a1=h2-1.
            d3=at1-a1
         
            a1=1.-h2
            d2=a1-at1
            d1=at2+1.
		
#       print("\n d1=%14.5g  d2=%14.5g  d3=%14.5g",d1,d2,d3);

            dlit=d1

            if(dlit > d2):
                dlit=d2
            if(dlit > d3):
                dlit=d3

            print ("\n stage %ld     dlit= %14.5g " %(i, dlit))

            if(dlit > als):
                print (" good stability")  			
				
            if( (dlit < als) and (dlit > 0.)):		  
                print(" marginally unstable ");
            
            if(dlit < 0.):
                print (" unstable ")	  	
                print ("\n")

################################################################################  
    @classmethod	
    def lco(cls,self):
    
        om2=self.om**2

        for k in range(1,int((self.l/2)+1)):
    
            den = om2-self.alpha[k-1]*self.om+1.
		
            self.a[k][0]=0.
            self.a[k][1]=2.*(om2 -1.)/den
            self.a[k][2]=( om2 +self.alpha[k-1]*self.om+ 1.)/den

            self.b[k][0]=om2/den
            self.b[k][1]=2.*self.b[k][0]
            self.b[k][2]=self.b[k][0]

            print ("\n filter coefficients")		
            print (" a[%i][1]=%10.5g  a[%i][2]=%10.5g" %(k,self.a[k][1],k,self.a[k][2]))
            print (" b[%i][0]=%10.5g  b[%i][1]=%10.5g  b[%i][2]=%10.5g" %(k,self.b[k][0],k,self.b[k][1],k,self.b[k][2]))
    
        print ("\n")
        

################################################################################  
    @classmethod	
    def hco(cls,self):
    
        print ("\n filter coefficients")
    
        om2=self.om**2

        for k in range(1,int((self.l/2)+1)):
    
            den = om2-self.alpha[k-1]*self.om+1.    
		
            self.a[k][0]=0.
            self.a[k][1]=2.*(-1.+ om2)/den
            self.a[k][2]=( 1.+self.alpha[k-1]*self.om+ om2)/den

            self.b[k][0]= 1./den;
            self.b[k][1]=-2.*self.b[k][0]
            self.b[k][2]=    self.b[k][0]
        
            print ("\n a[%i][1]=%10.5g  a[%i][2]=%10.5g" %(k,self.a[k][1],k,self.a[k][2]))
            print (" b[%i][0]=%10.5g  b[%i][1]=%10.5g  b[%i][2]=%10.5g" %(k,self.b[k][0],k,self.b[k][1],k,self.b[k][2]))
            print ("\n")
        

################################################################################  
    @classmethod	
    def poles(cls,self):
        arg=0
#        a1=0
#        a2=complex(0.,0.)
        h=complex(0.,0.)
        theta=complex(0.,0.)
    
        self.s=(1+1j)*np.zeros(20,'f')    
    
#    print("\n  calculate print ");

        print ("\n poles ")
	
        for k in range(0,int(2*self.l)):
            arg=(2.*(k+1) +self.l-1)*pi/(2.*self.l)
            self.s[k]=cos(arg)+sin(arg)*(1j)
            print (" %4.3f  +j %4.3f " %(self.s[k].real,self.s[k].imag))
         
        for i in range(0,201):   
            arg = i/40.        
        
            h=complex( self.s[0].real,( arg - self.s[0].imag  ))

        for j in range(1,int(self.l)):
            
            theta=complex( -self.s[j].real,( arg - self.s[j].imag ))
            
            temp=h*theta
            h=temp
               
            x=1/h
            h=x
               
#            a1 = self.freq*arg
	   
#            a2=abs(h)            
           
#            a3 = a2**2
            
#            fprint(pFile[3]," %lf %lf %lf \n", a1, a2, a3);     
            
###############################################################################

def DSS_waveform_reconstruction(t,accel,dt,first,freq,ffmin,ffmax,omega,damp,iunit,\
                                     nt,nfr,ac,bc,duration,nwavelets,nwtrials):

    tp=2*np.pi

    ac,bc=SRS_coefficients(damp,omega,dt)

    M=len(accel)
    residual=np.zeros(M)
    residual[:]=accel
        
    del accel
        
    num2=M

    print(" number of input points= %d " %num2)

    sr=1./dt

    print(" sample rate = %10.4g   duration=%8.4g sec\n" %(sr,duration))

    fl=3./duration
    fu=sr/10.

    print(" fl = %9.4g Hz   fu = %9.4g Hz  nfr=%ld  num2=%ld\n" %(fl,fu,nfr,num2))


    x1r=np.zeros(nwavelets)
    x2r=np.zeros(nwavelets)
    x3r=np.zeros(nwavelets)
    x4r=np.zeros(nwavelets)
    i1r=np.zeros(nwavelets)
    i2r=np.zeros(nwavelets) 
    
    errormax=1.0e+53     
        
    te2=float(0.)

    start = time.time()        
        
    for ie in range(0,nwavelets):

        if(ie>=1):
            end = time.time()
            elapsed = end - start
            
            time_per_wavelet=elapsed/(float(ie))
            
            remaining=(nwavelets-ie+1)*time_per_wavelet            
            
            print(" ")
            
            m, s = divmod(elapsed, 60)
            h, m = divmod(m, 60)
            print("  Elapsed time = %d hr %02d min %02d sec" % (h, m, s))   
            
            m, s = divmod(remaining, 60)
            h, m = divmod(m, 60)
            print("Remaining time = %d hr %02d min %02d sec  for phase 2" % (h, m, s))  
                
            te2=elapsed
            
            print(" ") 


        print("\n frequency case %d " %ie)
            
            
        
        x1r,x2r,x3r,x4r,i1r,i2r,yyr,errormax=DSS_wgen(t,residual,duration,\
                    x1r,x2r,x3r,x4r,i1r,i2r,fl,fu,nt,ie,ffmax,first,nwtrials,errormax)
        
        
 #           print(" amp=%10.4f   freq=%10.3f Hz   nhs=%d   delay=%10.4f " %(x1r[ie],x2r[ie]/tp,x3r[ie],x4r[ie]))        
        
        if(x2r[ie]<fl*tp):
            x2r[ie]=fl*tp
            x1r[ie]=1.0e-20    
            x3r[ie]=3
            x4r[ie]=0
                
#          print(" amp=%10.4f   freq=%10.3f Hz   nhs=%d   delay=%10.4f " %(x1r[ie],x2r[ie]/tp,x3r[ie],x4r[ie]))  
                
##         t1=x4r[ie] + t[0]        
        
##         for i in range(int(i1r[ie]), int(i2r[ie]+1)):

##             arg=x2r[ie]*(t[i]-t1)  
##             y=x1r[ie]*np.sin(arg/float(x3r[ie]))*np.sin(arg)   

##             residual[i]-=y
         
##        residual=original-running_sum
         
        residual-=yyr
         
        ave=np.mean(residual) 
        sd=np.std(residual)

        print(" ave=%12.4g  sd=%12.4g \n\n" %(ave,sd))
        
    NW=len(x1r)
    wavelet_table=np.zeros([NW,7])        
        
    for na in range(0,NW):
        wavelet_table[:,0]=na
        
    wavelet_table[:,1]=x1r   
    wavelet_table[:,2]=x2r/tp
    wavelet_table[:,3]=x3r 
    wavelet_table[:,4]=x4r 
    wavelet_table[:,5]=i1r 
    wavelet_table[:,6]=i2r         

    acceleration,velocity,displacement,srs_syn,srs_syn_abs =\
                 generate_wavelets_from_table(t,wavelet_table,iunit,ac,bc,freq)


    return acceleration,velocity,displacement,srs_syn,srs_syn_abs,wavelet_table,te2
 
##############################################################################

def SRS_function(last,acc,ac,bc):

    yy=acc
    xmax=np.zeros(last)
    xmin=np.zeros(last)
    xabs=np.zeros(last)
              
    for j in range(0,last):
            
#  bc coefficients are applied to the excitation
                             
        resp=lfilter(bc[j,:], ac[j,:], yy, axis=-1, zi=None)            

        xmax[j]= max(resp)
        xmin[j]= abs(min(resp)) 
        xabs[j]= max( xmax[j],xmin[j])

       
    for j in range(0,last):
           
        if(abs(xmin[j]) <1.0e-90):
            print("  warning: abs(xmin[%ld])=%8.4g " %(j,xmin[j]))
            break
    
        if(abs(xmax[j]) <1.0e-90):
            print("  warning: abs(xmax[%ld])=%8.4g " %(j,xmax[j]))
            break

    return xmin,xmax,xabs
 
 
##############################################################################


def DSS_wgen(t,residual,duration,x1r,x2r,x3r,x4r,i1r,i2r,fl,fu,nt,ie,ffmax,first,nwtrials,errormax):

    tp=2*np.pi
        
    num2=len(residual)
        
    yyr=np.zeros(num2)   
        
    min_delay=0.1*first

    ave=np.mean(residual)   
    sd=np.std(residual)

    asd=np.zeros([num2])

    for i in range(0,num2):
        asd[i]=(residual[i]**2)

#    aca=np.zeros(num2)
#    aca=np.cumsum(asd)

    am=np.max(abs(residual))
        
    print(" ave=%8.4g  sd=%8.4g  am=%8.4g nt=%ld num2=%ld  errormax=%8.4g" %(ave,sd,am,nt,num2,errormax))
          

    noct=np.log(fu/fl)/np.log(2.)

    print("\n  Trial     Error      Amplitude   Freq(Hz)   NHS    delay(sec) ")
    
#    if(np.random.rand()<0.5):
#        xx2=fl*2**(noct*np.random.rand())    
#    else:
#        xx2=(fu-fl)*np.random.rand()+fl
    
#    tmax=max(t)
    
#######    fff=fft_peak(t,residual)

#    noo=2.   
#    flower=xx2/noo
#    fupper=xx2*noo
        
#    if(flower<fl):
#        flower=fl
#    if(fupper>fu):
#        fupper=fu
        
    flower=fl
    fupper=fu    
    
    errormax=1.0e+90  # leave here

    for j in range(0,nwtrials):

        ran1=np.random.rand()
        ran2=np.random.rand()  
        ran3=np.random.rand()
               
        x1=np.random.rand()
        x33=np.random.rand()
        x4=np.random.rand()
            
        xa=np.random.rand()

        x1=(am*(x1-0.5)*xa)/2.    # amplitude
            
        if(abs(x1)<am/100.):
            x1=((x1)/abs(x1))*am/100.
            
#            print("r1 x1=%8.4g" %x1)
            
        if(np.random.rand()<0.5):
            x2=((fu-fl)*np.random.rand()+fl)   # freq
        else:
            x2=fl*2**(noct*np.random.rand())
                
        x2*=tp       
    
#        x2=fl*2**(noct*np.random.rand()
        
#        x2=((fupper-flower)*np.random.rand() + flower)*tp    
        
        if(np.random.rand()<0.8):
            x3= 3+int(2*round(x33*30))    # nhs
        else:
            x3= 3+int(2*round(x33*8))             

        x4=x4*((0.6*duration)**2) + min_delay     # delay

###
        if(abs(x1r[ie])<1.0e-20 and j>=1):
            x1/=10.
            
        if(abs(x1r[ie])>1.0e-20 and np.random.rand()>0.9):

            if(ran1>0.4 and ran1<=0.5 and j>100):
                       
                x2=x2r[ie]*(0.99+0.02*np.random.rand())
                x4=x4r[ie]*(0.99+0.02*np.random.rand())

            if(ran2<=0.25):
                x3=x3r[ie]-4
           
            if(ran2>0.25 and ran2<=0.5):
                x3=x3r[ie]-2
        
            if(ran2>0.50 and ran2<=0.75):
                x3=x3r[ie]+2
        
            if(ran2>0.75 and ran2<=1.0):
                x3=x3r[ie]+4
                x1=x1r[ie]*(0.95+0.10*np.random.rand())

            if(ran3>0.5):
                x1=-x1
        
            if(x3<3):
                x3=3
                
#             print("r2 x1=%8.4g" %x1)    
#      itype=2  % mainly NHS

            if(ran1>0.5 and ran1<=0.6 and j>100):  
           
               x1=x1r[ie]*(0.98+0.04*np.random.rand())
               x2=x2r[ie]
               x3=x3r[ie]
               x4=x4r[ie]

#               itype=3 % amp  
    
            if(ran1>0.6 and ran1<=0.7 and j>100):
           
               x1=x1r[ie]
               x2=x2r[ie]*(0.99+0.02*np.random.rand())    
               x3=x3r[ie]
               x4=x4r[ie]
               
#               itype=4  % freq
    
#             print("r3 x1=%8.4g" %x1)    
    
            if(ran1>0.8 and ran1<=0.9 and j>100):
           
               x1=x1r[ie]
               x2=x2r[ie]
               x3=x3r[ie]
               x4=x4r[ie]*(0.99+0.02*np.random.rand())

#               itype=5  % delay
    
            if(ran1>0.9 and ran1<=1. and j>100):
           
               x1=x1r[ie]*(0.999+0.002*np.random.rand())
               x2=x2r[ie]*(0.999+0.002*np.random.rand())
               x3=x3r[ie]
               x4=x4r[ie]*(0.999+0.002*np.random.rand())

#               itype=6  % all but NHS
###
          
        while(1):

            if( tp*x3/(2.*x2) + x4 < duration ):
                break
            else:
                x3=x3-2
                  
        if(x3==1):
            x1=0
            x2=fu*tp
            x3=3
            x4=0

        if(j==0 or x3 < 3):
            x1=0.
            x2=fu*tp
            x3=3
            x4=0.
    
        error=0.

        t1=x4 + t[0]
        t2=t1 + tp*x3/(2.*x2)

        if(j==0):
            x1=0.

        if( (x2/tp)<fl or x3 < 3):
            x2=((ffmax-fl)*np.random.rand() + fl)*tp
            x3=3
            x4=0.
    
        if( (x2/tp)>ffmax):
            x2=((ffmax-fl)*np.random.rand() + fl)*tp
            x3=3
            x4=0.
    
        if(x4<min_delay):
            x4=min_delay
                
#            print("r4 x1=%8.4g" %x1)    

        index1=int(np.round(t1/duration)*num2)-1
        index2=int(np.round(t2/duration)*num2)-1
        
        if(index1<0):
            index1=0

        
        
        x3=float(x3)
    
        xf=x2/tp
        if(xf<flower or xf>fupper):
            x2=((fupper-flower)*np.random.rand() + flower)*tp
     
        if(j>=1 and abs(x1)<1.0e-06):
            x1=am/100.
            
            if(np.random.rand()<0.5):
                x1=-x1
                
        yy=np.zeros(num2)
        
##        arg=np.zeros(num2)    
        
####        arg[index1:index2]=x2*(t[index1:index2]-t1)
        
####        yy[index1:index2]=x1*np.sin(arg[index1:index2]/x3)*np.sin(arg[index1:index2])    

####        error=sum(abs(residual-yy))            

#        e1=2*sum(asd[0:index1])

        for i in range(0,num2):
       
            if( t[i]>= t1 and t[i] <= t2):
                index1=i
                break
       
        for i in range(0,num2):
       
            if( t[i]>= t1 and t[i] <= t2):
                index2=i
              
            if(t[i]>t2):    
                break

###        e1=2.*aca[index1]

#        e2=np.zeros(num2)
        
        alpha=np.zeros(num2)
        beta=np.zeros(num2)
        
        apb=np.zeros(num2)
        amb=np.zeros(num2)
                
        beta[index1:index2]=x2*(t[index1:index2]-t1)
        alpha[index1:index2]=beta[index1:index2]/x3        
           
        apb[index1:index2]=alpha[index1:index2]+beta[index1:index2]   
        amb[index1:index2]=alpha[index1:index2]-beta[index1:index2]          
        
##        for i in range(index1,index2):
##            yy[i]=sina[i]*sinb[i]

        yy[index1:index2]=(x1/2.)*( -np.cos(apb[index1:index2]) + np.cos(amb[index1:index2]))

#        e3=sum(asd[index2:num2])  
     
##        arg[index1:index2]=x2*(t[index1:index2]-t1)
##        yy[index1:index2]=x1*np.sin(arg[index1:index2]/x3)*np.sin(arg[index1:index2])    

##        e2=sum(np.square(residual-yy))   
  
#        e2[index1:index2]=((abs(residual[index1:index2]-yy[index1:index2])))


#####        yv=residual-yy
        
####        error=sum(np.square( (residual-yy) ))
                
        error=np.sum(np.abs(residual-yy) )

####        e22=sum(np.square(((abs(residual[index1:index2]-yy[index1:index2])))))


#        e22=sum(np.square(((abs(yv)))))

     
###        e3=aca[num2-1]-aca[index2]
     
####        error=e1+e22+e3     
     
##        if(t2<tmax):
##    
##            for i in range(0,num2):
##        
##                if( t[i]>= t1 and t[i] <= t2):
##                    arg=x2*(t[i]-t1)  
##                
##                    yy[i]=x1*np.sin(arg/x3)*np.sin(arg)
##
##                    error+=((abs(residual[i]-yy[i]))**2.)
##                else:
##                    if(t[i]<first):
##                        error+=2*asd[i]
##                    else:
##                        error+=asd[i]                  
##        else:
##            error=1.0e+90
          
##        print("    %d     %9.4e   %9.4f   %9.4f   %d   %9.4f " %(j,error,x1,x2/tp,x3,x4))

        if(error<=errormax and x2>=(fl*tp )):

            x1r[ie]=x1
            x2r[ie]=x2
            x3r[ie]=x3
            x4r[ie]=x4
            i1r[ie]=index1
            i2r[ie]=index2                
            yyr=yy
            
            
 #               print("  %d   %12.6e   %12.6e  %12.6e " %(j,errormax,error,errormax-error))        

            print(" %d  %d  %12.6e  %9.4f  %9.4f  %d   %9.4f " %(ie,j,error,x1,x2/tp,x3,x4))
                
            errormax=error
                
#                print("len(t)=%ld len(y)=%ld  num2=%ld" %(len(t),len(yy),num2))   
                
#        print("   ie=%d     %9.4e   %9.4f   %9.4f   %d   %9.4f " %(ie,error,x1r[ie],x2r[ie]/tp,x3r[ie],x4r[ie]))              
    
    return x1r,x2r,x3r,x4r,i1r,i2r,yyr,errormax 
   
###############################################################################      

def SRS_coefficients(damp,omega,dt):
    
    N=len(omega)    
    
    ac=np.zeros([N,3])     
    bc=np.zeros([N,3])
        
    for j in range(0,N):
            
        omegad=omega[j]*np.sqrt(1.-(damp**2))

#  bc coefficients are applied to the excitation
            
        E=np.exp(-damp*omega[j]*dt)
        K=omegad*dt
        C=E*np.cos(K)
        S=E*np.sin(K)
        Sp=S/K

   
        ac[j,0]=1.   
        ac[j,1]=-2.*C
        ac[j,2]=+E**2   
        
        bc[j,0]=1.-Sp
        bc[j,1]=2.*(Sp-C)
        bc[j,2]=E**2-Sp
        
#            print("   ",E,K,C,S,Sp)

    return ac,bc 

def fft_peak(t,a):
        
#   Truncate to 2**n

    num=len(a)

    noct=int(np.log(num)/np.log(2.))

    num_fft=2**noct

    bb=a[0:num_fft]
        

    dur_fft=t[num_fft-1]-t[0]

    df=1/dur_fft
      
    z =fft(bb)

    nhalf=num_fft/2

#        print (" ")
#        print (" %d samples used for FFT " %num_fft)
#        print ("df = %8.4g Hz" %df)

    zz=np.zeros(nhalf,'f')
    ff=np.zeros(nhalf,'f')

    freq=np.zeros(num_fft,'f')

    z/=float(num_fft)

    for k in range(0,int(num_fft)):
        freq[k]=k*df
    
    ff=freq[0:nhalf]
        
    
    for k in range(0,int(nhalf)):    

        if(k > 0):			 
            zz[k]=2.*abs(z[k])
        else:    
            zz[k]= abs(z[k])
  

    idx = np.argmax(abs(zz)) 
        
    fft_freq=ff[idx]
  
    return fft_freq       
        
def linear_fade_out(ns,ratio,acc):

    nk=int(np.round(ratio*ns))
    LLL=ns-nk-1
                
                        
    for i in range(nk,ns):
        x=(i-nk)
        acc[i]*=(1.-(float(x)/float(LLL)))
        
        acc[ns-1]=0.   
                
    return acc
    
def srs_title_string(Q):
        
    title_string= 'Shock Response Spectrum Q='+str(Q)     

    for i in range(1,200):
        if(Q==float(i)):
            title_string= 'Shock Response Spectrum Q='+str(i)
            break
    return title_string
    
def tolerance_3dB(b):

    w=2.**(0.5)

    MM=len(b)
        
    tol1=np.zeros(MM)      # must do the long way
    tol2=np.zeros(MM)
        
    for i in range(0,MM):
        bb=float(b[i])
        tol1[i]=w*bb
        tol2[i]=bb/w   
            
    return tol1,tol2   

def calculate_slope_loglog(f,a):  

    n=len(f)      

    slope=np.zeros(n)

    for i in range(0,(n-1)):    
        slope[i]=np.log(a[i+1]/a[i])/np.log(f[i+1]/f[i])
              
    return slope
         
def generate_wavelets_from_table(t,wavelet_table,iunit,ac,bc,freq):
    
    num2=len(t)
    nwavelets=len(wavelet_table[:,0])
    tpi=2.*np.pi
     
    aaa=np.zeros([num2,1]) 
    vvv=np.zeros([num2,1]) 
    ddd=np.zeros([num2,1]) 

    vlast=np.zeros([num2,1])

    iscale=1
    
    x1r=np.zeros(nwavelets)
    x2r=np.zeros(nwavelets)
    x3r=np.zeros(nwavelets)
    x4r=np.zeros(nwavelets)    
    i1r=np.zeros(nwavelets)
    i2r=np.zeros(nwavelets)   
    
    x1r[:]=wavelet_table[:,1]
    x2r[:]=wavelet_table[:,2]*tpi
    x3r[:]=wavelet_table[:,3]
    x4r[:]=wavelet_table[:,4]    
    i1r[:]=wavelet_table[:,5]  
    i2r[:]=wavelet_table[:,6]        

    for k in range(0,num2):

        tt=t[k]
 
        for j in range(0,nwavelets):

            w=0.
            v=0.
            d=0.

            t1=x4r[j]+t[0]

            
#            t2=tp*x3r[j]/(2.*x2r[j])+t1 

            if( k>=int(i1r[j]) and k <= int(i2r[j])  ):   

                arg=x2r[j]*(tt-t1)  

                w=  x1r[j]*np.sin(arg/float(x3r[j]))*np.sin(arg)

                aa=x2r[j]/float(x3r[j])
                bb=x2r[j]

                te=tt-t1

                alpha1=aa+bb
                alpha2=aa-bb

                alpha1te=alpha1*te
                alpha2te=alpha2*te   

                v1= -np.sin(alpha1te)/(2.*alpha1)
                v2= +np.sin(alpha2te)/(2.*alpha2)

                d1= +(np.cos(alpha1te)-1)/(2.*(alpha1**2))
                d2= -(np.cos(alpha2te)-1)/(2.*(alpha2**2))

                v=(v2+v1)*iscale*x1r[j]
                d=(d2+d1)*iscale*x1r[j]

                vlast[j]=v

                aaa[k]=aaa[k]+w 
                vvv[k]=vvv[k]+v
                ddd[k]=ddd[k]+d
                                

    if(iunit==0):
        vvv=vvv*386
        ddd=ddd*386
        
    if(iunit==1):    
        vvv=vvv*9.81*100
        ddd=ddd*9.81*1000
        
    if(iunit==2):
        vvv=vvv*100
        ddd=ddd*1000       
            
####        aaa=running_sum    

####    print("  %ld  %ld" %(len(t),len(aaa)))

    acceleration=np.column_stack((t,aaa))
    velocity=np.column_stack((t,vvv))
    displacement=np.column_stack((t,ddd))

    last=len(ac[:,0])

    xmin,xmax,xabs=SRS_function(last,acceleration[:,1],ac,bc)

    srs_syn=np.column_stack((freq, xmax, xmin))     
        
    srs_syn_abs=np.column_stack((freq, xabs))

    return acceleration,velocity,displacement,srs_syn,srs_syn_abs                                                  