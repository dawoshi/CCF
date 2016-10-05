# encoding: utf8
import csv
import datetime
import time
import numpy as np

class User(object):

    def __init__(self):
        self.amount = {}
        self.id = None
        self.flag = None
        self.effect = False
        # 用户的特征
        self.mean = None
        self.var = None

    def set_id(self, id):
        self.id = id

    def set_consume(self, date, amount):
        self.amount[date] = amount

    def set_flag(self, flag):
        self.flag = flag

    def set_effective(self):
        """
        因为训练集里有很多数据无法在train中找到，所以设置一个标志位
        :param effect:
        :return:
        """
        self.effect = True


start_time = time.clock()

table = {}  # 这个table是用来映射对象和信息关系的

# 读取用户信息
user_tag_file = csv.reader(open('train.csv'))
user_tag = list(user_tag_file)
# user_tag.pop(0)

# 读取用户用电量
user_meter_file = csv.reader(open('meter.csv'))  # 一共6314495条记录
user_meter = list(user_meter_file)
user_meter.pop(0)
user_meter.sort(key= lambda user_id: (user_id[0], user_id[1]))
print 'meter数据共有{0}条记录'.format(len(user_meter))

users = []  # 所有用户的数组
currrent_user = User()
currrent_user.set_id(int(user_meter[0][0])) # 第一个人
for i in range(len(user_meter)):
    if user_meter[i][4] == '':
        continue
    elif (user_meter[i][2] == '' or user_meter[i][3] == ''):
        continue
    elif user_meter[i][4] != '':
        consumer = float(user_meter[i][4])
    else:
        consumer = abs(float(user_meter[i][3])-float(user_meter[i][2]))

    if int(user_meter[i][0]) == currrent_user.id:
        year, date, day = str(user_meter[i][1]).split('/')
        currrent_user.set_consume(datetime.datetime(int(year), int(date), int(day)), consumer)
    else:
        # sorted(currrent_user.amount)
        users.append(currrent_user)
        table[currrent_user.id] = len(users)-1  # 将用户的id与用户存的位置对应起来
        currrent_user = User()
        currrent_user.set_id(int(user_meter[i][0]))
        year, date, day = str(user_meter[i][1]).split('/')
        currrent_user.set_consume(datetime.datetime(int(year), int(date), int(day)), consumer)

users.append(currrent_user)
table[currrent_user.id] = len(users)-1
print '完成了用户用电数据的录入'

# 录入用户是否偷电
print 'meter数据集中共记录了{0}个用户'.format(len(users))
sum = 0
for i in range(len(user_tag)):
    user = int(user_tag[i][0])
    if user in table.keys():
        index = table[user]
        users[index].set_flag(int(user_tag[i][1]))
        users[index].set_effective()
        sum += 1

print 'train数据集中对应了{0}个用户'.format(sum)

end_time = time.clock()
print '整个程序共执行了%f s' % (end_time - start_time)



###############################################################################################################################
#  下面是对数据的一些处理信息
###########################################################################################################################

"""
计算normal用户和abnormal用户每个月的平均值和方差
"""
def count_noraml_abnormal():
    normal = [[], [], [], [], [], [], [], [], [], [], [], []]
    abnormal = [[], [], [], [], [], [], [], [], [], [], [], []]
    for user in users:
        if user.effect == False:
            continue
        keys = user.amount.keys()
        if user.flag == 1:  #  异常的用户
            for key in keys:
                yongdianliang = user.amount[key]  # 每个时间点的用电量
                abnormal[int(key.month)-1].append(yongdianliang)
        else:  # 正常的用户
            for key in keys:
                yongdianliang = user.amount[key]  # 每个时间点的用电量
                normal[int(key.month)-1].append(yongdianliang)

    normal = np.array(normal)
    abnormal = np.array(abnormal)

    normal_mean = []
    abnormal_mean =[]
    normal_var = []
    abnormal_var = []
    for i in range(12):
        if normal[i] == []:
            normal_mean.append(0)
            abnormal_mean.append(0)
            normal_var.append(0)
            abnormal_var.append(0)
        else:
            normal_mean.append(np.mean(normal[i]))
            abnormal_mean.append(np.mean(abnormal[i]))
            normal_var.append(np.var(normal[i]))
            abnormal_var.append(np.var(abnormal[i]))
    return normal_mean, abnormal_mean, normal_var, abnormal_var


"""
计算每个用户用电的均值方差
"""
def count_every_user():
    max_mean = 0
    max_var = 0
    for user in users:
        if user.effect == True:
            data = user.amount.values()  # 每个用户的所有用电量的数据
            user.mean = np.mean(np.array(data))
            user.var = np.var(np.array(data))
            if max_mean < user.mean:
                max_mean = user.mean
            if max_var < user.var:
                max_var = user.var

    print "max mean = {0} ,var = {1}".format(max_mean, max_var)



"""
计算每个用户每个月的平均值，作为一个向量
"""
def count_user_month_useage():
    samples = []
    tags = []
    for user in users:
        if user.effect == False:
            continue
        data = [[] for i in range(12)]
        keys = user.amount.keys()
        for key in keys:
            data[int(key.month)-1].append(user.amount[key])

        length = len(data)
        for i in range(length):
            if data[i] == []:
                data[i] = np.nan  # 如果是空的就填写为NAN
            else:
                data[i] = np.mean(np.array(data[i]))

        samples.append(data)
        tags.append(user.flag)

    samples = np.array(samples)
    tags = np.array(tags)
    return samples, tags


"""
将每个用户的NAN信息都取为该用户用电的平均值
"""
def filter0():
    samples, tags = count_user_month_useage()
    for i in range(len(samples[:,1])):
        # print samples[i]
        # for j in range(len(samples[i])):
        #     print type(samples[i][j])
        # print np.isnan(np.array(samples[i]))
        samples[i][np.isnan(samples[i])] = np.mean(samples[i][np.isnan(samples[i])==False])  # 未知的地方全部去平均值

    return samples, tags


"""
将每个用户的NAN信息都取为所有与该用户flag对应的平均值
那么测试时 如果测试用户也缺失这部分信息 那么就要通过聚类给它补全
"""
def filter1():
    pass


"""
将每个用户的信息按月进行折叠
"""
def filter2():
  pass































