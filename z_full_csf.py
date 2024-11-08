import numpy as np
import open3d
import slicer
from cv2 import minAreaRect
from skimage import measure
from scipy.spatial.distance import pdist, squareform
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


#三维mask轴位图像最大面积所在平面的最小外接2D矩形、真实长径及相应的坐标
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
    true=true_max3d(slice_mask)
    p1=[max_z,true[1][0],true[1][1]]
    p2=[max_z,true[2][0],true[2][1]]
    return(max_z,round(max_length/10,1),round(width/10,1),round(max_area/100,2),round(true[0]/10,2),p1,p2)


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


#计算三维mask的边缘
def find_edge_3d(mask):
    # 沿着6个方向分别平移，因为mask不会出现在最边缘，就不用考虑卷折到另一边
    shifted1 = np.roll(mask, 1, axis=0)
    shifted2 = np.roll(mask, -1, axis=0)
    shifted3 = np.roll(mask, 1, axis=1)
    shifted4 = np.roll(mask, -1, axis=1)
    shifted5 = np.roll(mask, 1, axis=2)
    shifted6 = np.roll(mask, -1, axis=2)
    
    # 计算差异，找到边缘。
    edge_mask = (mask > shifted1) | (mask > shifted2) | (mask > shifted3) | (mask > shifted4)| (mask > shifted5) | (mask > shifted6)
    return edge_mask


#计算二维mask的边缘
def find_edge_2d(mask):
    # 沿着4个方向分别平移，因为mask不会出现在最边缘，就不用考虑卷折到另一边
    shifted1 = np.roll(mask, 1, axis=0)
    shifted2 = np.roll(mask, -1, axis=0)
    shifted3 = np.roll(mask, 1, axis=1)
    shifted4 = np.roll(mask, -1, axis=1)
    
    # 计算差异，找到边缘。
    edge_mask = (mask > shifted1) | (mask > shifted2) | (mask > shifted3) | (mask > shifted4)
    return edge_mask


#计算三维最大径及相应的坐标(传入edge_mask以减少计算量)
def true_max3d(mask):
    coords = np.array(np.where(mask)).T
    distances = pdist(coords)
    max_distance=distances.max()
    
    distance_matrix = squareform(distances)
    max_distance_index = np.argmax(distance_matrix)
    i, j = np.unravel_index(max_distance_index, distance_matrix.shape)
    point1 = coords[i]
    point2 = coords[j]
    return(max_distance,point1,point2)


#计算轴位最大径、所在层面及相应的坐标
def true_max2d(mask):
    z_slices = np.unique(np.where(mask)[0]) 
    
    max_2d_in_slice = 0
    max_2d_z_value = 0
    point1 = None
    point2 = None
    
    for z in z_slices:
        slice_mask = find_edge_2d(mask[z,:, :])
        if slice_mask.sum()>1:#跳过只有一个体素的病灶
            temp=true_max3d(slice_mask)
            if max_2d_in_slice < temp[0]:
                max_2d_in_slice = temp[0]
                max_2d_z_value = z
                point1=[z,temp[1][0],temp[1][1]]
                point2=[z,temp[2][0],temp[2][1]]
    
    return(max_2d_z_value,max_2d_in_slice,point1,point2)


def mask154to22(mask):
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


