package mapred.subreddits;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import org.apache.hadoop.io.IntWritable;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class SimilarityReducer extends Reducer<Text, Text, Text, Text> {

	@Override
	protected void reduce(Text key, Iterable<Text> value,
			Context context)
			throws IOException, InterruptedException {		
		
		String line = null;
		int k = 5;
		for(Text t : value){
			line = t.toString();
		}
		// String[] test_user_featureVector = line.split("\\s+", 2);
		// StringBuilder builder = new StringBuilder();
		StringBuilder training_users_map = parseFeatureVector(line,k);
		// for(Map.Entry<String,Integer> e : training_users_map.entrySet()){
		// 	if (k>0){
		// 		builder.append(e.getKey() + ":" + e.getValue() + ";");
		// 		k--;
		// 	}
		// }
		context.write(key, new Text(training_users_map.toString()));

		// int count = 0;
		// for(IntWritable val : value){
		// 	count += val.get();
		// }
		// context.write(key,new IntWritable(count));
		/*
		 * We're serializing the word cooccurrence count as a string of the following form:
		 * 
		 * word1:count1;word2:count2;...;wordN:countN;
		 */
		// StringBuilder builder = new StringBuilder();
		// for (Map.Entry<String, Integer> e : counts.entrySet()) 
		// 	builder.append(e.getKey() + ":" + e.getValue() + ";");
		
		// context.write(key, new Text(builder.toString()));
	}

	// private Map<String, Integer> parseFeatureVector(String featureVector) {
	// 	Map<String, Integer> featureMap = new HashMap<String, Integer>();
	// 	String[] features = featureVector.split(";");
	// 	for (String feature : features) {
	// 		String[] word_count = feature.split(":");
	// 		featureMap.put(word_count[0], Integer.parseInt(word_count[1]));
	// 	}
	// 	return featureMap;
	// }
	private StringBuilder parseFeatureVector(String featureVector, int k) {
		StringBuilder featureMap = new StringBuilder();
		String[] features = featureVector.split(";");
		int count = k;
		for (String feature : features) {
			if (count>0){
				String[] word_count = feature.split(":");
				featureMap.append(word_count[0] + ":" + Integer.parseInt(word_count[1]) + ";");
				count--;	
			}
		}
		return featureMap;
	}
}
