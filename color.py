import pydicom,logging,numpy as np
from skimage.transform import resize
from pynetdicom import AE,evt,debug_logger,StoragePresentationContexts,ALL_TRANSFER_SYNTAXES

#debug_logger()

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
    
    if ds.Modality == 'MR' and min(ds.Rows,ds.Columns) < 256:
        normalized_data = pixel_data / np.max(pixel_data)
        resized_data = resize(normalized_data, (2*ds.Rows, 2*ds.Columns), mode='reflect', anti_aliasing=True)
        pixel_data = (resized_data * np.max(pixel_data)).astype(np.uint16)
        ds.Rows, ds.Columns = pixel_data.shape
        lower = np.percentile(pixel_data,2)
        upper = np.percentile(pixel_data,98)
    
    '''if 'RedPaletteColorLookupTableData' in ds:
        logging.warning(f'Palette {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.InstanceNumber,ds.SeriesDescription}')
        red_data = ds.RedPaletteColorLookupTableData
        green_data = ds.GreenPaletteColorLookupTableData
        blue_data = ds.BluePaletteColorLookupTableData
        
        red_palette = np.frombuffer(red_data, dtype=np.uint16)
        green_palette = np.frombuffer(green_data, dtype=np.uint16)
        blue_palette = np.frombuffer(blue_data, dtype=np.uint16)
        
        rgb_data = np.zeros((ds.Rows, ds.Columns, 3), dtype=np.uint8)
        rgb_data[..., 0] = red_palette[pixel_data]
        rgb_data[..., 1] = green_palette[pixel_data]
        rgb_data[..., 2] = blue_palette[pixel_data]
    else:
        logging.warning(f'P1275 {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.InstanceNumber,ds.SeriesDescription}')'''
    
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
    
    logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.InstanceNumber,ds.SeriesDescription}')
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
    
    '''PaletteTag = [0x281101,0x281102,0x281103,0x281199,0x281201,0x281202,0x281203]
    for tag in list(ds.keys()):
        if tag.group % 2 == 1 or tag in PaletteTag :
            del ds[tag]'''
    
    assoc = ae.associate('192.168.21.102', 11101, ae_title=b'IDMAPP1')
    #assoc = ae.associate('192.168.21.16', 2002, ae_title=b'SDM')
    #assoc = ae.associate('172.20.99.71', 11111, ae_title=b'SCP')
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
for context in StoragePresentationContexts:
    ae.add_supported_context(context.abstract_syntax, ALL_TRANSFER_SYNTAXES)
    ae.add_requested_context(context.abstract_syntax, ALL_TRANSFER_SYNTAXES)

ae.start_server(('', 11113), block=True, evt_handlers=handlers)
