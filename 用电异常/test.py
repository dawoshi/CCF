# encoding: utf8
import csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates
from datetime import datetime
from preprocessing import users, table, count_every_user

"""
读取测试集合
"""
# 读取测试集合用户信息
user_tag_file = csv.reader(open('test.csv'))
user_tag = list(user_tag_file)

"""
下面的代码是通用的
"""
sum = 0
missing_user = []
test_samples = []
test_user = []
for user_id in user_tag:
    try:
        index = table[int(user_id[0])]
        test_user.append(user_id)
    except:
        missing_user.append(user_id)  # 找不到这个用户的数据
        continue

    user = users[index]
    data = [[] for i in range(12)]
    keys = user.amount.keys()
    for key in keys:
        data[int(key.month) - 1].append(user.amount[key])

    length = len(data)
    for i in range(length):
        if data[i] == []:
            data[i] = np.nan  # 如果是空的就填写为NAN
        else:
            data[i] = np.mean(np.array(data[i]))

    test_samples.append(data)

test_samples = np.array(test_samples)   # 得到测试数据的用电量

"""
做法：
对nan数据做平均
"""
# for i in range(len(test_samples[:,1])):
#     test_samples[i][np.isnan(test_samples[i])] = np.mean(test_samples[i][np.isnan(test_samples[i]) == False])
#
# np.save('test_samples_mean.npy', test_samples)
# np.save('test_user.npy', test_user)

np.save('missing_user.npy', missing_user)


# csvfile = file('test_answer.csv', 'wb')
# writer = csv.writer(csvfile)
# writer.writerows(user_tag)
# csvfile.close()
