﻿import numpy as np
import open3d
import slicer
from cv2 import minAreaRect
from skimage import measure
from collections import Counter


#三维mask轴位图像最大面积所在平面的最小外接2D矩形的长宽
def max_area(mask):
    coords3d = np.array(np.where(mask)).T
    z_counter = Counter([p[0] for p in coords3d])
    max_z = z_counter.most_common(1)[0][0]
    slice_mask=mask[max_z,:,:]
    coords2d = np.array(np.where(slice_mask)).T
    rect=minAreaRect(coords2d)
    max_length=max(rect[1][0],rect[1][1])
    width=min(rect[1][0],rect[1][1])
    return(max_length,width)


#三维mask最小外接3D柱体
def max3d(mask,matrix):
    coords3d = np.array(np.where(mask)).T
    coords3d = [np.dot(matrix,i) for i in coords3d]
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(coords3d)
    obb = open3d.geometry.OrientedBoundingBox.create_from_points(pcd.points)
    d3 = sorted(obb.extent)
    L = round(d3[2]/10,1)
    W = round(d3[1]/10,1)
    H = round(d3[0]/10,1)
    return(L,W,H) #返回最大三维长径、宽度、高度


def mask154to21(mask):
    mapping={
    0:[1,2,3,4,17,20,21,22,23,36],
    1:[44,45,57,61,67,73,75,79,87,89,91,93,97,101,103,111,113,127,131,135,137,139,151],
    2:[51,52,58,62,68,74,76,80,88,90,92,94,98,102,104,112,114,128,132,136,138,140,152],
    3:[47,63,99,115,117,123,125,141,145],
    4:[54,64,100,116,118,124,126,142,146],
    5:[46,65,69,81,85,95,107,109,143],
    6:[53,66,70,82,86,96,108,110,144],
    7:[7,18,42,71,77,83,105,119,129,133,147,149,153],
    8:[8,19,49,72,78,84,106,120,130,134,148,150,154],
    9:[43,55,59,121],
    10:[50,56,60,122],
    11:[13,15],
    12:[14,16],
    13:[5,11,24,26,30,32,40],
    14:[6,12,25,27,31,33,41],
    15:[28],
    16:[29],
    17:[48],
    18:[9,10],
    19:[37,38,39],
    20:[34],
    21:[35]}
    
    new=mask.copy()
    new[:]=0
    for key,value in mapping.items():
        for i in value:
             new[mask==i]=key
    
    return(new)


#main()白质高信号定量
def w():
    brain_lobe= {
    1:'右侧额叶',
    2:'左侧额叶',
    3:'右侧顶叶',
    4:'左侧顶叶',
    5:'右侧枕叶',
    6:'左侧枕叶',
    7:'右侧颞叶',
    8:'左侧颞叶',
    9:'右侧岛叶',
    10:'左侧岛叶',
    11:'右侧小脑',
    12:'左侧小脑',
    13:'右侧基底节',
    14:'左侧基底节',
    15:'右侧丘脑',
    16:'左侧丘脑',
    17:'胼胝体',
    18:'脑干',
    19:'小脑蚓部',
    20:'右侧脑室旁白质',
    21:'左侧脑室旁白质'
    }
    
    mask_node=slicer.util.getNode('mask')
    mask=slicer.util.arrayFromVolume(mask_node)
    mask=mask154to21(mask)
    
    flair_node=slicer.util.getNode('lesion_L01')
    flair=slicer.util.arrayFromVolume(flair_node)
    spacing=flair_node.GetSpacing()  # 考虑了spacing
    voxel=np.prod(spacing)
    
    # 标记flair连通域
    labels = measure.label(flair, connectivity=1)
    flair_volume_all = Counter(labels[labels>0])
    flair_volume = [i for i in flair_volume_all.values() if i >= 3]  #大于3个像素
    lesions = len(flair_volume)
    total = sum(flair_volume)
    
    flair_sorted = sorted(flair_volume_all,key=flair_volume_all.get,reverse=True)
    
    max_flair=flair.copy()
    max_flair[:]=0
    max_flair[labels==flair_sorted[0]]=1
    
    max_flair_area=max_area(max_flair)
    max_flair_3d=max3d(max_flair,np.diag(spacing))
    
    mask2=mask.copy()
    mask2[flair==0]=0
    mask3=mask.copy()
    mask3[max_flair==0]=0
    
    c2 = Counter(mask2[mask2>0])
    c3 = Counter(mask3[mask3>0])
    max2=c2.most_common()
    max3=c3.most_common()
    
    print(f"\n全脑脑实质体积为 立方厘米；脑白质高信号病灶共有：{lesions}个，其总体积为：{round(total*voxel/1000,3)}立方厘米")
    
    if lesions>3:
        print("其中最大的三个病灶的体积为:")
        for i in flair_sorted[:3]:
            print(f"{round(flair_volume_all[i]*voxel/1000,3)}立方厘米")
    else:
        print("\n每个病灶的体积为:")
        for i in flair_sorted:
            print(f"{round(flair_volume_all[i]*voxel/1000,3)}立方厘米")      
    
    print(f"\n最大病灶的主体位于{brain_lobe[max3[0][0]]}，轴位图像上长度为{round(max_flair_area[0]*spacing[0]/10,1)}厘米，宽度为{round(max_flair_area[1]*spacing[0]/10,1)}厘米，其最大三维长径为{max_flair_3d[0]}厘米，对应的宽度为{max_flair_3d[1]}厘米，高度为{max_flair_3d[2]}厘米")
    
    print(f"\n{brain_lobe[max2[0][0]]}内的白质病灶总体积最大，为{round(max2[0][1]*voxel/1000,3)}立方厘米\n")


