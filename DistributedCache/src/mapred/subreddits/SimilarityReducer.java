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
		
		StringBuilder training_users_map = parseFeatureVector(line,k);
		
		context.write(key, new Text(training_users_map.toString()));

	}

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
