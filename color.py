
import os
import pydicom
import numpy as np
import colorsys

dicom_folder = r'C:\0'
dst_folder = r'C:\1'
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

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
            normalized_pixel_data = (pixel_data - np.min(pixel_data)) / (np.max(pixel_data) - np.min(pixel_data))
            colored_pixel_data = np.zeros((ds.Rows, ds.Columns, 3), dtype=np.float64)
            for row in range(ds.Rows):
                for col in range(ds.Columns):
                    hue = normalized_pixel_data[row, col]
                    colored_pixel_data[row, col, :] = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            colored_pixel_data = (colored_pixel_data * 255).astype(np.uint8) # 将颜色数据转换为8位整数格式
            ds.PixelData = colored_pixel_data.tobytes()
            ds.SamplesPerPixel = 3
            ds.PhotometricInterpretation = 'RGB'
            ds.BitsAllocated = 8
            ds.BitsStored = 8
            ds.HighBit = 7
            ds.PixelRepresentation = 0  # 无符号整数
            relative_path = os.path.relpath(src_file, dicom_folder)
            dst_path = os.path.join(dst_folder, relative_path)
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                  os.makedirs(dst_dir)
            ds.save_as(dst_path)
