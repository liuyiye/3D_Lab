import os,csv,time,shutil,pydicom,logging,threading,random,numpy as np
from datetime import datetime
from skimage.transform import resize
from pynetdicom import AE, evt
from pynetdicom.sop_class import CTImageStorage,MRImageStorage,PatientRootQueryRetrieveInformationModelFind


# 加载已传输图像的列表
RECEIVED_SERIES_FILE = '/home/edu/Color/received_series.csv'
with open(RECEIVED_SERIES_FILE, 'r', newline='') as f:
    reader = csv.reader(f)
    received_series = [row[3] for row in reader] 


# 设置接收目录及日志文件
STORAGE_DIR     = '/home/edu/Color/storage'
COMPLETE_DIR    = '/home/edu/Color/complete'
logging.basicConfig(
    filename='/home/edu/Color/color.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s')


palette = np.genfromtxt('/home/edu/Color/palette1275.csv', delimiter=',', skip_header=0)
def p(x):
    return(palette[x])


def color(series_dir):
    dicom_files = [os.path.join(series_dir, f) for f in os.listdir(series_dir)]
    datas = np.array([pydicom.dcmread(file).pixel_array for file in dicom_files])
    datas1,datas97,datas98,datas99 = np.percentile(datas,[1,97,98,99])
    
    siuid=pydicom.uid.generate_uid()
    for file in dicom_files:
        ds=pydicom.dcmread(file)
        if ds.PhotometricInterpretation != 'RGB':
            pixel_data = ds.pixel_array
            
            if min(ds.Rows,ds.Columns) < 256:
                normalized_data = pixel_data / np.max(pixel_data)
                resized_data = resize(normalized_data, (2*ds.Rows, 2*ds.Columns), mode='reflect', anti_aliasing=True)
                pixel_data = (resized_data * np.max(pixel_data)).astype(np.uint16)
                ds.Rows, ds.Columns = pixel_data.shape
            
            if ds.Modality == 'CT':
                try:
                    WindowCenter,WindowWidth = ds.WindowCenter[0],ds.WindowWidth[0]
                except:
                    WindowCenter,WindowWidth = ds.WindowCenter,ds.WindowWidth
                d = ds.RescaleIntercept
                pixel_data = pixel_data + d
                lower = max(WindowCenter - WindowWidth / 2, datas1 + d)
                upper = min(WindowCenter + WindowWidth / 2, datas99 + d)
            elif 'ttp' in ds.SeriesDescription.lower():
                lower = datas1
                upper = datas97
            elif 'mtt' in ds.SeriesDescription.lower():
                lower = datas1
                upper = datas98
            else:
                lower = datas1
                upper = datas99
            
            if lower==upper:
                upper += 1
            normalized_data = np.clip((pixel_data - lower) / (upper - lower),0,1)
            grey_data = (normalized_data * 1274).astype(np.uint16)
            rgb_data = p(grey_data).astype(np.uint8)
            
            if 'RescaleIntercept' in ds:
                ds.RescaleIntercept = 0
            ds.PhotometricInterpretation = 'RGB'
            ds.SamplesPerPixel = 3
            ds.BitsAllocated = 8
            ds.BitsStored = 8
            ds.HighBit = 7
            ds.PixelRepresentation = 0
            ds.PixelData = rgb_data.tobytes()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
            
            ds.SOPInstanceUID = pydicom.uid.generate_uid()
            ds.SeriesDescription = '3D_Lab_'+ds.SeriesDescription
            ds.SeriesInstanceUID = siuid
            
            ds.save_as(file)


# 接收图像
def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    series_instance_uid = ds.SeriesInstanceUID
    
    if (ds.PhotometricInterpretation.startswith('MONO') and
        series_instance_uid not in received_series ):
        
        series_dir = os.path.join(STORAGE_DIR, series_instance_uid)
        os.makedirs(series_dir, exist_ok=True)
        file_path = os.path.join(series_dir, f'{ds.SOPInstanceUID}.dcm')
        ds.save_as(file_path, write_like_original=False)
        return 0x0000
    else:
        logging.warning(f'discard {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.InstanceNumber,ds.SeriesDescription}')
        return 0x0000


def image_count_in_series(PID,SUID):
    ds = pydicom.Dataset()
    ds.PatientID = PID
    ds.SeriesInstanceUID = SUID
    ds.QueryRetrieveLevel = "IMAGE"
    
    ae = AE(ae_title=b'C3D')
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
    ae.connection_timeout=60
    assoc = ae.associate('192.168.21.16',2002,ae_title=b'SDM')
    image_count = -1
    if assoc.is_established:
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
        for (status, ds) in responses:
            if status:
                image_count += 1
            else:
                logging.error('Connection timed out, was aborted or received invalid response')
        
        # Release the association
        logging.warning(f'image_count_in_series: {image_count}')
        assoc.release()
        return(image_count)
    else:
        logging.error('Association rejected, aborted or never connected')


# 检查序列是否完整
def check_series():
    global received_series
    series_dirs = os.listdir(STORAGE_DIR)
    random.shuffle(series_dirs)
    for series_dir in series_dirs:
        series_path = os.path.join(STORAGE_DIR, series_dir)
        series_files = os.listdir(series_path)
        if series_files:
            ds = pydicom.dcmread(os.path.join(series_path, series_files[0]))
            try:images = ds.ImagesInAcquisition # 有些序列没有这个tag
            except:images = 0
            n=len(series_files)
            if n==images or n==image_count_in_series(ds.PatientID,series_dir):
                logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription} transfer complete, forwarding...')
                color(series_path)
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                series_info = [date_time, ds.PatientID, ds.StudyDate, ds.SeriesInstanceUID]
                received_series.append(ds.SeriesInstanceUID)
                if send_to_new_pacs(series_path):
                    with open(RECEIVED_SERIES_FILE, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(series_info)
                    complete_path = os.path.join(COMPLETE_DIR, series_dir)
                    shutil.move(series_path, complete_path)
                    logging.warning(f'series done')


def send_to_new_pacs(series_dir):
    ae.connection_timeout=60
    assoc = ae.associate('192.168.21.102', 11101, ae_title=b'IDMAPP1')
    if assoc.is_established:
        for file in os.listdir(series_dir):
            ds = pydicom.dcmread(os.path.join(series_dir, file))
            status = assoc.send_c_store(ds)
        assoc.release()
        return True


# 创建应用实体
handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=b'Color')
ae.add_supported_context(MRImageStorage)
ae.add_supported_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_requested_context(MRImageStorage)
ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_supported_context(CTImageStorage)
ae.add_supported_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_requested_context(CTImageStorage)
ae.add_requested_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])


# 启动服务器
ae.start_server(('172.20.99.71', 11113), block=False, evt_handlers=handlers)


while True:
    time.sleep(10)
    check_series()
    
