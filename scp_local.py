import msvcrt
while True:
  password = ''
  menu = False
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == '678':break
  if password == '678i':
      menu = True
      break

store_folder = 'scp'
all_sop = False
discard = False
debug = False
ip = ''
port = 12345
ae_title = 'local'

if menu:
    print('\nreturn for default:')
    print('store_folder = scp')
    print('all_sop = False')
    print('discard = False')
    print('debug = False')
    print('ip = local')
    print('port = 12345')
    print('ae_title = local\n')
    
    store_folder = input("store_folder:") or 'scp'
    all_sop = input("all_sop:") or False
    discard = input("discard:") or False
    debug = input("debug:") or False
    ip = input("ip:")
    try:port = int(input("port:")) or 12345
    except:pass
    ae_title = input("ae_title:") or 'local'

print(f"scp started. port:{port}, ae_title:{ae_title}, directory:{store_folder}")

import os,re,pydicom
from pynetdicom import AE, evt, debug_logger, AllStoragePresentationContexts
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

def handle_store(event):
    if debug:
        debug_logger()
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
    if not discard:
        os.makedirs(pdir, exist_ok=True)
        ds.save_as(f, write_like_original=False)
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=ae_title)

if all_sop:
    ae.supported_contexts = AllStoragePresentationContexts
else:
    for sop in storage_classes:
        ae.add_supported_context(sop)
        ae.add_supported_context(sop, [pydicom.uid.JPEGLosslessSV1])

ae.start_server((ip, port), block=True, evt_handlers=handlers)
