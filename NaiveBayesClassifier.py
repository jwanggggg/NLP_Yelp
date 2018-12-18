#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 13:52:42 2018

@author: jonathanwang
"""

import re
import math

def main():
    reviews = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/Clean_sample.txt"
    trainFile = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/YelpTraining.txt"
    testFile = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/YelpTraining.txt"
    vocabFile = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/YelpVocab.txt"
    stopwordFile = "/Users/jonathanwang/eclipse-workspace2/NLPFinal/files/stopwords.txt"
    
    NBClassify(trainFile, testFile, vocabFile, stopwordFile)
    

def NBClassify(trainFile, testFile, vocabFile, stopwordFile):
    stopWords = set(())
    distinctWords = 0
    
    stopWordsStr = set(())
    
    with open(stopwordFile, "r", encoding = "utf-8") as f:
        for line in f:
            stopWordsStr.add(line.rstrip('\n'))
    
    print(stopWordsStr)
    
    
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
            
#            print("Prob of pos: " + str(probOfPos))
#            print("Prob of neg: " + str(probOfNeg))
#            print("Sentiment: " + result +"\n")
            
            if predicted == actual:
                correctClassification += 1
            else:
                incorrectClassification += 1
            
                
    accuracy = correctClassification/(correctClassification + incorrectClassification)    
    print("Accuracy:", accuracy)

main()
