import os
import pydicom
import numpy as np

dicom_folder = r'C:\0'
dst_folder = r'C:\1'
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

grey2rgb = np.genfromtxt('jet.csv', delimiter=',', skip_header=1)
grey2rgb = grey2rgb[:,1:]
def jet(x):
    return(grey2rgb[x])

for root, dirs, files in os.walk(dicom_folder):
    for file in files:
        src_file = os.path.join(root, file)
        try:    
            ds=pydicom.dcmread(src_file)
            is_dicom = True
        except:
            is_dicom = False
        if is_dicom:
            if ds.PhotometricInterpretation == 'RGB':
                break
            pixel_data = ds.pixel_array
            if ds.Modality == 'CT':
                WindowCenter=list(ds.WindowCenter)[0]
                WindowWidth=list(ds.WindowWidth)[0]
                pixel_data = pixel_data + ds.RescaleIntercept
                lower=max(WindowCenter-WindowWidth/2,np.percentile(pixel_data,1))
                upper=min(WindowCenter+WindowWidth/2,np.percentile(pixel_data,99))
            else:
                lower=np.percentile(pixel_data,1)
                upper=np.percentile(pixel_data,99)
            if lower==upper:
                upper+=1
            normalized_pixel_data = np.clip((pixel_data - lower) / (upper - lower),0,1)
            grey_data = (normalized_pixel_data*255).astype(np.uint8)
            rgb_data = jet(grey_data).astype(np.uint8)
            
            if 'RescaleIntercept' in ds:
                ds.RescaleIntercept = 0
            ds.PhotometricInterpretation = 'RGB'
            ds.SamplesPerPixel = 3
            ds.BitsAllocated = 8
            ds.BitsStored = 8
            ds.HighBit = 7
            ds.PixelRepresentation = 0
            ds.PixelData = rgb_data.tobytes()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
            relative_path = os.path.relpath(src_file, dicom_folder)
            dst_path = os.path.join(dst_folder, relative_path)
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                  os.makedirs(dst_dir)
            ds.save_as(dst_path)
