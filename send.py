def send(IP,PORT,AET,PATH):
  import os
  import pydicom
  from pynetdicom import AE,debug_logger
  #debug_logger()
  from pynetdicom.sop_class import (
    RawDataStorage,          # 1.2.840.10008.5.1.4.1.1.66
    CTImageStorage,          # 1.2.840.10008.5.1.4.1.1.2
    MRImageStorage,          # 1.2.840.10008.5.1.4.1.1.4
    SecondaryCaptureImageStorage,  # 1.2.840.10008.5.1.4.1.1.7
    XRayAngiographicImageStorage,  # 1.2.840.10008.5.1.4.1.1.12.2
    DigitalMammographyXRayImageStorageForPresentation,  # 1.2.840.10008.5.1.4.1.1.1.2
    DigitalXRayImageStorageForPresentation,  # 1.2.840.10008.5.1.4.1.1.1.1
    NuclearMedicineImageStorage,            # 1.2.840.10008.5.1.4.1.1.20
    PositronEmissionTomographyImageStorage, # 1.2.840.10008.5.1.4.1.1.128
  )
  from pydicom.uid import (
    ExplicitVRLittleEndian, #1.2.840.10008.1.2.1
    ImplicitVRLittleEndian, #1.2.840.10008.1.2
    #JPEGLossless,   #1.2.840.10008.1.2.4.70
    JPEGLosslessSV1 #1.2.840.10008.1.2.4.57
  )
  
  ae = AE(ae_title=b'SDM')
  
  transfer_syntaxes = [
    #JPEGLossless,
    JPEGLosslessSV1,
    ExplicitVRLittleEndian,
    ImplicitVRLittleEndian
  ]
  
  storage_classes = [
    RawDataStorage,
    CTImageStorage,
    MRImageStorage,
    XRayAngiographicImageStorage,
    DigitalMammographyXRayImageStorageForPresentation,
    DigitalXRayImageStorageForPresentation,
    SecondaryCaptureImageStorage,
    NuclearMedicineImageStorage,
    PositronEmissionTomographyImageStorage,
  ]
  
  for storage_class in storage_classes:
    ae.add_requested_context(storage_class, transfer_syntaxes)
  
  assoc = ae.associate(IP,PORT,ae_title=AET)
  if assoc.is_established:
    for root, dirs, files in os.walk(PATH):
      n=0
      for f in files:
        if f.upper() in ['DIRFILE', 'DICOMDIR']:
            continue
        try:
          ds = pydicom.dcmread(os.path.join(root, f))
          is_dicom = True
        except:
          is_dicom = False
        if is_dicom:
          try:
            status = assoc.send_c_store(ds)
            n = n+1
          except:pass
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
  
  elif choice == '3d':
    try:send('172.20.99.33', 11112, '3D',PATH)
    except Exception as e:print(e)
  
  elif choice == 'i':
    print("1p.2c.3u,82,3d") 
    IP = input("please input IP: ")
    try:PORT = int(input("please input PORT: "))
    except:pass
    AET = input("please input AE_TITLE: ")
    try:send(IP,PORT,AET,PATH)
    except Exception as e:print(e)
  
  else:
    print("wrong input")

print("exit!")
