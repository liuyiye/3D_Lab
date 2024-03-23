import slicer

#resamplescalarvolume:

# 获取要重采样的体积节点
volumeNode = slicer.util.getNode("lesion_L01")

# 创建一个新的体积节点来存储重采样结果
outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "lesion_L01_111")

# 设置重采样参数
parameters = {}
parameters["InputVolume"] = volumeNode
parameters["OutputVolume"] = outputVolumeNode
parameters["outputPixelSpacing"] = "2,1,1"
parameters["interpolationType"] = "nearestNeighbor"

# 运行 Resample Scalar Volume 模块
slicer.cli.runSync(slicer.modules.resamplescalarvolume, None, parameters)

#brainsresample:

# 获取输入体积节点和参考图像节点
maskVolumeNode = slicer.util.getNode("mask")
referenceVolumeNode = slicer.util.getNode("lesion_L01_111")

# 创建一个新的体积节点来存储重采样结果
outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "mask_111")

# 设置重采样参数
parameters = {}
parameters["inputVolume"] = maskVolumeNode
parameters["referenceVolume"] = referenceVolumeNode
parameters["outputVolume"] = outputVolumeNode
parameters["pixelType"] = "float"
parameters["interpolationMode"] = "NearestNeighbor"

# 运行 Resample Image 模块
slicer.cli.runSync(slicer.modules.brainsresample, None, parameters)

# 显示重采样结果
#slicer.util.setSliceViewerLayers(background=outputVolumeNode)

