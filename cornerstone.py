import eia
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
rcParams['axes.unicode_minus'] = False   # 用来正常显示负号

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m]

def eia_w(eia_name,name):
	EIA_API = '16efcf83a8f6f03b0d2a8ffb4f074d28'
	storageURL = 'http://api.eia.gov/series/?api_key=' + EIA_API + '&series_id=' + eia_name
	storage = requests.get(storageURL)
	storage_json = storage.json()
	date_series = storage_json['series'][0]['data']
	data_T = list(map(list, zip(*date_series)))
	df = pd.DataFrame(data=data_T[1],index=pd.to_datetime(data_T[0]),columns=[name]).sort_index()
	return df

def eia_m(eia_name,name):
	EIA_API = '16efcf83a8f6f03b0d2a8ffb4f074d28'
	storageURL = 'http://api.eia.gov/series/?api_key=' + EIA_API + '&series_id=' + eia_name
	storage = requests.get(storageURL)
	storage_json = storage.json()
	date_series = storage_json['series'][0]['data']
	data_T = list(map(list, zip(*date_series)))
	df = pd.DataFrame(data=data_T[1],index=pd.to_datetime(data_T[0],format='%Y%m', errors='coerce').dropna(),columns=[name]).sort_index()
	return df

def plot_seasonal(df,ax,units):
    idx = pd.MultiIndex.from_arrays([df.index.strftime("%V"), df.index.year])
    dg = df.set_index(idx).unstack()
    dh = df[df.index.year == 2016]
    df2 = pd.DataFrame(data=dg.values, columns=dg.columns, index=dh.index)
    df2.plot(ax=ax,colormap='RdBu')
    ax.set_facecolor('tab:gray')
    ax.set_xlabel('')
    ax.set_ylabel(''.join(df.columns.values)+'   ' +units)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend('')
    
def plot_projection_m(df,ax,units):
    df.plot(ax=ax)
    ax.set_xlabel('')
    ax.set_ylabel(''.join(df.columns.values)+'   ' +units)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend('')
    
apicode=dict(    
    CRSTKW='PET.WCESTUS1.W',
    CRNIMPW='PET.WCRNTUS2.W',
    CRUTIW='PET.WPULEUS3.W',
    GOSTKW='PET.WDISTUS1.W',
    GOPRODW='PET.WDIRPUS2.W',
    GODEMW='PET.WDIUPUS2.W',
    GOEXPW='PET.WDIEXUS2.W',
    RBSTKW='PET.WGTSTUS1.W',
    RBPRODW='PET.WGFRPUS2.W',
    RBDEMW='PET.WGFUPUS2.W',
    RBEXPW='PET.W_EPM0F_EEX_NUS-Z00_MBBLD.W',

    CRSTK1W='PET.WCESTP11.W',
    CRSTK2W='PET.WCESTP21.W',
    CRSTK3W='PET.WCESTP31.W',
    CRSTK4W='PET.WCESTP41.W',
    CRSTK5W='PET.WCESTP51.W',
    CRUTI1W='PET.W_NA_YUP_R10_PER.W',
    CRUTI2W='PET.W_NA_YUP_R20_PER.W',
    CRUTI3W='PET.W_NA_YUP_R30_PER.W',
    CRUTI4W='PET.W_NA_YUP_R40_PER.W',
    CRUTI5W='PET.W_NA_YUP_R50_PER.W',
    GOSTK1W='PET.WDISTP11.W',
    GOSTK2W='PET.WDISTP21.W',
    GOSTK3W='PET.WDISTP31.W',
    GOSTK4W='PET.WDISTP41.W',
    GOSTK5W='PET.WDISTP51.W',
    GOPROD1W='PET.WDIRPP12.W',
    GOPROD2W='PET.WDIRPP22.W',
    GOPROD3W='PET.WDIRPP32.W',
    GOPROD4W='PET.WDIRPP42.W',
    GOPROD5W='PET.WDIRPP52.W',
    RBSTK1W='PET.WGTSTP11.W',
    RBSTK2W='PET.WGTSTP21.W',
    RBSTK3W='PET.WGTSTP31.W',
    RBSTK4W='PET.WGTSTP41.W',
    RBSTK5W='PET.WGTSTP51.W',
    RBPROD1W='PET.WGFRPP12.W',
    RBPROD2W='PET.WGFRPP22.W',
    RBPROD3W='PET.WGFRPP32.W',
    RBPROD4W='PET.WGFRPP42.W',
    RBPROD5W='PET.WGFRPP52.W',

    CRSTKP='STEO.COSXPUS.M',
    CRPRODP='STEO.COPRPUS.M',
    CRNIMPP='STEO.CONIPUS.M',
    CRUTIP='STEO.ORUTCUS.M',
    GOSTKP='STEO.DFPSPUS.M',
    GOPRODP='STEO.DFROPUS.M',
    GONIMPP='STEO.DFNIPUS.M',
    GODEMP='STEO.DFTCPUS.M',
    RBSTKP='STEO.MGTSPUS.M',
    RBPRODP='STEO.MGROPUS.M',
    RBIMPP='STEO.MGNIPUS.M',
    RBDEMP='STEO.MGTCPUSX.M'
)
