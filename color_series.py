import os,csv,time,shutil,pydicom,logging,random,numpy as np
from datetime import datetime
from skimage.transform import resize
from pynetdicom import AE,evt,debug_logger
from pynetdicom.sop_class import (
    CTImageStorage,
    MRImageStorage,
    PatientRootQueryRetrieveInformationModelFind,
    PatientRootQueryRetrieveInformationModelMove)

#debug_logger()

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
    files = [os.path.join(series_dir, f) for f in os.listdir(series_dir)]
    siuid=pydicom.uid.generate_uid()
    for f in files:
        ds=pydicom.dcmread(f)
        if ds.PhotometricInterpretation != 'RGB':
            pixel_data = ds.pixel_array
            datas1,datas97,datas98,datas99 = np.percentile(pixel_data,[1,97,98,99])
            
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
            
            #构建一个精简的dataset，适配uih
            data = pydicom.Dataset()
            data.file_meta = pydicom.Dataset()
            data.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
            
            data.SOPClassUID = ds.SOPClassUID
            data.PatientID = ds.PatientID
            data.StudyInstanceUID = ds.StudyInstanceUID
            data.PatientName = ds.PatientName
            data.StudyID = ds.StudyID
            data.StudyDate = ds.StudyDate
            data.StudyTime = ds.StudyTime
            data.ContentDate = ds.ContentDate
            data.ContentTime = ds.ContentTime
            data.AccessionNumber = ds.AccessionNumber
            data.Modality = ds.Modality
            data.SeriesNumber = ds.SeriesNumber
            data.PatientBirthDate = ds.PatientBirthDate
            data.ReferringPhysicianName = ds.ReferringPhysicianName
            data.PatientSex = ds.PatientSex
            
            data.SeriesDescription='3D_Lab_'+ds.SeriesDescription
            data.SeriesInstanceUID = siuid
            data.SeriesDate = ds.SeriesDate
            data.SeriesTime = ds.SeriesTime
            data.SOPInstanceUID = pydicom.uid.generate_uid()
            data.InstanceNumber = ds.InstanceNumber
            data.Rows=ds.Rows
            data.Columns=ds.Columns
            data.PhotometricInterpretation = 'RGB'
            data.PlanarConfiguration = 0
            data.RescaleIntercept=0
            data.SamplesPerPixel=3
            data.BitsAllocated = 8
            data.BitsStored = 8
            data.HighBit = 7
            data.PixelRepresentation = 0
            data.PixelData = rgb_data.tobytes()
            
            data.SliceLocation=''
            data.ImagePositionPatient = ''
            data.ImageOrientationPatient = ''
            data.NumberOfFrames = ''
            data.PixelSpacing = ''
            data.WindowCenter = ''
            data.WindowWidth = ''
            data.RescaleSlope = ''
            data.RescaleType = ''
            
            data.save_as(f, write_like_original=False)


def pwi(text):
    text = text.lower()
    keywords = ['cbv','cbf','mtt','ttp','asl','pbp']
    if any(word in text for word in keywords):
        return True


# 接收图像
def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    series_instance_uid = ds.SeriesInstanceUID
    
    if (ds.PhotometricInterpretation.startswith('MONO') and ds.Modality == 'MR' and
        series_instance_uid not in received_series and pwi(ds.SeriesDescription)):
        
        series_dir = os.path.join(STORAGE_DIR, series_instance_uid)
        os.makedirs(series_dir, exist_ok=True)
        file_path = os.path.join(series_dir, f'{ds.SOPInstanceUID}.dcm')
        ds.save_as(file_path, write_like_original=False)
        return 0x0000
    else:
        logging.warning(f'discard {ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.InstanceNumber,ds.SeriesDescription}')
        return 0x0000


