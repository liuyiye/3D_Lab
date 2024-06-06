import os
import pydicom
import numpy as np

dicom_folder = r'C:\0'
dst_folder = r'C:\1'
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

jet = np.genfromtxt('values_colors.csv', delimiter=',', skip_header=1)
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
            i,j = pixel_data.shape
            if ds.Modality=='CT':
                pixel_data = pixel_data + ds.RescaleIntercept
                lower=max(ds.WindowCenter-ds.WindowWidth/2,np.percentile(pixel_data,1))
                upper=min(ds.WindowCenter+ds.WindowWidth/2,np.percentile(pixel_data,99))
            else:
                lower=np.percentile(pixel_data,1)
                upper=np.percentile(pixel_data,99)
            if lower==upper:
                upper+=1
            normalized_pixel_data = np.clip((pixel_data - lower) / (upper - lower),0,1)
            grey_data = normalized_pixel_data*255
            rgb_data = np.zeros((i,j,3), dtype=np.uint8)
            for y in range(i):
                for x in range(j):
                    grey_value = grey_data[y, x]
                    rgb_value = jet[int(grey_value)]
                    rgb_data[y, x] = rgb_value[1:]
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
