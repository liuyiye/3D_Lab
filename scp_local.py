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
AllContexts = False
not_save = False
ip = ''
port = 11111
ae_title = 'local'

if menu:
    print('\nreturn for default:\n')
    print('store_folder = scp')
    print('AllContexts = False')
    print('not_save = False')
    print('ip = local')
    print('port = 11111')
    print('ae_title = local\n')
    
    store_folder = input("store_folder:") or 'scp'
    AllContexts = input("AllContexts:") or False
    not_save = input("not_save:") or False
    ip = input("ip:")
    try:port = int(input("port:")) or 11111
    except:pass
    ae_title = input("ae_title:") or 'local'

print(f"scp started. port:{port}, ae_title:{ae_title}, directory:{store_folder}")

import os,re,pydicom
from pynetdicom import AE, evt, AllStoragePresentationContexts
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
    ds = event.dataset
    ds.file_meta = event.file_meta
    try:
        sn=f'{ds.SeriesNumber}_{ds.SeriesDescription}'
        sn = re.sub(r'[<>:"/\\|?*]', '_', sn)
    except:
        sn=None
    pdir = os.path.join(store_folder,ds.PatientID,sn)
    f = os.path.join(pdir, f'{ds.SOPInstanceUID}.dcm')
    if not not_save:
        os.makedirs(pdir, exist_ok=True)
        ds.save_as(f, write_like_original=False)
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=ae_title)

if AllContexts:
    ae.supported_contexts = AllStoragePresentationContexts
else:
    for sop in storage_classes:
        ae.add_supported_context(sop)
        ae.add_supported_context(sop, [pydicom.uid.JPEGLosslessSV1])

ae.start_server((ip, port), block=True, evt_handlers=handlers)
