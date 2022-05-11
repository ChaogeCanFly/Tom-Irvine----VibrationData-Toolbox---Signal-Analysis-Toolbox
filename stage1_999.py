# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 20:08:09 2016

@author: tom
"""

 NW=len(wavelet_table[:,0])
        num2=len(t)
        
        x1=np.zeros(NW)
        x2=np.zeros(NW)        
        x3=np.zeros(NW)
        x4=np.zeros(NW)        
        
        error_max=1.0e+90

        for ijk in range(0,5):
            
            yy=np.zeros(num2)     
            
            x1[:]=wavelet_table[:,1]
            x2[:]=wavelet_table[:,2]*tpi                
            x3[:]=wavelet_table[:,3]
            x4[:]=wavelet_table[:,4]
            
            
            for i in range(0,NW):
                
                if(ijk>=1):
                    x1[i]=wavelet_table[i,1]*(0.99+0.02*np.random.rand())
                
                index1=int(wavelet_table[i,5])
                index2=int(wavelet_table[i,6]) 
                
                t1=x4[i]+t[0]                
                
                alpha=np.zeros(num2)
                beta=np.zeros(num2)
        
                apb=np.zeros(num2)
                amb=np.zeros(num2)
                
                beta[index1:index2]=x2[i]*(t[index1:index2]-t1)
                alpha[index1:index2]=beta[index1:index2]/x3[i]        
           
                apb[index1:index2]=alpha[index1:index2]+beta[index1:index2]   
                amb[index1:index2]=alpha[index1:index2]-beta[index1:index2]          

                yy[index1:index2]+=(x1[i]/2.)*( -np.cos(apb[index1:index2]) + np.cos(amb[index1:index2]))

            xmin,xmax,xabs=SRS_function(nlf,yy,ac,bc)
            
            syn_error,iflag,db1,db2=vb_srs_damped_sine_synth.DSS_srs_error(last,xmax,xmin,ra,iflag)
            
            if(syn_error<error_max):
                error_max=syn_error
                wavelet_table[:,1]=x1  
                
                srs_syn[:,1]=xmax
                srs_syn[:,2]=xmin
                
                print(" %d  %8.4g " %(ijk,error_max))


