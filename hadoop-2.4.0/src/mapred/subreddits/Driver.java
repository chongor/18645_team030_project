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


		//below for running on aws emr
		//Configuration conf = new Configuration();
		//FileSystem fs = FileSystem.get(URI.create(trainingInput),conf);
		// InputStream inStream = fs.open(new Path(trainingInput + "/trainingData10K.txt"));	

		//for running locally
		//File fv_file = new File(trainingInput);

		//if locally, replace inStream with fv_file
 	 	String trainingUsers = null;
 	 	//String trainingUsers = new Scanner(inStream).useDelimiter("\\Z").next();

		getRedditSimilarities(trainingInput, testInput, output);
	}



	private static void getRedditSimilarities(
			String fv_path, String input, String output) throws IOException,
			ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
		DistributedCache.addCacheFile(new Path(fv_path).toUri(), conf);
		System.out.println("Added file to cache");
		//conf.set("userVectors", trainingUsers); for using conf, pass training users from main function
		
		Optimizedjob job = new Optimizedjob(conf, input, output,
				"Get similarities between all subreddits");
		job.setClasses(SimilarityMapper.class, SimilarityReducer.class, null);
		job.setMapOutputClasses(Text.class, Text.class);
		job.run();
	}
}
