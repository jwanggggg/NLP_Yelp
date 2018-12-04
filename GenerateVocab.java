import java.io.*;
import java.util.*;
public class GenerateVocab {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		File file = new File("files/Clean_sample.txt");
		File vocab = new File("files/YelpVocab.txt");
		FileWriter fw = new FileWriter(vocab);
		
		Scanner input = new Scanner(file);
		
		Hashtable<Integer, String> freqIndex = new Hashtable<Integer, String>();
		Hashtable<String, Integer> indexFreq = new Hashtable<String, Integer>();
		
		ArrayList<String[]> allReviews = new ArrayList<String[]>();
		
		while (input.hasNextLine()) {
			String line = input.nextLine().replaceAll("\\p{P}", " ");
			String[] lineArray = line.split("\\ +");
			
			if (!lineArray[2].equals("id"))
					allReviews.add(lineArray);
			
			int index = 0;
			for (String word : lineArray) {
				if (word.equals("") || word.equals("stars"))
					continue;
				if (!freqIndex.containsValue(word)) {
					freqIndex.put(index, word);
					indexFreq.put(word, index);
					index++;
				}
			}
		}
				
		List<Integer> list = new ArrayList<Integer>(freqIndex.keySet());
		Collections.sort(list);
		
		System.out.println(list);
		
		for (int key : list) {
			fw.write(freqIndex.get(key) +"\n");
		}
		fw.close();
		input.close();
		
		// Now go through all reviews, get hashtable of frequencies for each 
		
		File trainingFile = new File("files/YelpTraining.txt");
		fw = new FileWriter(trainingFile);
		input = new Scanner(vocab);
		
		for (String[] review : allReviews) {
			// Hashtable that represent the current sentence's word ID frequencies.
			Hashtable<Integer, Integer> sentFreqs = new Hashtable<Integer, Integer>();

			String rating = review[2];
			
			for (int i = 3; i < review.length; i++ ) {
				String currWord = review[i];
				if (currWord.equals("") || currWord.equals("stars")) continue;
				if (!sentFreqs.containsKey(indexFreq.get(currWord))) {
					sentFreqs.put(indexFreq.get(currWord), 0);
				}
				
				sentFreqs.put(indexFreq.get(currWord), sentFreqs.get(indexFreq.get(currWord)) + 1);
			}
//			System.out.println(sentFreqs);
			
			StringBuilder sb = new StringBuilder();
			sb.append(rating + " ");
			for (int key : sentFreqs.keySet()) {
				sb.append(key + ":");
				sb.append(sentFreqs.get(key) + " ");
			}
			fw.write(sb.toString() + "\n");
		}
		fw.close();
		input.close();
		
	}

}
