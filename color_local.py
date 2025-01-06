import msvcrt
while True:
  password = ''
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == '678':break

while True:
    convert = input("Convert images in the current folder to color images. return for not.") or False
    if convert:break

import os,pydicom,numpy as np
from skimage.transform import resize

dicom_folder = '.'
dst_folder = 'color_output'

palette = np.genfromtxt('palette1275.csv', delimiter=',', skip_header=0)
def p(x):
    return(palette[x])

def color():
  for root, dirs, files in os.walk(dicom_folder):
      siuid = pydicom.uid.generate_uid()
      for file in files:
          src_file = os.path.join(root, file)
          try:    
              ds = pydicom.dcmread(src_file)
              is_dicom = True
          except:
              is_dicom = False
          if is_dicom and ds.PhotometricInterpretation != 'RGB':
              pixel_data = ds.pixel_array
              datas1,datas97,datas98,datas99 = np.percentile(pixel_data,[1,97,98,99])
              
              if min(ds.Rows,ds.Columns) < 256:
                  normalized_data = pixel_data / np.max(pixel_data)
                  resized_data = resize(normalized_data, (2*ds.Rows, 2*ds.Columns), mode='reflect', anti_aliasing=True)
                  pixel_data = (resized_data * np.max(pixel_data)).astype(np.uint16)
                  ds.Rows, ds.Columns = pixel_data.shape
              
              if ds.Modality == 'CT':
                  try:
                      WindowCenter,WindowWidth = ds.WindowCenter[0],ds.WindowWidth[0]
                  except:
                      WindowCenter,WindowWidth = ds.WindowCenter,ds.WindowWidth
                  d = ds.RescaleIntercept
                  pixel_data = pixel_data + d
                  lower = max(WindowCenter - WindowWidth / 2, datas1 + d)
                  upper = min(WindowCenter + WindowWidth / 2, datas99 + d)
              elif 'ttp' in ds.SeriesDescription.lower():
                  lower = datas1
                  upper = datas97
              elif 'mtt' in ds.SeriesDescription.lower():
                  lower = datas1
                  upper = datas98
              else:
                  lower = datas1
                  upper = datas99
              
              if lower==upper:
                  upper += 1
              normalized_data = np.clip((pixel_data - lower) / (upper - lower),0,1)
              grey_data = (normalized_data * 1274).astype(np.uint16)
              rgb_data = p(grey_data).astype(np.uint8)
              
              data = pydicom.Dataset()
              data.file_meta = pydicom.Dataset()
              data.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
              
              data.SOPClassUID = ds.SOPClassUID
              data.PatientID = ds.PatientID
              data.StudyInstanceUID = ds.StudyInstanceUID
              data.PatientName = ds.PatientName
              data.StudyDate = ds.StudyDate
              data.StudyTime = ds.StudyTime
              data.ContentDate = ds.ContentDate
              data.ContentTime = ds.ContentTime
              data.AccessionNumber = ds.AccessionNumber
              data.Modality = ds.Modality
              data.SeriesNumber = ds.SeriesNumber
              data.PatientBirthDate = ds.PatientBirthDate
              data.ReferringPhysicianName = ds.ReferringPhysicianName
              data.PatientSex = ds.PatientSex
              
              data.SeriesDescription='3D_Lab_'+ds.SeriesDescription
              data.SeriesInstanceUID = siuid
              data.SOPInstanceUID = pydicom.uid.generate_uid()
              data.InstanceNumber = ds.InstanceNumber
              data.Rows=ds.Rows
              data.Columns=ds.Columns
              data.PhotometricInterpretation = 'RGB'
              data.PlanarConfiguration = 0
              data.RescaleIntercept=0
              data.SamplesPerPixel=3
              data.BitsAllocated = 8
              data.BitsStored = 8
              data.HighBit = 7
              data.PixelRepresentation = 0
              data.PixelData = rgb_data.tobytes()
              
              data.SliceLocation=''
              data.ImagePositionPatient = ''
              data.ImageOrientationPatient = ''
              data.NumberOfFrames = ''
              data.PixelSpacing = ''
              data.WindowCenter = ''
              data.WindowWidth = ''
              data.RescaleSlope = ''
              data.RescaleType = ''
              data.SpecificCharacterSet = 'GB18030'
              
              relative_path = os.path.relpath(src_file, dicom_folder)
              dst_path = os.path.join(dst_folder, relative_path)
              dst_dir = os.path.dirname(dst_path)
              os.makedirs(dst_dir, exist_ok=True)
              data.save_as(dst_path, write_like_original=False)

if __name__ == '__main__':
  color()
  print('\nDone!')
