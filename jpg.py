import os
import pydicom
import numpy as np
from PIL import Image
from pydicom.uid import RLELossless

siuid=pydicom.uid.generate_uid()
ds=pydicom.dcmread(dcmfile,force=True)
ds.file_meta.TransferSyntaxUID='1.2.840.10008.1.2.1'
ds.SeriesInstanceUID=siuid
ds.SeriesDescription='3D_Lab'
ds.SeriesNumber=''
ds.SliceLocation=''
ds.ImagePositionPatient=''
ds.ImageOrientationPatient=''

os.chdir(jpgdir)
files=os.listdir()
n=1

for file in files:
  img=Image.open(file)

  if img.mode=='L':
    np_image=np.array(img.getdata(),dtype=np.uint8)
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
    ds.save_as(str(n))

  if 'RGB' in img.mode:
    np_image=np.array(img.getdata(), dtype=np.uint8)[:,:3]
    ds.SOPInstanceUID=pydicom.uid.generate_uid()
    ds.InstanceNumber=n
    ds.Rows=img.height
    ds.Columns=img.width
    ds.PhotometricInterpretation="RGB"
    ds.RescaleIntercept=0
    ds.SamplesPerPixel=3
    ds.BitsStored=8
    ds.BitsAllocated=8
    ds.HighBit=7
    ds.PixelRepresentation=0
    ds.PixelData=np_image.tobytes()
    ds.save_as(str(n))
  n=n+1

#compress
for i in np.arange(1,n):
    ds=pydicom.dcmread(str(i))
    ds.compress(RLELossless)
    ds.save_as(str(i))
