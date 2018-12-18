import re
from textblob import TextBlob
reviews = []
reviews_R = []
f=open('Development10000.txt', 'r')
for line in f:
    if(line!="\n"):
      reviews_R.append(line.strip())
f.close()
rating_count=0
for i in range(0, len(reviews_R)):
    review=dict()
    review['orig']=re.search(r'\"stars\"\:[0-9]\,\"(.*?)\"\,', reviews_R[i]).group(1)
    review['id']=i
    #re.search(r'\_id\"\:\"(.*?)\"\,\"', reviews_R[i]).group(1)
    review['rating']=re.search(r'stars\"\:(.*?)\,\"', reviews_R[i]).group(1)
    review['clean'] = review['orig']
    # Normalize case
    review['clean'] =review['clean'].lower()
    # Remove the hashtag symbol
    review['clean'] = review['clean'].replace(r'#', '')
    reviews.append(review)

for review in reviews:
    sentence=TextBlob(review["clean"])
    review['score']=sentence.sentiment
    review['score']=re.search(r'polarity\=(.*?)\,', str(review['score'])).group(1)
    
    if ( float(review['score']) > 0.08):
        review['sentiment'] = 'positive'
        if(int(review['rating'])>=3):
           rating_count+=1
    elif (float(review['score']) < 0.08):
        review['sentiment'] = 'negative'
        if(int(review['rating'])<3):
           rating_count+=1
    else:
        review['sentiment'] = 'neutral'
        if(int(review['rating'])>=3):
           rating_count+=1
    
#review_sorted = sorted(reviews, key=lambda k: k['score'])
total = float(len(reviews))
num_pos = sum([1 for t in reviews if t['sentiment'] == 'positive'])
num_neg = sum([1 for t in reviews if t['sentiment'] == 'negative'])
num_neu = sum([1 for t in reviews if t['sentiment'] == 'neutral'])
print ("Positive: %5d (%.1f%%)" % (num_pos, 100.0 * ((num_pos+num_neu)/total)))
print ("Negative: %5d (%.1f%%)" % (num_neg, 100.0 * (num_neg/total)))


f1=open('Development10000.txt', 'r')
pos=[]
neg=[]
Rreviews=[]
for line in f1:
    if(line!="\n"):
      Rreviews.append(line.strip())
f.close()
positive=0
negative=0
neutral=0
for i in range(0, len(Rreviews)):
    rating=re.search(r'stars\"\:(.*?)\,\"', Rreviews[i]).group(1)
    if(int(rating)>3):
        positive+=1
        review1=re.search(r'\"stars\"\:[0-9]\,\"(.*?)\"\,', Rreviews[i]).group(1)
        pos.append(review1)
    elif(int(rating)==0):
        neutral+=1
    else:
        negative+=1
        review1=re.search(r'\"stars\"\:[0-9]\,\"(.*?)\"\,', Rreviews[i]).group(1)
        neg.append(review1)

f.close()
           
print("True pos:",positive+neutral)
print("True neg:",negative)

print("Accuracy is ",rating_count/total)
