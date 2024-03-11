import os
import nibabel as nib
import numpy as np
from nibabel.processing import resample_from_to

nii_path = r'c:\0'
files = [file for file in os.listdir(nii_path) if file.endswith('.nii.gz')]

ref_nii = nib.load(os.path.join(nii_path,'skin.nii.gz'))
merged_data = ref_nii.get_fdata()

for file in files:
    nii = nib.load(os.path.join(nii_path, file))
    resampled_nii = resample_from_to(nii, ref_nii)
    merged_data=np.logical_or(merged_data, resampled_nii.get_fdata()).astype(int)

merged_data=(merged_data-ref_nii.get_fdata()).astype(int)
merged_nii = nib.Nifti1Image(merged_data, ref_nii.affine)
nib.save(merged_nii,os.path.join(nii_path, 'merged_seg.nii.gz'))
