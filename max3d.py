
import numpy as np

node=getNode('mask')
mask=arrayFromVolume(node)

z_slices = np.unique(np.where(mask)[0]) 

max_d = 0
max_w = 0
max_d_z = None

for z in z_slices:

    slice_mask = mask[z,:, :]
    
    # 1. 计算xy最大长径
    pos = np.where(slice_mask)
    inds = np.transpose(pos)
    deltas = inds[:, np.newaxis] - inds[np.newaxis, :]
    dists_sq = np.sum(np.square(deltas), axis=-1)
    #dists = np.sqrt(dists_sq)  
    
    max_slice_d = np.max(dists_sq)
    
    if max_slice_d > max_d:
        max_d = max_slice_d
        max_d_z = z

# 最终最大垂直宽度计算
slice_mask = mask[max_d_z, :, :]   

pos = np.where(slice_mask)
inds = np.transpose(pos)
deltas = inds[:, np.newaxis] - inds[np.newaxis, :]
dists_sq = np.sum(np.square(deltas), axis=-1)
dists = np.sqrt(dists_sq)
    
idx = np.unravel_index(dists.argmax(), dists.shape)
p1, p2 = inds[idx[0]], inds[idx[1]]

direction = p1 - p2
perpendicular = np.array([direction[1], -direction[0]])  
perp=perpendicular / np.linalg.norm(perpendicular)

###############

def dist(v):
    if v @ direction <0.01:
        d = v @ perp
        return abs(d)
    else:
        return(0)

distances = np.apply_along_axis(dist, 2, deltas)
max_w = np.max(distances)

print(np.sqrt(max_d), max_w)


###############

def dist(a,b):
    if (a-b) @ direction <0.01:
        d = (a-b) @ perp
        return abs(d)
    else:
        return(0)

max_w = 0
for i in range(len(inds)):
   for j in range(i+1, len(inds)):
      pt1 = inds[i]  
      pt2 = inds[j]
      distance = dist(pt1, pt2)
      max_w = max(max_w, distance)

