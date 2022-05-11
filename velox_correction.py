###########################################################################
# program: velox_correction.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.3
# date: October 10, 2016
#
# description: velocity & displacement correction for psd synthesis  
#
###########################################################################

from __future__ import print_function


from vb_utilities import BUTTERWORTH

from scipy.optimize import curve_fit

from numpy import zeros,linspace,pi,cos

from scipy import signal



def func(x, a, b, c, d):
    return a+b*x+c*(x**2)+d*(x**3)
    
   

def integrate_time_history(A,dt):
    """
    integrate time history
    
    A=input array
    B=output array
    
    dt=time step
    """

    n=len(A)    
    
    B=zeros(n,float)
    
    B[0]=A[0]*dt/2
       
    for i in range (1,n-1):    
        B[i]= B[i-1] +  A[i]*dt
       
    B[n-1]=B[n-2]+A[n-1]*dt/2
    
    return B

    
def differentiate_time_history(A,dt):
    """
    integrate time history
    
    A=input array
    B=output array
    
    dt=time step
    """
    ddt=12.*dt
    
    n=len(A)
#
    B=linspace(0,n*dt,n);
#
    B[0]=( -A[2]+4.*A[1]-3.*A[0] )/(2.*dt)
    B[1]=( -A[3]+4.*A[2]-3.*A[1] )/(2.*dt)
    
    B[2:(n-2)]=(-A[4:n]+8*A[3:(n-1)]-8*A[1:(n-3)]+A[0:(n-4)])/ddt
    
    B[n-2]=( +A[n-1]-A[n-3] )/(2.*dt)
    B[n-1]=( +A[n-1]-A[n-2] )/dt
    
    return B    


def velox_correction(acc,dt,f1):
    """
    velocity & displacement correction for psd synthesis 
    """
    n=len(acc)
#
###########################################################################      
#       

    x= linspace(0, (n - 1) * dt, n)

    acc = signal.detrend(acc, axis=-1, type='linear', bp=0)

    v=integrate_time_history(acc,dt)
    
#    v = signal.detrend(v, axis=-1, type='linear', bp=0)

#       
###########################################################################       

    popt, pcov = curve_fit(func, x, v)
   
    v-=(popt[0] + popt[1]*x + popt[2]*x**2+ popt[3]*x**3)

    l=6
    f=f1/2
    fh=f
    fl=0
    iband=2
    iphase=2

    v=BUTTERWORTH(l,f,fh,fl,dt,iband,iphase,v).Butterworth_filter_main()
       
###########################################################################       
#       
    perc=1.2
    nn=int(round(n*perc/100))
    
    nnf=float(nn)

    for i in range (0,nn):       
        ratio=(i-1)/nnf
        
        arg=pi*(ratio+1.);
        ratio=0.5*(1.+cos(arg))
        
        v[i]*=ratio
         
    j=0
     
    for i in range ((n-nn),n):
        ratio=1-(j/nnf)
        arg=pi*(ratio+1)
        ratio=0.5*(1.+cos(arg))             
        
        v[i]*=ratio
        j+=1
#
    dispx= integrate_time_history(v,dt)
#
###########################################################################
#
    velox=v
#
    acc=differentiate_time_history(velox,dt)
#
###########################################################################
#
    velox*=386
    dispx*=386       
       
    return acc,velox,dispx