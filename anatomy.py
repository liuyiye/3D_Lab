
import os
import pydicom
import numpy as np
from PIL import Image

jpg_folder = r'C:\0'
dcm_folder = r'C:\1'

ds = pydicom.Dataset()
ds.file_meta = pydicom.Dataset()

#Change three series parameters each time
ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
ds.SOPClassUID = pydicom.uid.CTImageStorage
#ds.SOPInstanceUID = ''
ds.StudyDate = '19240101'
ds.StudyTime = ''
ds.AccessionNumber = 'anatomy'
ds.Modality = 'CT'
ds.SeriesDescription = 'bone'
ds.PatientName = 'anatomy'
ds.PatientID = 'anatomy'
ds.PatientBirthDate = '19240101'
ds.StudyInstanceUID = '1.2.826.0.1.3680063.8.698.82899861836716669316719291096168666999'
ds.SeriesInstanceUID = '1.2.826.0.1.3680063.8.698.82899861836716669316719291096168666106'
ds.SeriesNumber = '106'
#ds.InstanceNumber = ''
ds.ImagePositionPatient = ''
ds.ImageOrientationPatient = ''
#ds.SamplesPerPixel = ''
#ds.PhotometricInterpretation = ''
ds.NumberOfFrames = ''
#ds.Rows = ''
#ds.Columns = ''
ds.PixelSpacing = ''
#ds.BitsAllocated = ''
#ds.BitsStored = ''
#ds.HighBit = ''
#ds.PixelRepresentation = ''
ds.WindowCenter = ''
ds.WindowWidth = ''
#ds.RescaleIntercept = ''
ds.RescaleSlope = ''
ds.RescaleType = ''

files = os.listdir(jpg_folder)
n=1

for file in files:
  img=Image.open(os.path.join(jpg_folder,file))
  if img.mode=='L':
    np_image = np.array(img.getdata(),dtype = np.uint8)
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.InstanceNumber = n
    ds.Rows = img.height
    ds.Columns = img.width
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.RescaleIntercept = 0
    ds.SamplesPerPixel = 1
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = np_image.tobytes()
    ds.save_as(os.path.join(dcm_folder,str(n).zfill(4)))
  if 'RGB' in img.mode:
    np_image = np.array(img.getdata(),dtype = np.uint8)[:,:3]
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.InstanceNumber = n
    ds.Rows = img.height
    ds.Columns = img.width
    ds.PhotometricInterpretation = "RGB"
    ds.RescaleIntercept = 0
    ds.SamplesPerPixel = 3
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = np_image.tobytes()
    ds.save_as(os.path.join(dcm_folder,str(n).zfill(4)))
  n=n+1
