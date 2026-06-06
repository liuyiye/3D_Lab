import pydicom
from pynetdicom import AE,debug_logger
from pynetdicom.sop_class import StudyRootQueryRetrieveInformationModelFind

#debug_logger()

ds = pydicom.Dataset()
ds.QueryRetrieveLevel = 'STUDY'
ds.AccessionNumber = 'MR02921855'
ds.PatientID = ''
ds.PatientName = ''

ae = AE(ae_title=b'SDM')
ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)
assoc = ae.associate('192.168.21.114', 104, ae_title=b'PLAZAAPP1')
if assoc.is_established:
    responses = assoc.send_c_find(ds, StudyRootQueryRetrieveInformationModelFind)
    for status, identifier in responses:
        if identifier:
            print("Patient ID:",identifier.PatientID)
            print('Patient Name:',identifier.PatientName)
    assoc.release()

#findscu -S -aet SDM -aec PLAZAAPP1 192.168.21.114 104 -k QueryRetrieveLevel=STUDY -k AccessionNumber=MR02921855
