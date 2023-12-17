import numpy as np
import open3d
from cv2 import minAreaRect
from skimage import measure
from skimage.filters import threshold_otsu
from collections import Counter


#三维mask最大长径平面的最小外接2D矩形
def max2d(mask):
    z_slices = np.unique(np.where(mask)[0])
    max_length=0
    width=0
    max_z=0
    for z in z_slices:
        slice_mask=mask[z,:,:]
        coords2d = np.array(np.where(slice_mask)).T
        rect=minAreaRect(coords2d)
        if max_length < max(rect[1][0],rect[1][1]):
            max_length=max(rect[1][0],rect[1][1])
            width=min(rect[1][0],rect[1][1])
            max_z=z
    return(max_z,round(max_length/10,1),round(width/10,1))





#最小外接3D柱体
def max3d(mask):
    coords3d = np.array(np.where(mask)).T
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(coords3d)
    obb = open3d.geometry.OrientedBoundingBox.create_from_points(pcd.points)
    return(round(obb.extent.max()/10,1)) #返回最大三维长径



#白质高信号定量
def w():
    mask_node=getNode('mask')
    mask=arrayFromVolume(mask_node)

    t1_node=getNode('t1')
    t1=arrayFromVolume(t1_node)
    thresh = threshold_otsu(t1[mask>0]) #mask范围内T1WI脑脊液和脑组织的阈值

    brain=mask.copy()
    brain[:]=0
    brain[(mask>0) & (t1 >= thresh)] = 1 #brain只保留脑组织

    flair_node=getNode('flair')
    flair=arrayFromVolume(flair_node)
    #flair[brain==0]=0 #可能被脑脊液分割开
    flair[mask==0]=0

    # 标记flair连通域并获取属性
    labels = measure.label(flair, connectivity=1)
    props = measure.regionprops(labels)

    regions=labels.max()
    total=(labels!=0).sum()

    flair_volume = Counter(labels[labels>0])
    flair_sorted = sorted(flair_volume,key=flair_volume.get,reverse=True)

    max_flair=flair.copy()
    max_flair[:]=0
    max_flair[labels==flair_sorted[0]]=1
    max_flair_2d=max2d(max_flair)
    max_flair_3d=max3d(max_flair)
    
    print(f"脑白质高信号共有{regions}个区域,总体积为{round(total/1000,2)} 立方厘米")
    print(f"最大病灶位于第{max_flair_2d[0]}层面，长度为{max_flair_2d[1]}厘米，宽度为{max_flair_2d[2]}厘米,最大三维长径为{max_flair_3d}厘米")

    if regions>3:
        print("其中最大的三个区域的体积为:")
        for i in flair_sorted[:3]:
            print(f"{round(flair_volume[i]/1000,2)} 立方厘米")
    else:
        print("每个区域的体积为:")
        for i in flair_sorted:
            print(f"{round(flair_volume[i]/1000,2)} 立方厘米")

    #another method
    for i in flair_sorted[1:4]:
        print(f"region {props[i-1].label}")
        print(f"volume {props[i-1].area}")
        print(f"区域的边界框坐标 {props[i-1].bbox}")
        print(f"extent {props[i-1].extent}")
        print(f"axis_major_length {props[i-1].axis_major_length}")
        print(f"axis_minor_length {props[i-1].axis_minor_length}")
        print()



