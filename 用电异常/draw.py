# encoding: utf8
from preprocessing import users
from matplotlib import pyplot as plt
from matplotlib import font_manager
from preprocessing import count_noraml_abnormal, count_every_user
"""
折线图
"""
# plt.figure(figsize=(800, 500), dpi=80)
# axes = plt.subplot(111)
# for user in users:
#     y = []
#     if user.effect == False:  # 该用户不在训练集中
#         continue
#     keys = user.amount.keys()
#     sorted(keys)
#     print keys
#     for key in keys:
#         y.append(user.amount[key])
#     plt.plot(keys, y)
# plt.show()

"""
点状图
"""
#
# plt.figure(figsize=(800, 500), dpi=80)
# axes = plt.subplot(111)
#
# normal_x = []
# normal_y = []
# abnormal_x = []
# abnormal_y = []
# print len(users)
#
# for user in users:
#     if user.effect == False:  # 该用户不在训练集中
#         continue
#     keys = user.amount.keys()
#     if user.flag == 0:
#         for key in keys:
#             normal_x.append(key)
#             normal_y.append(user.amount[key])
#     else:
#         for key in keys:
#             abnormal_x.append(key)
#             abnormal_y.append(user.amount[key])
#
# abnormal = axes.scatter(abnormal_x, abnormal_y, s=40, c='yellow', norm=0.1)
# normal = axes.scatter(normal_x, normal_y, s=20, c='blue', norm=0.2)
#
#
# plt.xlabel(u'时间')
# plt.ylabel(u'用电差量')
# # axes.legend((normal, abnormal_y), ('normal', 'abnormal'), loc=2)
#
# plt.show()

# month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# mean0, mean1, var0, var1 = count_noraml_abnormal()
# plt.figure(figsize=(80, 50), dpi=80)
# axes = plt.subplot(111)
#
# plt.plot(month, var0, color='blue')
# plt.plot(month, var1, color='green')
#
# plt.show()

"""
柱状图，每个用户的均值和方差
"""
count_every_user()
mean0 = []  # 以5为一个断点
var0 = []  # 以500为一个断点
mean1 = []
var1 = []



for user in users:
    if user.effect == False:
        continue
    if user.flag == 0:
        index = int(user.mean / 5)
        if len(mean0) <= index:
            length = len(mean0)
            for _ in range(int(index-length)+1):
                mean0.append(0)
        mean0[index] += 1

        index = int(user.var / 500)
        if len(var0) <= index:
            length = len(var0)
            for _ in range(int(index-length)+1):
                var0.append(0)
        var0[index] += 1
    else:
        index = int(user.mean / 5)
        if len(mean1) <= index:
            length = len(mean1)
            for _ in range(int(index - length) + 1):
                mean1.append(0)
        mean1[index] += 1

        index = int(user.var / 500)
        if len(var1) <= index:
            length = len(var1)
            for _ in range(int(index - length) + 1):
                var1.append(0)
        var1[index] += 1

print mean0
print mean1
print var0
print var1