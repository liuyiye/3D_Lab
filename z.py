import numpy as np
import open3d
import slicer
from cv2 import minAreaRect
from skimage import measure
from skimage.filters import threshold_otsu
from collections import Counter


#三维mask轴位图像最大长径所在平面的最小外接2D矩形
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
    
    return(max_z,round(max_length/10,1),round(width/10,1),round(mask[max_z,:,:].sum()/100,2))


#三维mask轴位图像最大面积所在平面的最小外接2D矩形
def max_area(mask):
    coords3d = np.array(np.where(mask)).T
    z_counter = Counter([p[0] for p in coords3d])
    max_z = z_counter.most_common(1)[0][0]
    max_area = z_counter.most_common(1)[0][1]
    slice_mask=mask[max_z,:,:]
    coords2d = np.array(np.where(slice_mask)).T
    rect=minAreaRect(coords2d)
    max_length=max(rect[1][0],rect[1][1])
    width=min(rect[1][0],rect[1][1])
    return(max_z,round(max_length/10,1),round(width/10,1),round(max_area/100,2))


#三维mask最小外接3D柱体
def max3d(mask):
    coords3d = np.array(np.where(mask)).T
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(coords3d)
    obb = open3d.geometry.OrientedBoundingBox.create_from_points(pcd.points)
    d3 = sorted(obb.extent)
    L = round(d3[2]/10,1)
    W = round(d3[1]/10,1)
    H = round(d3[0]/10,1)
    return(L,W,H) #返回最大三维长径、宽度、高度


#白质高信号定量
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
    18:'脑干'
    }
    
    mask_node=slicer.util.getNode('mask')
    mask=slicer.util.arrayFromVolume(mask_node)
    
    t1_node=slicer.util.getNode('t1')
    t1=slicer.util.arrayFromVolume(t1_node)
    thresh = threshold_otsu(t1[mask>0]) #mask范围内T1WI脑脊液和脑组织的阈值
    
    brain=mask.copy()
    brain[:]=0
    brain[(mask>0) & (t1 >= thresh)] = 1 #brain只保留脑组织，不要脑脊液
    
    flair_node=slicer.util.getNode('flair')
    flair=slicer.util.arrayFromVolume(flair_node)
    #flair[brain==0]=0 #可能被脑脊液分割开
    #flair[mask==0]=0 #可能被脑叶交界区分割开
    
    # 标记flair连通域并获取属性
    labels = measure.label(flair, connectivity=1)
    lesions=labels.max()
    total=(labels!=0).sum()
    
    flair_volume = Counter(labels[labels>0])
    flair_sorted = sorted(flair_volume,key=flair_volume.get,reverse=True)
    
    max_flair=flair.copy()
    max_flair[:]=0
    max_flair[labels==flair_sorted[0]]=1
    max_flair_2d=max2d(max_flair)
    max_flair_area=max_area(max_flair)
    max_flair_3d=max3d(max_flair)
    
    mask1=mask.copy()
    mask1[brain==0]=0
    mask2=mask1.copy()
    mask2[flair==0]=0
    mask3=mask1.copy()
    mask3[max_flair==0]=0
    
    c1 = Counter(mask1[mask1>0])
    c2 = Counter(mask2[mask2>0])
    c3 = Counter(mask3[mask3>0])
    max3=c3.most_common()
    
    print(f"\n脑白质高信号共有{lesions}个病灶,总体积为{round(total/1000,2)}立方厘米")
    if lesions>3:
        print("其中最大的三个病灶的体积为:")
        for i in flair_sorted[:3]:
            print(f"{round(flair_volume[i]/1000,2)}立方厘米")
    else:
        print("\n每个病灶的体积为:")
        for i in flair_sorted:
            print(f"{round(flair_volume[i]/1000,2)}立方厘米")
    
    print(f"\n白质高信号体积最大病灶主体位于{brain_lobe[max3[0][0]]}，该叶内的白质高信号体积为：{round(max3[0][1]/1000,2)}立方厘米")
    print(f"其最大三维长径为{max_flair_3d[0]}厘米，对应的宽度为{max_flair_3d[1]}厘米，高度为{max_flair_3d[2]}厘米")
    print(f"其轴位图像最大长径位于第{max_flair_2d[0]}层面，长度为{max_flair_2d[1]}厘米，宽度为{max_flair_2d[2]}厘米，面积为{max_flair_2d[3]}平方厘米")
    print(f"其轴位图像最大面积位于第{max_flair_area[0]}层面，长度为{max_flair_area[1]}厘米，宽度为{max_flair_area[2]}厘米，面积为{max_flair_area[3]}平方厘米")
    
    print()
    for i in sorted(c1):
        if i in brain_lobe:
            print(f"序号{i},{brain_lobe[i]}的体积为：{round(c1[i]/1000,2)}立方厘米")
        #else:
            #print(i,round(c1[i]/1000,2))
    
    print()
    ratio={}
    for i in sorted(c2):
        if i in brain_lobe:
            print(f"序号{i},{brain_lobe[i]}的体积为：{round(c1[i]/1000,2)}立方厘米，该叶内的白质高信号体积为：{round(c2[i]/1000,2)}立方厘米，白质高信号占比为：{round(c2[i]/c1[i],3)}")
            ratio[i]=100*round(c2[i]/c1[i],3)
    
    print()
    max1=sorted(ratio,key=ratio.get,reverse=True)
    max2=c2.most_common()
    print(f"白质高信号最大占比位于{brain_lobe[max1[0]]}，占比为：{ratio[max1[0]]}%")
    print(f"{brain_lobe[max2[0][0]]}内的白质高信号总体积最大，该叶内的白质高信号体积为：{round(max2[0][1]/1000,2)}立方厘米\n")

