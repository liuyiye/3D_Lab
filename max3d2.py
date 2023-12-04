import numpy as np
from scipy.spatial.distance import pdist, squareform

#计算mask的边缘
def find_edge(mask):
    # 沿着6个方向分别平移
    shifted1 = np.roll(mask, 1, axis=0)
    shifted2 = np.roll(mask, -1, axis=0)
    shifted3 = np.roll(mask, 1, axis=1)
    shifted4 = np.roll(mask, -1, axis=1)
    shifted5 = np.roll(mask, 1, axis=2)
    shifted6 = np.roll(mask, -1, axis=2)
    
    # 计算差异，找到边缘
    edge_mask = (mask - shifted1) | (mask - shifted2) | (mask - shifted3) | (mask - shifted4)| (mask - shifted5) | (mask - shifted6)
    
    return edge_mask


node=getNode('mask')
mask=arrayFromVolume(node)
edge_mask=find_edge(mask)

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

#计算轴位最大径
z_slices = np.unique(np.where(edge_mask)[0]) 

max_l = 0
max_w = 0
max_l_z = None

for z in z_slices:
    slice_mask = edge_mask[z,:, :]
    max_slice_d=max_d(slice_mask)
    if max_slice_d[0] > max_l:
        max_l = max_slice_d[0]
        max_l_z = z

print(max_d(edge_mask))
print(max_l,max_l_z)

