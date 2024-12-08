import os,re,pydicom
from pynetdicom import AE, evt, AllStoragePresentationContexts

store_folder=r'D:\SCP'

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    try:
        sn=f'{ds.SeriesNumber}_{ds.SeriesDescription}'
        sn = re.sub(r'[<>:"/\\|?*]', '_', sn)
    except:
        sn=None
    pdir = os.path.join(store_folder,ds.PatientID,sn)
    f = os.path.join(pdir, f'{ds.SOPInstanceUID}.dcm')
    os.makedirs(pdir, exist_ok=True)
    ds.save_as(f, write_like_original=False)
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE(ae_title=b'C3D')
ae.supported_contexts = AllStoragePresentationContexts
ae.start_server(("", 11112), block=True, evt_handlers=handlers)