def image_count_in_series(ID,STUID,SUID):
    ds = pydicom.Dataset()
    ds.PatientID=ID
    ds.StudyInstanceUID = STUID
    ds.SeriesInstanceUID = SUID
    ds.QueryRetrieveLevel = 'SERIES'
    ds.NumberOfSeriesRelatedInstances = None
    ds.SeriesDescription= None
    
    ae = AE(ae_title=b'C3D')
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
    ae.connection_timeout=60
    assoc = ae.associate('192.168.21.102', 11101, ae_title=b'IDMAPP1')
    
    if assoc.is_established:
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
        for (status, identifier) in responses:
            if identifier:
                image_count = int(identifier.NumberOfSeriesRelatedInstances)
                logging.warning(f'image_count_in_series_{identifier.SeriesDescription}: {image_count}')
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
            n=len(series_files)
            logging.warning(f'n1={n}')
            try:m = image_count_in_series(ds.PatientID,ds.StudyInstanceUID,series_dir)
            except:m = 0
            if m==0: #图像未发送到pacs
                logging.warning(f'count=0')
                time.sleep(60)
            if n>0 and n<m: #接收到的图像不全
                time.sleep(60)
                n_files = os.listdir(series_path)
                n=len(n_files)
                logging.warning(f'n2={n}')
                if n<m:
                    move_series_to_color(ds.PatientID,ds.StudyInstanceUID,ds.SeriesInstanceUID)
                    n_files = os.listdir(series_path)
                    n=len(n_files)
                    logging.warning(f'n3={n}')
            if (n==m or m==0) and n < 36 and n > 16:
                logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription} transfer complete, forwarding...')
                color(series_path)
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                series_info = [date_time, ds.PatientID, ds.StudyDate, ds.SeriesInstanceUID]
                received_series.append(ds.SeriesInstanceUID)
                if send(series_path,'192.168.21.114', 104, 'PLAZAAPP1'):
                    send(series_path,'192.168.21.102', 11101, 'IDMAPP1')
                    send(series_path,'172.21.253.62', 30966, 'UIHHXZS66')
                    with open(RECEIVED_SERIES_FILE, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(series_info)
                    complete_path = os.path.join(COMPLETE_DIR, series_dir)
                    shutil.move(series_path, complete_path)
                    logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription} all done\n')
            else:
                complete_path = os.path.join(COMPLETE_DIR, series_dir)
                try:
                    shutil.move(series_path, complete_path)
                    logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription} moved\n')
                except Exception as e:
                    logging.warning(e)
                    shutil.rmtree(series_path,ignore_errors=True)
                    logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription} deleted\n')


def send(s_path,ip,port,aet):
    ae = AE(ae_title=b'SDM')
    ae.add_requested_context(MRImageStorage)
    ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
    ae.add_requested_context(CTImageStorage)
    ae.add_requested_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])
    ae.connection_timeout=60
    assoc = ae.associate(ip,port,ae_title=aet)
    if assoc.is_established:
        for f in os.listdir(s_path):
            ds = pydicom.dcmread(os.path.join(s_path, f))
            status = assoc.send_c_store(ds)
        assoc.release()
        logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesNumber,ds.SeriesDescription} send to {aet} OK')
        return True


def move_series_to_color(PID,SDUID,SUID):
    ae = AE(ae_title=b'C3D')
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
    ae.connection_timeout=60
    assoc = ae.associate('192.168.21.102', 11101, ae_title=b'IDMAPP1')
    if assoc.is_established:
        ds = pydicom.Dataset()
        ds.PatientID = PID
        ds.StudyInstanceUID = SDUID
        ds.SeriesInstanceUID = SUID
        ds.QueryRetrieveLevel = "SERIES"
        responses = assoc.send_c_move(ds, 'Color', PatientRootQueryRetrieveInformationModelMove)
        for (status, identifier) in responses:
            if status:
                logging.warning(f'Color: 0x{status.Status:04x}')
        assoc.release()
    else:
        logging.warning('Association rejected, aborted or never connected')


# 创建应用实体
handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=b'Color')
ae.add_supported_context(MRImageStorage)
ae.add_supported_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_supported_context(CTImageStorage)
ae.add_supported_context(CTImageStorage,[pydicom.uid.JPEGLosslessSV1])


# 启动服务器
ae.start_server(('172.20.99.71', 11113), block=False, evt_handlers=handlers)


while True:
    time.sleep(10)
    check_series()
