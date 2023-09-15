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

def t3237csv(dcmdir='c:/0'):
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
    print('\nerror!!!more than one series!!!'*3)
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
  from pynetdicom import AE
  from pynetdicom.sop_class import CTImageStorage,MRImageStorage,SecondaryCaptureImageStorage
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

def exec_():
  import io
  import os
  import sys
  import csv
  import time
  import msvcrt
  import shutil
  import PIL
  import numpy
  import pydicom
  import pynetdicom
  a=input('filename: ')
  with open(a,'r') as f:
    exec(f.read())

def exec8():
  import io
  import os
  import sys
  import csv
  import time
  import msvcrt
  import shutil
  import PIL
  import numpy
  import pydicom
  import pynetdicom
  a=input('filename: ')
  with open(a,'r',encoding='utf-8') as f:
    exec(f.read())

def execlines():
  import io
  import os
  import sys
  import csv
  import time
  import msvcrt
  import shutil
  import PIL
  import numpy
  import pydicom
  import pynetdicom
  print('lines:')
  mem_file=io.StringIO()
  while True:
    line=input()
    if line=='':break
    mem_file.write(line+'\n')
  code=mem_file.getvalue()
  exec(code)

def eval_():
  import io
  import os
  import sys
  import csv
  import time
  import msvcrt
  import shutil
  import PIL
  import numpy
  import pydicom
  import pynetdicom
  a=input('line: \n')
  print(eval(a))

def h():
  print(r'''
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

def t3237csv(dcmdir='c:/0'):
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
    print('\nerror!!!more than one series!!!'*3)
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
  from pynetdicom import AE
  from pynetdicom.sop_class import CTImageStorage,MRImageStorage,SecondaryCaptureImageStorage
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

def exec_():
  import io
  import os
  import sys
  import csv
  import time
  import msvcrt
  import shutil
  import PIL
  import numpy
  import pydicom
  import pynetdicom
  a=input('filename: ')
  with open(a,'r') as f:
    exec(f.read())

def exec8():
  import io
  import os
  import sys
  import csv
  import time
  import msvcrt
  import shutil
  import PIL
  import numpy
  import pydicom
  import pynetdicom
  a=input('filename: ')
  with open(a,'r',encoding='utf-8') as f:
    exec(f.read())

def execlines():
  import io
  import os
  import sys
  import csv
  import time
  import msvcrt
  import shutil
  import PIL
  import numpy
  import pydicom
  import pynetdicom
  print('lines:')
  mem_file=io.StringIO()
  while True:
    line=input()
    if line=='':break
    mem_file.write(line+'\n')
  code=mem_file.getvalue()
  exec(code)

def eval_():
  import io
  import os
  import sys
  import csv
  import time
  import msvcrt
  import shutil
  import PIL
  import numpy
  import pydicom
  import pynetdicom
  a=input('line: \n')
  print(eval(a))

def h():
  print(r' ' '

    ' ' ')

import msvcrt
while True:
  password = ''
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == '2133f':break

while True:
  print("\nfunctions:")
  print("0 - t3237      a - exec ansi GBK") 
  print("1 - t3237w     b - exec utf-8 no BOM")
  print("2 - t8w        c - exec lines")
  print("3 - c3d        d - eval line")
  print("6 - t3237csv   9 - exit\n")
  choice = input("select:")

  if choice == '9': 
    break

  elif choice == '0':
    t3237()

  elif choice == '1':
    t3237w()

  elif choice == '2':
    t8w()

  elif choice == '3':
    c3d()

  elif choice == '6':
    t3237csv()

  elif choice == 'a':
    try:exec_()
    except Exception as e:print(e)

  elif choice == 'b':
    try:exec8()
    except Exception as e:print(e)

  elif choice == 'c':
    try:execlines()
    except Exception as e:print(e)

  elif choice == 'd':
    try:eval_()
    except Exception as e:print(e)

  elif choice=='h':
    h()

  else:
    print(choice)

print("exit!")

    ''')

import msvcrt
while True:
  password = ''
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == '2133f':break

while True:
  print("\nfunctions:")
  print("0 - t3237      a - exec ansi GBK") 
  print("1 - t3237w     b - exec utf-8 no BOM")
  print("2 - t8w        c - exec lines")
  print("3 - c3d        d - eval line")
  print("6 - t3237csv   9 - exit\n")
  choice = input("select:")

  if choice == '9': 
    break

  elif choice == '0':
    t3237()

  elif choice == '1':
    t3237w()

  elif choice == '2':
    t8w()

  elif choice == '3':
    c3d()

  elif choice == '6':
    t3237csv()

  elif choice == 'a':
    try:exec_()
    except Exception as e:print(e)

  elif choice == 'b':
    try:exec8()
    except Exception as e:print(e)

  elif choice == 'c':
    try:execlines()
    except Exception as e:print(e)

  elif choice == 'd':
    try:eval_()
    except Exception as e:print(e)

  elif choice=='h':
    h()

  else:
    print(choice)

print("exit!")

