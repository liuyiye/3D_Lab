import os
import time
import shutil
import pydicom
import threading
from pynetdicom.sop_class import MRImageStorage
from pynetdicom import (AE, debug_logger, evt, AllStoragePresentationContexts,ALL_TRANSFER_SYNTAXES)

# 设置接收目录
STORAGE_PATH = r'C:\GE_Not_Good\storage'
COMPLETE_PATH = r'C:\GE_Not_Good\complete'

# 处理C-STORE请求
def handle_store(event):
    """处理C-STORE请求并保存图像到文件夹"""
    ds = event.dataset
    ds.file_meta = event.file_meta
    #判断是GE的图像，并且序列名称不是3D_Lab开头
    if ds.Manufacturer=='GE MEDICAL SYSTEMS' and not ds.SeriesDescription.startswith('3D_Lab'):
    #if True:
        study_instance_uid = ds.StudyInstanceUID
        series_instance_uid = ds.SeriesInstanceUID
        series_dir = os.path.join(STORAGE_PATH, series_instance_uid)
        os.makedirs(series_dir, exist_ok=True)
        
        file_path = os.path.join(series_dir, f'{ds.SOPInstanceUID}.dcm')
        ds.save_as(file_path, write_like_original=False)
        print(f'Received image {ds.SOPInstanceUID}')

# 转发序列
def forward_series(series_dir):
    """将完整的序列转发到目标节点"""
    assoc = ae.associate('127.0.0.1', 11116, ae_title=b'RA')
    if assoc.is_established:
        for file_path in os.listdir(series_dir):
            ds = pydicom.dcmread(os.path.join(series_dir, file_path))
            status = assoc.send_c_store(ds)
            if status.Status != 0x0000:
                print(f'C-STORE failed: {status.Status:04x}')
        assoc.release()
    else:
        print('Association rejected, unable to send images.')

# 检查序列是否完整
def check_series():
    for series_dir in os.listdir(STORAGE_PATH):
        series_path = os.path.join(STORAGE_PATH, series_dir)
        series_files = os.listdir(series_path)
        if series_files:
            ds = pydicom.dcmread(os.path.join(series_path, series_files[0]))
            if len(series_files) == ds.ImagesInAcquisition:
                print(f'Series {series_dir} transfer complete, forwarding...')
                forward_series(series_path)
                complete_path = os.path.join(COMPLETE_PATH, series_dir)
                shutil.move(series_path, complete_path)
                print(f'all done')

def check_series_thread():
    while True:
        time.sleep(10)
        check_series()

# 创建应用实体
handlers = [(evt.EVT_C_STORE, handle_store)]
ae = AE(ae_title=b'Lab')
ae.add_supported_context(MRImageStorage)
ae.add_supported_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])
ae.add_requested_context(MRImageStorage)
ae.add_requested_context(MRImageStorage,[pydicom.uid.JPEGLosslessSV1])

# 创建检查线程
check_thread = threading.Thread(target=check_series_thread)
check_thread.start()

# 启动服务器
ae.start_server(('127.0.0.1', 11112), evt_handlers=handlers)
