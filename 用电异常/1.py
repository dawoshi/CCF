from matplotlib import pyplot as plt
from matplotlib import font_manager
import datetime
import numpy as np

import csv
file = csv.reader(open('test_answer.csv'))
file = list(file)
file.reverse()

k = open('testla.csv', 'wb')
writer = csv.writer(k)
writer.writerows(file)
k.close()
