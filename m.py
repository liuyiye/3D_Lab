import os,msvcrt,pydicom,numpy as np
from PIL import Image
from pynetdicom import AE,debug_logger
from pynetdicom.sop_class import CTImageStorage,MRImageStorage

#debug_logger()
root_dir='.'
output_root = os.path.join(root_dir, "dicom_output")
supported_extensions = ['.jpg', '.jpeg', '.png']

def dcm():
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            try:    
                ds=pydicom.dcmread(os.path.join(root, f))
                return ds
            except:
                pass
    print('\nNo DICOM file!!!')

def convert():
    data = dcm()
    if data == None:
        return
    ds = pydicom.Dataset()
    ds.file_meta = pydicom.Dataset()
    
    ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    ds.SOPClassUID = data.SOPClassUID
    
    ds.PatientID = data.PatientID
    ds.StudyInstanceUID = data.StudyInstanceUID
    ds.PatientName = data.PatientName
    ds.StudyDate = data.StudyDate
    ds.StudyTime = data.StudyTime
    ds.ContentDate = data.ContentDate
    ds.ContentTime = data.ContentTime
    ds.AccessionNumber = data.AccessionNumber
    ds.Modality = data.Modality
    ds.SeriesNumber = data.SeriesNumber
    ds.PatientBirthDate = data.PatientBirthDate
    ds.ReferringPhysicianName = data.ReferringPhysicianName
    ds.PatientSex = data.PatientSex
    
    ds.SeriesDescription='3D_Lab'
    ds.SliceLocation=''
    ds.ImagePositionPatient = ''
    ds.ImageOrientationPatient = ''
    ds.NumberOfFrames = ''
    ds.PixelSpacing = ''
    ds.WindowCenter = ''
    ds.WindowWidth = ''
    ds.RescaleSlope = ''
    ds.RescaleType = ''
    
    for current_dir, dirs, files in os.walk(root_dir):
        n = 1
        siuid=pydicom.uid.generate_uid()
        for f in files:
            if os.path.splitext(f)[1].lower() in supported_extensions:
                input_path = os.path.join(current_dir, f)
                relative_path = os.path.relpath(current_dir, root_dir)
                
                os.makedirs(output_root, exist_ok=True)
                output_subdir = os.path.join(output_root, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                output_filename = os.path.splitext(f)[0] + '.dcm'
                output_path = os.path.join(output_subdir, output_filename)
                
                img = Image.open(input_path)
                if img.mode=='L':
                    np_image=np.array(img.getdata(),dtype=np.uint8)
                    ds.SeriesInstanceUID=siuid
                    ds.SOPInstanceUID=pydicom.uid.generate_uid()
                    ds.InstanceNumber=n
                    ds.Rows=img.height
                    ds.Columns=img.width
                    ds.PhotometricInterpretation="MONOCHROME2"
                    ds.RescaleIntercept=0
                    ds.SamplesPerPixel=1
                    ds.BitsStored=8
                    ds.BitsAllocated=8
                    ds.HighBit=7
                    ds.PixelRepresentation=0
                    ds.PixelData=np_image.tobytes()
                    ds.save_as(output_path, write_like_original=False)
                if 'RGB' in img.mode:
                    np_image=np.array(img.getdata(), dtype=np.uint8)[:,:3]
                    ds.SeriesInstanceUID=siuid
                    ds.SOPInstanceUID=pydicom.uid.generate_uid()
                    ds.InstanceNumber=n
                    ds.Rows=img.height
                    ds.Columns=img.width
                    ds.PhotometricInterpretation="RGB"
                    ds.PlanarConfiguration = 0
                    ds.RescaleIntercept=0
                    ds.SamplesPerPixel=3
                    ds.BitsStored=8
                    ds.BitsAllocated=8
                    ds.HighBit=7
                    ds.PixelRepresentation=0
                    ds.PixelData=np_image.tobytes()
                    ds.save_as(output_path, write_like_original=False)
                n = n+1
    print('\n\n\n\n\n\n****************************************')
    print('转换完成，请确认转换图像的信息是否正确:')
    print(f'病人姓名：{ds.PatientName}')
    print(f'  病人ID：{ds.PatientID}')
    print(f'检查日期：{ds.StudyDate}')
    print('上述信息完全正确，才可发送到PACS！！！')
    print('****************************************')
    
def send(ip,port,aet,name):
    ae = AE(ae_title=b'SDM')
    ae.add_requested_context(MRImageStorage)
    ae.add_requested_context(CTImageStorage)
    ae.connection_timeout=60
    assoc = ae.associate(ip,port,ae_title=aet)
    if assoc.is_established:
        for root, dirs, files in os.walk(output_root):
            for f in files:
                ds=pydicom.dcmread(os.path.join(root, f))
                assoc.send_c_store(ds)
        try:id = ds.PatientID
        except:id = None
        assoc.release()
        print(f'\n{id} {name}')

while True:
  password = ''
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == '678':break

while True:
  print("\n\n\n将当前文件夹JPG、PNG图像转换为DICOM文件")
  print("当前文件夹需包含至少一张相关的DICOM图像")
  print("1：转换         2：发送         9：退出") 
  choice = int(input("请输入数字序号:"))

  if choice == 9: 
    break
  
  elif choice == 1:
    convert()

  elif choice == 2:
    send('192.168.21.114',104,'PLAZAAPP1','1P')
    send('192.168.21.102',11101,'IDMAPP1','2C')
    send('172.21.253.62',30966,'UIHHXZS66','3U')
    
  else:
    print("输入的序号有误")

print("程序已退出!")
