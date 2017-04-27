package mapred.processdata;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by Darren on 4/27/2017.
 */
public class RawDataReducer extends Reducer<Text, Text, Text, Text> {

    /*
     * Inputs: author \t subreddit
     * Outputs: author sub1,count1;sub2,count2;sub3,count3; etc...
     */
    @Override
    protected void reduce(Text key, Iterable<Text> value, Context context) throws IOException, InterruptedException {
        Map<String, Integer> counts = new HashMap<String, Integer>();
        for (Text word : value) {
            String w = word.toString();
            Integer count = counts.get(w);
            if (count == null)
                count = 0;
            count++;
            counts.put(w, count);
        }

        StringBuilder builder = new StringBuilder();
        for(Map.Entry<String, Integer> e : counts.entrySet())
            builder.append(e.getKey() + "," + e.getValue() + ";");

        context.write(key, new Text(builder.toString()));
    }

}
