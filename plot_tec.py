#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 18:57:56 2021

@author: rizal
"""
import os
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd

def listfile(srcdata):
    filename = []
    sinfile = []
    files = os.listdir(srcdata)
    files.sort()
    for file in files:
        if file.endswith('.json'):
            if len(file) > 13:
                fnstr = file.split('.')
                tfile = fnstr[0].split('_')
                if tfile[1] == 'tec':
                    filename.append(srcdata+file)
            else:
                sinfile.append(srcdata+file)
    
    return filename, sinfile

def readfile():
    timeobs=[]
    stec = []
    for srcfile in filename:
        f=open(srcfile, 'r')
        djson = json.load(f)
        for vargps in djson:
            timeobs.append(datetime.strptime(vargps['time'], '%Y-%m-%d %H:%M:%S'))
            stec.append(vargps['TEC_MEDIAN'])  
        f.close()
    #Read File Scintillation
    timesin=[]
    sindex = []
    for srcfile in sinfile:
        with open (srcfile, 'r') as finput:
            dsin = json.load(finput)
            for varsin in dsin:
                timesin.append(datetime.strptime(varsin['time'], '%Y-%m-%d %H:%M:%S'))
                sindex.append(varsin['S4'])
                
    return timeobs, stec, timesin, sindex

def plotTEC():
    majorFmt = mdates.DateFormatter('%Y/%m')  
    minorFmt = mdates.DateFormatter('%Y/%m')
    fig, ax = plt.subplots()
    plt.title('Plot TEC BAKO 2008', fontsize=10 )
    plt.plot(timeobs, stec, '.', markersize=10)
    ax.xaxis.set_minor_formatter(minorFmt)
    ax.xaxis.set_major_formatter(majorFmt)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation='horizontal')
    ax.tick_params(axis='x', labelsize=10)
    
    plt.xlabel('Date')
    plt.ylabel('STEC [TECU]')
    
    plt.show()
    plt.close()
    
    return

def plotS4():
    majorFmt = mdates.DateFormatter('%Y/%m')  
    minorFmt = mdates.DateFormatter('%Y/%m')
    fig, ax = plt.subplots()
    plt.title('Plot SINTILASI BAKO 2008', fontsize=10 )
    plt.plot(timesin, sindex, '.',markersize=10)
    ax.xaxis.set_minor_formatter(minorFmt)
    ax.xaxis.set_major_formatter(majorFmt)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation='horizontal')
    ax.tick_params(axis='x', labelsize=10)
    
    plt.xlabel('Date')
    plt.ylabel('S4 Index')
    
    plt.show()
    plt.close()
    
    return

def readDST():
    obstime=[]
    idst=[]
    timeFlux=[]
    flux=[]
    
    filedst='/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/DATA_DST.xlsx'
    fileflux='/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/DATA_FLUX.xlsx'
    df = pd.read_excel(filedst, sheet_name='data 2008')
    
    for dt in range(len(df['Tanggal'])):
        
        obstime.append(df['Tanggal'][dt])
        for i in range(0, 24):
            if i == 0:
                idst.append(df[24][dt])
            else:
                idst.append(df[i][dt])
                obstime.append(df['Tanggal'][dt]+timedelta(hours=i))
    
    dfFlux =  df = pd.read_excel(fileflux, sheet_name='data 2008')
    for x in range(len(dfFlux['Tanggal'])):
        timeFlux.append(dfFlux['Tanggal'][x]+timedelta(hours=dfFlux['Waktu'][x].hour))
        flux.append(dfFlux['Observed flux'][x])
                
    return obstime, idst, timeFlux, flux

def plotDST():
    majorFmt = mdates.DateFormatter('%Y/%m')  
    minorFmt = mdates.DateFormatter('%Y/%m')
    fig, ax = plt.subplots()
    plt.title('Plot DST 2008', fontsize=10 )
    plt.plot(obstime, idst, '.',markersize=10)
    ax.xaxis.set_minor_formatter(minorFmt)
    ax.xaxis.set_major_formatter(majorFmt)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation='horizontal')
    ax.tick_params(axis='x', labelsize=10)
    
    plt.xlabel('Date')
    plt.ylabel('Index DST')
    
    plt.show()
    plt.close()
    
    return

def plotFlux():
    majorFmt = mdates.DateFormatter('%Y/%m')  
    minorFmt = mdates.DateFormatter('%Y/%m')
    fig, ax = plt.subplots()
    
    plt.title('Plot Flux 2008', fontsize=10 )
    plt.plot(timeFlux, flux, '.',markersize=10)
    ax.xaxis.set_minor_formatter(minorFmt)
    ax.xaxis.set_major_formatter(majorFmt)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation='horizontal')
    ax.tick_params(axis='x', labelsize=10)
    
    plt.xlabel('Date')
    plt.ylabel('Flux')
    
    plt.show()
    plt.close()
    
    return

if __name__=='__main__':
    srcpath='/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/2008/'
    filename, sinfile = listfile(srcpath)
    timeobs, stec, timesin, sindex = readfile()
    plotTEC()
    plotS4()
    obstime, idst, timeFlux, flux = readDST()
    plotDST()
    plotFlux()