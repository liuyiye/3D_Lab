import slicer
from sklearn.cluster import KMeans
n=slicer.util.getNode('v')
a=slicer.util.arrayFromVolume(n)
n2=slicer.util.getNode('l')
a2=slicer.util.arrayFromVolume(n2)
a[a2==0]=0
for y in range(a.shape[1]):
  array=a[:,y,:][a2[:,y,:]==1]
  if len(array>2):
     cls=KMeans(n_clusters=2).fit_predict(array.reshape(-1,1))
     if  a[:,y,:][a2[:,y,:]==1][cls==0].mean() <  a[:,y,:][a2[:,y,:]==1][cls==1].mean():
        cls=cls+1
     else: 
        cls=2-cls
     a[:,y,:][a2[:,y,:]==1]=cls

slicer.util.updateVolumeFromArray(n,a)
