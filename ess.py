import os
import pydicom

ori_folder = r'C:\1'
ess_folder = r'C:\2'

if not os.path.exists(ess_folder):
    os.makedirs(ess_folder)

essential_tag=[0x80005,0x80008,0x80016,0x80018,0x80020,0x80021,0x80023,0x80030,0x80031,0x80033,0x80050,0x80060,0x80070,0x80090,0x81030,0x8103e,0x81090,0x100010,0x100020,0x100030,0x100040,0x180050,0x185100,0x20000d,0x20000e,0x200010,0x200011,0x200013,0x200032,0x200037,0x200052,0x201040,0x280002,0x280004,0x280010,0x280011,0x280030,0x280100,0x280101,0x280102,0x280103,0x281050,0x281051,0x281052,0x281053,0x281054,0x7fe00010]	

for root, dirs, files in os.walk(ori_folder):
    for file in files:
        src_file = os.path.join(root, file)
        try:    
            ds=pydicom.dcmread(src_file)
            is_dicom = True
        except:
            is_dicom = False
        if is_dicom:
            for elem in ds:
               if elem.tag not in essential_tag:
                   del ds[elem.tag]
            
            ds.file_meta = pydicom.Dataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
            ds.SOPInstanceUID=pydicom.uid.generate_uid()
            
            relative_path = os.path.relpath(src_file, ori_folder)
            dst_path = os.path.join(ess_folder, relative_path)
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                  os.makedirs(dst_dir)
            ds.save_as(dst_path)

