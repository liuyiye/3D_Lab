import os,pydicom,numpy as np
from skimage.transform import resize

dicom_folder = '/home/edu/0'
dst_folder = '/home/edu/1'
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

for root, dirs, files in os.walk(dicom_folder):
    for f in files:
        src_file = os.path.join(root, f)
        try:    
            ds=pydicom.dcmread(src_file)
            series_dir = os.path.join(dst_folder, ds.SeriesInstanceUID)
            os.makedirs(series_dir, exist_ok=True)
            file_path = os.path.join(series_dir, f'{ds.SOPInstanceUID}.dcm')
            ds.save_as(file_path, write_like_original=False)
        except:
            pass # or continue

palette = np.genfromtxt('/home/edu/Color/palette1275.csv', delimiter=',', skip_header=0)
def p(x):
    return(palette[x])

for root, dirs, files in os.walk(dst_folder):
    for d in dirs:
        files = [os.path.join(root,d,f) for f in os.listdir(os.path.join(root,d))]
        datas = np.array([pydicom.dcmread(f).pixel_array for f in files])
        datas1,datas97,datas98,datas99 = np.percentile(datas,[1,97,98,99])
        for f in files:
            ds=pydicom.dcmread(f)
            if ds.PhotometricInterpretation != 'RGB':
                pixel_data = ds.pixel_array
                
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
                ds.save_as(f)
