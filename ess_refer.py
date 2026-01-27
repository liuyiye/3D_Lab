import os
import pydicom

reference_dcm = pydicom.dcmread(r'C:\0.dcm')
reference_tags = set(e.tag for e in reference_dcm)

ori_folder = r'C:\1'
ess_folder = r'C:\2'

if not os.path.exists(ess_folder):
    os.makedirs(ess_folder)

for root, dirs, files in os.walk(ori_folder):
    # siuid=pydicom.uid.generate_uid() # 1dir 1series
    for file in files:
        src_file = os.path.join(root, file)
        try:    
            ds=pydicom.dcmread(src_file)
            is_dicom = True
        except:
            is_dicom = False
        if is_dicom:
            for elem in ds:
                if (elem.tag) not in reference_tags:
                    del ds[elem.tag]

            ds.file_meta = pydicom.Dataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
            ds.SOPInstanceUID=pydicom.uid.generate_uid()
            # ds.SeriesDescription='ess_'+ds.SeriesDescription
            # ds.SeriesInstanceUID = siuid
            
            relative_path = os.path.relpath(src_file, ori_folder)
            dst_path = os.path.join(ess_folder, relative_path)
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                  os.makedirs(dst_dir)
            ds.save_as(dst_path)
