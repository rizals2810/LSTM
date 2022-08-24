import julian
from datetime import datetime, timedelta
import os
import numpy as np
import json

class FirstProcess():
    '''
    def __init__(self, s4VarPRN=[], s4Var=[], 
                 srcdata='/Volumes/DATA 1/data_bako_gopi_asnawi/data_TEC_cmnBAKO/2012/', 
                 filename=[],dt=[]):
        self.s4VarPRN = s4VarPRN
        self.s4Var = s4Var
        self.srcdata = srcdata
        self.filename = filename
        self.dt = dt
        self.genPRN()
    '''
   
    def __init__(self, srcdata='/Volumes/DATA 1/data_bako_gopi_asnawi/data_TEC_cmnBAKO/2018/', 
                 filename=[],dt=[], tecmed=[]):
        self.tecmed = tecmed
        self.srcdata = srcdata
        self.filename = filename
        self.dt = dt
        self.genPRN()  
    
    def genPRN(self):
        self.gps = {}
        for i in range(1, 33):
            self.gps[i]=[]
            
    def datetime_range(self, start, end, delta):
        current = start
        while current < end:
            yield current 
            current += delta
    
    def medianS4(self, dtfile):
        datefile = datetime.strftime(dtfile, "%Y%m%d")
        collects4=[]
        allcols4=[]
        
        for x in range(len(self.dt)-1):
            for prn in range(1, 33):
                for dgps in self.gps[prn]:
                    if dgps['time'] >= self.dt[x] and dgps['time'] < self.dt[x+1]:
                        collects4.append(dgps['S4'])
                        allcols4.append(dgps['S4'])
                    elif dgps['time'] >= self.dt[x] and dgps['time'] > self.dt[x+1]:
                        break
                if len(collects4) != 0:
                    means4 = np.mean(collects4)
                    self.s4VarPRN.append({'time':str(self.dt[x]), 'PRN':prn, 'S4':means4})
                    collects4=[]
            if len(allcols4) != 0:
                allmeans4 = np.mean(allcols4)
                self.s4Var.append({'time':str(self.dt[x]), 'S4':allmeans4})
                allcols4.clear()
            
        with open(self.srcdata+datefile+"_prn.json", "w") as fout:
            json.dump(self.s4VarPRN, fout)
        
        with open(self.srcdata+datefile+".json", "w") as fout:
            json.dump(self.s4Var, fout)
            
        return
    
    def medianTEC(self, dtfile):
        datefile = datetime.strftime(dtfile, "%Y%m%d")
        collectTEC=[]
        
        for x in range(len(self.dt)-1):
            for prn in range(1, 33):
                for dgps in self.gps[prn]:
                    if dgps['time'] >= self.dt[x] and dgps['time'] < self.dt[x+1]:
                        collectTEC.append(dgps['STEC'])
                    elif dgps['time'] >= self.dt[x] and dgps['time'] > self.dt[x+1]:
                        break
            if len(collectTEC) != 0:
                meanTEC = np.mean(collectTEC)
                self.tecmed.append({'time':str(self.dt[x]), 'TEC_MEDIAN':meanTEC})
                collectTEC=[]
                #print("Nilai TEC: ", self.tecmed)
            
        with open(self.srcdata+datefile+"_tec.json", "w") as fout:
            json.dump(self.tecmed, fout)
            
        
        return
    
    def listfile(self):
        files = os.listdir(self.srcdata)
        files.sort()
        for file in files:
            if file.endswith('.Cmn'):
                self.filename.append(self.srcdata+file)
        
        return
    
    def readFile(self):
        for srcfile in self.filename:
            print("Reading Filename: {}".format(srcfile))
            f=open(srcfile, 'r')
            for line in f:
                if len(line) != 1:
                    gpsVar = line.strip().split()
                    if gpsVar[0] == 'bako,':
                        continue
                    elif gpsVar[0] == 'MJdatet':
                        continue
                    elif gpsVar[0] == '-6.49105':
                        continue
                    elif gpsVar[0] == '-6.49106':
                        continue
                    elif gpsVar[0] == '-6.49107':
                        continue
                    else:
                        mjd = float(gpsVar[0]) 
                        obstime_str = datetime.strftime(julian.from_jd(mjd, fmt='mjd'),'%Y-%m-%d %H:%M:%S')
                        obsTime = datetime.strptime(obstime_str, '%Y-%m-%d %H:%M:%S')
                        prn = '0'+ gpsVar[2] if int(gpsVar[2]) < 10 else str(gpsVar[2]) 
                        stec = float(gpsVar[7]) 
                        vtec = float(gpsVar[8]) 
                        s4 = 0.0 if float(gpsVar[9]) == -99.0 else float(gpsVar[9])
                        self.gps[int(gpsVar[2])].append({'time':obsTime, 'PRN':prn, 'STEC':stec, 'VTEC':vtec, 'S4':s4})
            f.close()
            start = obsTime - timedelta(hours=obsTime.hour, minutes=obsTime.minute, seconds=obsTime.second, microseconds=obsTime.microsecond)
            end = start + timedelta(days=1, hours=1)
            self.dt=[dts for dts in self.datetime_range(start, end, timedelta(hours=1))]
            #self.medianS4(start)
            #self.s4VarPRN.clear()
            #self.s4Var.clear()
            self.medianTEC(start)
            self.tecmed.clear()
            #break
            for i in range(1, 33):
                self.gps[i].clear()
            
        return
        
if __name__ == '__main__':
    s = FirstProcess()
    s.listfile()
    s.readFile() 
        