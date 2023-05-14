import os
import pydicom
import numpy as np
os.chdir(dcmdir)
files=os.listdir()
files.sort(key=lambda x: pydicom.dcmread(x)[0x00200032].value[2])
position=[pydicom.dcmread(file)[0x00200032].value for file in files]
orientation=[pydicom.dcmread(file)[0x00200037].value for file in files]
a=np.array(position)
a=np.round(np.linspace(a[0],a[-1],a[:,0].size),6)
n=0
for file in files:
  ds=pydicom.dcmread(file)
  ds[0x00200013].value=n+1
  ds[0x00200032].value=list(a[n])
  ds[0x00200037].value=orientation[0]
  n=n+1
  ds.save_as(file)
