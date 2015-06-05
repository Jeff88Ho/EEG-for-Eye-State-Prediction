__author__ = 'Jeff'

import numpy as np
import sklearn.cross_validation as cv
from sklearn.ensemble import RandomForestClassifier


x = np.loadtxt("x.txt")
y = np.loadtxt("eeg_label.txt")
y = y[60:]

print x.shape
print y.shape



accuracy_list = []
for i in range(10):

    round = i+1

    print "############### round %s ###################" % round

    x_train, x_test, y_train, y_test = cv.train_test_split(x, y, test_size=0.2, random_state=i*7)

    clf = RandomForestClassifier(n_estimators=1000, max_depth=None, min_samples_split=1, random_state=None).fit(x_train, y_train)

    scores = clf.score(x_test, y_test)

    print ""
    print "accuracy: " + str(scores)
    accuracy_list.append(scores)
    print ""

print "accuracy_list: " + str(accuracy_list)
print "mean is " + str(np.mean(accuracy_list))
print "std is " + str(np.std(accuracy_list))

quantiles = (accuracy_list[2], (accuracy_list[4]+accuracy_list[5])/2, accuracy_list[7])
print "25%, 50%, 75%, quantiles are " + str(quantiles)



