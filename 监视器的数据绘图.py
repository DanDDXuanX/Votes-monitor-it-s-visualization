import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.font_manager import FontProperties
import sys
myfont = FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf')

# ### IO

I_path=sys.argv[1]
O_path=sys.argv[2]

def sep_(Series,sep):
    i=0
    dict={'':None}
    while i<len(Series):
        dict[i]=Series[i]
        i+=sep
    return pd.Series(dict)

if I_path.split(sep='.')[-1] in ['csv','txt']:                       #如果输入是路径
    data=pd.read_csv(I_path,encoding='gbk',index_col='Unnamed: 0')
else:                                                                #否则就是目录
    os.listdir(I_path)
    data=None
    for file in os.listdir(I_path):
        filepath=I_path+'\\'+file
        data_this=pd.read_csv(filepath,encoding='gbk',index_col='Unnamed: 0')
        if data is None:
            data=data_this
        else:
            data=pd.concat([data,data_this],axis=0)#,sort=False

data=data.drop_duplicates(keep='first',subset='time')
data.index=range(0,len(data))

try:
    keep=int(sys.argv[5]) #keep<=len(full_time.columns[1:])

except:
    keep=0     #default 0 = all
if keep>(len(data.columns)-1):
    keep=0

# ### 生成数字时间

time_d={}
for key,item in data['time'].iteritems():
    try:
        time_d[key]=time.mktime(time.strptime(item,'%Y-%m-%d %H:%M'))
    except:
        time_d[key]=time.mktime(time.strptime(item,'%Y/%m/%d %H:%M'))
        pass
time_d=pd.Series(time_d)
time_d=(time_d-time_d.min())/60
data['dtime']=time_d.astype(int)
data=data.drop_duplicates(keep='first',subset='dtime')
data=data.set_index('dtime')

# ### 补全表时间

full_time=pd.DataFrame(index=range(int(data.index.min()),int(data.index.max())))
full_time=pd.merge(full_time,data,left_index=True,right_index=True,how='left')

try:
    recent=bool(int(sys.argv[4]))
except:
    recent=False     #default

if recent==True:
    if len(full_time)<240:
        pass
    else:
        full_time=full_time.iloc[-240:]
        full_time.index=range(0,len(full_time))

# ### 线性插值

absence=[]
for name in full_time.columns[1:]:
    name_Series=pd.Series(full_time[name])
    time_values={}
    i=0
    while i<len(name_Series):
        if name_Series[i]>=0:
            time_values[i]=name_Series[i]
            i+=1
        elif i==0:
            for j in range(0,len(name_Series)):
                if name_Series[j]>=0:
                    i=j
                    break
        else:
            for j in range(i,len(name_Series)):
                if name_Series[j]>=0:
                    a=(name_Series[j]-name_Series[i-1])/(j-i+1)
                    break
            absence.append((i,j))
            for k in range(i,j):
                time_values[k]=time_values[k-1]+a
            i=j
    full_time[name]=pd.Series(time_values)
absence=set(absence)


# ### 求增长率

grow_rate=pd.DataFrame(None)
grow_rate['time']=full_time['time']
for name in full_time.columns[1:]:
    name_Series=pd.Series(full_time[name])
    time_values={0:np.nan}
    for j in range(0,len(name_Series)):
        if name_Series[j]>=0:
            i=j+1
            break
    while i<len(name_Series):
        time_values[i]=name_Series[i]-name_Series[i-1]
        i+=1
    grow_rate[name]=pd.Series(time_values)


# ### 边界范围
if keep==0:
    labels=full_time.columns[1:]
else:
    labels=full_time.iloc[-1,1:].sort_values(ascending=False).index[0:keep]

min_y=np.nanmin(full_time[labels].values.flatten())
max_y=np.nanmax(full_time[labels].values.flatten())
f_min_y=min_y-(max_y-min_y)*0.2
f_max_y=max_y+(max_y-min_y)*0.2
min_y=np.nanmin(grow_rate[labels].values.flatten())
max_y=np.nanmax(grow_rate[labels].values.flatten())
g_min_y=0
try:
    g_max_y=int(sys.argv[3])
except:
    g_max_y=max_y+(max_y-min_y)*0.2     #default

min_x=0
max_x=len(full_time)


# ### 绘图

if recent==True:
    figwide=15
else:
    figwide=len(full_time)/75

plt.figure(figsize=(figwide,15))
ax=plt.subplot(1,1,1)
line=[]
for name in labels:
    line_this,=ax.plot(full_time.index,full_time[name],linewidth=2)
    line.append(line_this)
ax.set_xlim(min_x,max_x)
ax.set_ylim(f_min_y,f_max_y)
ax.xaxis.set_major_locator(MultipleLocator(240))
ax.xaxis.set_ticklabels(ticklabels=sep_(full_time.time,240))
ax.xaxis.set_minor_locator(MultipleLocator(60))
ax.xaxis.grid(True, which='major',alpha=0.5)
ax.xaxis.grid(True, which='minor',alpha=0.2)
ax.yaxis.grid(True, which='major',alpha=0.5)
plt.title('票数走势',fontproperties=myfont,fontsize=20)
legend_name=labels
plt.legend(line,legend_name,prop=myfont)
for item in absence:
    ax.plot(list(item),[f_min_y*1.007,f_min_y*1.007],color=(1,0,0),linewidth=5)
    
plt.savefig(O_path+r'/票数走势.png')
plt.close()

plt.figure(figsize=(figwide,15))
ax=plt.subplot(1,1,1)
line=[]
for name in labels:
    line_this,=ax.plot(grow_rate.index,grow_rate[name],linewidth=1.5)
    line.append(line_this)
ax.set_xlim(min_x,max_x)
ax.set_ylim(g_min_y,g_max_y)
ax.xaxis.set_major_locator(MultipleLocator(240))
ax.xaxis.set_ticklabels(ticklabels=sep_(grow_rate.time,240))
ax.xaxis.set_minor_locator(MultipleLocator(60))
ax.xaxis.grid(True, which='major',alpha=0.5)
ax.xaxis.grid(True, which='minor',alpha=0.2)
ax.yaxis.grid(True, which='major',alpha=0.5)
plt.title('增长量/min',fontproperties=myfont,fontsize=20)
legend_name=labels
plt.legend(line,legend_name,prop=myfont)
for item in absence:
    ax.plot(list(item),[g_max_y*0.997,g_max_y*0.997],color=(1,0,0),linewidth=5)
    
plt.savefig(O_path+r'/增长率.png')
plt.close()

print('OK')