#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:38:24 2021

@author: rizal
"""
import pandas as pd
import numpy as np
from datetime import timedelta, datetime 
import csv, urllib
import pytz
#import collections

class getprocess():
    def __init__(self, data_features=[]):
        self.srcpath = '/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/'
        self.lastdate=datetime.strptime('2019-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.tzone = pytz.timezone('Asia/Jakarta')
        self.data_features = data_features
        
    def datetime_range(self, start, end, delta):
        current = start
        while current < end:
            yield current 
            current += delta
        
        return
        
    def download(self):
        #Download flux 10.7 internet, satu hari pengamatan akan menghasilkan 2 - 5 data
        #https://lasp.colorado.edu/lisird/latis/dap/penticton_radio_flux.csv?&time>=2008-01-01T00:00:00.000Z&time<=2018-12-31T06:53:00.000Z&format_time(yyyy-MM-dd HH:mm:ss)
        url = 'https://lasp.colorado.edu/lisird/latis/dap/penticton_radio_flux.csv?&time>=2008-01-01T00:00:00.000Z&time<=2019-01-01T06:53:00.000Z&format_time(yyyy-MM-dd_HH:mm:ss)'
        df = pd.read_csv(url, delimiter=',')
        sfu = df['adjusted_flux (solar flux unit (SFU))']
        fmt="{0:.2f}"
        self.dateobs = [datetime.strptime(tobs.split('_')[0], '%Y-%m-%d') for tobs in df['time (yyyy-MM-dd_HH:mm:ss)']]
        self.timeobs = []
        self.sfu_mean = []
        tsfu=[]
        
        for i in range(len(self.dateobs)):
            if i == 0:
                tsfu.append(sfu[i]) 
            else:
                if self.dateobs[i] != self.dateobs[i-1]:
                    sdate = self.dateobs[i-1]
                    edate = sdate+timedelta(days=1)
                    dt=[dts for dts in self.datetime_range(sdate, edate, timedelta(minutes=60))]
                    tmean = float(fmt.format(np.mean(tsfu)))
                    for dtime in dt:
                        self.timeobs.append(dtime)
                        self.sfu_mean.append(tmean)
                    tsfu.clear()
                    tsfu.append(sfu[i])
                else:
                    tsfu.append(sfu[i])
                    if i == len(self.dateobs)-1:
                        sdate = self.dateobs[i-1]
                        edate = sdate+timedelta(days=1)
                        dt=[dts for dts in self.datetime_range(sdate, edate, timedelta(minutes=60))]
                        tmean = float(fmt.format(np.mean(tsfu)))
                        for dtime in dt:
                            self.timeobs.append(dtime)
                            self.sfu_mean.append(tmean)

        print("Panjang timeobs:",len(self.timeobs)," Panjang sfu_mean:", len(self.sfu_mean))  
                
        #print([item for item, count in collections.Counter(self.dtobs).items() if count > 1])
        #Download data Sunspot Number from internet, satu hari pengamatan akan menghasilkan 1 data.
        #http://www.sidc.be/silso/INFO/sndhemcsv.php
        self.url = 'http://www.sidc.be/silso/INFO/sndhemcsv.php'
        names = ['Year','Month','Day','Date_FracOfYear','Daily_total_SN','Daily_North_SN',\
                 'Daily_South_SN','STD_total_SN','STD_Nort_SN','STD_South_SN','N_OBS','N_OBS_Norht',\
                     'N_OBS_Sourth','Definitive_marker']
        df = pd.read_csv(self.url, delimiter=';', names=names)
        Years = df['Year']
        Months = df['Month']
        Days = df['Day']
        SSN = df['Daily_total_SN']
        
        self.ValSSN = []
        self.DtSSN=[]
        sdate = datetime.strptime('2008-01-01', '%Y-%m-%d')
        edate = datetime.strptime('2019-01-01', '%Y-%m-%d')
        
        for i in range(len(Years)):
            tmpDate = datetime.strptime(str(Years[i])+'-'+str(Months[i])+'-'+str(Days[i]), '%Y-%m-%d')
            if tmpDate >= sdate and tmpDate < edate:
                stdate = tmpDate
                endate = tmpDate+timedelta(days=1)
                dt=[dts for dts in self.datetime_range(stdate, endate, timedelta(minutes=60))]
                for dtime in dt:
                    self.ValSSN.append(SSN[i])
                    self.DtSSN.append(dtime)
            elif tmpDate > edate:
                break
        print("Panjang DtSSN:", len(self.DtSSN), " Panjang ValSSN:", len(self.ValSSN))
        
        #Get Index DST from http://wdc.kugi.kyoto-u.ac.jp menggunakan format IAGA-2002 
        # Satu hari pengamatan terdiri dari 24 data (data jaman)
        url = 'http://wdc.kugi.kyoto-u.ac.jp///dstae///wwwtmp/WWW_dstae00016126.dat'
        data = urllib.request.urlopen(url)
        self.dt_obj=[]
        self.vdst = []
        firstTime = datetime.strptime('2008-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        endTime = datetime.strptime('2018-12-31 23:00:00', '%Y-%m-%d %H:%M:%S')
        for line in data:
            lines = line.decode('utf-8').strip().split()
            try:
                dt_str = lines[0]+' '+lines[1]
                dt_utc=datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
                dt_localTime = pytz.utc.localize(dt_utc).astimezone(self.tzone).replace(tzinfo=None)
                if dt_localTime >= firstTime and dt_localTime <= endTime:
                    self.dt_obj.append(dt_localTime)
                    self.vdst.append(float(lines[-1]))
            except:
                continue
        print("Panjang dt_obj:", len(self.dt_obj), " Panjang vdst:", len(self.vdst)) 
        
        #Check tanggal pengamatan yang sama pada data Sunspot and flux 
        self.dTimeObs = list(np.intersect1d(self.DtSSN, self.timeobs))
        self.ObsDateTime=[]

        idx=[self.DtSSN.index(j) for j in self.dTimeObs]
        ixs=[self.timeobs.index(j) for j in self.dTimeObs]
     
        self.ssnflux = np.zeros([2, len(idx)])
        print("ssnflux:", self.ssnflux.shape)

        for i in range(len(idx)):
            self.ssnflux[0][i]=self.ValSSN[idx[i]]
            self.ssnflux[1][i]=self.sfu_mean[ixs[i]]
            
        print("dTimeObs:", len(self.dTimeObs), " All Value:", self.ssnflux.shape[1])
        
        #Check tanggal pengamatan yang sama pada data flux, sunspot dan dst
        self.NewdTimeObs = list(np.intersect1d(self.dTimeObs, self.dt_obj))
        idx =[self.dTimeObs.index(i) for i in self.NewdTimeObs] #Searching Index from date time flux and sunspot
        ixs =[self.dt_obj.index(i) for i in self.NewdTimeObs] ##Searching Index from date time dst
        
        self.vall=[]
        for i in range(len(idx)):
            self.vall.append({'time_tag':self.NewdTimeObs[i], 'F10.7':self.ssnflux[1][i], 'SSN':self.ssnflux[0][i],
                              'DST':self.vdst[ixs[i]]})
        
        print("Panjang vall:", len(self.vall))
        self.save2csv()
        
        return
 
    def save2csv(self):
        csvFile = open("FluxSSNDST-0818.csv", 'w', newline='')
        csvWriter = csv.writer((csvFile))
        count = 0
        for data in self.vall:
            if count == 0:
                header=data.keys()
                csvWriter.writerow(header)
                count += 1
            csvWriter.writerow(data.values())
        csvFile.close()
        """
        headers =['time_obs', 'Flux 10.7','Index DST', 'SSN']
        data=[]
        for i in range(len(timeobs)):
            data.append([timeobs[i], sfu[i], dst[i], ssn[i]])
            
        with open('FluxDSTSSN_2008_2018.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        """   
        return
    
if __name__ == '__main__':
    process = getprocess()
    process.download()
    #process.getData()