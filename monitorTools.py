# 调试工具与监控工具

# 记录距离/速度曲线，并进行压缩；
# 车辆超出边缘线/实线距离判定
# 车辆与障碍物距离判定

import numpy as np
import math
from scipy.spatial.transform import Rotation as R

class Monitor():
    def __init__(self):
        self.infoFreq = 1000 #消息输出频率 1000ms
        self.distEndList = []
        self.velList = []

        self.distSolidList = []

        self.distObstList = []

        # 定时器监听  timer --callback

    def __distEndInfo__(self, pos, end):
        return math.sqrt(math.pow(pos.x - end[0], math.pow(pos.y - end[1])))

    def __velInfo__(self, velList):
        self.velList = velList

    # 判断包络面与solidline交点/距离
    def __distSolidInfo__(self, pos, referencePath, sizelen, sizeWid):
        # 拟合一次函数
        para = np.polyfit(pos.x, pos.y, 1)

        # 判断点与多边形是否相交

    def __stateClear__(self):
        self.distEndList = []
        self.velList = []
        self.distSolidList = []
        self.distObstList = []


