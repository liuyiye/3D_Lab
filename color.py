from pynetdicom import AE, evt, StoragePresentationContexts
import pydicom,logging,numpy as np
#import cv2

logging.basicConfig(
    filename='/home/edu/Color/color.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s')

SERIES_UID_FILE = '/home/edu/Color/received_series.txt'
SOP_UID_FILE = '/home/edu/Color/received_sop.txt'
COLOR_MAP = '/home/edu/Color/color_map.csv'

jet = np.genfromtxt(COLOR_MAP, delimiter=',', skip_header=1)

def get_series_uid_value(uid):
    with open(SERIES_UID_FILE, 'r+') as f:
        for line in f:
            key, value = line.strip().split(':')
            if key == uid:
                return value
        
        new_value = pydicom.uid.generate_uid()
        f.write(f'{uid}:{new_value}\n')
        return new_value

def exist_sop(uid):
    with open(SOP_UID_FILE, 'r+') as f:
        uids = f.read().splitlines()
        if uid in uids:
            return True
        else:
            f.write(f'{uid}\n')

def rgb(ds):
    logging.warning(f'jet {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription}')
    pixel_data = ds.pixel_array
    i,j = pixel_data.shape
    if ds.Modality == 'CT':
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
    
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesDescription = '3D_Lab_'+ds.SeriesDescription
    ds.SeriesInstanceUID = get_series_uid_value(ds.SeriesInstanceUID)
    
    #assoc = ae.associate('192.168.21.102', 11101, ae_title=b'IDMAPP1')
    assoc = ae.associate('192.168.21.16', 2002, ae_title=b'SDM')
    if assoc.is_established:
        status = assoc.send_c_store(ds)
        assoc.release()
    return 0x0000

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    if ds.PhotometricInterpretation.startswith('MONO') and not exist_sop(ds.SOPInstanceUID):
        rgb(ds)
    else:
        logging.warning(f'discard {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription}')
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=b'Color')

for context in StoragePresentationContexts:
    ae.add_supported_context(context.abstract_syntax)
    ae.add_requested_context(context.abstract_syntax)

ae.start_server(('', 11113), block=True, evt_handlers=handlers)

