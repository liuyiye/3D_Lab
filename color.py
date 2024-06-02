from pynetdicom import AE, evt, StoragePresentationContexts
import matplotlib.pyplot as plt
import pydicom,logging,numpy as np

logging.basicConfig(
    filename=r'C:\Color\color.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s')

cmap = plt.get_cmap('jet')

def rgb(ds):
    pixel_data = ds.pixel_array
    if 'RedPaletteColorLookupTableData' in ds:
        logging.warning(f'Palette {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription}')
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
        logging.warning(f'cmap {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription}')
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
    
    ds[0x00080018].value = pydicom.uid.generate_uid()
    ds[0x0008103e].value = '3D_Lab_'+ds[0x0008103e].value
    
    uid=ds[0x0020000e].value
    root = uid[:-1]
    last_digit = int(uid[-1])
    new_last_digit = (last_digit + 2) % 10
    modified_uid = root + str(new_last_digit)
    ds[0x0020000e].value = modified_uid
    
    assoc = ae.associate('172.19.83.228',4006,ae_title=b'AE_TITLE')
    if assoc.is_established:
        status = assoc.send_c_store(ds)
        assoc.release()
    return 0x0000

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    if ds.PhotometricInterpretation == 'RGB':
        logging.warning(f'discard {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription}')
    else:
        rgb(ds)
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=b'Color')

for context in StoragePresentationContexts:
    ae.add_supported_context(context.abstract_syntax)
    ae.add_requested_context(context.abstract_syntax)

ae.start_server(('', 11112), block=False, evt_handlers=handlers)
