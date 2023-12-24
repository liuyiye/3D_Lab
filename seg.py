import numpy as np
import slicer
from sklearn.cluster import KMeans


def t1(num=3):
    mask_node=slicer.util.getNode('mask')
    mask=slicer.util.arrayFromVolume(mask_node)
    
    t1_node=slicer.util.getNode('t1')
    t1=slicer.util.arrayFromVolume(t1_node)
    T1WI_node=slicer.modules.volumes.logic().CloneVolume(slicer.mrmlScene,t1_node,'T1WI')
    
    km=num  #按照脑组织信号强度分为3组
    array=t1[mask>0]
    cls=KMeans(n_clusters=km).fit_predict(array.reshape(-1,1)) #cls值为0，1，2
    
    t1_km=t1.copy()
    t1_km[:]=133 #为了与mask外的0区分开
    t1_km[mask>0]=cls
    
    km_means=[t1[t1_km==i].mean() for i in range(km)]  #各组的均值
    km_order=np.argsort(km_means)
    
    t1_km_sorted=t1_km.copy()
    for i in range(km):
        t1_km_sorted[t1_km==i]=km_order[i]#按照均值大小，重新赋值
    
    t1_km_sorted=t1_km_sorted+1
    t1_km_sorted[t1_km_sorted==134]=0
    slicer.util.updateVolumeFromArray(T1WI_node,t1_km_sorted*100)
    
    #t1_max=np.zeros_like(t1)
    #t1_max[t1_km==km_order[-1]]=1  #均值最大组的t1_km值,脑白质信号强度最高，排在最后
    #slicer.util.updateVolumeFromArray(T1WI_node,t1_max*100)


def flair(num=4):
    mask_node=slicer.util.getNode('mask')
    mask=slicer.util.arrayFromVolume(mask_node)
    
    flair_node=slicer.util.getNode('flair')
    flair=slicer.util.arrayFromVolume(flair_node)
    FLAIR_node=slicer.modules.volumes.logic().CloneVolume(slicer.mrmlScene,flair_node,'FLAIR')
    
    km=num  #按照脑组织信号强度分为4组
    array=flair[mask>0]
    cls=KMeans(n_clusters=km).fit_predict(array.reshape(-1,1)) #cls值为0，1，2，3
    
    f_km=flair.copy()
    f_km[:]=133 #为了与mask外的0区分开
    f_km[mask>0]=cls
    
    km_means=[flair[f_km==i].mean() for i in range(km)]  #各组的均值
    km_order=np.argsort(km_means)

    f_km_sorted=f_km.copy() 
    for i in range(km):
        f_km_sorted[f_km==i]=km_order[i] #按照均值大小，重新赋值
    
    #f_km_sorted=f_km_sorted+1
    #f_km_sorted[f_km_sorted==134]=0
    #slicer.util.updateVolumeFromArray(FLAIR_node,f_km_sorted*100)
    
    f_max=np.zeros_like(flair)
    f_max[f_km==km_order[-1]]=1 #均值最大组的f_km值,白质高信号强度最高，排在最后
    slicer.util.updateVolumeFromArray(FLAIR_node,f_max*100)