def orient(node):
    import vtk

    m = vtk.vtkMatrix4x4()
    node.GetIJKToRASMatrix(m)

    k_direction = [m.GetElement(0,2),m.GetElement(1,2),m.GetElement(2,2)]

    max_index = np.argmax(np.abs(k_direction))

    if max_index == 0:
        orientation = '矢状位'
    elif max_index == 2:
        orientation = '轴位'
    else:
        orientation = '冠状位'

    return orientation


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
    
    
    volumeNode = slicer.util.getNode("lesion_L01")
    orientation = orient(volumeNode)
    outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "lesion_L01_111")
    
    parameters = {}
    parameters["InputVolume"] = volumeNode
    parameters["OutputVolume"] = outputVolumeNode
    parameters["outputPixelSpacing"] = "1,1,1"
    parameters["interpolationType"] = "nearestNeighbor"
    
    slicer.cli.runSync(slicer.modules.resamplescalarvolume, None, parameters)
    
    maskVolumeNode = slicer.util.getNode("mask")
    referenceVolumeNode = slicer.util.getNode("lesion_L01_111")
    outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "mask_111")
    
    parameters = {}
    parameters["inputVolume"] = maskVolumeNode
    parameters["referenceVolume"] = referenceVolumeNode
    parameters["outputVolume"] = outputVolumeNode
    parameters["pixelType"] = "float"
    parameters["interpolationMode"] = "NearestNeighbor"
    
    slicer.cli.runSync(slicer.modules.brainsresample, None, parameters)
    
    csf=[4,5,14,15,24,43,44]
    synthseg_node=slicer.util.getNode('synthseg')
    synthseg_ori=slicer.util.arrayFromVolume(synthseg_node)
    synthseg=synthseg_ori.copy() #避免改动该节点的显示
    for i in csf:
        synthseg[synthseg==i]=1
    
    synthseg[synthseg>1]=2
    spacing=synthseg_node.GetSpacing()  # 考虑了spacing
    voxel=np.prod(spacing)
    csf_volume=len(synthseg[synthseg==1])*voxel
    brain_volume=len(synthseg[synthseg==2])*voxel
    
    mask_node=slicer.util.getNode('mask_111')
    mask=slicer.util.arrayFromVolume(mask_node)
    if mask.max() > 64:
        mask=mask154to22(mask)
    
    flair_node=slicer.util.getNode('lesion_L01_111')
    flair=slicer.util.arrayFromVolume(flair_node)
    flair=np.where(flair==0,0,1) #转换matlab得到的lesion_L01，np.where比flair.astype(bool).astype(int)更快
    
    # 标记flair连通域并获取属性
    labels = measure.label(flair, connectivity=1)
    flair_volume_all = Counter(labels[labels>0])
    flair_volume = [i for i in flair_volume_all.values() if i >= 3]  #大于3个像素
    lesions = len(flair_volume)
    total = sum(flair_volume)
    flair_sorted = sorted(flair_volume_all,key=flair_volume_all.get,reverse=True)
    
    max_flair=flair.copy()
    max_flair[:]=0
    max_flair[labels==flair_sorted[0]]=1
    
    max_flair_2d=max2d(max_flair)
    max_flair_area=max_area(max_flair)
    max_flair_3d=max3d(max_flair)
    
    true_max_flair_3d=true_max3d(find_edge_3d(max_flair))
    true_max_flair_2d=true_max2d(max_flair)
    
    mask2=mask.copy()
    mask2[flair==0]=0
    mask3=mask.copy()
    mask3[max_flair==0]=0
    
    c1 = Counter(mask[mask>0])
    c2 = Counter(mask2[mask2>0])
    c3 = Counter(mask3[mask3>0])
    max2=c2.most_common()
    max3=c3.most_common()
    
    print(f"\n全脑脑实质体积为{round(brain_volume/1000)}立方厘米；脑白质高信号病灶共有：{lesions}个，其总体积为：{round(total/1000,3)}立方厘米")
    
    if lesions>3:
        print("其中最大的三个病灶的体积为:")
        for i in flair_sorted[:3]:
            print(f"{round(flair_volume_all[i]/1000,3)}立方厘米")
    else:
        print("\n每个病灶的体积为:")
        for i in flair_sorted:
            print(f"{round(flair_volume_all[i]/1000,3)}立方厘米")
    
    print(f"\n最大病灶的主体位于{brain_lobe[max3[0][0]]}，轴位图像上长度为{max_flair_area[1]}厘米，宽度为{max_flair_area[2]}厘米，其最大三维长径为{max_flair_3d[0]}厘米，对应的宽度为{max_flair_3d[1]}厘米，高度为{max_flair_3d[2]}厘米")
    
    print(f"\n{brain_lobe[max2[0][0]]}内的白质病灶总体积最大，为{round(max2[0][1]/1000,3)}立方厘米\n")
    
    ###附加信息###
    print("\n###附加信息###:")
    print(f"\n白质高信号体积最大病灶主体位于{brain_lobe[max3[0][0]]}")
    print(f"其最大三维长径为{max_flair_3d[0]}厘米，对应的宽度为{max_flair_3d[1]}厘米，高度为{max_flair_3d[2]}厘米")
    print(f"其真实三维长径为{round(true_max_flair_3d[0]/10,2)}厘米，两个端点的坐标ZYX为{true_max_flair_3d[1]}和{true_max_flair_3d[2]}")
    #在flair图像中标记相应的坐标
    flair[true_max_flair_3d[1][0],true_max_flair_3d[1][1],true_max_flair_3d[1][2]]=2
    flair[true_max_flair_3d[2][0],true_max_flair_3d[2][1],true_max_flair_3d[2][2]]=2
    
    print(f"\n其{orientation}图像最大长径位于第{max_flair_2d[0]}层面，长度为{max_flair_2d[1]}厘米，宽度为{max_flair_2d[2]}厘米，面积为{max_flair_2d[3]}平方厘米")
    print(f"其{orientation}图像真实长径位于第{true_max_flair_2d[0]}层面，长度为{round(true_max_flair_2d[1]/10,2)}厘米，两个端点的坐标ZYX为{true_max_flair_2d[2]}和{true_max_flair_2d[3]}")
    #在flair图像中标记相应的坐标
    flair[true_max_flair_2d[2][0],true_max_flair_2d[2][1],true_max_flair_2d[2][2]]=3
    flair[true_max_flair_2d[3][0],true_max_flair_2d[3][1],true_max_flair_2d[3][2]]=3
    
    print(f"\n其{orientation}图像最大面积位于第{max_flair_area[0]}层面，长度为{max_flair_area[1]}厘米，宽度为{max_flair_area[2]}厘米，面积为{max_flair_area[3]}平方厘米")
    print(f"其真实长径为{max_flair_area[4]}厘米，两个端点的坐标ZYX为{max_flair_area[5]}和{max_flair_area[6]}")
    #在flair图像中标记相应的坐标
    flair[max_flair_area[5][0],max_flair_area[5][1],max_flair_area[5][2]]=4
    flair[max_flair_area[6][0],max_flair_area[6][1],max_flair_area[6][2]]=4
    mark_node=slicer.modules.volumes.logic().CloneVolume(slicer.mrmlScene,flair_node,'mark')
    slicer.util.updateVolumeFromArray(mark_node,flair)
    
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
    print(f"白质高信号最大占比位于{brain_lobe[max1[0]]}，占比为：{ratio[max1[0]]}%")





