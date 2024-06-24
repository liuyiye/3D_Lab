import pydicom,logging,numpy as np
from skimage.transform import resize
from pynetdicom import AE, evt
from pynetdicom.sop_class import CTImageStorage,MRImageStorage

logging.basicConfig(
    filename='/home/edu/Color/color.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s')

SERIES_UID_FILE = '/home/edu/Color/received_series.txt'
SOP_UID_FILE = '/home/edu/Color/received_sop.txt'

palette = np.genfromtxt('/home/edu/Color/palette1275.csv', delimiter=',', skip_header=0)
def p(x):
    return(palette[x])

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
        pixel_data = pixel_data + ds.RescaleIntercept
        lower = WindowCenter - WindowWidth / 2
        upper = WindowCenter + WindowWidth / 2
    elif 'ttp' in ds.SeriesDescription.lower():
        lower = np.percentile(pixel_data,1)
        upper = np.percentile(pixel_data,97)
    elif 'mtt' in ds.SeriesDescription.lower():
        lower = np.percentile(pixel_data,1)
        upper = np.percentile(pixel_data,98)
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
    
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesDescription = '3D_Lab_'+ds.SeriesDescription
    ds.SeriesInstanceUID = get_series_uid_value(ds.SeriesInstanceUID)
    
    logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.InstanceNumber,ds.SeriesDescription}')
    
    assoc = ae.associate('192.168.21.102', 11101, ae_title=b'IDMAPP1')
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
        logging.warning(f'discard {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.InstanceNumber,ds.SeriesDescription}')
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=b'Color')
ae.add_supported_context(MRImageStorage)
ae.add_supported_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_requested_context(MRImageStorage)
ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_supported_context(CTImageStorage)
ae.add_supported_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_requested_context(CTImageStorage)
ae.add_requested_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])

ae.start_server(('172.20.99.71', 11113), block=True, evt_handlers=handlers)
