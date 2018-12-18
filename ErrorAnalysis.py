#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 14:35:49 2018

@author: jonathanwang
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 13:52:42 2018

@author: jonathanwang
"""

import re
import math
import re
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

allReviews = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/Clean_sample.txt"
trainFile = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/YelpTraining.txt"
testFile = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/YelpTraining.txt"
vocabFile = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/YelpVocab.txt"
stopwordFile = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/stopwords.txt"

naiveBayesRatings = []
vaderRatings = []
textBlobRatings = []

# Error analysis will perform Naive Bayes until an OOV word is encountered,
# at which point the average of VADER and TextBlob will be taken to 
# determine the sentiment.

def main():
    ErrorAnalysis()
    
# -------- Error Analysis ----------

def ErrorAnalysis():
    reviews=[]
    f=open(allReviews, 'r', encoding = "utf-8")
    for line in f:
        if(line != "\n"):
            reviews.append(re.sub(r'[^\w\s]','',line.strip())[6:])
    f.close()
    
    dictionary = dict()
    
    for i in range(0, len(reviews)):
        words = reviews[i].split(" ")
        for word in words:
            text = nltk.pos_tag(nltk.word_tokenize(word))
            if (len(text) != 0):
                term = text[0][0].lower()
                pos = text[0][1]
                dictionary[term] = pos
    
    print(dictionary)
    
    return NBClassify(trainFile, testFile, vocabFile, stopwordFile, naiveBayesRatings)
    

# -------- Naive Bayes' ----------

def NBClassify(trainFile, testFile, vocabFile, stopwordFile, naiveBayesRatings):
    stopWords = set(())
    distinctWords = 0
    
    stopWordsStr = set(())
    
    with open(stopwordFile, "r", encoding = "utf-8") as f:
        for line in f:
            stopWordsStr.add(line.rstrip('\n'))

    # Check number of distinct words
    
    with open(vocabFile, "r", encoding = "utf-8") as f:
        for line in f:
            line = line.rstrip('\n')
            if line in stopWordsStr:
                stopWords.add(distinctWords)
            distinctWords+=1;
        
    posWords = [0] * distinctWords
    negWords = [0] * distinctWords

    posReviews = 0
    negReviews = 0
    wordsInPosReviews = 0
    wordsInNegReviews = 0
    
    with open(trainFile, "r", encoding = "utf-8") as f:
        for line in f:
            line = line.rstrip('\n')
    
            lineArray = re.split(" |:", line)
            lineArray.pop()
            
            if len(lineArray) == 0: continue
            stars = int(lineArray[0])
            
            if stars >= 3:
                posReviews += 1
                for num in range(1, len(lineArray) - 1, 2):
                    word = int(lineArray[num])
                    frequency = int(lineArray[num + 1])
                    if (word in stopWords): continue
                    # OOV word detected, switch to the average polarity score
                    if word >= len(posWords):
                        vader = VaderClassify(vaderRatings)
                        textBlob = TextBlobClassify(textBlobRatings)
                        frequency = (vader + textBlob) / 2
                    posWords[word]+=frequency
                    wordsInPosReviews+=frequency
            
            else:
                negReviews += 1
                for num in range(1, len(lineArray) - 1, 2):
                    word = int(lineArray[num])
                    frequency = int(lineArray[num + 1])
                    if (word in stopWords): continue
                    negWords[word]+=frequency
                    wordsInNegReviews+=frequency
    
    correctClassification = 0
    incorrectClassification = 0
    actualRatings = []
    
    with open(testFile, "r", encoding = "utf-8") as f:
        for line in f:
            line = line.rstrip('\n')
            lineArray = re.split(" |:", line)
            lineArray.pop()
            stars = int(lineArray[0])
            # Compare to the actual rating
            actual = 1 if stars >= 3 else 0
            
            probOfPos = math.log(posReviews / (posReviews + negReviews))
            probOfNeg = math.log(negReviews / (posReviews + negReviews))
            
            for num in range(1, len(lineArray)-1,2):
                word = int(lineArray[num])
                frequency = int(lineArray[num + 1])
                
                if(word in stopWords): continue
                probOfPos += frequency * math.log((posWords[word] + 1) / (wordsInPosReviews + distinctWords))
                probOfNeg += frequency * math.log((negWords[word] + 1) / (wordsInNegReviews + distinctWords))
                       
            predicted = 1 if probOfPos > probOfNeg else 0
            result = "Positive" if predicted == 1 else "Negative"
            naiveBayesRatings.append(predicted)
            actualRatings.append(actual)
            
#            print("Prob of pos: " + str(probOfPos))
#            print("Prob of neg: " + str(probOfNeg))
#            print("Sentiment: " + result +"\n")
            
            if predicted == actual:
                correctClassification += 1
            else:
                incorrectClassification += 1
            
                
    accuracy = correctClassification/(correctClassification + incorrectClassification)    
    print("Accuracy of Error Analysis:", accuracy)
    return actualRatings

# -------- VADER ----------
    
def VaderClassify(vaderRatings):
    analyzeSentences(vaderRatings)
    
def printResult(scores, actualStars, vaderRatings):
    # Accuracy = correct/total
    correctClassification = 0
    incorrectClassification = 0

    for score in range(0, len(scores)-1):
        
        predicted = scores[score]
        actual = actualStars[score]
        
        if (predicted >= 0.05 and (actual == 4 or actual == 5)) or (predicted <= -0.05 and (actual == 1 or actual == 2) or (predicted < 0.05 and predicted > -0.05 and actual == 3)):
            correctClassification += 1
        else:
            incorrectClassification += 1
        
        # Add to the vaderRatings
        if (predicted > -0.05):
            vaderRatings.append(1)
        else:
            vaderRatings.append(0)
            
    accuracy = correctClassification/(correctClassification + incorrectClassification)
    print("Accuracy of VADER:", accuracy)
    
def parseSentences():
    sentences = []
    actualStars = []
    with open(allReviews, "r", encoding = "utf-8") as f:
        for line in f:
            stars = line[9]
            line = line[11:len(line)-3]
            sentences.append(line)
            if stars != "\"":
                actualStars.append(int(stars))
            else:
                actualStars.append(3)
        
    f.close()

    return sentences, actualStars

def analyzeSentences(vaderRatings):
    
    sid = SentimentIntensityAnalyzer()
    
    sentences, actualStars = parseSentences()
    scores = []
        
    for sentence in sentences:
#        print(sentence + "\n")
        ss = sid.polarity_scores(sentence)
        scores.append(ss["compound"])
      
    printResult(scores, actualStars, vaderRatings)


# -------- TextBlob ----------

def TextBlobClassify(textBlobRatings):
    reviews = []
    reviews_R = []
    f=open(allReviews, 'r', encoding = "utf-8")
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
        
        if ( float(review['score']) > 0.07):
            review['sentiment'] = 'positive'
            textBlobRatings.append(1)
            if(int(review['rating'])>=3):
               rating_count+=1
        elif (float(review['score']) < 0.07):
            review['sentiment'] = 'negative'
            textBlobRatings.append(0)
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
#    print ("Positive: %5d (%.1f%%)" % (num_pos, 100.0 * ((num_pos+num_neu)/total)))
#    print ("Negative: %5d (%.1f%%)" % (num_neg, 100.0 * (num_neg/total)))
    
    
    f1=open(allReviews, 'r', encoding = "utf-8")
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
    
    print("Accuracy of TextBlob:",rating_count/total)

main()
