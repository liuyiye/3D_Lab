import msvcrt
while True:
  password = ''
  menu = False
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == '678':break
  if password == '678i':
    menu = True
    break

while True:
  print("\n请输入需要传输的完整文件夹路径")
  src_dir = input("please input the dicom folder: ")
  if src_dir:break

jpg = False
debug = False
all_sop = False
scu_ae_title = 'SDM'

if menu:
  print('\nreturn for default:')
  print('jpg = False')
  print('debug = False')
  print('all_sop = False')
  print('scu_ae_title = SDM')
  
  jpg = input("jpg:") or False
  debug = input("debug:") or False
  all_sop = input("all_sop:") or False
  scu_ae_title = input("scu_ae_title:") or 'SDM'

import os,sys,pydicom,tempfile
from pynetdicom import AE,debug_logger,StoragePresentationContexts
from pynetdicom.sop_class import *

def send(IP,PORT,AET,src_dir):
  if debug:
    debug_logger()
  
  ae = AE(ae_title=scu_ae_title)
  
  storage_classes = [
    RawDataStorage,          # 1.2.840.10008.5.1.4.1.1.66
    CTImageStorage,          # 1.2.840.10008.5.1.4.1.1.2
    MRImageStorage,          # 1.2.840.10008.5.1.4.1.1.4
    SecondaryCaptureImageStorage,  # 1.2.840.10008.5.1.4.1.1.7
    XRayAngiographicImageStorage,  # 1.2.840.10008.5.1.4.1.1.12.2
    DigitalMammographyXRayImageStorageForPresentation,  # 1.2.840.10008.5.1.4.1.1.1.2
    DigitalXRayImageStorageForPresentation, # 1.2.840.10008.5.1.4.1.1.1.1
    NuclearMedicineImageStorage,            # 1.2.840.10008.5.1.4.1.1.20
    PositronEmissionTomographyImageStorage  # 1.2.840.10008.5.1.4.1.1.128
  ]
  
  if all_sop:
    ae.requested_contexts = StoragePresentationContexts
  else:
    for sop in storage_classes:
      ae.add_requested_context(sop)
      ae.add_requested_context(sop, [pydicom.uid.JPEGLosslessSV1])
  
  assoc = ae.associate(IP,PORT,ae_title=AET)
  if assoc.is_established:
    for root, dirs, files in os.walk(src_dir):
      n=0
      for f in files:
        if f.upper() in ['DIRFILE', 'DICOMDIR']:
            continue
        try:
          ds = pydicom.dcmread(os.path.join(root, f))
          is_dicom = True
        except:
          is_dicom = False
        if is_dicom and not jpg:
          try:
            status = assoc.send_c_store(ds)
            n = n+1
          except Exception as e:print(e)
        if is_dicom and jpg:
          temp_dir = tempfile.gettempdir()
          try:
            array = ds.pixel_array
            ds.PixelData = array.tobytes()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
            relative_path = os.path.relpath(os.path.join(root, f), src_dir)
            dst_path = os.path.join(temp_dir, 'dicom_output',relative_path)
            dst_dir = os.path.dirname(dst_path)
            os.makedirs(dst_dir, exist_ok=True)
            ds.save_as(dst_path,write_like_original=False)
            status = assoc.send_c_store(ds)
            n = n+1
          except Exception as e:print(e)
      print(f'{n} dicom files sent. {root}')
    assoc.release()

while True:
  print("\nselect destination:")
  print("6 - PH_ISP01_ADV_AE")
  print("7 - PH_ISP02_ADV_AE")
  print("8 - PH_ISP03_ADV_AE")
  print("9 - exit\n")
  choice = input("please input number: ")
  
  if choice == '9': 
    break
  
  elif choice == '6':
    try:send('172.21.97.26',104,'PH_ISP01_ADV_AE',src_dir)
    except Exception as e:print(e)
  
  elif choice == '7':
    try:send('172.21.97.27',104,'PH_ISP02_ADV_AE',src_dir)
    except Exception as e:print(e)
  
  elif choice == '8':
    try:send('172.21.97.28',104,'PH_ISP03_ADV_AE',src_dir)
    except Exception as e:print(e)
  
  elif choice == '1p':
    try:send('192.168.21.114', 104, 'PLAZAAPP1',src_dir)
    except Exception as e:print(e)
  
  elif choice == '2c':
    try:send('192.168.21.102', 11101, 'IDMAPP1',src_dir)
    except Exception as e:print(e)
  
  elif choice == '3u':
    try:send('172.21.253.62', 30966, 'UIHHXZS66',src_dir)
    except Exception as e:print(e)
  
  elif choice == '82':
    try:send('172.20.99.82', 11112, 'C3D',src_dir)
    except Exception as e:print(e)
  
  elif choice == '3d':
    try:send('172.20.99.33', 11112, '3D',src_dir)
    except Exception as e:print(e)
  
  elif choice == 'local':
    try:send('127.0.0.1', 11111, 'local',src_dir)
    except Exception as e:print(e)
  
  elif choice == 'i':
    print("1p,2c,3u,82,3d,local")
    IP = input("please input IP: ")
    try:PORT = int(input("please input PORT: "))
    except:pass
    AET = input("please input AE_TITLE: ")
    try:send(IP,PORT,AET,src_dir)
    except Exception as e:print(e)
  
  else:
    print("wrong input")

print("exit!")
