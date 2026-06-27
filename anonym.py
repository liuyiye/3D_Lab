import os
import pydicom

dicom_folder = r'.\ori'
output_folder = r'.\plaza'
newdate = '20260601'

study_uid = {}
series_uid = {}

for root, dirs, files in os.walk(dicom_folder):
    name = os.path.relpath(root,dicom_folder).split(os.sep)[0]
    for file in files:
        src_file = os.path.join(root, file)
        try:
            ds = pydicom.dcmread(src_file)
            ds.PatientName = name
            ds.PatientID = name
            ds.AccessionNumber = name
            ds.Modality = 'MR'
            
            if name not in study_uid:
               study_uid[name] = pydicom.uid.generate_uid()
            ds.StudyInstanceUID = study_uid[name]
            
            if ds.SeriesInstanceUID not in series_uid:
               series_uid[ds.SeriesInstanceUID] = pydicom.uid.generate_uid()
            ds.SeriesInstanceUID = series_uid[ds.SeriesInstanceUID]
            
            for elem in ds.iterall():
               if elem.VR in ('DA','DT'):
                   elem.value = newdate
            
            ds.SOPInstanceUID = pydicom.uid.generate_uid()
            relative_path = os.path.relpath(root,dicom_folder)
            output_file = os.path.join(output_folder,relative_path,ds.SOPInstanceUID)
            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
               os.makedirs(output_dir)
            ds.save_as(f'{output_file}.dcm')
        except:
            print(src_file)
