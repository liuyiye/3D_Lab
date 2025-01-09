import os,re,pydicom
from pynetdicom import AE, evt
from pynetdicom.sop_class import *

storage_classes = [
    RawDataStorage,
    CTImageStorage,
    MRImageStorage,
    SecondaryCaptureImageStorage,
    XRayAngiographicImageStorage,
    DigitalMammographyXRayImageStorageForPresentation,
    DigitalXRayImageStorageForPresentation,
    NuclearMedicineImageStorage,
    PositronEmissionTomographyImageStorage
]

store_folder=r'D:\SCP'

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    try:
        sn = f'{ds.SeriesNumber}_{ds.SeriesDescription}'
        sn = re.sub(r'[<>:"/\\|?*]', '_', sn)
        id_name = f'{ds.PatientID}_{ds.PatientName}_{ds.ContentDate}'
        id_name = re.sub(r'[<>:"/\\|?*]', '_', id_name)
    except:
        sn='unknown_series'
        id_name=ds.PatientID
    pdir = os.path.join(store_folder,id_name,sn)
    f = os.path.join(pdir, f'{ds.SOPInstanceUID}.dcm')
    os.makedirs(pdir, exist_ok=True)
    ds.save_as(f, write_like_original=False)
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE(ae_title=b'C3D')
for sop in storage_classes:
    ae.add_supported_context(sop)
    ae.add_supported_context(sop, [pydicom.uid.JPEGLosslessSV1])

ae.start_server(("", 11112), block=True, evt_handlers=handlers)
