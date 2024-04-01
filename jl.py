
def send(IP,PORT,ISP):
  import os
  import pydicom
  from pynetdicom import AE
  from pynetdicom.sop_class import CTImageStorage,MRImageStorage,SecondaryCaptureImageStorage

  dcmdir='c:/jl'
  file_list = []
  for root, dirs, files in os.walk(dcmdir):
    for file in files:
      file_list.append(os.path.join(root, file))

  ae = AE(ae_title=b'C3D')
  ae.add_requested_context(CTImageStorage)
  ae.add_requested_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(MRImageStorage)
  ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
  ae.add_requested_context(SecondaryCaptureImageStorage)
  ae.add_requested_context(SecondaryCaptureImageStorage,[pydicom.uid.JPEGLosslessSV1])
  
  assoc = ae.associate(IP,PORT,ae_title=ISP)
  if assoc.is_established:
    for f in file_list:
      try:
        ds = pydicom.dcmread(f)
        is_dicom = True
      except:
        is_dicom = False
      if is_dicom:
        status = assoc.send_c_store(ds)
    assoc.release()


import msvcrt
while True:
  password = ''
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == 'jiling':break


while True:
  print("\nC:\\jl\n")
  print("6 - send") 
  print("9 - exit\n")
  choice = input("please input number: ")

  if choice == '9': 
    break

  elif choice == '6':
    try:send('192.168.21.102',11101,'IDMAPP1')
    except Exception as e:print(e)

  elif choice == 'i':
    IP = input("please input IP: ")
    PORT = int(input("please input PORT: "))
    ISP = input("please input AE_TITLE: ")
    try:send(IP,PORT,ISP)
    except Exception as e:print(e)

  else:
    print("wrong input")

print("exit!")
