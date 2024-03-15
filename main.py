
import sys
import numpy as np

n = 200            #地图大小200x200
robot_num = 10     #机器人数量10
berth_num = 10     #泊位数量10    船的数量为5
N = 210            #gds数组的大小为210*210。

#机器人类
class Robot:
    def __init__(self, startX=0, startY=0, goods=0, status=0, mbx=6, mby=0):
        self.x = startX
        self.y = startY
        self.goods = goods
        self.status = status
        self.mbx = mbx
        self.mby = mby

robot = [Robot() for _ in range(robot_num + 10)]  #这难道不是一个20*20的列表？？


#泊位类
class Berth:
    def __init__(self, x=0, y=0, transport_time=0, loading_speed=0):
        self.x = x
        self.y = y
        self.transport_time = transport_time
        self.loading_speed = loading_speed

berth = [Berth() for _ in range(berth_num + 10)]    #这难道不是一个20*20的列表？？

#船类
class Boat:
    def __init__(self, num=0, pos=0, status=0):
        self.num = num
        self.pos = pos
        self.status = status

boat = [Boat() for _ in range(10)]  #这难道不是一个10*10的列表？？


money = 0           #得分
boat_capacity = 0   #船的容积
id = 0          #？
ch = []         #接收地图信息的列表
gds = [[0 for _ in range(N)] for _ in range(N)]     #用于接收判题器在第一帧生成的货物坐标。210*210

#初始化，传入地图，泊位坐标，泊位装卸速度
#-------------------------------------------------------------------------------------------------
def Init():
    for i in range(0, n):
        line = input()
        ch.append([c for c in line.split(sep=" ")])
    for i in range(berth_num):
        line = input()
        berth_list = [int(c) for c in line.split(sep=" ")]
        id = berth_list[0]
        berth[id].x = berth_list[1]
        berth[id].y = berth_list[2]
        berth[id].transport_time = berth_list[3]
        berth[id].loading_speed = berth_list[4]
    boat_capacity = int(input())        #船的容积
    okk = input()
    print("OK")
    sys.stdout.flush()

#接收判题器传入的数据
#-------------------------------------------------------------------------------------------------------
def Input():
    id, money = map(int, input().split(" "))
    num = int(input())
    for i in range(num):
        x, y, val = map(int, input().split())
        gds[x][y] = val
    for i in range(robot_num):
        robot[i].goods, robot[i].x, robot[i].y, robot[i].status = map(int, input().split())
    for i in range(5):
        boat[i].status, boat[i].pos = map(int, input().split())
    okk = input()
    return id


#将地图分为10个区域，并进行编号，记录每个区域左上角和右下角的坐标，放在字典中。
def map_split():
    # for i in range(0, n):
    #     line = input()
    #     cha.append([c for c in line.split(sep=" ")])
    map_width = 200
    map_height = 200
    num_regions = 10
    region_width = map_width // num_regions
    region_height = map_height // num_regions
    regions_dict = {} #空字典
    for i in range(num_regions):
        for j in range(num_regions):
            regions_dict["region{}".format(i)] = {     #对划分的区域进行编号，并把得到的左上角和右下角的坐标给到原来的键
                'x1': i * region_width,
                'y1': j * region_height,
                'x2': (i + 1) * region_width if i < num_regions - 1 else map_width,
                'y2': (j + 1) * region_height if j < num_regions - 1 else map_height
            }
    return regions_dict   #获得10个区域,并返回region_dict的字典
            #地图划分，字典保存示例：{'region0': {'x1': 0, 'y1': 180, 'x2': 20, 'y2': 200}, 'region1': {'x1': 20, 'y1': 180, 'x2': 40, 'y2': 200}, 'region2': {'x1': 40, 'y1': 180, 'x2': 60, 'y2': 200}, 'region3': {'x1': 60, 'y1': 180, 'x2': 80, 'y2': 200}}
#-------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    Init()
    for zhen in range(1, 15001):
        id = Input()
        money = int(input())
        regions=map_split()
        l = 0
        #获取第一帧所有货物的坐标点，并每隔1000帧重新获取一次。
        #gds_lo:存放货物坐标的数组
        gds_val_lo = {}#gds_val_lo:存放货物坐标及其价值的字典
        if zhen == 1 or zhen%1000 == 0 :
            gds_location= np.nonzero(gds)
            for ii, (i, j) in enumerate(zip(gds_location[0], gds_location[1])):
                key = "gds{}".format(ii)  # 构建键名
                value = {gds[i, j]: {"x": i, "y": j}}
                gds_val_lo[key] = value
                #gds_val_lo字典，键为货物价值，值则为货物的坐标。
                #gds_val_lo保存的形式例子：{'gds0': {2: {'x': 0, 'y': 1}}, 'gds1': {4: {'x': 1, 'y': 0}}, 'gds2': {6: {'x': 1, 'y': 2}}, 'gds3': {8: {'x': 2, 'y': 1}}, 'gds4': {9: {'x': 2, 'y': 2}}}
    #______________________________________________________________________________________________________
        #方案1：
            #优点：通过分区的形式，将机器人个数平均分配到不同的区域，且避免在运输过程中发生碰撞。
            #缺点：前期会消耗大量时间
            #未考虑行走间的障碍。
        # 将10个机器人分别行走到相应区域
        for l in range(10):
            #计算机器人坐标和指定区域坐标的插值（！存在问题！即使满足条件，但每次都会进行一个ax和by的算数操作。）
            ax = ((regions["region"+str(l)]["x2"]-regions["region"+str(l)]["x1"])/2-(robot[l].mbx))
            by = ((regions["region"+str(l)]["y2"]-regions["region"+str(l)]["y1"])/2-(robot[l].mby))
            if ax != 0 and by != 0:
                if ax != 0 :
                    if ax > 0:  #确定初始应该行走的x大致方向
                        print("move", l, 2)
                    elif ax < 0:
                        print("move", l, 3)
                elif by != 0:   #确定初始应该行走的y大致方向
                    if by > 0:
                        print("move", l, 1)
                    elif by < 0:
                        print("move", l, 0)
            else:
                break
            # 限制机器人运动区域,不带货物的时候不能离开自己的区域。
            for iii in range(10):
                if robot[iii].goods == 0 :
                    regions["region"+str(iii)]["x1"]< robot[iii].mbx < regions["region"+str(iii)]["x2"]
                    regions["region"+str(iii)]["y1"]< robot[iii].mbx < regions["region"+str(iii)]["y2"]
    #_______________________________________________________________________________________________________



    #机器人确定最佳货物
        for i in range(robot_num):
            print("move", i, 2)
            robot_a,robot_b =robot[i].mbx,robot[i].mby
        for boat in range(4):
            a = 0
            print("ship",boat,a)
            a+=2
            sys.stdout.flush()
        print("OK")
        sys.stdout.flush()

