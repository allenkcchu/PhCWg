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

for index in indexList:
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
        
        ax_index.append(np.ones(np.size(wavelength))*index)
        ax_r.append(np.ones(np.size(wavelength))*r)
        ax_wavelength.append(wavelength)
        ax_s21.append(s21_2)
        
        ax_index2.append(np.ones(np.size(w2))*index)
        ax_r2.append(np.ones(np.size(w2))*r)
        ax_w2.append(w2)
        ax_ng.append(ng)

ax_index = np.array(flattenList(ax_index,samplingNum=5))
ax_r = np.array(flattenList(ax_r,samplingNum=5))
ax_wavelength = np.array(flattenList(ax_wavelength,samplingNum=5))
ax_s21 = np.array(flattenList(ax_s21,samplingNum=5))

ax_index2 = np.array(flattenList(ax_index2,samplingNum=5))
ax_r2 = np.array(flattenList(ax_r2,samplingNum=5))
ax_w2 = np.array(flattenList(ax_w2,samplingNum=5))
ax_ng = np.array(flattenList(ax_ng,samplingNum=5))


fig = plt.figure(figsize=(12,6))
ax1 = fig.add_subplot(121,projection='3d')
sc1 = ax1.scatter(ax_index,ax_r,ax_wavelength,s=10*(-ax_s21-(0))/(np.max(-ax_s21)-(0)),c=ax_s21,cmap='jet',vmin=-10)
fig.colorbar(sc1,ax=ax1)

ax2 = fig.add_subplot(122,projection='3d')
sc2 = ax2.scatter(ax_index2,ax_r2,ax_w2,s=10*(ax_ng/np.max(ax_ng)),c=ax_ng,cmap='jet',vmin=0)
fig.colorbar(sc2,ax=ax2)

fig.tight_layout()


    
    # fig.tight_layout()
    # fig.savefig(f'{path.split("_sweepCore")[0]}.png',transparent=True)