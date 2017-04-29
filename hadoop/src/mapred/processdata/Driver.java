package mapred.processdata;

import mapred.util.EasyJob;
import mapred.util.SimpleParser;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;

/**
 * Created by Darren on 4/28/2017.
 */
public class Driver {

    public static void main(String args[]) throws Exception {
        SimpleParser parser = new SimpleParser(args);

        String input = parser.get("input");
        String output = parser.get("output");
        String tmpdir = parser.get("tmpdir");

        //run the three jobs to get affinity scores
        getSubCounts(input, tmpdir + "/sub_counts");
        getRawData(input, tmpdir + "/process_data");
        getAffinityScores(tmpdir + "/process_data", output, tmpdir + "/sub_counts");

    }

    /**
     * Runs the mapreduce job to obtain the total number of comments for each subreddit from the raw data
     * @param input
     * @param output
     * @throws Exception
     */
    private static void getSubCounts(String input, String output) throws Exception {
        EasyJob ejob = new EasyJob(new Configuration(), input, output,"Get total number of comments for each subreddit");
        ejob.setClasses(SubCountMapper.class, SubCountReducer.class, null);
        ejob.setMapOutputClasses(Text.class, IntWritable.class);
        ejob.run();
    }

    /**
     * Runs the mapreduce job to transfer the raw reddit data from json into more manageable size
     * @param input
     * @param output
     * @throws Exception
     */
    private static void getRawData(String input, String output) throws Exception {
        EasyJob ejob = new EasyJob(new Configuration(), input, output,"Process raw reddit comment data from json into more manageable size");
        ejob.setClasses(RawDataMapper.class, RawDataReducer.class, null);
        ejob.setMapOutputClasses(Text.class, Text.class);
        ejob.run();

    }

    /**
     * Runs the map job to calculate the affinity score for each (user, sub) pair
     * @param input
     * @param output
     * @param data_filename
     * @throws Exception
     */
    private static void getAffinityScores(String input, String output, String data_filename) throws Exception {
        EasyJob ejob = new EasyJob(new Configuration(), input, output, "Take preprocessed data and total sub comment counts and calculate affinity scores per (user, sub) pair.");
        ejob.job.addCacheFile(new Path(data_filename).toUri());
        ejob.setClasses(AffinityMapper.class, null, null);
        ejob.setMapOutputClasses(Text.class, DoubleWritable.class);
        ejob.run();
    }

}
