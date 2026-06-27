import os
import pydicom

dicom_folder = r'D:\anonym\ori'
output_folder = r'D:\anonym\plaza'
newdate = '20260601'

uid = {}
PatientName = [i for i in os.listdir(dicom_folder)]

for name in PatientName:
    StudyUID = pydicom.uid.generate_uid()
    for root, dirs, files in os.walk(os.path.join(dicom_folder,name)):
        for file in files:
            src_file = os.path.join(root, file)
            try:
                ds = pydicom.dcmread(src_file)
                for elem in ds.iterall():
                   if elem.VR in ('DA','DT'):
                       elem.value = newdate
                ds.PatientName = name
                ds.PatientID = name
                ds.StudyInstanceUID = StudyUID
                if ds.SeriesInstanceUID not in uid:
                   uid[ds.SeriesInstanceUID] = pydicom.uid.generate_uid()
                ds.SeriesInstanceUID = uid[ds.SeriesInstanceUID]
                ds.AccessionNumber = name
                ds.Modality = 'MR'
                ds.SOPInstanceUID = pydicom.uid.generate_uid()

                output_file = os.path.join(root, ds.SOPInstanceUID)
                relative_path = os.path.relpath(output_file,dicom_folder)
                output_path = os.path.join(output_folder,relative_path)
                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                   os.makedirs(output_dir)
                ds.save_as(output_path)
            except:
                print(src_file)
