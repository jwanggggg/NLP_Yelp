import re
from textblob import TextBlob
reviews = []
reviews_R = []
f=open('Development10000.txt', 'r')
for line in f:
    if(line!="\n"):
      reviews_R.append(line.strip())
f.close()

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
    
    if ( float(review['score']) > 0.15):
        review['sentiment'] = 'positive'
    elif (float(review['score']) < 0.15):
        review['sentiment'] = 'negative'
    else:
        review['sentiment'] = 'neutral'
    
review_sorted = sorted(reviews, key=lambda k: k['score'])
total = float(len(reviews))
num_pos = sum([1 for t in reviews if t['sentiment'] == 'positive'])
num_neg = sum([1 for t in reviews if t['sentiment'] == 'negative'])
num_neu = sum([1 for t in reviews if t['sentiment'] == 'neutral'])
print ("Positive: %5d (%.1f%%)" % (num_pos, 100.0 * (num_pos/total)))
print ("Negative: %5d (%.1f%%)" % (num_neg, 100.0 * (num_neg/total)))
print ("Neutral:  %5d (%.1f%%)" % (num_neu, 100.0 * (num_neu/total)))






print ("\n\nTOP NEGATIVE REVIEWS")
negative_reviews = [d for d in review_sorted if d['sentiment'] == 'negative']
for review in negative_reviews[0:10]:
    print( "id=%s, score=%.2f, clean=%s" % (review['id'], float(review['score']), review['clean']))

print( "\n\nTOP POSITIVE REVIEWS")
positive_reviews = [d for d in review_sorted if d['sentiment'] == 'positive']
for review in positive_reviews[-10:]:
    print ("id=%s, score=%.2f, clean=%s" % (review['id'], float(review['score']), review['clean']))

print ("\n\nTOP NEUTRAL Reviews")
neutral_reviews = [d for d in review_sorted if d['sentiment'] == 'neutral']
for review in neutral_reviews[0:10]:
    print ("id=%s, score=%.2f, clean=%s" % (review['id'], float(review['score']), review['clean']))
