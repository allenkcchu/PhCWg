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
path = 's1sweep_a210_n270_r125'

fileList = list()
dfile = list()
for root,dirs,files in os.walk(os.path.join(os.getcwd(),path)):
    for filename in files:
        if filename.endswith('.mat'):
            # fileList.append(filename)
            params = re.findall('s1sweep_a(.*)_r(.*)_n(.*)_sx(.*)_sy(.*)_ssx(.*)_ssy(.*).mat',filename)
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
r = 125
index = 2.7

s2x = 0
s2y = 0

s1xList = sorted(dfile.s1x.unique())
s1yList = sorted(dfile.s1y.unique())

for s1x in s1xList:
    ax_s1x = list()
    ax_s1y = list()
    ax_wavelength = list()
    ax_w2 = list()
    ax_s21 = list()
    ax_ng = list()
    
    for s1y in s1yList:
        
        fileanme = dfile[(dfile.LatticeConstant == a) & (dfile.Index == index) & (dfile.Radius == r) & (dfile.s1x == s1x) & (dfile.s1y == s1y)].filename.values[0]
        
        data = dict()
        f = h5py.File(os.path.join(path,fileanme))
        for k, v in f.items():
            data[k] = np.array(v)
        
        wavelength = np.squeeze(data['wavelength'])*1e9
        w2 = np.squeeze(data['l2'])*1e9
        s21_2 = 10*np.log10(np.squeeze(data['s21']['real']**2+data['s21']['imag']**2))
        ng = np.squeeze(data['ng'])
        
        ax_s1y.append(s1y)
        
        ax_s21.append(s21_2)
        ax_ng.append(ng)
        
    
    ax_s21 = np.array(ax_s21)
    ax_ng = np.array(ax_ng)
    ax_s1y = np.array(ax_s1y)
    
    # fig, ax = plt.subplots(ncols=2,nrows=1,sharex=True,sharey=True)
    
    
    # sc1 = ax[0].contourf(wavelength,ax_s1y,ax_s21,cmap='jet',vmin=-100,vmax=0)
    # fig.colorbar(sc1,ax=ax[0])
    # ax[0].grid(True)
    # ax[0].set_ylabel('s1_yshift')
    
    
    # sc2 = ax[1].contourf(w2,ax_s1y,ax_ng,cmap='jet',vmin=0,vmax=20)
    # fig.colorbar(sc2,ax=ax[1])
    # ax[1].grid(True)
    # ax[0].set_ylabel('s1_yshift')
    
    # fig.tight_layout()


for s1y in s1yList:
    ax_s1x = list()
    ax_s1y = list()
    ax_wavelength = list()
    ax_w2 = list()
    ax_s21 = list()
    ax_ng = list()
    for s1x in s1xList:
        
        fileanme = dfile[(dfile.LatticeConstant == a) & (dfile.Index == index) & (dfile.Radius == r) & (dfile.s1x == s1x) & (dfile.s1y == s1y)].filename.values[0]
        data = dict()
        f = h5py.File(os.path.join(path,fileanme))
        for k, v in f.items():
            data[k] = np.array(v)
        
        wavelength = np.squeeze(data['wavelength'])*1e9
        w2 = np.squeeze(data['l2'])*1e9
        s21_2 = 10*np.log10(np.squeeze(data['s21']['real']**2+data['s21']['imag']**2))
        ng = np.squeeze(data['ng'])
        
        ax_s1x.append(s1x)
        
        ax_s21.append(s21_2)
        ax_ng.append(ng)
        
    
    ax_s21 = np.array(ax_s21)
    ax_ng = np.array(ax_ng)
    ax_s1x = np.array(ax_s1x)
    
    fig, ax = plt.subplots(ncols=2,nrows=1,sharex=True,sharey=True)
    
    
    sc1 = ax[0].contourf(wavelength,ax_s1x,ax_s21,cmap='jet')
    fig.colorbar(sc1,ax=ax[0])
    ax[0].grid(True)
    
    
    sc2 = ax[1].contourf(w2,ax_s1x,ax_ng,cmap='jet')
    fig.colorbar(sc2,ax=ax[1])
    ax[1].grid(True)
