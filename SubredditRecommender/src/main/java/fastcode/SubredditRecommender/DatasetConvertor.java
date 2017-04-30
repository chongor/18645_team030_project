package fastcode.SubredditRecommender;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class DatasetConvertor {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		Map<String,Integer> users = new HashMap<String,Integer>();
		Map<String,Integer> subreddits = new HashMap<String,Integer>();
		int userCount = 0 ; 
		int subredditCount = 0;
		//		File file = null;
		//		if(args.length > 0) {
		//			file = new File(args[0]);
		//			// Work with your 'file' object here
		//		}else{
		//			System.err.println("Input File must be specified");
		//		}
		BufferedReader br = new BufferedReader(new FileReader("data/rc_affinity_1k_subs.txt"));
		BufferedWriter bw = new BufferedWriter(new FileWriter("data/votes.csv"));

		String line;
		int userID = 0 ; 
		int subredditID = 0 ; 
		while((line = br.readLine()) != null) {
			String[] values = line.split(",");
			//System.out.println(values[0] + "," + values[1] + "," + values[2] + "\n");
			//bw.write(values[0] + "," + values[1] + "," + values[2] + "\n");
			if (users.containsKey(values[0])){
				userID = users.get(values[0]);
			}else {
				users.put(values[0], userCount);
				userID = userCount;
				userCount++;
				 
			}
			if (subreddits.containsKey(values[1])){
				subredditID = subreddits.get(values[1]);		
			}
			else{
				subreddits.put(values[1], subredditCount);		
				subredditID = subredditCount; 
				subredditCount++;
			}
			bw.write(userID + "," + subredditID + "," + Double.parseDouble(values[2])*10 + "\n");
		}

		br.close();
		bw.close();




		System.out.println("Reading from File : Finished");
		System.out.println("Unique Users :" + users.size());
		System.out.println("Unique Subreddits :" + subreddits.size());
	}

}