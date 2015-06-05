__author__ = 'Jeff'


from numpy import loadtxt




time_frame = 10



F = loadtxt("eeg_features_14.txt", delimiter=',')
print F
print F.shape[0], F.shape[1]

L = loadtxt("eeg_label.txt", delimiter=', ')
print L
print L.shape[0]


###
for i in range( 10, 20 ): #6 models

    model = i+1

    n = i+1-10

    write_path = "x_"+ str(model) + ".txt"

    text_file = open(write_path, "w")


    #rows
    for row in range(int(F.shape[0])): #5000 rows
        text_file.write( str(int(L[row])) ) #ith label

        #append all features from all row ranges
        features = []
        for line in range( ((n-1)*time_frame+1),(n*time_frame+1) ):
            if row+line in range(int(F.shape[0])): ###
                features.extend( F[row+line, ] )

        count = 1
        for feature in features: #all append features
            text_file.write(" "+str(count)+":"+str(feature))  #write keys and all features
            count+=1

        text_file.write(str("\n"))


    text_file.close()