import os,pydicom,numpy as np
from skimage.transform import resize

dicom_folder = r'c:\0'
dst_folder = r'c:\1'
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

palette = np.genfromtxt('palette1275.csv', delimiter=',', skip_header=0)
def p(x):
    return(palette[x])

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
            
            if ds.Modality == 'MR' and min(ds.Rows,ds.Columns) < 256:
                normalized_data = pixel_data / np.max(pixel_data)
                resized_data = resize(normalized_data, (2*ds.Rows, 2*ds.Columns), mode='reflect', anti_aliasing=True)
                pixel_data = (resized_data * np.max(pixel_data)).astype(np.uint16)
                ds.Rows, ds.Columns = pixel_data.shape
                lower = np.percentile(pixel_data,2)
                upper = np.percentile(pixel_data,98)
            
            '''if 'RedPaletteColorLookupTableData' in ds:
                print("Palette")
                red_data = ds.RedPaletteColorLookupTableData
                green_data = ds.GreenPaletteColorLookupTableData
                blue_data = ds.BluePaletteColorLookupTableData
                
                red_palette = np.frombuffer(red_data, dtype=np.uint16)
                green_palette = np.frombuffer(green_data, dtype=np.uint16)
                blue_palette = np.frombuffer(blue_data, dtype=np.uint16)
                
                rgb_data = np.zeros((ds.Rows, ds.Columns, 3), dtype=np.uint8)
                rgb_data[..., 0] = red_palette[pixel_data]
                rgb_data[..., 1] = green_palette[pixel_data]
                rgb_data[..., 2] = blue_palette[pixel_data]'''
            
            if ds.Modality == 'CT':
                try:
                    WindowCenter,WindowWidth = ds.WindowCenter[0],ds.WindowWidth[0]
                except:
                    WindowCenter,WindowWidth = ds.WindowCenter,ds.WindowWidth
                pixel_data = pixel_data + ds.RescaleIntercept
                lower = max(WindowCenter - WindowWidth / 2, np.percentile(pixel_data,1))
                upper = min(WindowCenter + WindowWidth / 2, np.percentile(pixel_data,99))
            else:
                lower = np.percentile(pixel_data,1)
                upper = np.percentile(pixel_data,99)
                
            if lower==upper:
                upper += 1
            normalized_data = np.clip((pixel_data - lower) / (upper - lower),0,1)
            grey_data = (normalized_data * 1274).astype(np.uint16)
            rgb_data = p(grey_data).astype(np.uint8)
            
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
            
            '''PaletteTag = [0x281101,0x281102,0x281103,0x281199,0x281201,0x281202,0x281203]
            for tag in list(ds.keys()):
                if tag.group % 2 == 1 or tag in PaletteTag :
                    del ds[tag]'''
            
            relative_path = os.path.relpath(src_file, dicom_folder)
            dst_path = os.path.join(dst_folder, relative_path)
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                  os.makedirs(dst_dir)
            ds.save_as(dst_path)
