import os
import pydicom
import numpy as np
os.chdir(dcmdir)
files=os.listdir()
position=[pydicom.dcmread(file)[0x00200032].value for file in files]
position.sort(key=lambda x:x[2])
a=np.asarray(position)
b=np.diff(a,axis=0)
b=np.insert(b,0,b[0],axis=0)
a=np.append(a,b,axis=1)
orientation=[pydicom.dcmread(file)[0x00200037].value for file in files]
a=np.append(a,np.asarray(orientation),1)
np.savetxt(dcmdir+'/position.csv',a,delimiter=',')
c=[(a[:,i].max()-a[:,i].min()) for i in range(12)]
for i in c:
  print(i)
