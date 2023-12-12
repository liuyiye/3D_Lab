import numpy as np
import open3d
import cv2
from skimage import measure

node=getNode('mask')
mask=arrayFromVolume(node)
coords3d = np.array(np.where(mask)).T

#最大平面的最小外接2D矩形
z_slices = np.unique(np.where(mask)[0])
max_length=0
width=0
max_z=0
for z in z_slices:
    slice_mask=mask[z,:,:]
    coords2d = np.array(np.where(slice_mask)).T
    rect=cv2.minAreaRect(coords2d)
    if max(rect[1][0],rect[1][1]) > max_length:
        max_length=max(rect[1][0],rect[1][1])
        width=min(rect[1][0],rect[1][1])
        max_z=z

print(max_z,max_length,width)

#最小外接3D柱体
pcd = open3d.geometry.PointCloud()
pcd.points = open3d.utility.Vector3dVector(coords)
obb = open3d.geometry.OrientedBoundingBox.create_from_points(pcd.points)
print(obb)


# 标记连通域并获取属性
labels = measure.label(mask, connectivity=1) 
props = measure.regionprops(labels)
for region in props:
    print(f"region {region.label}")
    print(f"volume {region.area}")
    print(f"区域的边界框坐标 {region.bbox}")
    print(f"extent {region.extent}")
    print(f"axis_major_length {region.axis_major_length}")
    print(f"axis_minor_length {region.axis_minor_length}")
    print()
