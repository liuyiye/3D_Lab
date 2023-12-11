import numpy as np
from scipy.spatial.distance import pdist, squareform


#计算三维mask的边缘
def find_edge_3d(mask):
    # 沿着6个方向分别平移，因为mask不会出现在最边缘，就不用考虑卷折到另一边
    shifted1 = np.roll(mask, 1, axis=0)
    shifted2 = np.roll(mask, -1, axis=0)
    shifted3 = np.roll(mask, 1, axis=1)
    shifted4 = np.roll(mask, -1, axis=1)
    shifted5 = np.roll(mask, 1, axis=2)
    shifted6 = np.roll(mask, -1, axis=2)
    
    # 计算差异，找到边缘。-1 or 1 = -1,所以使用clip将结果限制在0和1。也可用mask.astype(bool)，-1 or 1 就等于1了。前者代码更简单。
    edge_mask = (mask - shifted1) | (mask - shifted2) | (mask - shifted3) | (mask - shifted4)| (mask - shifted5) | (mask - shifted6)
    edge_mask =edge_mask.clip(0, 1)
    return edge_mask

#计算二维mask的边缘
def find_edge(mask):
    # 沿着4个方向分别平移，因为mask不会出现在最边缘，就不用考虑卷折到另一边
    shifted1 = np.roll(mask, 1, axis=0)
    shifted2 = np.roll(mask, -1, axis=0)
    shifted3 = np.roll(mask, 1, axis=1)
    shifted4 = np.roll(mask, -1, axis=1)
    
    # 计算差异，找到边缘。-1 or 1 = -1,所以使用clip将结果限制在0和1。也可用mask.astype(bool)，-1 or 1 就等于1了。前者代码更简单。
    edge_mask = (mask - shifted1) | (mask - shifted2) | (mask - shifted3) | (mask - shifted4)
    edge_mask =edge_mask.clip(0, 1)
    return edge_mask

#计算最大径及相应的坐标
def max_d(mask):
    coords = np.array(np.where(mask)).T
    distances = pdist(coords)
    max_distance=distances.max()
    
    distance_matrix = squareform(distances)
    max_distance_index = np.argmax(distance_matrix)
    i, j = np.unravel_index(max_distance_index, distance_matrix.shape)
    point1 = coords[i]
    point2 = coords[j]
    
    return(max_distance,point1,point2)


node=getNode('mask')
mask=arrayFromVolume(node)
n=getNode('v')
a=arrayFromVolume(n)

edge_mask_3d=find_edge_3d(mask)


#计算三维最大径及相应的坐标
m=max_d(edge_mask_3d)
#在volume中标记相应的坐标
a[m[1][0],m[1][1],m[1][2]]=a.max()+1000
a[m[2][0],m[2][1],m[2][2]]=a.max()+1000


#计算轴位最大径所在层面及相应的坐标
z_slices = np.unique(np.where(mask)[0]) 

max_l = 0
max_l_z = None
point1 = None
point2 = None

for z in z_slices:
    slice_mask = find_edge(mask[z,:, :])
    max_slice_d=max_d(slice_mask)
    if max_slice_d[0] > max_l:
        max_l = max_slice_d[0]
        max_l_z = z
        point1=max_slice_d[1]
        point2=max_slice_d[2]

a[max_l_z,point1[0],point1[1]]=a.max()+1000
a[max_l_z,point2[0],point2[1]]=a.max()+1000


# 计算最大垂直宽度计算
def dist(a,b):
    line0=a-b
    line = line0.astype(np.float64)/np.linalg.norm(line0)
    if abs(line@ direction) <0.01:
        d = line0 @ perp
        return abs(d)
    else:
        return(0)

direction = point1 - point2
perpendicular = np.array([direction[1], -direction[0]])  
perp=perpendicular / np.linalg.norm(perpendicular)
direction = direction.astype(np.float64)/ np.linalg.norm(direction)

max_w = 0
pt1 = None
pt2 = None
slice_mask = find_edge(mask[max_l_z, :, :])
coords = np.array(np.where(slice_mask)).T
for i in range(len(coords)):
   for j in range(i+1, len(coords)):
      p1 = coords[i]  
      p2 = coords[j]
      width = dist(p1, p2)
      if width>max_w:
          max_w=width
          pt1,pt2=p1,p2

a[max_l_z,pt1[0],pt1[1]]=a.max()+1000
a[max_l_z,pt2[0],pt2[1]]=a.max()+1000


print(m)
print(max_l,max_l_z,point1,point2)
print(max_w,pt1,pt2)

