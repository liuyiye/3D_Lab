import slicer
from sklearn.cluster import KMeans
n=slicer.util.getNode('v')
a=slicer.util.arrayFromVolume(n)
n2=slicer.util.getNode('l')
a2=slicer.util.arrayFromVolume(n2)
a[a2==0]=0
array=a[a2==1]
cls=KMeans(n_clusters=2).fit_predict(array.reshape(-1,1))
print(
'Mean=',round(a[a2==1].mean(),1),
'\nROI_1=',round(a[a2==1][cls==0].mean(),1),
'\nROI_2=',round(a[a2==1][cls==1].mean(),1))
a[a2==1]=cls+1
slicer.util.updateVolumeFromArray(n,a)
