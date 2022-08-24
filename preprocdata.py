#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 13:28:21 2021

@author: rizal
"""
import os
from datetime import timedelta, datetime 
import numpy as np
import csv
import pandas as pd


class preprocdata():
    def __init__(self, sdate='2013-01-01 00:00:00', edate='2014-01-01 00:00:00', dflux=[], ddst=[], dsin=[],
                 fluxfile='/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/DATA_FLUX.xlsx',
                 dstfile='/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/DATA_DST.xlsx',
                 SRCPATH='/Volumes/Data/DSS_NAVIGASI/Data/KTB/', lstFile=[], fils4=[], rflux=[], rdst=[], rs4=[]):
        self.sdate = datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S')
        self.edate = datetime.strptime(edate, '%Y-%m-%d %H:%M:%S')
        self.fluxfile = fluxfile
        self.dstfile = dstfile
        self.dflux = dflux
        self.ddst = ddst
        self.dsin = dsin
        self.SRCPATH = SRCPATH
        self.lstFile = lstFile
        self.fils4 = fils4
        self.gendate(self.sdate, self.edate)
        self.rs4 = rs4
        self.rflux = rflux
        self.rdst = rdst
        
    def gendate(self, nsdate, nedate):
        self.dt=[dts for dts in self.datetime_range(nsdate, nedate, timedelta(minutes=60))]
        
    def datetime_range(self, start, end, delta):
        current = start
        while current < end:
            yield current 
            current += delta
        
        return

    def csv2json(self):
        frameFlux=pd.read_excel(self.fluxfile, sheet_name='data 2013')
        jams=[]
        defaultJam = ['18:00:00', '20:00:00', '23:00:00']
        #djson = []
        for i in range(3):
            wkt=datetime.strptime(defaultJam[i], '%H:%M:%S')
            jams.append(wkt.time())
            
        for i in range(len(frameFlux['Tanggal'])):
            tgl = frameFlux['Tanggal'][i]
            jam = frameFlux['Waktu'][i]
            vflux = frameFlux['Adjusted Flux'][i]
            if jam <= jams[0]:
                self.dflux.append({'time_tag':str(tgl), 'flux':vflux})
                while tgl.time() < jams[0]:
                    tgl = tgl+timedelta(hours=1)
                    self.dflux.append({'time_tag':str(tgl), 'flux':vflux})
            elif jam <= jams[1] and jam > jams[0]:
                tgl = tgl+timedelta(hours=19)
                self.dflux.append({'time_tag':str(tgl), 'flux':vflux})
                tgl = tgl+timedelta(hours=1)
                self.dflux.append({'time_tag':str(tgl), 'flux':vflux})
            elif jam <= jams[2] and jam > jams[1]:
                tgl = tgl+timedelta(hours=21)
                self.dflux.append({'time_tag':str(tgl), 'flux':vflux})
                for i in range(2):
                    tgl = tgl+timedelta(hours=1)
                    self.dflux.append({'time_tag':str(tgl), 'flux':vflux})
        '''            
        SRCPATH = '/Volumes/Data/DSS_NAVIGASI/Data/FLUX107/'
        jfile='flux_2013.json'
        with open(SRCPATH+jfile, 'w') as fout:
            json.dump(self.dflux, fout)
        '''    
        return
    
    def csv2jsondst(self):
        frameDst=pd.read_excel(self.dstfile, sheet_name='data 2013')
        for j in range(len(frameDst['Tanggal'])):
            for i in range(24):
                if i == 0:
                    idst=frameDst[24][j]
                    dateObs = frameDst['Tanggal'][j]
                    self.ddst.append({'time_tag':str(dateObs), 'index_dst':idst})
                else:
                    idst=frameDst[i][j]
                    dateObs = frameDst['Tanggal'][j]+timedelta(hours=i)
                    self.ddst.append({'time_tag':str(dateObs), 'index_dst':idst})
                    
        return
    
    def calMedian(self, dsin):
        sins4=[]
        #print(dsin)
        #for i in range(24):
        for j in range(len(dsin)-1):
            if dsin[j]['time_tag'].hour == dsin[j+1]['time_tag'].hour:
                sins4.append(dsin[j]['S4'])
            else:
                sins4.append(dsin[j]['S4'])
                sinmedian = np.mean(sins4)
                ndate = dsin[j]['time_tag']-timedelta(minutes=dsin[j]['time_tag'].minute)
                self.dsin.append({'time_tag':str(ndate), 'S4':float("{0:.2f}".format(sinmedian))})
                #print(sinmedian)
                sins4.clear()
                #break
        sins4.append(dsin[j]['S4'])
        sinmedian = np.mean(sins4)
        ndate = dsin[j]['time_tag']-timedelta(minutes=dsin[j]['time_tag'].minute)
        self.dsin.append({'time_tag':str(ndate), 'S4':float("{0:.2f}".format(sinmedian))})
        sins4.clear()
        
        return
    
    def lFileS4(self):
        files = os.listdir(self.SRCPATH)
        for file in files:
            if file.endswith('.json'):
                if int(file[0:4]) == 2013:
                    self.lstFile.append(self.SRCPATH+file)
        
        self.lstFile.sort()
        
    def readS4(self):
        sintilasi = []
        for file in self.lstFile:
            df = pd.read_json(file)
            #djson = np.array(dframe)
            for i in range(len(df)):
                tgl = df['date'][i]
                jam = datetime.strptime(df['time'][i], '%H:%M:%S')
                sidx = df['S4'][i]
                tgl = tgl+timedelta(hours=jam.hour, minutes=jam.minute)
                #print(tgl)
                sintilasi.append({'time_tag':tgl, 'S4':sidx})
            self.calMedian(sintilasi)
            sintilasi.clear()
        return
    
    def filterData(self):
        #fildst = []
        #filflux = []
        temps4 = []
        for j in range(0, len(self.dt)-24, 24):
            for i in range(len(self.dsin)):
                start_date = datetime.strptime(self.dsin[i]['time_tag'], '%Y-%m-%d %H:%M:%S')
                if start_date >= self.dt[j] and start_date <= self.dt[j+23]:
                    temps4.append(self.dsin[i])
                elif start_date > self.dt[j+23]:
                    if len(temps4) < 24:
                        temps4.clear()
                    else:
                        for ndata in temps4:
                            self.fils4.append(ndata)
                        temps4.clear()
                    break
                    
        return
    
    def crosCheckData(self):
        i=0; bc=0
        tS4=[]
        tflux=[]
        tdst=[]
        for j in self.dt:
            resS4 = next((sub for sub in self.fils4 if sub['time_tag'] == str(j)), None)
            resflux = next((sub1 for sub1 in self.dflux if sub1['time_tag'] == str(j)), None)
            resdst = next((sub2 for sub2 in self.ddst if sub2['time_tag'] == str(j)), None)
            #tS4.append(resS4) #; tflux.append(resflux); tdst.append(resdst)
            if resS4 != None:
                tS4.append(resS4)
            if resflux != None:
                tflux.append(resflux)
            if resdst != None:
                tdst.append(resdst)
            i += 1
            if i == 24:
                if len(tS4) == 24 and len(tflux) == 24 and len(tdst) == 24:
                    #print("Jumlah tgl: ", len(tS4), len(tflux), len(tdst), "No i:", i)
                    for sidx in tS4:
                        self.rs4.append(sidx)
                    for flx in tflux:
                        self.rflux.append(flx)
                    for idx in tdst:
                        self.rdst.append(idx)
                else:
                    bc += 1
                tS4.clear()
                tflux.clear()
                tdst.clear()
                i=0
        #print(tS4)
        print("data kosong: ", bc)            
        return   
    
    def save2csv(self):
        SRCPATH = '/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/'
        fileCSV = ['2013_S4.csv', '2013_flux.csv', '2013_dst.csv']
        varData = [self.rs4, self.rflux, self.rdst]
        for j in range(len(fileCSV)):
            data_file = open(os.path.join(SRCPATH, fileCSV[j]), 'w')
            csv_writer = csv.writer(data_file)
            count = 0
            for emp in varData[j]:
                if count == 0:
                    header = emp.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(emp.values())
            
            data_file.close()
        return
              
if __name__ == "__main__":
    s = preprocdata()
    s.csv2json()
    s.csv2jsondst()
    s.lFileS4()
    s.readS4()
    s.filterData()
    s.crosCheckData()
    s.save2csv()