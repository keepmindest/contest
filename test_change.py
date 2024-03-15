import time

from matplotlib import pyplot as plt
from matplotlib.patches import Circle

fig = plt.figure(figsize=(110, 110))

subplot = fig.add_subplot(111)   #向创建的110*110的图形里面添加一个子图，这个子图的位置是1。在将主图分为1*1的区域情况下

subplot.set_xlabel('X-distance: m')
subplot.set_ylabel('Y-distance: m')

def plot_my(x,y,k):
    subplot.plot(y, 99-x,k)

ch = []
weight = [[0 for _ in range(200)] for _ in range(200)]
za = []

with open('E:\\ruantiao\demo\WindowsRelease2.0\maps\map1.txt','r') as file:
        lines = file.readlines()
        for line in lines:
            ah = [char for char in line]
            ch.append(ah)
for ii in range(200):
    for jj in range(200):
        if ch[ii][jj] in ['#', '*']:
            plot_my(ii, jj,".b")
        elif ch[ii][jj] in ['B']:
            plot_my(ii, jj,"ko")




# for iii in range(1,99):
#     for jjj in range(1,99):
#         wei = 0
#         for ii in range(iii-1, iii+2):
#             for jj in range(jjj - 1, jjj + 2):
#                 if ch[ii][jj] in ['#', '*']:
#                     wei = wei + 1
#         weight[iii][jjj]=wei
# for iii in range(100):
#     for jjj in range(100):
#         if ch[iii][jjj] in ['#', '*']:
#             plot_my(iii, jjj,".b")
#         elif ch[iii][jjj] in ['B']:
#             plot_my(iii,jjj,"ko")
#         za.append([iii, jjj])

subplot.set_aspect('equal', adjustable='box')  #保持子图在主图放大缩小是，能够保持子图的纵横比，保证图形不变形
plt.show()
