import java.io.*;
import java.util.Arrays;
import java.util.Scanner;
public class ParseReviews {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		File file = new File("files/Clean_sample.txt");
		Scanner input = new Scanner(file);
		
		while (input.hasNextLine()) {
			String line = input.nextLine();
			String[] lineArray = line.split("\\{\"stars\":");
			// Skip invalids
			if (!lineArray[0].equals("")) continue;
			
			// Append rating and 
			
			char rating = lineArray[1].charAt(0);
			StringBuilder sb = new StringBuilder();
			sb.append(rating);
			System.out.println(sb);
		}
		
		input.close();
	}

}
