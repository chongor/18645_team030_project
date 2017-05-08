package mapred.subreddits;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Paths;

import mapred.job.Optimizedjob;
import mapred.util.FileUtil;
import java.io.File;
import java.util.Scanner;
import mapred.util.SimpleParser;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
import java.net.URI;
import org.apache.hadoop.filecache.DistributedCache;


public class Driver {

	public static void main(String args[]) throws Exception {
		SimpleParser parser = new SimpleParser(args);

		String testInput = parser.get("input");
		String trainingInput = parser.get("input2");
		String output = parser.get("output");
		String tmpdir = parser.get("tmpdir");


		//below for running on aws emr, without using distributed cache

		//Configuration conf = new Configuration();
		//FileSystem fs = FileSystem.get(URI.create(trainingInput),conf);
		// InputStream inStream = fs.open(new Path(trainingInput + "/trainingData10K.txt"));	

		//for running locally, comment above lines and uncomment line below
		//File fv_file = new File(trainingInput);

		
 	 	String trainingUsers = null;
 	 	//if locally, replace inStream with fv_file
 	 	//String trainingUsers = new Scanner(inStream).useDelimiter("\\Z").next();

		getRedditSimilarities(trainingInput+"/trainingData1m.txt", testInput, output);
	}


	private static void getWordVectors(String input, String output)
		throws IOException,ClassNotFoundException, InterruptedException {
		// Share the feature vector of #job to all mappers.
		Configuration conf = new Configuration();
		//DistributedCache.addCacheFile(fv_path.toUri(), conf);
		//conf.set("jobFeatureVector", jobFeatureVector);
		
		Optimizedjob job = new Optimizedjob(conf, input, output,
				"Get Word Vectors");
		job.setClasses(WordMapper.class, WordReducer.class, null);
		job.setMapOutputClasses(Text.class, Text.class);
		job.run();
	}
	/**
	 * Computes the word cooccurrence counts for hashtag #job
	 * 
	 * @param input
	 *            The directory of input files. It can be local directory, such
	 *            as "data/", "/home/ubuntu/data/", or Amazon S3 directory, such
	 *            as "s3n://myawesomedata/"
	 * @param output
	 *            Same format as input
	 * @throws IOException
	 * @throws ClassNotFoundException
	 * @throws InterruptedException
	 */
	private static void getJobFeatureVector(String input, String output)
			throws IOException, ClassNotFoundException, InterruptedException {
		Optimizedjob job = new Optimizedjob(new Configuration(), input, output,
				"Get feature vector for hashtag #Job");

		job.setClasses(JobMapper.class, JobReducer.class, null);
		job.setMapOutputClasses(Text.class, Text.class);
		job.setReduceJobs(1);

		job.run();
	}

	/**
	 * Loads the computed word cooccurrence count for hashtag #job from disk.
	 * 
	 * @param dir
	 * @return
	 * @throws IOException
	 */
	private static String loadJobFeatureVector(String dir) throws IOException {
		// Since there'll be only 1 reducer that process the key "#job", result
		// will be saved in the first result file, i.e., part-r-00000
		String job_featureVector = FileUtil.load(dir + "/part-r-00000");

		// The feature vector looks like "#job word1:count1;word2:count2;..."
		String featureVector = job_featureVector.split("\\s+", 2)[1];
		return featureVector;
	}

	/**
	 * Same as getJobFeatureVector, but this one actually computes feature
	 * vector for all hashtags.
	 * 
	 * @param input
	 * @param output
	 * @throws Exception
	 */
	private static void getHashtagFeatureVector(String input, String output)
			throws Exception {
		Optimizedjob job = new Optimizedjob(new Configuration(), input, output,
				"Get feature vector for all hashtags");
		job.setClasses(HashtagMapper.class, HashtagReducer.class, null);
		job.setMapOutputClasses(Text.class, Text.class);
		job.run();
	}

	/**
	 * When we have feature vector for both #job and all other hashtags, we can
	 * use them to compute inner products. The problem is how to share the
	 * feature vector for #job with all the mappers. Here we're using the
	 * "Configuration" as the sharing mechanism, since the configuration object
	 * is dispatched to all mappers at the beginning and used to setup the
	 * mappers.
	 * 
	 * @param jobFeatureVector
	 * @param input
	 * @param output
	 * @throws IOException
	 * @throws ClassNotFoundException
	 * @throws InterruptedException
	 */
	private static void getHashtagSimilarities(
			String input, String output) throws IOException,
			ClassNotFoundException, InterruptedException {
		// Share the feature vector of #job to all mappers.
		Configuration conf = new Configuration();
		//DistributedCache.addCacheFile(fv_path.toUri(), conf);
		//conf.set("jobFeatureVector", jobFeatureVector);
		
		Optimizedjob job = new Optimizedjob(conf, input, output,
				"Get similarities between all hashtags");
		job.setClasses(SimilarityMapper.class, SimilarityReducer.class, null);
		job.setMapOutputClasses(Text.class, IntWritable.class);
		job.run();
	}

	private static void getRedditSimilarities(
			String fv_path, String input, String output) throws IOException,
			ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
		DistributedCache.addCacheFile(new Path(fv_path).toUri(), conf);
		System.out.println("Added file to cache");
		//if using config, add vectors as an argument to this function passed by main
		//conf.set("userVectors", userVectors);
		
		Optimizedjob job = new Optimizedjob(conf, input, output,
				"Get similarities between all subreddits");
		job.setClasses(SimilarityMapper.class, SimilarityReducer.class, null);
		job.setMapOutputClasses(Text.class, Text.class);
		job.run();
	}
}
