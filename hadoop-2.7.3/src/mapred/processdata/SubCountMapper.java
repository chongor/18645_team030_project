package mapred.processdata;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.codehaus.jettison.json.JSONException;
import org.codehaus.jettison.json.JSONObject;

import java.io.IOException;

/**
 * Created by Darren on 4/27/2017.
 */
public class SubCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    /*
     * Inputs: raw reddit comments in JSON format
     * Outputs: subreddit 1
     */
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        try {
            JSONObject json = new JSONObject(value.toString());

            String sub = (String) json.get("subreddit");

            context.write(new Text(sub), new IntWritable(1));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
