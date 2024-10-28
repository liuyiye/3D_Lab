import os
import pydicom

dicom_folder = r'C:\0'
dst_folder = r'C:\1'
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

sduid=pydicom.uid.generate_uid()
for root, dirs, files in os.walk(dicom_folder):
    siuid=pydicom.uid.generate_uid()
    for file in files:
        src_file = os.path.join(root, file)
        try:    
            ds=pydicom.dcmread(src_file)
            is_dicom = True
        except:
            is_dicom = False
        if is_dicom:
            
            ds.PatientName='3D_Lab_exam'
            ds.PatientID='3D_Lab_exam'
            ds.AccessionNumber='3D_Lab_exam'
            ds.SeriesDescription='3D_Lab_exam'
            ds.StudyInstanceUID=sduid

            ds.StudyDate='20240101'
            ds.ContentDate='20240101'
            ds.StudyTime='160608'
            ds.ContentTime='160608'

            ds.ReferringPhysicianName='' #plaza need 
            ds.PatientSex=''#plaza need 

            ds.SeriesInstanceUID=siuid
            ds.SOPInstanceUID=pydicom.uid.generate_uid()

           
            relative_path = os.path.relpath(src_file, dicom_folder)
            dst_path = os.path.join(dst_folder, relative_path)
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                  os.makedirs(dst_dir)
            ds.save_as(dst_path, write_like_original=False)


