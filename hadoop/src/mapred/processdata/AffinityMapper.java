package mapred.processdata;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by Darren on 4/27/2017.
 */
public class AffinityMapper extends Mapper<LongWritable, Text, Text, DoubleWritable> {

    Map<String, Integer> subTotalComments;

    /*
     * Obtain list of subreddits with total number of comments posted in that subreddit
     * List of total comments for each subreddit generated by
     * SubCountMapper/Reducer
     * data format per row: subreddit \t total_count
     */
    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        super.setup(context);

        //run if distributed
        //getSubDataFromCache(context);

        //run if not distributed
        getSubDataLocally(context);
    }

    /*
     * Input: author sub1,count1;sub2,count2;sub3,count3; etc...
     * Output: author subreddit affinity_score
     */
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        String[] author_subVector = line.split("\\s+", 2);
        String author = author_subVector[0];

        Map<String, Integer> subs = parseSubVector(author_subVector[1]);

        StringBuilder builder;
        // for each sub in the vector
        // check if it's a sub we care about from subTotalComments
        // if we do care about it, create an affinity score of it
        for (Map.Entry<String, Integer> e : subs.entrySet()){
            String sub = e.getKey();

            //if sub exists in subTotalComments
            //calculate affinity score and write
            if(subTotalComments.containsKey(sub)){
                Double aScore = e.getValue() / (double) subTotalComments.get(sub);

                builder = new StringBuilder();
                builder.append(author + "," + sub);

                context.write(new Text(builder.toString()), new DoubleWritable(aScore));
            }
        }

    }

    /**
     * De-serialize the feature vector into a map
     * 
     * @param subVector
     *            The format is "sub1:count1;sub2:count2;...;wordN:countN;"
     * @return A HashMap, with key being each word and value being the count.
     */
    private Map<String, Integer> parseSubVector(String subVector) {
        Map<String, Integer> subMap = new HashMap<String, Integer>();
        String[] subs = subVector.split(";");
        for (String sub : subs) {
            String[] sub_count = sub.split(",");
            subMap.put(sub_count[0], Integer.parseInt(sub_count[1]));
        }
        return subMap;
    }

    /**
     * When hadoop is running in single-node use this to get the subreddit data
     * @param context
     * @throws IOException
     */
    private void getSubDataLocally (Context context) throws IOException {
        String sub_filename = context.getConfiguration().get("sub_data");
        File f = new File(sub_filename);

        loadSubData(f);
    }

    /**
     * When hadoop is running in a distributed or semi-distributed environment use this to get the subreddit data
     * @param context
     * @throws IOException
     */
    private void getSubDataFromCache(Context context) throws IOException {
        URI[] localURIs = context.getCacheFiles();
        File f = new File(localURIs[0]);

        loadSubData(f);
    }

    /**
     * Read through the output of SubCount Mapreduce job and store in HashMap
     * @param f
     * @throws IOException
     */
    private void loadSubData(File f) throws IOException{
        subTotalComments = new HashMap<String, Integer>();

        try(BufferedReader br = new BufferedReader(new FileReader(f))) {
            String line;
            while((line = br.readLine()) != null) {
                String[] l = line.split("\t");
                String sub = l[0];
                Integer count = Integer.parseInt(l[1]);
                subTotalComments.put(sub, count);
            }
        }
    }

}
