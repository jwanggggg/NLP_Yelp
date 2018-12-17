import java.util.*;
import java.io.*;

public class NaiveBayesClassifier {
	
	public static void main(String[] args) throws IOException {
		String trainFile = "files/YelpTraining.txt";
		String testFile = "files/YelpTraining.txt";
		String vocabFile = "files/YelpVocab.txt";
		String stopwordFile = "files/stopwords.txt";
		
		NBClassify(trainFile, testFile, vocabFile, stopwordFile);
	}
	
	public static void NBClassify(String trainFile, String testFile, String vocabFile, String stopwordFile) throws IOException {
		BufferedReader sWordReader = new BufferedReader(new FileReader(stopwordFile));
		BufferedReader vocabReader = new BufferedReader(new FileReader(vocabFile));
		BufferedReader trainReader = new BufferedReader(new FileReader(trainFile));
		BufferedReader testReader = new BufferedReader(new FileReader(testFile));
		
		HashSet<Integer> stopwords = new HashSet<>();
		int distinctWords = 0;
		
		HashSet<String> stopwordsStr = new HashSet<>();
		String line;
		
		// Hash the stopwords
		
		while ((line = sWordReader.readLine()) != null) 
			stopwordsStr.add(line);
		
		sWordReader.close();
		
		System.out.println(stopwordsStr);
		
		// Check the number of distinct words
		
		while ((line = vocabReader.readLine()) != null) {
			if (stopwordsStr.contains(line)) stopwords.add(distinctWords);
			distinctWords++;
		}
		vocabReader.close();
		
		int[] posWords = new int[distinctWords];
		int[] negWords = new int[distinctWords];
		
		int posReviews = 0;
		int negReviews = 0;
		int wordsInPosReviews = 0;
		int wordsInNegReviews = 0;
		
		while ((line = trainReader.readLine()) != null) {
			StringTokenizer st = new StringTokenizer(line, " :");
			if (st.countTokens() == 0) continue;
			int stars = Integer.parseInt(st.nextToken());
			
			// Mark ratings as >= 3 as positive, negative otherwise
			
			if (stars >= 3) {
				posReviews++;
				while (st.hasMoreTokens()) {
					int word = Integer.parseInt(st.nextToken());
					int frequency = Integer.parseInt(st.nextToken());
					if(stopwords.contains(word))	continue;
					posWords[word]+=frequency;
					wordsInPosReviews+=frequency;
				}
			}
			// Negative Review
			else { 
				negReviews++;
				while(st.hasMoreTokens()) {
					int word = Integer.parseInt(st.nextToken());
					int freq = Integer.parseInt(st.nextToken());
//					freq = binaryNB ? 1 : freq;
					if(stopwords.contains(word))	continue;
					negWords[word]+=freq;
					wordsInNegReviews+=freq;
				}
			}
			
		}
		trainReader.close();
		
		// Record true positives/negatives to calculate
		// accuracy/precision/recall/fscore
		
		int truePositive = 0;
		int falsePositive = 0; 
		int falseNegative = 0; 
		int correctClassification = 0;
		int incorrectClassification = 0;
		
		while ((line = testReader.readLine()) != null) {
			StringTokenizer st = new StringTokenizer(line, " :");
			int stars = Integer.parseInt(st.nextToken());
			
			// Save the actual number of stars, and compare to calculated at the end for true/false pos/neg
			int actual = stars >= 3 ? 1 : 0;
			
			double probOfPos = Math.log(posReviews / (posReviews + negReviews + 0.0));
			double probOfNeg = Math.log(negReviews / (posReviews + negReviews + 0.0));
			
			while(st.hasMoreTokens()) {
				int word = Integer.parseInt(st.nextToken());
				int freq = Integer.parseInt(st.nextToken());

				if(stopwords.contains(word)) continue;
				// freq * log(neg or pos words[word] + 1)/ (words in respective review + distinct words)
				probOfPos += freq * Math.log((posWords[word]+1) / (wordsInPosReviews + distinctWords + 0.0));
				probOfNeg += freq * Math.log((negWords[word]+1) / (wordsInNegReviews + distinctWords + 0.0));
			}
			
			System.out.println("Prob of pos: " + probOfPos);
			System.out.println("Prob of neg: " + probOfNeg);
			
			int predicted = (probOfPos > probOfNeg ? 1 : 0);
			String result = (predicted == 1 ? "Positive" : "Negative");
			
			System.out.println("Sentiment: " + result +"\n");
			
			if(predicted == actual)
				correctClassification++;
			else
				incorrectClassification++;
		
			if(predicted == 1 && actual == 1)
				truePositive++;
			else if(predicted == 1 && actual == 0)
				falseNegative++;
			else if(predicted == 0 && actual == 1)
				falsePositive++;
		}
		testReader.close();
		// Accuracy: correct/total
		double accuracy = correctClassification/(correctClassification + incorrectClassification + 0.0);
		// Precision:  true positive/true positive + false positive
		double precision = truePositive/(truePositive + falsePositive + 0.0);
		// Recall: true positive/true positive + false negative
		double recall = truePositive/(truePositive + falseNegative + 0.0);
		// F-score: 2pr/(p+r)
		double fscore = 2*precision*recall/(precision + recall);
		
		System.out.println("Accuracy: "+accuracy);
		System.out.println("Precision: " + precision);
		System.out.println("Recall: " + recall);
		System.out.println("F-Score: " + fscore);
	}
	
}
