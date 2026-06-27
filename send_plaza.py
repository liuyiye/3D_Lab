print("\n输入密码，将当前目录plaza文件夹的内容上传到plaza节点")

import msvcrt
while True:
  password = ''
  while True:
    ch = msvcrt.getwch()
    if ch == '\r':break
    password += ch
  if password == '678':break

send_dir = r'.\plaza'

print('\nSending')

import os,pydicom
from pynetdicom import AE,debug_logger,StoragePresentationContexts

#debug_logger()

ae = AE(ae_title=b'SDM')
ae.requested_contexts = StoragePresentationContexts
ae.connection_timeout=60
assoc = ae.associate('192.168.21.114', 104, ae_title='PLAZAAPP1')
if assoc.is_established:
    for root, dirs, files in os.walk(send_dir):
        for f in files:
            ds=pydicom.dcmread(os.path.join(root, f))
            assoc.send_c_store(ds)
        print(f'\n{root} sent')
    assoc.release()
    input('\nDone!')


