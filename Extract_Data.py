reviews_train = []
f=open('yelp_academic_dataset_review.json', 'r')
reviews_train=f.readlines()[0:10000]
f.close()

f_output= open("Long_Main_Clean_Sample.txt","w+")
for i in range(0,len(reviews_train)):
    f_output.write(reviews_train[i])
    f_output.write("\n")
f_output.close()
