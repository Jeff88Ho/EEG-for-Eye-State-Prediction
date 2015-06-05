__author__ = 'Jeff'


from numpy import loadtxt


block = 10

time_frame = 30



F = loadtxt("eeg_features_14.txt", delimiter=',')
print F
print F.shape[0], F.shape[1]

L = loadtxt("eeg_label.txt", delimiter=', ')
print L
print L.shape[0]


i = 4 # start with model 5

model = i+1
n = i+1
write_path = "x_21.txt"

text_file = open(write_path, "w")


#rows
for row in range(int(F.shape[0])): #5000 rows
    text_file.write( str(int(L[row])) ) #ith label #label

    #append all features from all row ranges
    features = []
    for line in range( ((n-1)*block+1),(n*block+1) ): #
        if row-line in range(int(F.shape[0])):
            features.extend( F[row-line, ] )

    for line in range( ((n)*block+1),((n+1)*block+1) ): #
        if row-line in range(int(F.shape[0])):
            features.extend( F[row-line, ] )


    count = 1
    for feature in features: #all append features
        text_file.write(" "+str(count)+":"+str(feature))  #write keys and all features
        count+=1

    text_file.write(str("\n"))


text_file.close()