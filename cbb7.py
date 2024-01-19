def packages():
  import profile
  import smtplib
  import sqlite3
  import time
  import timeit
  import trace
  import argparse
  import asyncio
  import codecs
  import collections
  import configparser
  import copy
  import csv
  import datetime
  import difflib
  import getpass
  import gettext
  import io
  import itertools
  import json
  import locale
  import logging
  import math
  import mmap
  import multiprocessing
  import os
  import pickle
  import pydoc
  import random
  import re
  import shutil
  import signal
  import socket
  import sys
  import tempfile
  import threading
  import unittest
  import webbrowser
  import zlib

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
  from pynetdicom.sop_class import CTImageStorage,MRImageStorage,SecondaryCaptureImageStorage,XRayRadiofluoroscopicImageStorage,ComputedRadiographyImageStorage,DigitalMammographyXRayImageStorageForPresentation,DigitalXRayImageStorageForPresentation
  ae = AE(ae_title=b'C3D')
  ae.add_requested_context(CTImageStorage)
  ae.add_requested_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(MRImageStorage)
  ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(SecondaryCaptureImageStorage)
  ae.add_requested_context(SecondaryCaptureImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(XRayRadiofluoroscopicImageStorage)
  ae.add_requested_context(ComputedRadiographyImageStorage)
  ae.add_requested_context(DigitalMammographyXRayImageStorageForPresentation)
  ae.add_requested_context(DigitalXRayImageStorageForPresentation)
  files=os.listdir(dcmdir)
  ds_all = [pydicom.dcmread(os.path.join(dcmdir, file),force=True) for file in files]
  assoc = ae.associate('192.168.21.16',2002,ae_title=b'SDM')
  if assoc.is_established:
    for ds in ds_all:
      status = assoc.send_c_store(ds)
    assoc.release()

def sft():
  from win32file import CreateFile, GetFileTime, SetFileTime, CloseHandle
  from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
  from pywintypes import Time
  from datetime import datetime
  import win32timezone
  
  file=input(r'filename c:\0\1.txt: ') or 'c:\\0\\1.txt'
  ct=input('createTime datetime(2023,9,17,9,17,9): ') or 'datetime(2023,9,17,9,17,9)'
  at=input('accessTime datetime(2023,9,17,9,17,7): ') or 'datetime(2023,9,17,9,17,7)'
  mt=input('modifyTime datetime(2023,9,17,9,17,1): ') or 'datetime(2023,9,17,9,17,1)'

  c=Time(eval(ct).timestamp())
  a=Time(eval(at).timestamp())
  m=Time(eval(mt).timestamp())
  
  fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
  SetFileTime(fh, c,a,m)
  CloseHandle(fh)

def detect_encoding(filename):
    import chardet
    with open(filename, 'rb') as f: 
        rawdata = f.read(10000)
    result = chardet.detect(rawdata)
    return result['encoding']

def exec_file():
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
  import codecs
  a=input(r'filename:')
  with codecs.open(a, encoding=detect_encoding(a)) as f:
    exec(f.read())

def line():
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
  import codecs
  while True:
    try:
      code=input('line>>>')
      if code=='r':return
      exec(code)
    except Exception as e:print(e)

def lines():
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
  import codecs
  while True:
    try:
      print('lines:')
      mem_file=io.StringIO()
      while True:
        i=input()
        if i=='':break
        if i=='r':return
        mem_file.write(i+'\n')
      code=mem_file.getvalue()
      exec(code)
    except Exception as e:print(e)
    
def h():
  print(r'''
def packages():
  import profile
  import smtplib
  import sqlite3
  import time
  import timeit
  import trace
  import argparse
  import asyncio
  import codecs
  import collections
  import configparser
  import copy
  import csv
  import datetime
  import difflib
  import getpass
  import gettext
  import io
  import itertools
  import json
  import locale
  import logging
  import math
  import mmap
  import multiprocessing
  import os
  import pickle
  import pydoc
  import random
  import re
  import shutil
  import signal
  import socket
  import sys
  import tempfile
  import threading
  import unittest
  import webbrowser
  import zlib

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
  from pynetdicom.sop_class import CTImageStorage,MRImageStorage,SecondaryCaptureImageStorage,XRayRadiofluoroscopicImageStorage,ComputedRadiographyImageStorage,DigitalMammographyXRayImageStorageForPresentation,DigitalXRayImageStorageForPresentation
  ae = AE(ae_title=b'C3D')
  ae.add_requested_context(CTImageStorage)
  ae.add_requested_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(MRImageStorage)
  ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(SecondaryCaptureImageStorage)
  ae.add_requested_context(SecondaryCaptureImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(XRayRadiofluoroscopicImageStorage)
  ae.add_requested_context(ComputedRadiographyImageStorage)
  ae.add_requested_context(DigitalMammographyXRayImageStorageForPresentation)
  ae.add_requested_context(DigitalXRayImageStorageForPresentation)
  files=os.listdir(dcmdir)
  ds_all = [pydicom.dcmread(os.path.join(dcmdir, file),force=True) for file in files]
  assoc = ae.associate('192.168.21.16',2002,ae_title=b'SDM')
  if assoc.is_established:
    for ds in ds_all:
      status = assoc.send_c_store(ds)
    assoc.release()

def sft():
  from win32file import CreateFile, GetFileTime, SetFileTime, CloseHandle
  from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
  from pywintypes import Time
  from datetime import datetime
  import win32timezone
  
  file=input(r'filename c:\0\1.txt: ') or 'c:\\0\\1.txt'
  ct=input('createTime datetime(2023,9,17,9,17,9): ') or 'datetime(2023,9,17,9,17,9)'
  at=input('accessTime datetime(2023,9,17,9,17,7): ') or 'datetime(2023,9,17,9,17,7)'
  mt=input('modifyTime datetime(2023,9,17,9,17,1): ') or 'datetime(2023,9,17,9,17,1)'

  c=Time(eval(ct).timestamp())
  a=Time(eval(at).timestamp())
  m=Time(eval(mt).timestamp())
  
  fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
  SetFileTime(fh, c,a,m)
  CloseHandle(fh)

def detect_encoding(filename):
    import chardet
    with open(filename, 'rb') as f: 
        rawdata = f.read(10000)
    result = chardet.detect(rawdata)
    return result['encoding']

def exec_file():
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
  import codecs
  a=input(r'filename:')
  with codecs.open(a, encoding=detect_encoding(a)) as f:
    exec(f.read())

def line():
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
  import codecs
  while True:
    try:
      code=input('line>>>')
      if code=='r':return
      exec(code)
    except Exception as e:print(e)

def lines():
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
  import codecs
  while True:
    try:
      print('lines:')
      mem_file=io.StringIO()
      while True:
        i=input()
        if i=='':break
        if i=='r':return
        mem_file.write(i+'\n')
      code=mem_file.getvalue()
      exec(code)
    except Exception as e:print(e)

def h():
  print(r' ' '

    ' ' ')

def main():
  import msvcrt
  while True:
    password = ''
    while True:
      ch = msvcrt.getwch()
      if ch == '\r':break
      password += ch
    if password == '2133f':break

  while True:
    print("\nc:\\0 functions:")
    print("0 - t3237      a - set file time") 
    print("1 - t3237w     b - exec file")
    print("2 - t8w        c - exec lines r return")
    print("3 - c3d        d - exec line r return")
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
      try:sft()
      except Exception as e:print(e)

    elif choice == 'b':
      try:exec_file()
      except Exception as e:print(e)

    elif choice == 'c':
      try:lines()
      except Exception as e:print(e)

    elif choice == 'd':
      try:line()
      except Exception as e:print(e)

    elif choice=='h':
      h()

    else:
      print(choice)

  print("exit!")

import sys
import codecs
if len(sys.argv)>1:
  with codecs.open(sys.argv[1], encoding=detect_encoding(sys.argv[1])) as f:
    exec(f.read())
else:main()

    ''')

def main():
  import msvcrt
  while True:
    password = ''
    while True:
      ch = msvcrt.getwch()
      if ch == '\r':break
      password += ch
    if password == '2133f':break

  while True:
    print("\nc:\\0 functions:")
    print("0 - t3237      a - set file time") 
    print("1 - t3237w     b - exec file")
    print("2 - t8w        c - exec lines r return")
    print("3 - c3d        d - exec line r return")
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
      try:sft()
      except Exception as e:print(e)

    elif choice == 'b':
      try:exec_file()
      except Exception as e:print(e)

    elif choice == 'c':
      try:lines()
      except Exception as e:print(e)

    elif choice == 'd':
      try:line()
      except Exception as e:print(e)

    elif choice=='h':
      h()

    else:
      print(choice)

  print("exit!")

import sys
import codecs
if len(sys.argv)>1:
  with codecs.open(sys.argv[1], encoding=detect_encoding(sys.argv[1])) as f:
    exec(f.read())
else:main()
