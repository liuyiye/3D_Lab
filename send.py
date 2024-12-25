
def send(IP,PORT,AET,PATH):
  import os
  import pydicom
  from pynetdicom import AE
  from pynetdicom.sop_class import CTImageStorage,MRImageStorage,SecondaryCaptureImageStorage
  
  ae = AE(ae_title=b'SDM')
  ae.add_requested_context(CTImageStorage)
  ae.add_requested_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(MRImageStorage)
  ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(SecondaryCaptureImageStorage)
  ae.add_requested_context(SecondaryCaptureImageStorage,[pydicom.uid.JPEGLosslessSV1])
  
  assoc = ae.associate(IP,PORT,ae_title=AET)
  if assoc.is_established:
    for root, dirs, files in os.walk(PATH):
      n=0
      for f in files:
        try:
          ds = pydicom.dcmread(os.path.join(root, f))
          is_dicom = True
        except:
          is_dicom = False
        if is_dicom:
          status = assoc.send_c_store(ds)
          n = n+1
      print(f'{n} dicom files sent. {root}')
    assoc.release()


import msvcrt
while True:
  password = ''
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == '678':break


while True:
  print("\n请输入需要传输的完整文件夹路径")
  PATH = input("please input path: ")
  if PATH:break


while True:
  print("\n6 - PH_ISP01_ADV_AE") 
  print("7 - PH_ISP02_ADV_AE")
  print("8 - PH_ISP03_ADV_AE")
  print("9 - exit\n")
  choice = input("please input number: ")
  
  if choice == '9': 
    break
  
  elif choice == '6':
    try:send('172.21.97.26',104,'PH_ISP01_ADV_AE',PATH)
    except Exception as e:print(e)
  
  elif choice == '7':
    try:send('172.21.97.27',104,'PH_ISP02_ADV_AE',PATH)
    except Exception as e:print(e)
  
  elif choice == '8':
    try:send('172.21.97.28',104,'PH_ISP03_ADV_AE',PATH)
    except Exception as e:print(e)
  
  elif choice == '1p':
    try:send('192.168.21.114', 104, 'PLAZAAPP1',PATH)
    except Exception as e:print(e)
  
  elif choice == '2c':
    try:send('192.168.21.102', 11101, 'IDMAPP1',PATH)
    except Exception as e:print(e)
  
  elif choice == '3u':
    try:send('172.21.253.62', 30966, 'UIHHXZS66',PATH)
    except Exception as e:print(e)
  
  elif choice == '82':
    try:send('172.20.99.82', 11112, 'C3D',PATH)
    except Exception as e:print(e)
  
  elif choice == 'i':
    print("1p.2c.3u,82") 
    IP = input("please input IP: ")
    try:PORT = int(input("please input PORT: "))
    except:pass
    AET = input("please input AE_TITLE: ")
    try:send(IP,PORT,AET,PATH)
    except Exception as e:print(e)
  
  else:
    print("wrong input")

print("exit!")
