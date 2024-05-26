import math

import matplotlib.pyplot as plt
import random
import matplotlib
import numpy as np
import cv2
import xmltodict

data = xmltodict.parse(open("Main-CrossRoad.xodr").read())
# data = xmltodict.parse(open("StraightRoad.xodr").read())
type(data)

opendrive = data["OpenDRIVE"]

o_header = opendrive["header"]
o_road = opendrive["road"]
# print(o_road)

o_road_1 = o_road[20] #多条lane的情况
# o_road_1 = o_road # 单条lane的情况

print(opendrive.keys())
print(len(o_road))
print(o_road_1.keys())
print(o_road_1["@name"])
print(o_road_1["@length"])
print(o_road_1["@id"])
print(o_road_1["@junction"])
print("link: ", o_road_1["link"])
print(o_road_1["type"])
print(o_road_1["planView"])
print(o_road_1["elevationProfile"])
print(o_road_1["lateralProfile"])
print(o_road_1["lanes"])