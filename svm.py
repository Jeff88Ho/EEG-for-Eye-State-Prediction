__author__ = 'Jeff'


import datetime
import subprocess
import re
from collections import Counter, OrderedDict
import numpy as np
import random
import sys




class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/Users/Jeff/Desktop/svm_result.txt", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

sys.stdout = Logger()



def get_key(key):
    try:
        return int(key)
    except ValueError:
        return key


def summary(tag_dir):

    lines = np.loadtxt(tag_dir)

    s = Counter(lines)

    sorted_s = OrderedDict(sorted(s.items(), key=lambda t: get_key(t[0])))

    return sorted_s


# def distance_evaluation( x_dir, y_dir ):
#
#     read_x = open(x_dir, "r").read().splitlines()
#     read_y = open(y_dir, "r").read().splitlines()
#
#     x = np.array(read_x, np.float)
#     y = np.array(read_y, np.float)
#
#     return np.sqrt(sum((x-y)**2))






# model_distance_values = []

model_accuracy_values = []

model_means = []
model_stds = []
model_quantiles = []



#perform svm_hmm for different models (different feature combinations), processed by data_1 ~ data_12
for i in range(-1,20):
    model = i+1
    dir = "x_%s.txt" % model  #data path for different models (total 16)
    print dir


    accuracy_stats = []
    # distance_stats = []

    for i in range(10): #do it 10 times to get loss stats

        round = i+1

        total_instance = 14976

        block_size = total_instance/10

        test_index = random.sample(range(1, total_instance), 2*block_size)

        test_a_index = test_index[:block_size]
        test_b_index = test_index[block_size:]

        train_index = list(set(range(total_instance)) - set(test_a_index) - set(test_b_index))


        # #random permutation
        # shuffle_list = range(10)
        # shuffle(shuffle_list)




        #write file for training and training
        f = open(dir, "r")
        lines = f.readlines()

        test_a_dir = "x_%s_test_a.txt" % model
        w = open(test_a_dir, "w")

        for i in test_a_index:
            w.write(lines[i])

        w.close()
        f.close()



        f = open(dir, "r")
        lines = f.readlines()

        test_b_dir = "x_%s_test_b.txt" % model
        w = open(test_b_dir, "w")

        for i in test_b_index:
            w.write(lines[i])

        w.close()
        f.close()



        f = open(dir, "r")
        lines = f.readlines()

        train_dir = "x_%s_train.txt" % model
        w = open(train_dir, "w")

        for i in train_index:
            w.write(lines[i])

        w.close()
        f.close()


        #write true y file for tagging evaluation
        # f = open("y.txt", "r")
        # lines = f.readlines()
        #
        # test_a_dir = "y_a.txt"
        # w = open(test_a_dir, "w")
        #
        # for i in test_a_index:
        #     w.write(lines[i])
        #
        # w.close()
        # f.close()



        # f = open("y.txt", "r")
        # lines = f.readlines()
        #
        # test_b_dir = "y_b.txt"
        # w = open(test_b_dir, "w")
        #
        # for i in test_b_index:
        #     w.write(lines[i])
        #
        # w.close()
        # f.close()



        #now comes cmd
        def subprocess_cmd(command):
            process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
            proc_stdout = process.communicate()[0].strip()
            return proc_stdout



        #all c values to be validated
        c_list = [ pow(10, -6), pow(10, -5), pow(10, -4), pow(10, -3), pow(10, -2), pow(10, -1),
                   pow(10, 0),
                   pow(10, 1), pow(10, 2), pow(10, 3), pow(10, 4), pow(10, 5), pow(10, 6)]



        accuracy_a_list = []
        accuracy_b_list = []
        # distance_a_list = []
        # distance_b_list = []


        #for all c values do validate to get loss
        for c in c_list:

            model_dir = "model_%s_c_%s.txt" % (model, c)
            tag_a_dir = "tag_model_%s_c_%s_a.txt" % (model, c)
            tag_b_dir = "tag_model_%s_c_%s_b.txt" % (model, c)


            #learning cmd
            learn_cmd = "./svm-train -c %s -e 0.1 -t 0 %s %s" % (c, train_dir, model_dir)

            #classifying set a command
            classify_a_cmd = "./svm-predict %s %s %s" % (test_a_dir, model_dir, tag_a_dir)

            #classifying set b command
            classify_b_cmd = "./svm-predict %s %s %s" % (test_b_dir, model_dir, tag_b_dir)

            #learning
            print ""
            print "------------------------------------------model %s, round %s, c=%s, learning...-----------------------------------------------------" % (model, round, c)
            print datetime.datetime.now()
            learn_result = subprocess_cmd(learn_cmd)
            print ""

            #classyfying set a
            print ""
            print "------------------------------------------model %s, round %s, c=%s, classifying_a...------------------------------------------------" % (model, round, c)
            print datetime.datetime.now()
            print ""
            classify_a_result = subprocess_cmd(classify_a_cmd)
            print classify_a_result

            #classfying set b
            print ""
            print "------------------------------------------model %s, round %s, c=%s, classifying_b...------------------------------------------------" % (model, round, c)
            print datetime.datetime.now()
            print ""
            classify_b_result = subprocess_cmd(classify_b_cmd)
            print classify_b_result

            #retrieve loss values from classifying cmd result
            accuracy_a = re.findall( r"[-+]?\d*\.\d+|\d+", classify_a_result )[0]
            accuracy_b = re.findall( r"[-+]?\d*\.\d+|\d+", classify_b_result )[0]

            # distance_a = distance_evaluation(tag_a_dir, "y_a.txt") / distance_evaluation("y_bar.txt", "y_a.txt")
            # distance_b = distance_evaluation(tag_b_dir, "y_b.txt") / distance_evaluation("y_bar.txt", "y_b.txt")

            print ""
            print "****************************************"
            print ""
            print "accuracy a is ", accuracy_a
            print ""
            print summary(tag_a_dir)
            # print "distance a is ", distance_a
            print ""
            print "****************************************"
            print ""
            print "accuracy b is ", accuracy_b
            print ""
            print summary(tag_b_dir)
            # print "distance b is ", distance_b
            print ""
            print "****************************************"
            print ""

            accuracy_a = float(accuracy_a)
            accuracy_b = float(accuracy_b)

            #store all losses as lists
            accuracy_a_list.append(accuracy_a)
            accuracy_b_list.append(accuracy_b)

            # distance_a_list.append(distance_a)
            # distance_b_list.append(distance_b)


        print ""
        print "##########################################finish model %s, round %s####################################################" % (model, round)
        print datetime.datetime.now()
        print ""


        #find optimal loss values of set a and set b
        accuracy_b = accuracy_b_list[accuracy_a_list.index(max(accuracy_a_list))] #min value in loss_a_list -> optimal C value of set a -> train and classify set b -> loss_b
        accuracy_a = accuracy_a_list[accuracy_b_list.index(max(accuracy_b_list))] #min value in loss_b_list -> optimal C value of set a -> train and classify set b -> loss_a

        # distance_b = distance_b_list[distance_a_list.index(min(distance_a_list))] #min value in loss_a_list -> optimal C value of set a -> train and classify set b -> loss_b
        # distance_a = distance_a_list[distance_b_list.index(min(distance_b_list))] #min value in loss_b_list -> optimal C value of set a -> train and classify set b -> loss_a


        print "summary of model %s, round %s: " % (model, round)
        print "accuracy_a_list is " + str(accuracy_a_list)
        print "accuracy_b_list is " + str(accuracy_b_list)
        print ""
        print "accuracy a is ", accuracy_a
        print "accuracy b is ", accuracy_b
        print ""

        # print "distance_a_list is " + str(distance_a_list)
        # print "distance_b_list is " + str(distance_b_list)
        # print ""
        # print "distance a is ", distance_a
        # print "distance b is ", distance_b


        accuracy_a = float(accuracy_a)
        accuracy_b = float(accuracy_b)

        #weights for set a and set b
        a_num_lines = sum(1 for line in open(test_a_dir))
        b_num_lines = sum(1 for line in open(test_b_dir))



        #final loss of the round
        accuracy = (accuracy_a*a_num_lines + accuracy_b*b_num_lines) / (a_num_lines+b_num_lines)

        # distance = (distance_a*a_num_lines + distance_b*b_num_lines) / (a_num_lines+b_num_lines)

        print ""
        print "accuracy is ", accuracy
        # print "distance is ", distance

        #store all losses
        accuracy_stats.append(accuracy)
        # distance_stats.append(distance)


        print ""
        print "##########################################end of model %s, round %s####################################################" % (model, round)
        print datetime.datetime.now()
        print ""



    #summary and stats for each model
    print ""
    print "##########################################finish model %s####################################################" % model
    print datetime.datetime.now()
    print ""
    print "summary of model %s:" % model

    print "accuracy values: " + str(accuracy_stats)

    accuracy_stats.sort()
    print "sorted accuracy values: " + str(accuracy_stats)

    # print "distance values: " + str(distance_stats)

    # distance_stats.sort()
    # print "sorted distance values: " + str(distance_stats)

    # accuracy_stats = 1 - np.array(loss_stats)
    # print "accuracy values: " + str(accuracy_stats)
    # accuracy_stats.sort()
    # print "sorted accuracy values: " + str(accuracy_stats)

    print "mean is " + str(np.mean(accuracy_stats))
    print "std is " + str(np.std(accuracy_stats))

    quantiles = (accuracy_stats[2], (accuracy_stats[4]+accuracy_stats[5])/2, accuracy_stats[7])
    print "25%, 50%, 75%, quantiles are " + str(quantiles)


    #store for all summary
    model_accuracy_values.append(accuracy_stats)
    # model_distance_values.append(distance_stats)

    model_accuracy_values.append(accuracy_stats)
    model_means.append(np.mean(accuracy_stats))
    model_stds.append(np.std(accuracy_stats))
    model_quantiles.append(quantiles)

    print ""
    print "##########################################end of model %s####################################################" % model
    print datetime.datetime.now()
    print ""


#summary and stats for the report
print ""
print datetime.datetime.now()
print "all summary:"

# print "all distance values for all models: " + str(model_distance_values)

print "all accuracy values for all models: " + str(model_accuracy_values)
print "means for all models are " + str(model_means)
print "stds for all models are " + str(model_stds)

print "25%, 50%, 75%, quantiles for all models are " + str(model_quantiles)


#END
