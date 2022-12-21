#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:22:15 2022

@author: allenchu
"""

import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import os
import re

def flattenList(lst,samplingNum=1):
    tmp = list()
    N = 0
    for i in lst:
        for ii in i:
            if N%samplingNum == 0:
                tmp.append(ii)
            N = N+1
               
    return tmp

plt.close('all')
path = 'BandEdgeSweep'

fileList = list()
dfile = list()
for root,dirs,files in os.walk(os.path.join(os.getcwd(),path)):
    for filename in files:
        if filename.endswith('.mat'):
            # fileList.append(filename)
            params = re.findall('BandEdgeSweep_a(.*)_r(.*)_n(.*)_sx(.*)_sy(.*)_ssx(.*)_ssy(.*).mat',filename)
            a = float(params[0][0])
            r = float(params[0][1])
            n = float(params[0][2])/100
            sx = float(params[0][3])
            sy = float(params[0][4])
            ssx = float(params[0][5])
            ssy = float(params[0][6])
            dfile.append([a, r, n, sx, sy, ssx, ssy, filename])
            
dfile = pd.DataFrame(dfile,columns=['LatticeConstant','Radius','Index',
                                  's1x','s1y','s2x','s2y','filename'])
            

a = 420
s1x = 0
s1y = 0
s2x = 0
s2y = 0

indexList = sorted(dfile.Index.unique())
rList = sorted(dfile.Radius.unique())
ax_index = list()
ax_index2 = list()
ax_r = list()
ax_r2 = list()
ax_wavelength = list()
ax_w2 = list()
ax_s21 = list()
ax_ng = list()

index=2.7
for r in rList:
    fileanme = dfile[(dfile.LatticeConstant == a) & (dfile.Index == index) & (dfile.Radius == r)].filename.values[0]
    
    data = dict()
    f = h5py.File(os.path.join(path,fileanme))
    for k, v in f.items():
        data[k] = np.array(v)
    
    wavelength = np.squeeze(data['wavelength'])*1e9
    w2 = np.squeeze(data['l2'])*1e9
    s21_2 = 10*np.log10(np.squeeze(data['s21']['real']**2+data['s21']['imag']**2))
    ng = np.squeeze(data['ng'])
    
    ax_r.append(r)
    
    ax_s21.append(s21_2)
    ax_ng.append(ng)
    

ax_s21 = np.array(ax_s21)
ax_ng = np.array(ax_ng)
ax_r = np.array(ax_r)

fig, ax = plt.subplots(ncols=2,nrows=1,sharex=True,sharey=True)

# fig = plt.figure(figsize=(12,6))
# ax1 = fig.add_subplot(121,projection='3d')
sc1 = ax[0].contourf(wavelength,ax_r,ax_s21,cmap='jet',levels=np.linspace(-50,0,101))
fig.colorbar(sc1,ax=ax[0])
ax[0].grid(True)

# ax2 = fig.add_subplot(122,projection='3d')
sc2 = ax[1].contourf(w2,ax_r,ax_ng,cmap='jet',levels=np.linspace(0,20,101))
fig.colorbar(sc2,ax=ax[1])
ax[1].grid(True)

# fig.tight_layout()


        # if N == 0:
        #     s21_2 = np.squeeze(data['s21']['real']**2+data['s21']['imag']**2)
        #     ng = np.squeeze(data['ng'])
        # else:
        #     s21_2 = np.vstack((s21_2, np.squeeze(data['s21']['real']**2+data['s21']['imag']**2)))
        #     ng = np.vstack((ng, np.squeeze(data['ng'])))
    
    # selectIndex = 272
    # loc = np.where(indexList == selectIndex)
    
    # fig, ax = plt.subplots(ncols=2,nrows=2,sharex=True,sharey=False,figsize=(8,6))
    # cs0 = ax[0,0].contourf(wavelength*1e9,indexList/100,10*np.log10(s21_2),cmap='jet')
    # ax[0,0].set_xlabel('Wavelength (nm)')
    # ax[0,0].set_ylabel(r'$Si_7N_3$ refractive index')
    
    # fig.colorbar(cs0, ax=ax[0,0], shrink=0.9)
    # cs1 = ax[1,0].contourf(w2*1e9,indexList/100,ng,cmap='jet')
    # fig.colorbar(cs1, ax=ax[1,0], shrink=0.9)
    # ax[1,0].set_xlabel('Wavelength (nm)')
    # ax[1,0].set_ylabel(r'$Si_7N_3$ refractive index')
    
    
    # ax[0,1].plot(wavelength*1e9,10*np.log10(np.squeeze(s21_2[loc,:])))
    # ax[0,1].set_xlabel('Wavelength (nm)')
    # ax[0,1].set_ylabel('Intensity (dB)')
    # ax[0,1].set_title(r'$n_{Si_7N3}$='+f'{selectIndex/100}')
    
    # ax[1,1].plot(w2*1e9,np.squeeze(ng[loc,:]))
    # ax[1,1].set_xlabel('Wavelength (nm)')
    # ax[1,1].set_ylabel(r'Group index $n_g$')
    # ax[1,1].set_title(r'$n_{Si_7N_3}$='+f'{selectIndex/100}')