import slicer

patientUID='0038074114'

# 设置阈值范围
thresholdRange = [250, 1500]

# 获取 Data 模块中的 Subject Hierarchy 节点
shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)

# 获取指定病人的 Subject Hierarchy 项目 ID
patientItemID = shNode.GetItemByUID(slicer.vtkMRMLSubjectHierarchyConstants.GetDICOMUIDName(), patientUID)

# 检查病人是否存在
if patientItemID == slicer.vtkMRMLSubjectHierarchyNode.GetInvalidItemID():
    raise ValueError(f"Patient with UID '{patientUID}' not found in the Data module.")

# 获取病人所有体积节点
volumeNodes = vtk.vtkCollection()
shNode.GetDataNodesInBranch(patientItemID, volumeNodes)

# 过滤体积节点
volumeNodes = [node for node in volumeNodes if node.IsA("vtkMRMLScalarVolumeNode")]
n=0
# 遍历每个体积节点并执行阈值分割
for volumeNode in volumeNodes:
    # 创建旋转变换
    n=n+1
    rotationTransform = vtk.vtkTransform()
    rotationTransform.RotateY(2*n)

    # 将旋转变换应用于体积节点
    volumeNode.ApplyTransform(rotationTransform)

    # 创建分割节点
    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    segmentationNode.CreateDefaultDisplayNodes()  # 仅在需要显示时才需要
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(volumeNode)

    # 添加一个新的空段
    segmentationNode.GetSegmentation().AddEmptySegment("Segment_1")

    # 切换到 Segment Editor 模块
    slicer.util.selectModule("SegmentEditor")

    # 选择分割节点和源体积
    segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
    segmentEditorWidget.setSegmentationNode(segmentationNode)
    segmentEditorWidget.setSourceVolumeNode(volumeNode)

    # 选择“阈值”效应
    segmentEditorWidget.setActiveEffectByName("Threshold")

    # 设置“阈值”效应参数
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("ThresholdType", "Between")
    effect.setParameter("MinimumThreshold", str(thresholdRange[0]))
    effect.setParameter("MaximumThreshold", str(thresholdRange[1]))

    # 应用“阈值”效应
    effect.self().onApply()

    # 显示分割结果
    segmentationNode.CreateClosedSurfaceRepresentation()