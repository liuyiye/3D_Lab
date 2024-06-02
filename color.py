
import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt

dicom_folder = r'C:\0'
dst_folder = r'C:\1'
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

cmap = plt.get_cmap('jet')

for root, dirs, files in os.walk(dicom_folder):
    for file in files:
        src_file = os.path.join(root, file)
        try:    
            ds=pydicom.dcmread(src_file)
            is_dicom = True
        except:
            is_dicom = False
        if is_dicom:
            pixel_data = ds.pixel_array
            if 'RedPaletteColorLookupTableData' in ds:
                width = ds.Rows
                height = ds.Columns
                red_clut = ds.RedPaletteColorLookupTableData
                green_clut = ds.GreenPaletteColorLookupTableData
                blue_clut = ds.BluePaletteColorLookupTableData
                rgb_data = np.zeros((height, width, 3), dtype=np.uint8)
                for i in range(height):
                    for j in range(width):
                        index = pixel_data[i, j]
                        rgb_data[i, j, 0] = red_clut[index]
                        rgb_data[i, j, 1] = green_clut[index]
                        rgb_data[i, j, 2] = blue_clut[index]
            else:
                normalized_pixel_data = (pixel_data - np.min(pixel_data)) / (np.max(pixel_data) - np.min(pixel_data))
                rgb_data = cmap(normalized_pixel_data)[:, :, :3]
                rgb_data = (rgb_data * 255).astype(np.uint8)
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


                
