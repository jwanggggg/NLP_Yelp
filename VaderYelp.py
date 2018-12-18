#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 21:45:48 2018

@author: jonathanwang
"""

import re
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main():
    analyzeSentences()

def printResult(scores, actualStars):
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
            
    accuracy = correctClassification/(correctClassification + incorrectClassification)
    print("Accuracy:", accuracy)
    
def parseSentences():
    sentences = []
    actualStars = []
    with open("Clean_sample.txt", "r", encoding = "utf-8") as f:
        for line in f:
            stars = line[9]
            line = line[11:len(line)-3]
            sentences.append(line)
            if stars != "\"":
                actualStars.append(int(stars))
            else:
                actualStars.append(3)
        
    f.close()
    print(len(actualStars))
    print(len(sentences))
    return sentences, actualStars

def analyzeSentences():
    
    sid = SentimentIntensityAnalyzer()
    
    sentences, actualStars = parseSentences()
    scores = []
        
    for sentence in sentences:
#        print(sentence + "\n")
        ss = sid.polarity_scores(sentence)
        scores.append(ss["compound"])
#        for k in sorted(ss):
#            print('{0}: {1}, '.format(k, ss[k]), end='')
#        print()
        
    printResult(scores, actualStars)

main()
