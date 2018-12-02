import re
reviews_train = []
f=open('yelp_academic_dataset_review.json', 'r')
for line in f:
    reviews_train.append(line.strip())

f.close()
REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
REPLACE_WITH_SPACE1 = re.compile('\"review_id\"\:\"[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*\"\,')
REPLACE_WITH_SPACE2 = re.compile('\"user_id\"\:\"[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*\"\,')
REPLACE_WITH_SPACE3 = re.compile('\"business_id\"\:\"[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*[_]*[-]*[a-zA-Z0-9]*\"\,')
REPLACE_WITH_SPACE4 = re.compile('\"date\"\:\"[0-9]*[-][0-9]*[-][0-9]*\"\,')
REPLACE_WITH_SPACE5 = re.compile('\"useful\"\:[0-9]*\,')
REPLACE_WITH_SPACE6 = re.compile('\"funny\"\:[0-9]*\,')
REPLACE_WITH_SPACE7 = re.compile('\"cool\"\:[0-9]*')
REPLACE_WITH_SPACE8 = re.compile('\"text\"\:')


def preprocess_reviews(reviews):
    for i in range(0,len(reviews)):
        R=REPLACE_WITH_SPACE.findall(reviews[i])
        R1=REPLACE_WITH_SPACE1.findall(reviews[i])
        R2=REPLACE_WITH_SPACE2.findall(reviews[i])
        R3=REPLACE_WITH_SPACE3.findall(reviews[i])
        R4=REPLACE_WITH_SPACE4.findall(reviews[i])
        R5=REPLACE_WITH_SPACE5.findall(reviews[i])
        R6=REPLACE_WITH_SPACE6.findall(reviews[i])
        R7=REPLACE_WITH_SPACE7.findall(reviews[i])
        R8=REPLACE_WITH_SPACE8.findall(reviews[i])
        str1 = ''.join(R1)
        str2 = ''.join(R2)
        str3 = ''.join(R3)
        str4 = ''.join(R4)
        str5 = ''.join(R5)
        str6 = ''.join(R6)
        str7 = ''.join(R7)
        str8 = ''.join(R8)
        reviews[i]=reviews[i].replace(str1,"")
        reviews[i]=reviews[i].replace(str2,"")
        reviews[i]=reviews[i].replace(str3,"")
        reviews[i]=reviews[i].replace(str4,"")
        reviews[i]=reviews[i].replace(str5,"")
        reviews[i]=reviews[i].replace(str6,"")
        reviews[i]=reviews[i].replace(str7,"")
        reviews[i]=reviews[i].replace(str8,"")
    return reviews
f_output= open("Main_Clean_Sample.txt","w+")

reviews_train_clean = preprocess_reviews(reviews_train)
for i in range(0,len(reviews_train)):
    f_output.write(reviews_train[i])
    f_output.write("\n")
f_output.close()

