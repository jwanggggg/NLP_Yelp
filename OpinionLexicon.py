"""
Author: Stephen W. Thomas
Perform sentiment analysis using the MPQA lexicon.
Note, in this simple approach, we don't do anything to handle negations
or any of the other hard problems.
"""
import re
import operator

# Intialize an empty list to hold all of our tweets
reviews = []
reviews_R = []


# A helper function that removes all the non ASCII characters
# from the given string. Retuns a string with only ASCII characters.
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)



# LOAD AND CLEAN DATA
# Load in the input file and process each row at a time.
# We assume that the file has three columns:
# 0. The tweet text.
# 1. The tweet ID.
# 2. The tweet publish date
# Create a data structure for each tweet:
# id:       The ID of the tweet
# pubdate:  The publication date of the tweet
# orig:     The original, unpreprocessed string of characters
# clean:    The preprocessed string of characters
f=open('Main_Clean_Sample.txt', 'r')


for line in f:
    reviews_R.append(line.strip())
f.close()
for i in range(0, len(reviews_R)):
    review=dict()
    review['orig']=re.search(r'\"stars\"\:[0-9]\,\"(.*?)\"\,', reviews_R[i]).group(1)
    review['id']=re.search(r'\_id\"\:\"(.*?)\"\,\"', reviews_R[i]).group(1)
    review['rating']=re.search(r'stars\"\:(.*?)\,\"', reviews_R[i]).group(1)
    # Remove all non-ascii characters
    review['clean'] = review['orig']
    review['clean'] = strip_non_ascii(review['clean'])
    # Normalize case
    review['clean'] =review['clean'].lower()
    # Remove the hashtag symbol
    review['clean'] = review['clean'].replace(r'#', '')
    reviews.append(review)



# Create a data structure to hold the lexicon.
# We will use a Python diction. The key of the dictionary will be the word
# and the value will be the word's score.
lexicon = dict()
# Read in the lexicon. 
f1=open('opinion_lexicon/negative-words.txt', 'r')
for line in f1:
    lexicon[line.strip()]=-1
f1.close()
f2=open('opinion_lexicon/positive-words.txt', 'r')
for line in f2:
    lexicon[line.strip()]=1
f2.close()
#f3=open('opinion_lexicon/subtext.txt', 'r')
#for line in f3:
#    sentiment=line[-9:]
    
#    word=re.search(r'word1\=(.*?) pos1', line).group(1)
#    if(word in lexicon.keys()):
#        continue
#    else:    
#      if(sentiment=="negative"):
#        lexicon[word]=-1
#      else:
#        lexicon[word]=1
#f3.close()


# Use lexicon to score tweets
for review in reviews:
    score = 0
    for word in review['clean'].split():
        if word in lexicon:
            score = score + lexicon[word]

    review['score'] = score
    if (score > 0):
        review['sentiment'] = 'positive'
    elif (score < 0):
        review['sentiment'] = 'negative'
    else:
        review['sentiment'] = 'neutral'




# Print out summary stats
total = float(len(reviews))
num_pos = sum([1 for t in reviews if t['sentiment'] == 'positive'])
num_neg = sum([1 for t in reviews if t['sentiment'] == 'negative'])
num_neu = sum([1 for t in reviews if t['sentiment'] == 'neutral'])
print ("Positive: %5d (%.1f%%)" % (num_pos, 100.0 * (num_pos/total)))
print ("Negative: %5d (%.1f%%)" % (num_neg, 100.0 * (num_neg/total)))
print ("Neutral:  %5d (%.1f%%)" % (num_neu, 100.0 * (num_neu/total)))



# Print out some of the tweets
review_sorted = sorted(reviews, key=lambda k: k['score'])

print ("\n\nTOP NEGATIVE REVIEWS")
negative_reviews = [d for d in review_sorted if d['sentiment'] == 'negative']
for review in negative_reviews[0:10]:
    print( "id=%s, score=%.2f, clean=%s" % (review['id'], review['score'], review['clean']))

print( "\n\nTOP POSITIVE REVIEWS")
positive_reviews = [d for d in review_sorted if d['sentiment'] == 'positive']
for review in positive_reviews[-10:]:
    print ("id=%s, score=%.2f, clean=%s" % (review['id'], review['score'], review['clean']))

print ("\n\nTOP NEUTRAL Reviews")
neutral_reviews = [d for d in review_sorted if d['sentiment'] == 'neutral']
for review in neutral_reviews[0:10]:
    print ("id=%s, score=%.2f, clean=%s" % (review['id'], review['score'], review['clean']))
