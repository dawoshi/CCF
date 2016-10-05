# encoding: utf8
# 这里使用SVM对数据进行分类
import numpy as np
from sklearn import svm
# from preprocessing import count_user_month_useage, filter0
import time

TRAIN_SAMPLE = 'samples_means.npy'
TRAIN_TAG = 'tags_means.npy'
TEST_SAMPLE = 'test_samples_mean.npy'
TEST_USER = 'test_user.npy'

train_samples = np.load(TRAIN_SAMPLE)
train_tags = np.load(TRAIN_TAG)
test_samples = np.load(TEST_SAMPLE)
test_users = np.load(TEST_USER)
missing_user = np.load('missing_user.npy')

print train_samples.shape, train_tags.shape, test_samples.shape, test_users.shape

"""
下面进行svm的计算
"""
from sklearn import svm

"""
for test
"""
# train_samples = train_samples[:1000, ]
# train_tags = train_tags[:1000]
# test_samples = test_samples[:1000]
# test_users = test_users[:1000]
# print test_users

start_time = time.clock()
print train_samples.shape, train_tags.shape

clf_linear = svm.SVC(kernel='linear', probability=True).fit(train_samples, train_tags)
print clf_linear.classes_
print clf_linear
answer = clf_linear.predict_proba(test_samples)  # 计算每个的概率

end_time = time.clock()
print 'SVM共执行了%f s' % (end_time - start_time)

# [0, 1]
print test_users
print "**************************************************************"
for i in range(len(answer)):
    for j in range(i+1, len(answer)):
        if answer[i][1] < answer[j][1]:
            tmp = answer[i]
            answer[i] = answer[j]
            answer[j]= tmp
            tmp = test_users[i][0]
            test_users[i][0] = test_users[j][0]
            test_users[j][0] = tmp

import csv
csvfile = file('test_answer.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerows(test_users)
writer.writerows(missing_user)
csvfile.close()