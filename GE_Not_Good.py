import os,csv,time,shutil,pydicom,logging,threading,numpy as np
from datetime import datetime
from pynetdicom import (AE, evt)
from pynetdicom.sop_class import MRImageStorage,PatientRootQueryRetrieveInformationModelFind


# 加载已传输图像的列表
RECEIVED_SERIES_FILE = r'C:\GE_Not_Good\received_series.csv'
with open(RECEIVED_SERIES_FILE, 'r', newline='') as f:
    reader = csv.reader(f)
    received_series = [row[3] for row in reader] 


# 设置接收目录及日志文件
STORAGE_DIR     = r'C:\GE_Not_Good\storage'
COMPLETE_DIR    = r'C:\GE_Not_Good\complete'
logging.basicConfig(
    filename=r'C:\GE_Not_Good\GE_Not_Good.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s')


# 接收图像
def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    series_instance_uid = ds.SeriesInstanceUID
    
    # 判断是GE的图像,并且序列名称不是3D_Lab开头,也没在已传输列表中
    if (# 'ORIGINAL' in ds.ImageType                    and
        ds.Manufacturer=='GE MEDICAL SYSTEMS'           and
        not ds.SeriesDescription.startswith('3D_Lab')   and
        series_instance_uid not in received_series ):
        
        series_dir = os.path.join(STORAGE_DIR, series_instance_uid)
        os.makedirs(series_dir, exist_ok=True)
        file_path = os.path.join(series_dir, f'{ds.SOPInstanceUID}.dcm')
        ds.save_as(file_path, write_like_original=False)
        print(f'Received image {ds.SOPInstanceUID}')
        return 0x0000
    else:
        logging.warning(f'discarding image {ds.PatientID,ds.StudyDate,ds.SeriesDescription,ds.SOPInstanceUID}')
        return 0x0000


# 如果图像不能重建,返回True,函数缺省返回值为None
def t3237(series_dir):
    files = [os.path.join(series_dir, f) for f in os.listdir(series_dir)]
    orientation=[pydicom.dcmread(file)[0x00200037].value for file in files]
    if len(set(map(tuple,orientation)))>1:   # map生成器表达式只能使用一次
        return True
    files.sort(key=lambda x: pydicom.dcmread(x)[0x00200032].value[2])
    position=[pydicom.dcmread(file)[0x00200032].value for file in files]
    a=np.array(position)
    b=np.diff(a,axis=0)
    c=np.diff(b,axis=0)
    if all((c>0.001).reshape(-1)):
        return True


def t3237w(series_dir):
    files = [os.path.join(series_dir, f) for f in os.listdir(series_dir)]
    
    f2013 = files.copy()
    f2013.sort(key=lambda x: pydicom.dcmread(x)[0x00200013].value)
    firstImg = pydicom.dcmread(f2013[0])[0x00200032].value[2]
    lastImg = pydicom.dcmread(f2013[-1])[0x00200032].value[2]
    order = firstImg > lastImg
    
    files.sort(key=lambda x: pydicom.dcmread(x)[0x00200032].value[2],reverse=order)
    position=[pydicom.dcmread(file)[0x00200032].value for file in files]
    orientation=pydicom.dcmread(files[0])[0x00200037].value
    a=np.array(position)
    a=np.round(np.linspace(a[0],a[-1],a[:,0].size),6)
    n=0
    siuid=pydicom.uid.generate_uid()
    for file in files:
        ds=pydicom.dcmread(file)
        ds[0x00080018].value=pydicom.uid.generate_uid()
        ds[0x0008103e].value='3D_Lab_'+ds[0x0008103e].value
        ds[0x0020000e].value=siuid
        ds[0x00200013].value=n+1
        ds[0x00200032].value=list(a[n])
        ds[0x00200037].value=orientation
        n=n+1
        ds.save_as(file)


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
        return(image_count)
        assoc.release()
    else:
        logging.error('Association rejected, aborted or never connected')


# 检查序列是否完整
def check_series():
    global received_series
    for series_dir in os.listdir(STORAGE_DIR):
        series_path = os.path.join(STORAGE_DIR, series_dir)
        series_files = os.listdir(series_path)
        if series_files:
            ds = pydicom.dcmread(os.path.join(series_path, series_files[0]))
            try:images = ds.ImagesInAcquisition # 有些序列没有这个tag
            except:images = 0
            n=len(series_files)
            if n>60 and (n==images or n==image_count_in_series(ds.PatientID,ds.SeriesInstanceUID)):
                logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesDescription} transfer complete, forwarding...')
                if t3237(series_path):
                    now = datetime.now()
                    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    series_info = [date_time, ds.PatientID, ds.StudyDate, ds.SeriesInstanceUID]
                    received_series.append(ds.SeriesInstanceUID)
                    if forward_series(series_path):
                        with open(RECEIVED_SERIES_FILE, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(series_info)
                        complete_path = os.path.join(COMPLETE_DIR, series_dir)
                        shutil.move(series_path, complete_path)
                        logging.warning(f'all done')
                        print(f'all done')
                else:
                    shutil.rmtree(series_path)
                    logging.warning(f'{ds.PatientID,ds.StudyDate,ds.SeriesDescription} t3237 right, removed')


# 修正图像标签,转发图像序列
def forward_series(series_dir):
    ae.connection_timeout=60
    assoc = ae.associate('192.168.21.16', 2002, ae_title=b'SDM')
    if assoc.is_established:
        t3237w(series_dir)
        for file in os.listdir(series_dir):
            ds = pydicom.dcmread(os.path.join(series_dir, file))
            status = assoc.send_c_store(ds)
        assoc.release()
        return True
    else:
        logging.error('Association rejected, unable to send images.')
        return False


def check_series_thread():
    while True:
        time.sleep(10)
        check_series()


# 创建检查线程
check_thread = threading.Thread(target=check_series_thread)
check_thread.start()


# 创建应用实体
handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=b'GE_Not_Good')
ae.add_supported_context(MRImageStorage)
ae.add_supported_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_requested_context(MRImageStorage)
ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])


# 启动服务器
ae.start_server(('172.20.99.71', 11112), evt_handlers=handlers)

