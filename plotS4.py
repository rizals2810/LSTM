import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime as dt 

filename='/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/FLuxSSNDSTS4_0813.csv'
df = pd.read_csv(filename, delimiter=',')
S4Index = df['S4'].values
S4Index = S4Index.tolist()
datetimeobs = df['time_tag'].values.astype('datetime64[s]')
dtobs = [dt.datetime.strptime(str(date), '%Y-%m-%dT%H:%M:%S') for date in datetimeobs]
#tobs = [dt.datetime.strptime(str(date), '%Y-%m-%dT%H:%M:%S') for date in datetimeobs]
dateObs = []
S4=[]
for tgl in dtobs:
    if tgl.year == 2008:
        i = dtobs.index(tgl)
        dateObs.append(tgl)
        S4.append(S4Index[i])
        
#dateObs = [tgl for tgl in dtobs if tgl.year == 2008]
tobs=[]
for i in range(24):
    if i < 10:
      tobs.append(dt.datetime.strptime("0"+str(i)+":00:0", "%H:%M:%S"))
    else:
        tobs.append(dt.datetime.strptime(str(i)+":00:00", "%H:%M:%S"))
        
sIndex=np.zeros([24, len(dateObs)])
for i in range(len(dateObs)):
    x = dtobs[i].hour
    sIndex[x][i] = S4[i]
    
fig, ax = plt.subplots()
    
#pos = ax.contourf(self.dtObs, self.dt, self.arrSin, 40, cmap='jet')
pos = ax.contourf(dateObs, tobs, sIndex, 5, cmap='jet')
cb = fig.colorbar(pos, ax=ax)
cb.set_label(r'S4 Index')
    
ax.set_xlabel("Month")
ax.set_ylabel("Universal Time")
ax.xaxis.set_major_formatter(DateFormatter('%b'))
ax.yaxis.set_major_formatter(DateFormatter('%H'))
plt.title("S4")

 
plt.show()
plt.close()