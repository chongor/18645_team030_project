package mapred.subreddits;

import java.io.IOException;
import java.io.FileNotFoundException;
import java.io.File;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Map;
import java.util.List;
import java.util.LinkedList;
import java.util.LinkedHashMap;
import java.util.Iterator;
import java.util.Collections;

import java.util.TreeMap;
import java.util.Set;
import java.util.Scanner;
import org.apache.hadoop.filecache.DistributedCache;

import java.util.Comparator;



import org.apache.hadoop.fs.Path;
import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class SimilarityMapper extends Mapper<LongWritable, Text, Text, Text> {

	String[] training_vector_list = null;

	/**
	 * We compute the inner product of every test user will all of the training user vectors
	 */
	@Override
	protected void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {
		String line = value.toString();
		String[] test_featureVector = line.split("\t", 2);

		String test_username = test_featureVector[0];
		HashMap<String, Integer> test_subreddits_map = parseFeatureVector(test_featureVector[1]);


		String[] training_featureVector = null;
		String training_username = null;
		String training_subreddits = null;
		int similarity = 0;
		HashMap<String, Integer> training_subreddits_map = null;
		HashMap<String,Integer> similarityMap = new HashMap<String,Integer>();

		for(String s: training_vector_list){
			
			training_featureVector = s.split("\t", 2);
			training_username = training_featureVector[0];
			training_subreddits = training_featureVector[1];
			training_subreddits_map = parseFeatureVector(training_featureVector[1]);
			similarity = computeInnerProduct(training_subreddits_map,test_subreddits_map);
			similarityMap.put(training_username,similarity);

		}


		List list = new LinkedList(similarityMap.entrySet());
        Collections.sort(list, new Comparator() {

            @Override
            public int compare(Object o1, Object o2) {
                return ((Comparable) ((Map.Entry) (o2)).getValue()).compareTo(((Map.Entry) (o1)).getValue());
            }
        });

        HashMap<String,Integer> result = new LinkedHashMap<String,Integer>();
        for (Iterator it = list.iterator(); it.hasNext();) {
            Map.Entry<String,Integer> entry = (Map.Entry) it.next();
            result.put(entry.getKey(), entry.getValue());
        }



		//write sorted map values into context
		StringBuilder builder = new StringBuilder();
		for (Map.Entry<String, Integer> e : result.entrySet()) 
			builder.append(e.getKey() + ":" + e.getValue() + ";");

		context.write(new Text(test_username), new Text(builder.toString()));


	}

	/**
	 * This function is ran before the mapper actually starts processing the
	 * records, so we can use it to setup the job feature vector.
	 * 
	 * Loads the feature vector for hashtag #job into mapper's memory
	 */
	@Override
	protected void setup(Context context) 
		throws IOException, FileNotFoundException {
		Path[] cacheFiles = DistributedCache.getLocalCacheFiles(context.getConfiguration());
		File cache = new File(cacheFiles[0].toString());
		training_vector_list = new Scanner(cache).useDelimiter("\\Z").next().split("\n");

		//for passing training data through config
		//training_vector_list = context.getConfiguration().get("userVectors").split("\n");
	}

	/**
	 * De-serialize the feature vector into a map
	 * 
	 * @param featureVector
	 *            The format is "word1:count1;word2:count2;...;wordN:countN;"
	 * @return A HashMap, with key being each word and value being the count.
	 */
	private HashMap<String, Integer> parseFeatureVector(String featureVector) {
		HashMap<String, Integer> featureMap = new HashMap<String, Integer>();
		String[] features = featureVector.split(";");
		for (String feature : features) {
			String[] feature_affinity = feature.split(",");
			featureMap.put(feature_affinity[0], 1);
		}
		return featureMap;
	}

	/**
	 * Computes the dot product of two feature vectors
	 * @param featureVector1
	 * @param featureVector2
	 * @return 
	 */
	private Integer computeInnerProduct(HashMap<String, Integer> featureVector1,
			Map<String, Integer> featureVector2) {
		Integer sum = 0;
		for (String word : featureVector1.keySet()) 
			if (featureVector2.containsKey(word))
				sum += featureVector1.get(word) * featureVector2.get(word);
		
		return sum;
	}

	



}
















