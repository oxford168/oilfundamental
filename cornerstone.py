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
    
def plot_seasonal_m(df,ax,units):
    idx = pd.MultiIndex.from_arrays([df.index.month, df.index.year])
    df.set_index(idx).unstack().plot(ax=ax,colormap='RdBu')
    ax.set_facecolor('tab:gray')
    ax.set_xlabel('')
    ax.set_ylabel(''.join(df.columns.values)+'   ' +units)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend('')