def t3237(dcmdir='c:/0'):
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
  #np.savetxt(dcmdir+'/position.csv',a,delimiter=',')
  c=[(a[:,i].max()-a[:,i].min()) for i in range(12)]
  for i in c:
    print(i)

def t3237s(dcmdir='c:/0'):
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

def t3237w(dcmdir='c:/0'):
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

def t8w(dcmdir='c:/0'):
  import os
  import pydicom
  os.chdir(dcmdir)
  files=os.listdir()
  if(len(set([pydicom.dcmread(file).SeriesInstanceUID for file in files])))>1:
    print('\n错误!!!文件夹中包含多个图像序列!!!'*3)
    return
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

def c3d(dcmdir='c:/0'):
  import os
  import pydicom
  from pynetdicom import AE, debug_logger
  from pynetdicom.sop_class import CTImageStorage,MRImageStorage,SecondaryCaptureImageStorage
  #debug_logger()
  ae = AE(ae_title=b'C3D')
  ae.add_requested_context(CTImageStorage)
  ae.add_requested_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(MRImageStorage)
  ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(SecondaryCaptureImageStorage)
  ae.add_requested_context(SecondaryCaptureImageStorage,[pydicom.uid.JPEGLosslessSV1])
  files=os.listdir(dcmdir)
  ds_all = [pydicom.dcmread(os.path.join(dcmdir, file),force=True) for file in files]
  assoc = ae.associate('192.168.21.16',2002,ae_title=b'SDM')
  if assoc.is_established:
    for ds in ds_all:
      status = assoc.send_c_store(ds)
    assoc.release()
while True:
  if input()=='2133':break
while True:
  print("\n请选择要执行的功能:")
  print("0 - t3237") 
  print("1 - t3237w")
  print("2 - t8w")
  print("3 - c3d")
  print("6 - t3237save")
  print("9 - exit\n")
  choice = int(input("请输入数字序号:"))

  if choice == 9: 
    break
  
  elif choice == 0:
    t3237()
  
  elif choice == 1:
    t3237w()

  elif choice == 2:
    t8w()
  
  elif choice == 3:
    c3d()

  elif choice == 6:
    t3237s()

  else:
    print("输入的序号有误")

print("程序已退出!")

