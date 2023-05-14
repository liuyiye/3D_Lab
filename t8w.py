import os
import pydicom
os.chdir(dcmdir)
files=os.listdir()
siuid=pydicom.uid.generate_uid()
for file in files:
  ds=pydicom.dcmread(file)
  #SOP Instance UID
  ds[0x00080018].value=pydicom.uid.generate_uid()
  #Series Description
  ds[0x0008103e].value='3D_Lab_'+ds[0x0008103e].value
  #Patient's Name
  #ds[0x00100010].value='3D_Lab'
  #Patient ID
  #ds[0x00100020].value='Anonymous'
  #Study Instance UID
  #ds[0x0020000d].value=ds[0x0020000d].value
  #Series Instance UID
  ds[0x0020000e].value=siuid
  #Series Number
  #ds[0x00200011].value=ds[0x00200011].value
  #Instance Number
  #ds[0x00200013].value=ds[0x00200013].value
  ds.save_as(file)
